"""Data loading.

Builds the participant, request and suggestion tables from the raw study
exports. The raw exports are not part of this repository (see README.md and
analysis/DATA_FORMAT.md); this file documents exactly how they were read.

Only records on the three study websites are kept; records on any other
domain are dropped before analysis.
"""
import glob
import json
import os

import numpy as np
import pandas as pd

SURVEY_NAMES = {
    "QID13": "age", "QID14": "gender", "QID15": "edu", "QID16_1": "exp",
    "QID17_1": "c_bother", "QID17_2": "c_twice", "QID17_3": "c_collect",
    "QID20": "n_ext", "QID21": "prior_ext", "QID22": "pii",
    "QID58_4": "u_flag", "QID58_5": "u_ctx", "QID58_6": "u_score", "QID58_7": "u_easy", "QID58_8": "u_expl",
    "QID59": "k_under", "QID60": "k_anon", "QID61": "k_ctx", "QID62": "k_score",
    "QID64_1": "e_read", "QID64_7": "e_local", "QID64_8": "e_ext",
    "QID67_1": "cf_read", "QID67_4": "cf_backend", "QID67_5": "cf_meta",
    "QID68_1": "a_necessary", "QID68_2": "a_reasonable", "QID68_3": "a_more", "QID68_4": "a_fewer",
    "QID69_1": "cf_overall",
    "QID70_1": "b_interrupt", "QID70_2": "b_effort", "QID70_3": "b_manage", "QID70_4": "b_compat", "QID70_5": "b_riskinfl",
    "QID71_1": "w_use", "QID71_2": "w_benefit", "QID71_3": "w_fit",
    "QID72_1": "ct_override", "QID72_2": "ct_choice", "QID73_1": "p_control", "QID74": "p_conflict",
}

# Correct answers to the four comprehension items (choice codes of the survey export).
CORRECT = {"k_under": 2, "k_anon": 3, "k_ctx": 2, "k_score": 3}

COMPOSITES = {
    "DATA": ["cf_read", "cf_backend", "cf_meta", "cf_overall", "a_reasonable", "a_necessary"],
    "UNDER": ["u_flag", "u_ctx", "u_score", "u_easy", "u_expl"],
    "BURDEN": ["b_interrupt", "b_effort"],
    "CONTROL": ["ct_override", "ct_choice"],
    "ADOPT": ["w_use", "w_benefit", "w_fit"],
    "CONCERN": ["c_bother", "c_twice", "c_collect"],
}
COMPOSITE_LABELS = {
    "DATA": "Data-practice comfort", "UNDER": "Self-rated understanding", "BURDEN": "Burden",
    "CONTROL": "Experienced control", "ADOPT": "Adoption intent", "CONCERN": "Baseline privacy concern",
}

LOG_TABLES = ["text_warning_metrics", "text_anonymisation_attempts", "text_replacement_interactions",
              "usage_metrics", "anonymization_requests"]


# Substrings that identify the three study websites in the logged domain. The
# host names are withheld; they are read from sites.json in the data folder
# (see DATA_FORMAT.md): {"social": "...", "chatbot": "...", "search": "..."}.
SITE_PATTERNS = {}


def site_of(domain):
    d = str(domain)
    for site, pattern in SITE_PATTERNS.items():
        if pattern in d:
            return site
    return "other"


def _jsonish(x):
    """Log JSON columns arrive as strings (CSV) or native objects (JSON)."""
    if isinstance(x, str):
        try:
            return json.loads(x)
        except ValueError:
            return x
    return x


def load_survey(root):
    appr = pd.read_csv(f"{root}/recruitment/approved_ids.csv", dtype=str)
    m = pd.read_csv(f"{root}/survey/session_code_mapping.csv", dtype=str)
    m = m[m.prolific_id.isin(appr.prolific_id)]
    keep = set(m.response_id)
    rows = []
    for r in json.load(open(f"{root}/survey/responses_export.json"))["responses"]:
        if r["responseId"] in keep:
            v = r["values"]
            row = {"response_id": r["responseId"], "duration_s": pd.to_numeric(v.get("duration"), errors="coerce"), "QID75": v.get("QID75")}
            for qid, name in SURVEY_NAMES.items():
                row[name] = pd.to_numeric(v.get(qid), errors="coerce")
            rows.append(row)
    s = pd.DataFrame(rows).merge(m[["response_id", "session_code"]], on="response_id")
    s = s.rename(columns={"session_code": "pid"}).drop(columns="response_id")
    # Expectation items are coded 1 = definitely yes ... 5 = definitely not; flip so high = expected.
    for c in ["e_read", "e_local", "e_ext"]:
        s[c] = 6 - s[c]
    for k, items in COMPOSITES.items():
        s[k] = s[items].mean(axis=1)
    for k, ans in CORRECT.items():
        s[k + "_ok"] = (s[k] == ans)
    assert len(s) == 50 and s.pid.nunique() == 50, "expected 50 approved participants"
    return s


