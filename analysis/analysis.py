"""All analyses reported in the paper.

Usage:  python3 analysis/analysis.py <data_root> <output_dir>

Writes aggregate CSV tables to <output_dir>/tables and a readable summary to
<output_dir>/RESULTS.md. The three planned associations are in the section
"Planned tests"; everything else is exploratory.
"""
import os
import re
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import friedmanchisquare, spearmanr, wilcoxon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import (COMPOSITE_LABELS, COMPOSITES, load_logs, load_survey,  # noqa: E402
                       participant_behaviour)

SEED = 20261111
N_BOOT = 10_000

# ----------------------------------------------------------------------------
# Task and task-need coding
# ----------------------------------------------------------------------------
RE_BANK = re.compile(r"BSB|Account No", re.I)
RE_CAPTION = re.compile(r"caption|post|trip|holiday|vacation|Milan|Paris|New York|\[LOCATION\]", re.I)


def task_of(site, text):
    """Which study task a suggestion request belongs to."""
    if site == "social":
        return "social_post"
    if site == "search":
        return "search_bank"
    t = str(text)
    if RE_BANK.search(t):
        return "chat_other"  # bank message pasted into the chatbot
    if RE_CAPTION.search(t):
        return "chat_caption"
    return "chat_health"


# Task-need codes of the two coders (coding/coder_A.csv, coding/coder_B.csv), keyed by
# (task, information type): True = needed, False = incidental.
def load_codes(path):
    T = {"Social post": "social_post", "Caption request": "chat_caption", "Health query": "chat_health",
         "Bank-message search": "search_bank"}
    I = {"Name of a person": "Personal", "Place (city or suburb)": "Location", "Age": "Age", "Health condition": "Health",
         "Organisation name": "Organisation", "Email address": "Email", "Phone number": "Phone"}
    out = {}
    for _, x in pd.read_csv(path).iterrows():
        info = x.information_flagged
        cat = "Relationship" if info.startswith("Relationship") else "Bank Account" if info.startswith("Bank account") else I[info]
        out[(T[x.task], cat)] = str(x.needed).strip().upper() == "Y"
    return out


def code_need(r, codes_a, codes_b):
    """need = 'needed' / 'incidental' where the coders agree, 'disputed' where they do not.
    Requests in which the bank message was pasted into the chatbot (chat_other) take the
    codes of the bank-message rows."""
    def one(t, c):
        key = ("search_bank", c) if t == "chat_other" else (t, c)
        a, b = codes_a[key], codes_b[key]
        return "disputed" if a != b else "needed" if a else "incidental"
    r = r.copy()
    r["need"] = [one(t, c) for t, c in zip(r.task, r.cat)]
    return r


# ----------------------------------------------------------------------------
# Small statistics helpers
# ----------------------------------------------------------------------------
def cronbach(df):
    df = df.dropna()
    k = df.shape[1]
    return k / (k - 1) * (1 - df.var(ddof=1).sum() / df.sum(axis=1).var(ddof=1))


def boot_spearman(x, y, rng):
    d = pd.concat([x, y], axis=1).dropna().to_numpy()
    rho = spearmanr(d[:, 0], d[:, 1]).statistic
    n = len(d)
    out = []
    for _ in range(N_BOOT):
        i = rng.integers(0, n, n)
        with np.errstate(invalid="ignore"):
            v = spearmanr(d[i, 0], d[i, 1]).statistic
        if np.isfinite(v):
            out.append(v)
    lo, hi = np.percentile(out, [2.5, 97.5])
    return rho, lo, hi, n


def std_betas(d, y, xs):
    z = (d - d.mean()) / d.std(ddof=1)
    X = np.c_[np.ones(len(z)), z[xs].to_numpy()]
    b = np.linalg.lstsq(X, z[y].to_numpy(), rcond=None)[0]
    res = z[y].to_numpy() - X @ b
    return b[1:], 1 - res.var() / z[y].to_numpy().var()


def holm(ps):
    ps = np.asarray(ps, float)
    order = np.argsort(ps)
    adj = np.empty_like(ps)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (len(ps) - rank) * ps[i])
        adj[i] = min(1.0, run)
    return adj


