"""Figures 2 to 6 of the paper, sized for a two-column template.

Usage:  python3 analysis/figures.py <output_dir>

Reads <output_dir>/private/*.csv and <output_dir>/tables/*.csv written by
analysis.py and writes vector PDFs (TrueType fonts embedded) and PNG
previews to <output_dir>/figures.

Widths: one column = 3.35 in, full text width = 7.0 in.
"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch, Rectangle

COL, FULL = 3.35, 7.0
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8983", "#e4e3de"
BLUE_D, BLUE, BLUE_M, BLUE_L = "#184f95", "#2a78d6", "#5598e7", "#9ec5f4"
RED, RED_L, NEUTRAL = "#c8403f", "#eaa29b", "#cfcec8"

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "DejaVu Sans", "font.size": 7,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK, "xtick.major.width": 0.5, "ytick.major.width": 0,
    "xtick.major.size": 2.5, "ytick.major.size": 0, "legend.frameon": False, "figure.dpi": 150,
    "hatch.linewidth": 0.5,
})


def clean(ax, keep=("bottom",)):
    for sp in ["top", "right", "left", "bottom"]:
        ax.spines[sp].set_visible(sp in keep)


def save(fig, out, name):
    fig.savefig(f"{out}/figures/{name}.pdf")
    fig.savefig(f"{out}/figures/{name}.png", dpi=300)
    plt.close(fig)


# ---------------------------------------------------------------------------
def fig_outcomes(out, r):
    """Figure 3: what happened to displayed suggestions, overall and by destination."""
    def shares(x):
        acc = x[x.outcome == "accepted"]
        n = len(x)
        return [((acc.action_source == "apply_all").sum()) / n, ((acc.action_source == "individual").sum()) / n,
                (x.outcome == "dismissed").sum() / n, (~x.outcome.isin(["accepted", "dismissed"])).sum() / n], n
    rows = [("All destinations", r)] + [(lab, r[r.site == s]) for lab, s in
                                         [("Social post", "social"), ("Chatbot prompt", "chatbot"), ("Search query", "search")]]
    labels = ["Accepted with Apply All", "Accepted one by one", "Dismissed", "Left without a decision"]
    colors = [BLUE_D, BLUE_M, RED, NEUTRAL]
    fig, ax = plt.subplots(figsize=(COL, 1.75))
    for i, (lab, x) in enumerate(rows):
        sh, n = shares(x)
        left = 0
        for j, v in enumerate(sh):
            ax.barh(i, v * 100, left=left, height=0.56, color=colors[j], edgecolor="white", linewidth=1.0)
            if v >= 0.085:
                ax.text(left + v * 50, i, f"{v*100:.0f}%", ha="center", va="center", fontsize=6.5,
                        color="white" if j in (0, 2) else INK)
            left += v * 100
        ax.text(-2, i, f"{lab}\n", ha="right", va="center", fontsize=7, linespacing=0.9)
        ax.text(-2, i + 0.2, f"n = {n}", ha="right", va="center", fontsize=6, color=INK2)
    ax.axhline(0.5, color=GRID, lw=0.6)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Share of displayed suggestions (%)")
    clean(ax)
    ax.legend(handles=[Patch(facecolor=c, label=l) for c, l in zip(colors, labels)], ncol=2, loc="lower center",
              bbox_to_anchor=(0.36, 1.0), fontsize=6.5, handlelength=1.0, handleheight=0.8, columnspacing=1.0, borderaxespad=0.2)
    fig.subplots_adjust(left=0.265, right=0.955, top=0.80, bottom=0.2)
    save(fig, out, "fig3_suggestion_outcomes")


def fig_stated_enacted(out, D):
    """Figure 4: stated control preferences beside behaviour types from the logs."""
    fig = plt.figure(figsize=(FULL, 2.05))
    a1 = fig.add_axes([0.275, 0.19, 0.20, 0.66])
    a2 = fig.add_axes([0.765, 0.19, 0.20, 0.66])
    stated = [("Preferred role of the tool", None),
              ("Tool recommends, I decide", int((D.p_control == 5).sum())),
              ("I decide without recommendations", int((D.p_control == 4).sum())),
              ("Tool acts for me", int((D.p_control == 1).sum())),
              ("If the tool and I disagree", None),
              ("Follow my own judgement", int((D.p_conflict == 1).sum())),
              ("Depends on the situation", int((D.p_conflict == 2).sum())),
              ("Follow the tool", int((D.p_conflict == 3).sum()))]
    y = 0
    ticks = []
    for lab, v in stated:
        if v is None:
            a1.text(-0.03, y, lab, transform=a1.get_yaxis_transform(), ha="right", va="center", fontsize=7, color=INK2, style="italic")
        else:
            a1.barh(y, v, height=0.56, color=BLUE)
            a1.text(v + 0.8, y, str(v), va="center", fontsize=6.5, color=INK)
            ticks.append((y, lab))
        y += 1 if v is not None else 0.85
    a1.set_yticks([t for t, _ in ticks], [l for _, l in ticks])
    a1.set_ylim(y - 0.4, -0.6)
    fig.text(0.005, 0.94, "(a) What participants said", fontsize=7.5, fontweight="bold")

    order = ["Bulk accept only", "Accepted some, left the rest", "Requested, then left",
             "Selective (ever dismissed)", "Accepted all, one by one", "Never requested"]
    nice = {"Bulk accept only": "Accepted only with Apply All", "Accepted some, left the rest": "Accepted some, left the rest undecided",
            "Requested, then left": "Requested suggestions, decided none",
            "Selective (ever dismissed)": "Dismissed at least one suggestion",
            "Accepted all, one by one": "Accepted every suggestion one by one",
            "Never requested": "Never requested suggestions"}
    vc = D.behaviour_type.value_counts()
    for i, k in enumerate(order):
        v = int(vc.get(k, 0))
        a2.barh(i, v, height=0.56, color=NEUTRAL if k == "Never requested" else BLUE)
        a2.text(v + 0.8, i, str(v), va="center", fontsize=6.5)
    a2.set_yticks(range(len(order)), [nice[k] for k in order])
    a2.set_ylim(len(order) - 0.4, -0.6)
    fig.text(0.505, 0.94, "(b) What the logs show", fontsize=7.5, fontweight="bold")
    for ax in (a1, a2):
        ax.set_xlim(0, 50)
        ax.set_xticks([0, 10, 20, 30, 40, 50])
        ax.set_xlabel("Participants (of 50)")
        clean(ax)
    save(fig, out, "fig4_stated_vs_enacted_control")


def fig_expect_comfort(out, D):
    """Figure 5: expectations before the disclosure and comfort after it."""
    blocks = [
        ("Expected before the disclosure", ["Definitely not", "Probably not", "Not sure", "Probably yes", "Definitely yes"],
         [("e_read", "The tool can read text I type or paste"),
          ("e_local", "Most sensitive information is processed on my device"),
          ("e_ext", "Some information is sent to external servers")]),
        ("Comfort after the disclosure", ["Very uncomfortable", "Uncomfortable", "Neutral", "Comfortable", "Very comfortable"],
         [("cf_read", "The tool reads text I type or paste"),
          ("cf_backend", "Typed text is sent to the backend for suggestions"),
          ("cf_meta", "Website details and data categories are sent to the backend"),
          ("cf_overall", "The tool's data practices overall")]),
    ]
    colors = [RED, RED_L, NEUTRAL, BLUE_L, BLUE_D]
    fig, axes = plt.subplots(2, 1, figsize=(FULL, 2.75), gridspec_kw={"height_ratios": [3, 4], "hspace": 0.62})
    for ax, (title, levels, items) in zip(axes, blocks):
        for i, (col, lab) in enumerate(items):
            v = D[col].dropna()
            p = np.array([(v == k).mean() * 100 for k in range(1, 6)])
            start = -(p[0] + p[1] + p[2] / 2)
            left = start
            for j in range(5):
                ax.barh(i, p[j], left=left, height=0.58, color=colors[j], edgecolor="white", linewidth=1.0)
                if p[j] >= 9:
                    ax.text(left + p[j] / 2, i, f"{p[j]:.0f}", ha="center", va="center", fontsize=6.3,
                            color="white" if j in (0, 4) else INK)
                left += p[j]
            ax.text(104, i, f"{p[3] + p[4]:.0f}%", va="center", ha="left", fontsize=7, fontweight="bold")
        ax.set_yticks(range(len(items)), [l for _, l in items])
        ax.set_ylim(len(items) - 0.45, -0.55)
        ax.set_xlim(-100, 100)
        ax.axvline(0, color=MUTED, lw=0.6, zorder=0)
        ax.set_xticks([-100, -50, 0, 50, 100], ["100", "50", "0", "50", "100"])
        clean(ax)
        ax.text(-0.96, 1.0, title, transform=ax.transAxes, fontsize=7.5, fontweight="bold", va="bottom", ha="left")
        ax.legend(handles=[Patch(facecolor=c, label=l) for c, l in zip(colors, levels)], ncol=5, loc="lower right",
                  bbox_to_anchor=(1.0, 0.985), fontsize=6.3, handlelength=0.9, handleheight=0.8, columnspacing=0.9,
                  handletextpad=0.4, borderaxespad=0.0)
    axes[1].set_xlabel("Share of participants (%), centred on the middle category")
    fig.subplots_adjust(left=0.465, right=0.935, top=0.92, bottom=0.14)
    save(fig, out, "fig5_expectations_and_comfort")


def fig_correlates(out):
    """Figure 6: Spearman correlation of each construct with adoption intent."""
    t = pd.read_csv(f"{out}/tables/rq4_adoption_correlates.csv")
    t = t[~t.construct.str.startswith("Item:")].sort_values("rho_with_adoption_scale", ascending=False).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(COL, 1.55))
    ax.axvline(0, color=MUTED, lw=0.6)
    for i, x in t.iterrows():
        ax.plot([x.ci_low, x.ci_high], [i, i], color=BLUE, lw=1.6, solid_capstyle="round")
        ax.plot(x.rho_with_adoption_scale, i, "o", color=BLUE, ms=5.5, mec="white", mew=1.0)
        ax.text(1.04, i, f"{x.rho_with_adoption_scale:+.2f}".replace("-", "−"), va="center", ha="left", fontsize=7)
    ax.set_yticks(range(len(t)), t.construct)
    ax.set_ylim(len(t) - 0.5, -0.5)
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1], ["−1", "−0.5", "0", "0.5", "1"])
    ax.set_xlabel("Spearman ρ with adoption intent")
    ax.xaxis.grid(True, color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    clean(ax)
    fig.subplots_adjust(left=0.40, right=0.89, top=0.97, bottom=0.26)
    save(fig, out, "fig6_adoption_correlates")


def _box(ax, x, y, w, h, text, fc="white", ec=MUTED, fs=5.6, bold=False, ls="-", color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012", fc=fc, ec=ec, lw=0.7, linestyle=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal",
            color=color, linespacing=1.15)


def fig_procedure(out):
    """Figure 2: study procedure with the position of each measure."""
    fig, ax = plt.subplots(figsize=(FULL, 1.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.12, 1)
    ax.axis("off")
    steps = [("Consent,\nscreening,\ndemographics", None), ("Pre-survey:\nprivacy\nattitudes,\nextensions", None),
             ("Install\nextension,\nread guide", None),
             ("Three tasks as\na fictional\npersona: social\npost, chatbot\n(caption, health),\nsearch", "task"),
             ("Understanding:\n5 self-rated,\n4 comprehension\nitems", None), ("Expected\ndata practices:\n3 items", None),
             ("Disclosure\nof the tool's\ndata practices", "disc"), ("Comfort and\naccess\ntrade-offs:\n8 items", None),
             ("Burden,\nadoption,\ncontrol:\n13 items", None)]
    widths = [0.092, 0.092, 0.088, 0.118, 0.108, 0.098, 0.098, 0.092, 0.088]
    gap = (1 - sum(widths)) / (len(steps) - 1)
    x, y, h = 0, 0.42, 0.42
    xs = []
    for (txt, kind), w in zip(steps, widths):
        fc = {"task": "#e8f0fb", "disc": "#fbe9e7"}.get(kind, "white")
        ec = {"task": BLUE, "disc": RED}.get(kind, MUTED)
        _box(ax, x, y, w, h, txt, fc=fc, ec=ec, bold=(kind == "disc"))
        xs.append((x, w))
        x += w + gap
    for (x0, w0), (x1, _) in zip(xs[:-1], xs[1:]):
        ax.add_patch(FancyArrowPatch((x0 + w0 + 0.002, y + h / 2), (x1 - 0.002, y + h / 2), arrowstyle="-|>", mutation_scale=5,
                                     lw=0.6, color=INK2, shrinkA=0, shrinkB=0))

    def span(i, j, label, yy, color=INK2):
        a, b = xs[i][0], xs[j][0] + xs[j][1]
        ax.plot([a, a, b, b], [yy + 0.035, yy, yy, yy + 0.035], color=color, lw=0.7)
        ax.text((a + b) / 2, yy - 0.03, label, ha="center", va="top", fontsize=6.2, color=color)
    span(3, 3, "Interaction logs\n(RQ2)", 0.36, BLUE_D)
    span(4, 4, "RQ1", 0.36)
    span(5, 7, "RQ3: expectations before, comfort after", 0.36)
    span(8, 8, "RQ2, RQ4", 0.36)
    ax.text(xs[0][0], 0.95, "Pre-use", fontsize=6.5, fontweight="bold", va="center")
    ax.text(xs[3][0], 0.95, "Use", fontsize=6.5, fontweight="bold", va="center")
    ax.text(xs[4][0], 0.95, "Post-use survey", fontsize=6.5, fontweight="bold", va="center")
    ax.plot([xs[0][0], xs[2][0] + xs[2][1]], [0.89, 0.89], color=MUTED, lw=0.6)
    ax.plot([xs[3][0], xs[3][0] + xs[3][1]], [0.89, 0.89], color=MUTED, lw=0.6)
    ax.plot([xs[4][0], xs[8][0] + xs[8][1]], [0.89, 0.89], color=MUTED, lw=0.6)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
    save(fig, out, "fig2_study_procedure")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(f"{out}/figures", exist_ok=True)
    D = pd.read_csv(f"{out}/private/participant_level.csv")
    r = pd.read_csv(f"{out}/private/suggestion_level.csv")
    fig_procedure(out)
    fig_outcomes(out, r)
    fig_stated_enacted(out, D)
    fig_expect_comfort(out, D)
    fig_correlates(out)
    print("figures written to", f"{out}/figures")