def load_logs(root):
    """Log tables: one CSV per table in logs/by_table, plus optional per-participant
    JSON exports of the same tables in logs/by_participant."""
    SITE_PATTERNS.clear()
    SITE_PATTERNS.update(json.load(open(f"{root}/sites.json")))
    keys = {"text_warning_metrics": "set_id", "text_anonymisation_attempts": "attempt_id",
            "text_replacement_interactions": "replacement_id", "usage_metrics": "id",
            "anonymization_requests": "request_id"}
    t = {}
    for n in LOG_TABLES:
        t[n] = pd.read_csv(f"{root}/logs/by_table/{n}.csv", na_values="\\N",
                           dtype={"export_participant_id": str, "participant_code": str})
    for f in sorted(glob.glob(f"{root}/logs/by_participant/*.json")):
        d = json.load(open(f))
        pid = str(d["participant_code"])
        for n in LOG_TABLES:
            add = pd.DataFrame(d["tables"].get(n, []))
            if add.empty:
                continue
            add["export_participant_id"] = pid
            add = add[~add[keys[n]].astype(str).isin(set(t[n][keys[n]].astype(str)))]  # skip duplicates
            t[n] = pd.concat([t[n], add], ignore_index=True)
    w, a, r, u, q = [t[n] for n in LOG_TABLES]
    w["site"] = w.domain.map(site_of)
    q["site"] = q.domain.map(site_of)
    w["pid"] = w.export_participant_id
    a = a.merge(w[["set_id", "site", "pid"]], on="set_id", how="left")
    r = r.merge(a[["attempt_id", "site", "pid", "explanation_open_count", "end_reason", "requested_at"]],
                on="attempt_id", how="left")
    r["cat"] = r.category.map(lambda x: (_jsonish(x) or [None])[0])
    r["cat"] = r["cat"].map(lambda c: c.title() if isinstance(c, str) else c)
    q["meta"] = q.request_metadata.map(_jsonish)
    # Study sites only.
    w = w[w.site != "other"].copy()
    a = a[a.site != "other"].copy()
    r = r[(r.site != "other") & r.displayed_at.notna()].copy()
    q = q[q.site != "other"].copy()
    r["accepted"] = r.outcome.eq("accepted")
    r["explicit"] = r.outcome.isin(["accepted", "dismissed"])
    return w, a, r, u, q


def participant_behaviour(s, w, a, r):
    p = pd.DataFrame({"pid": s.pid})
    cnt = lambda df, col="pid": p.pid.map(df.groupby(col).size()).fillna(0).astype(int)
    p["warning_sets"] = cnt(w)
    p["attempts"] = cnt(a)
    p["displayed"] = cnt(r)
    for o in ["accepted", "dismissed", "unresolved", "invalidated", "pending"]:
        p[o] = cnt(r[r.outcome == o])
    p["apply_all"] = cnt(r[(r.outcome == "accepted") & (r.action_source == "apply_all")])
    p["individual_accept"] = cnt(r[(r.outcome == "accepted") & (r.action_source == "individual")])
    p["expl_attempts"] = cnt(a[a.explanation_open_count > 0])
    p["requester"] = p.attempts > 0

    def typ(x):
        if x.attempts == 0:
            return "Never requested"
        if x.accepted + x.dismissed == 0:
            return "Requested, then left"
        if x.dismissed > 0:
            return "Selective (ever dismissed)"
        if x.apply_all > 0 and x.individual_accept == 0:
            return "Bulk accept only"
        if x.accepted == x.displayed:
            return "Accepted all, one by one"
        return "Accepted some, left the rest"
    p["behaviour_type"] = p.apply(typ, axis=1)
    return p