def cluster_rate(df, num, rng, by="pid"):
    """Pooled rate with a participant-cluster percentile interval."""
    g = df.groupby(by)[num].agg(["sum", "size"]).to_numpy()
    rate = g[:, 0].sum() / g[:, 1].sum()
    n = len(g)
    idx = rng.integers(0, n, (N_BOOT, n))
    boots = g[idx, 0].sum(axis=1) / g[idx, 1].sum(axis=1)
    return rate, *np.percentile(boots, [2.5, 97.5])


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.1f}%)"


# ----------------------------------------------------------------------------
def perm_spearman(x, y, rng, n_perm=N_BOOT):
    """Spearman rho with a two-sided permutation p-value."""
    d = pd.concat([x, y], axis=1).dropna().to_numpy()
    rho = spearmanr(d[:, 0], d[:, 1]).statistic
    null = np.array([spearmanr(d[:, 0], rng.permutation(d[:, 1])).statistic for _ in range(n_perm)])
    return rho, (1 + (np.abs(null) >= abs(rho) - 1e-12).sum()) / (n_perm + 1)


def main(root, out):
    os.makedirs(f"{out}/tables", exist_ok=True)
    rng = np.random.default_rng(SEED)
    s = load_survey(root)
    w, a, r, u, q = load_logs(root)
    p = participant_behaviour(s, w, a, r)
    D = s.merge(p, on="pid")
    q = q.assign(task=[task_of(si, t) for si, t in zip(q.site, q.text)])
    a = a.merge(q[["attempt_id", "task"]].drop_duplicates("attempt_id"), on="attempt_id", how="left")
    a["task"] = a.task.fillna(a.site.map({"social": "social_post", "search": "search_bank", "chatbot": "chat_unknown"}))
    here = os.path.dirname(os.path.abspath(__file__))
    r = code_need(r.merge(a[["attempt_id", "task"]], on="attempt_id", how="left"),
                  load_codes(f"{here}/../coding/coder_A.csv"), load_codes(f"{here}/../coding/coder_B.csv"))
    md = ["# Results (n = 50)", "",
          f"Dataset: {len(s)} participants, {len(w)} warning sets on study sites, {len(a)} suggestion requests from "
          f"{int(p.requester.sum())} participants, {len(r)} displayed suggestions. Seed {SEED}, {N_BOOT:,} bootstrap draws, "
          "participants resampled as whole units.", ""]

    def save(df, name, title, note=None, index=False):
        df.to_csv(f"{out}/tables/{name}.csv", index=index)
        md.extend([f"## {title}", "", df.to_markdown(index=index, floatfmt=".3f"), ""])
        if note:
            md.extend([note, ""])

    # ---- RQ1 ---------------------------------------------------------------
    k = pd.DataFrame([
        ("Underlining means potentially sensitive", "k_under_ok", "u_flag"),
        ("Anonymisation reduces identifiability", "k_anon_ok", ""),
        ("Advice depends on information and website", "k_ctx_ok", "u_ctx"),
        ("Lower score means relatively lower risk", "k_score_ok", "u_score"),
    ], columns=["item", "k", "self"])
    rows = []
    for _, x in k.iterrows():
        x = x.to_dict()
        x = type("Row", (), x)
        row = {"comprehension_item": x.item, "correct": pct(int(D[x.k].sum()), len(D)),
               "correct_requesters": pct(int(D[D.requester][x.k].sum()), int(D.requester.sum())),
               "correct_non_requesters": pct(int(D[~D.requester][x.k].sum()), int((~D.requester).sum()))}
        row["self_rated_agree"] = pct(int((D[x.self] >= 4).sum()), int(D[x.self].notna().sum())) if x.self else ""
        rows.append(row)
    save(pd.DataFrame(rows), "rq1_comprehension", "RQ1: comprehension and self-rated understanding")

    nr = D[~D.requester]
    exp = pd.DataFrame([
        {"group": "Never requested a suggestion", "n": len(nr),
         "agree_explanations_helped": pct(int((nr.u_expl >= 4).sum()), int(nr.u_expl.notna().sum())),
         "agree_enough_choice_over_suggestions": pct(int((nr.ct_choice >= 4).sum()), len(nr))},
        {"group": "Requested, never opened an explanation", "n": int((D.requester & (D.expl_attempts == 0)).sum()),
         "agree_explanations_helped": pct(int((D[D.requester & (D.expl_attempts == 0)].u_expl >= 4).sum()),
                                           int(D[D.requester & (D.expl_attempts == 0)].u_expl.notna().sum())),
         "agree_enough_choice_over_suggestions": ""},
        {"group": "Opened an explanation at least once", "n": int((D.expl_attempts > 0).sum()),
         "agree_explanations_helped": pct(int((D[D.expl_attempts > 0].u_expl >= 4).sum()),
                                           int(D[D.expl_attempts > 0].u_expl.notna().sum())),
         "agree_enough_choice_over_suggestions": ""},
    ])
    save(exp, "rq1_selfreport_vs_exposure", "RQ1: endorsement of explanation items by actual exposure",
         "Participants who never saw a suggestion panel still endorse items about it, so experience items are reported with a requester-only check.")
    att = a.assign(opened=a.explanation_open_count > 0)
    md.append(f"Explanation opened in {pct(int(att.opened.sum()), len(att))} of requests, by "
              f"{int((D.expl_attempts > 0).sum())} of {int(D.requester.sum())} requesters.\n")

    # ---- RQ2 ---------------------------------------------------------------
    oc = r.outcome.value_counts()
    n = len(r)
    rate, lo, hi = cluster_rate(r, "accepted", rng)
    ex = r[r.explicit]
    rate_e, lo_e, hi_e = cluster_rate(ex, "accepted", rng)
    acc = r[r.accepted]
    over = pd.DataFrame([
        ("Displayed suggestions accepted", pct(int(oc.get("accepted", 0)), n), f"{100*lo:.1f}-{100*hi:.1f}%"),
        ("Displayed suggestions dismissed", pct(int(oc.get("dismissed", 0)), n), f"{r[r.outcome=='dismissed'].pid.nunique()} participants"),
        ("Displayed suggestions left without a decision", pct(int(n - ex.shape[0]), n),
         "; ".join(f"{int(oc.get(o, 0))} {o}" for o in ["unresolved", "invalidated", "pending"])),
        ("Accepted among explicit decisions", pct(int(ex.accepted.sum()), len(ex)), f"{100*lo_e:.1f}-{100*hi_e:.1f}%"),
        ("Acceptances made with Apply All", pct(int((acc.action_source == "apply_all").sum()), len(acc)),
         f"{acc[acc.action_source=='apply_all'].pid.nunique()} participants"),
        ("Median response time, Apply All (s)", f"{acc[acc.action_source=='apply_all'].groupby('pid').response_ms.median().median()/1000:.1f}", "median of participant medians"),
        ("Median response time, individual accept (s)", f"{acc[acc.action_source=='individual'].groupby('pid').response_ms.median().median()/1000:.1f}", "median of participant medians"),
    ], columns=["measure", "value", "interval_or_note"])
    save(over, "rq2_outcomes", "RQ2: what happened to displayed suggestions")

    order = ["Bulk accept only", "Accepted some, left the rest", "Requested, then left",
             "Selective (ever dismissed)", "Accepted all, one by one", "Never requested"]
    bt = D.behaviour_type.value_counts().reindex(order).fillna(0).astype(int).rename("participants").reset_index()
    bt.columns = ["behaviour_type", "participants"]
    bt["share_of_50"] = (100 * bt.participants / len(D)).round(1)
    save(bt, "rq2_behaviour_types", "RQ2: behaviour types from the logs")

    D["stated_control"] = D.p_control.map({1: "Tool acts for me", 5: "Tool recommends, I decide", 4: "I decide without recommendations"})
    D["stated_conflict"] = D.p_conflict.map({1: "Follow my own judgement", 2: "Depends on the situation", 3: "Follow the tool"})
    sv = pd.crosstab(D.stated_conflict, D.behaviour_type).reindex(columns=order, fill_value=0)
    sv["n"] = sv.sum(axis=1)
    save(sv.reset_index(), "rq2_stated_vs_enacted", "RQ2: stated conflict preference by behaviour type")
    deciders = D[(D.accepted + D.dismissed) > 0]
    own = D[D.p_conflict == 1]
    md.append(f"Of {len(deciders)} participants who made any explicit decision, {int((deciders.dismissed == 0).sum())} never dismissed a suggestion. "
              f"Of {len(own)} who say they would follow their own judgement in a conflict, {int((own.dismissed > 0).sum())} dismissed anything "
              f"({int(own.requester.sum())} of them requested suggestions).\n")
    md.append(f"Stated control: {D.stated_control.value_counts().to_dict()}.\n")

    # destinations
    rows = []
    for site in ["social", "chatbot", "search"]:
        x = r[r.site == site]
        rt, l, h = cluster_rate(x, "accepted", rng)
        rows.append({"destination": site, "requesters": x.pid.nunique(), "accepted_of_displayed": pct(int(x.accepted.sum()), len(x)),
                     "cluster_95_interval": f"{100*l:.1f}-{100*h:.1f}%",
                     "accepted_of_explicit": pct(int(x[x.explicit].accepted.sum()), int(x.explicit.sum()))})
    piv = r.groupby(["pid", "site"]).accepted.mean().unstack()
    full = piv.dropna()
    fr = friedmanchisquare(full.social, full.chatbot, full.search)
    gee_site = smf.gee("acc ~ C(site, Treatment('social'))", "pid", r.assign(acc=r.accepted.astype(int)),
                       family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
    save(pd.DataFrame(rows), "rq2_by_destination", "RQ2: acceptance by destination",
         f"Within participants with suggestions on all three destinations (n = {len(full)}): mean acceptance social {full.social.mean():.2f}, "
         f"chatbot {full.chatbot.mean():.2f}, search {full.search.mean():.2f}; Friedman chi2 = {fr.statistic:.2f}, p = {fr.pvalue:.3f}. "
         f"GEE (logit, participant clusters), odds ratios versus social: chatbot {np.exp(gee_site.params.iloc[1]):.2f} "
         f"(p = {gee_site.pvalues.iloc[1]:.3f}), search {np.exp(gee_site.params.iloc[2]):.2f} (p = {gee_site.pvalues.iloc[2]:.3f}).")

    # task need
    rows = []
    for label, fill in [("agreed codes only", None), ("disputed counted as needed", "needed"), ("disputed counted as incidental", "incidental")]:
        for scope, x in [("all displayed", r), ("explicit decisions only", r[r.explicit]), ("chatbot only", r[r.site == "chatbot"])]:
            x = x.assign(nd=x.need.replace("disputed", fill) if fill else x.need)
            x = x[x.nd.isin(["needed", "incidental"])]
            x = x.assign(nd=(x.nd == "needed").astype(int), acc=x.accepted.astype(int))
            ne, inc = x[x.nd == 1], x[x.nd == 0]
            pp = x.groupby(["pid", "nd"]).acc.mean().unstack().dropna()
            wl = wilcoxon(pp[1], pp[0]) if len(pp) > 5 and (pp[1] != pp[0]).any() else None
            g = smf.gee("acc ~ nd", "pid", x, family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
            ci = np.exp(g.conf_int().loc["nd"])
            rows.append({"coding": label, "scope": scope,
                         "needed_accepted": pct(int(ne.acc.sum()), len(ne)), "incidental_accepted": pct(int(inc.acc.sum()), len(inc)),
                         "paired_participants": len(pp),
                         "needed_higher/equal/lower": f"{int((pp[1] > pp[0]).sum())}/{int((pp[1] == pp[0]).sum())}/{int((pp[1] < pp[0]).sum())}",
                         "wilcoxon_p": round(wl.pvalue, 3) if wl else np.nan,
                         "gee_odds_ratio_needed": round(float(np.exp(g.params["nd"])), 2),
                         "gee_95_ci": f"{ci.iloc[0]:.2f}-{ci.iloc[1]:.2f}", "gee_p": round(float(g.pvalues["nd"]), 3)})
    save(pd.DataFrame(rows), "rq2_task_need", "RQ2: acceptance of task-needed versus incidental information",
         "Needed = the task as worded cannot be completed as intended once the information is replaced. Codes are those of two "
         "independent coders; 'disputed' marks the combinations on which they disagreed. An odds ratio below 1 would mean needed "
         "information is accepted for removal less often.")
    tc = r.groupby(["task", "cat"]).agg(displayed=("accepted", "size"), accepted=("accepted", "sum"),
                                         dismissed=("outcome", lambda x: (x == "dismissed").sum()), need=("need", "first")).reset_index()
    tc["accept_pct"] = (100 * tc.accepted / tc.displayed).round(1)
    save(tc, "rq2_task_by_category", "RQ2: outcomes by task and information type")

    sel = D.QID75.map(lambda v: [str(x) for x in v] if isinstance(v, list) else ([] if v is None or (isinstance(v, float) and np.isnan(v)) else [str(v)]))
    rs = pd.DataFrame([{"choice_code": k, "participants": int(sel.map(lambda v: k in v).sum())} for k in sorted({c for v in sel for c in v})])
    save(rs, "rq2_override_reasons", "RQ2: reasons selected for dismissing or overriding (multiple response)",
         f"{int((sel.map(len) > 0).sum())} participants selected at least one reason. Choice codes follow the survey export; "
         "see materials/survey_instrument.md for the wording.")

    # ---- RQ3 ---------------------------------------------------------------
    pairs = [("cf_read", "cf_backend", "Reading text vs text sent to backend"),
             ("cf_read", "cf_meta", "Reading text vs website details sent"),
             ("cf_backend", "cf_meta", "Text sent vs website details sent")]
    rows, ps = [], []
    for x, y, lab in pairs:
        d = D[[x, y]].dropna()
        wl = wilcoxon(d[x], d[y])
        ps.append(wl.pvalue)
        rows.append({"comparison": lab, "pairs": len(d), "first_higher": int((d[x] > d[y]).sum()),
                     "equal": int((d[x] == d[y]).sum()), "first_lower": int((d[x] < d[y]).sum()), "wilcoxon_p": wl.pvalue})
    cp = pd.DataFrame(rows)
    cp["holm_p"] = holm(ps)
    save(cp, "rq3_comfort_paired", "RQ3: paired comfort comparisons")

    nec = D[D.a_necessary >= 4]
    rq = D[D.requester]
    acc_p = D[D.accepted > 0]
    rq3 = pd.DataFrame([
        ("Agree access is necessary", pct(len(nec), len(D))),
        ("... of whom uncomfortable with text sent to backend", pct(int((nec.cf_backend <= 2).sum()), len(nec))),
        ("... of whom not comfortable (uncomfortable or neutral)", pct(int((nec.cf_backend <= 3).sum()), len(nec))),
        ("... of whom would take fewer features for less access", pct(int((nec.a_fewer >= 4).sum()), int(nec.a_fewer.notna().sum()))),
        ("Expected mostly local processing", pct(int((D.e_local >= 4).sum()), len(D))),
        ("Expected local and did not expect external processing", pct(int(((D.e_local >= 4) & (D.e_ext <= 3)).sum()), len(D))),
        ("Requesters (sent text to backend before the disclosure)", str(len(rq))),
        ("... later uncomfortable with text sent to backend", pct(int((rq.cf_backend <= 2).sum()), len(rq))),
        ("... later neutral", pct(int((rq.cf_backend == 3).sum()), len(rq))),
        ("... later comfortable", pct(int((rq.cf_backend >= 4).sum()), len(rq))),
        ("... had expected mostly local processing", pct(int((rq.e_local >= 4).sum()), len(rq))),
        ("Accepted at least one suggestion, later uncomfortable with backend", pct(int((acc_p.cf_backend <= 2).sum()), len(acc_p))),
    ], columns=["measure", "value"])
    save(rq3, "rq3_necessity_and_prior_transmission", "RQ3: necessity, expectations and transmission before disclosure")

    # ---- RQ4 ---------------------------------------------------------------
    rel = pd.DataFrame([{"scale": COMPOSITE_LABELS[k], "items": len(v), "cronbach_alpha": cronbach(D[v]),
                         "mean": D[k].mean(), "sd": D[k].std(ddof=1)} for k, v in COMPOSITES.items()])
    save(rel, "rq4_scale_reliability", "RQ4: scale reliability")

    rows = []
    for k in ["DATA", "UNDER", "BURDEN", "CONTROL", "CONCERN"]:
        rho, lo, hi, nn = boot_spearman(D[k], D.ADOPT, rng)
        rho2, lo2, hi2, n2 = boot_spearman(D[k], D.w_use, rng)
        rows.append({"construct": COMPOSITE_LABELS[k], "n": nn, "rho_with_adoption_scale": rho, "ci_low": lo, "ci_high": hi,
                     "rho_with_willingness_item": rho2, "item_ci_low": lo2, "item_ci_high": hi2, "item_n": n2})
    for item, lab in [("cf_backend", "Item: comfort, text sent to backend"), ("cf_read", "Item: comfort, tool reads text"),
                      ("b_interrupt", "Item: interrupted more than liked"), ("b_effort", "Item: too much effort"),
                      ("u_score", "Item: understood the risk score")]:
        rho, lo, hi, nn = boot_spearman(D[item], D.ADOPT, rng)
        rho2, lo2, hi2, n2 = boot_spearman(D[item], D.w_use, rng)
        rows.append({"construct": lab, "n": nn, "rho_with_adoption_scale": rho, "ci_low": lo, "ci_high": hi,
                     "rho_with_willingness_item": rho2, "item_ci_low": lo2, "item_ci_high": hi2, "item_n": n2})
    save(pd.DataFrame(rows), "rq4_adoption_correlates", "RQ4: what goes with adoption intent (Spearman, bootstrap 95% intervals)")

    xs = ["DATA", "UNDER", "BURDEN", "CONTROL", "CONCERN"]
    d = D[["ADOPT"] + xs].dropna().reset_index(drop=True)
    b, r2 = std_betas(d, "ADOPT", xs)
    boots = np.array([std_betas(d.iloc[rng.integers(0, len(d), len(d))], "ADOPT", xs)[0] for _ in range(N_BOOT)])
    loo = np.array([std_betas(d.drop(i), "ADOPT", xs)[0] for i in range(len(d))])
    reg = pd.DataFrame({"predictor": [COMPOSITE_LABELS[x] for x in xs], "std_beta": b,
                        "ci_low": np.percentile(boots, 2.5, axis=0), "ci_high": np.percentile(boots, 97.5, axis=0),
                        "leave_one_out_min": loo.min(axis=0), "leave_one_out_max": loo.max(axis=0)})
    save(reg, "rq4_adoption_regression", "RQ4: adoption intent regressed on all five constructs",
         f"Ordinary least squares on standardised scale scores, n = {len(d)}, R2 = {r2:.2f}. Intervals are bootstrap percentile intervals.")

    bk = pd.cut(D.cf_backend, [0, 2, 3, 5], labels=["Uncomfortable", "Neutral", "Comfortable"])
    wk = pd.cut(D.w_use, [0, 2, 3, 5], labels=["Unwilling", "Neutral", "Willing"])
    save(pd.crosstab(bk, wk).reset_index().rename(columns={"cf_backend": "comfort_text_sent_to_backend"}),
         "rq4_willing_by_backend_comfort", "RQ4: willingness by comfort with text sent to the backend")

    # ---- Appendix checks ---------------------------------------------------
    def survey_summary(x):
        rho = spearmanr(x.DATA, x.ADOPT).statistic if len(x) > 3 else np.nan
        return {"n": len(x), "score_item_correct": pct(int(x.k_score_ok.sum()), len(x)),
                "comfortable_reading": pct(int((x.cf_read >= 4).sum()), len(x)),
                "comfortable_backend": pct(int((x.cf_backend >= 4).sum()), len(x)),
                "expected_local": pct(int((x.e_local >= 4).sum()), len(x)),
                "willing": pct(int((x.w_use >= 4).sum()), int(x.w_use.notna().sum())),
                "want_recommend_i_decide": pct(int((x.p_control == 5).sum()), len(x)),
                "rho_data_comfort_adoption": round(rho, 3)}
    grp = {"All participants": D, "Requesters only": D[D.requester], "Never requested": D[~D.requester]}
    save(pd.DataFrame({k: survey_summary(v) for k, v in grp.items()}).T.reset_index().rename(columns={"index": "group"}),
         "appendix_survey_by_group", "Appendix: survey results by requester status")

    # ---- Planned tests ------------------------------------------------------
    rows, ps = [], []
    for lab, x, y in [("Context item correct with self-rated understanding of context dependence", D.k_ctx_ok.astype(float), D.u_ctx),
                      ("Overall comfort with data practices with willingness to use", D.cf_overall, D.w_use),
                      ("Perceived effort with willingness to use", D.b_effort, D.w_use)]:
        rho, lo, hi, nn = boot_spearman(x, y, rng)
        _, pv = perm_spearman(x, y, rng)
        ps.append(pv)
        rows.append({"planned_association": lab, "n": nn, "spearman_rho": rho, "ci_low": lo, "ci_high": hi, "permutation_p": pv})
    pl = pd.DataFrame(rows)
    pl["holm_p"] = holm(ps)
    save(pl, "planned_tests", "Planned tests (Spearman, bootstrap 95% interval, permutation p, Holm-adjusted)")

    # ---- Survey items and sample -------------------------------------------
    labels = {"c_bother": "Bothered when websites ask for personal information", "c_twice": "Thinks twice before sharing",
              "c_collect": "Websites collect too much",
              "u_flag": "Understood why information was flagged", "u_ctx": "Understood why advice differs across websites",
              "u_score": "Understood the risk score", "u_easy": "Advice easy to understand", "u_expl": "Explanations helped",
              "e_read": "Expected: reads typed text", "e_local": "Expected: mostly local processing",
              "e_ext": "Expected: sends information to external servers",
              "cf_read": "Comfortable: reading text", "cf_backend": "Comfortable: text sent to backend",
              "cf_meta": "Comfortable: website details and categories sent", "cf_overall": "Comfortable overall with data practices",
              "a_necessary": "Access is necessary", "a_reasonable": "Access is reasonable", "a_more": "Accesses more than expected",
              "a_fewer": "Prefer fewer features for less access",
              "b_interrupt": "Interrupted more than liked", "b_effort": "Too much effort", "b_manage": "Number of warnings manageable",
              "b_compat": "Protects privacy without preventing tasks", "b_riskinfl": "Risk level influenced following advice",
              "w_use": "Willing to use", "w_benefit": "Benefit justifies use", "w_fit": "Fits how I browse",
              "ct_override": "Could easily override", "ct_choice": "Enough control over suggestions"}
    it = pd.DataFrame([{"item": lab, "variable": v, "n": int(D[v].notna().sum()), "top_two": int((D[v] >= 4).sum()),
                        "middle": int((D[v] == 3).sum()), "bottom_two": int((D[v] <= 2).sum()),
                        "top_two_pct": round(100 * (D[v] >= 4).sum() / D[v].notna().sum(), 1)} for v, lab in labels.items()])
    save(it, "survey_items", "Survey items: responses in the top two, middle and bottom two of five options",
         "Top two = agree / comfortable / expected.")
    dm = []
    for v in ["age", "gender", "edu", "exp", "prior_ext"]:
        for code, cnt in D[v].value_counts().sort_index().items():
            dm.append({"variable": v, "choice_code": int(code), "participants": int(cnt)})
    save(pd.DataFrame(dm), "sample", "Sample description (choice codes follow the survey export)",
         f"Median session length {D.duration_s.median()/60:.1f} minutes (interquartile range "
         f"{D.duration_s.quantile(.25)/60:.1f}-{D.duration_s.quantile(.75)/60:.1f}).")
    op, nop = D[D.expl_attempts > 0], D[D.expl_attempts == 0]
    md.append(f"Expected mostly local processing: {pct(int((op.e_local >= 4).sum()), len(op))} of participants who opened the "
              f"explanation panel, {pct(int((nop.e_local >= 4).sum()), len(nop))} of those who never opened it.\n")
    md.append(f"Requests by site: {a.site.value_counts().to_dict()}; median requests per requester "
              f"{D[D.requester].attempts.median():.0f}; median suggestions per request {r.groupby('attempt_id').size().median():.0f}.\n")

    with open(f"{out}/RESULTS.md", "w") as f:
        f.write("\n".join(md))
    # participant-level files for figures.py: never publish this folder
    os.makedirs(f"{out}/private", exist_ok=True)
    D.drop(columns=["QID75"]).to_csv(f"{out}/private/participant_level.csv", index=False)
    r.drop(columns=["category"]).to_csv(f"{out}/private/suggestion_level.csv", index=False)
    a.to_csv(f"{out}/private/request_level.csv", index=False)
    print("\n".join(md))


if __name__ == "__main__":
    root = sys.argv[1]
    main(root, sys.argv[2])
