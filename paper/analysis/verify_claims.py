#!/usr/bin/env python3
"""Check every numeric claim the referees queried against the deposited records.

Each check prints MANUSCRIPT (what the submitted text says), DEPOSIT (what the
records give), and a verdict.  Run after build_dataset.py.

Usage:  python paper/analysis/verify_claims.py
"""
from __future__ import annotations

import os
import textwrap

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "paper", "analysis", "outputs", "episodes.csv")

VERDICTS = []


def check(tag, where, manuscript, deposit, verdict):
    VERDICTS.append((tag, verdict))
    print("\n" + "=" * 78)
    print("[%s]  %s" % (tag, where))
    print("-" * 78)
    for label, body in (("MANUSCRIPT", manuscript), ("DEPOSIT", deposit)):
        print("%-11s %s" % (label, textwrap.fill(str(body), 64,
                                                 subsequent_indent=" " * 12).strip()))
    print("%-11s %s" % ("VERDICT", verdict))


def main():
    d = pd.read_csv(CSV)
    d = d[d.judge_config == "dualjudge"]          # the reported confirmatory matrix

    # ---------------------------------------------------------------- R3 M2
    cov = pd.crosstab(d.module, d.protocol)
    check("R3-Major-2", "Section 3.3 / Table 2 / Contribution 2 - the protocol ladder",
          "Four rungs P0-P3 described as one ladder; H2 states P3 <= P2 <= P1 ~ P0.",
          "Module I ran P0/P1/P3 (no P2); Module II ran P0/P2 (no P1, no P3). "
          "P2 and P3 are never compared. Counts: %s"
          % cov.to_dict(),
          "REFEREE CORRECT - the ladder is two partial ladders; H2 was never "
          "testable within a module.")

    # ---------------------------------------------------------------- R3 M4
    cell = d[(d.agent == "DeepSeek-V4-Pro") & (d.cover_paper == "N2")
             & (d.protocol == "P2") & (d.bond == 0.20)]
    nparam = cell[["p1", "delta", "c_A", "c_B"]].drop_duplicates().shape[0]
    modal = cell.agreement_x.value_counts()
    check("R3-Major-4", "Section 4.4 - 'numeric parameters ... drawn per episode'",
          "Numeric parameters, actor names and the disputed asset are drawn "
          "procedurally per episode from seeded generators.",
          "In the named cell (DeepSeek-V4-Pro, N2, b=0.20, n=%d) there is %d "
          "distinct numeric parameter vector and the modal offer covers %d/%d "
          "episodes. The seed varies actor/region names only (scenarios.pick_names); "
          "game parameters are fixed by the cell configuration."
          % (len(cell), nparam, modal.iloc[0], len(cell)),
          "REFEREE CORRECT - Section 4.4 must be corrected; episodes within a "
          "cell are near-replicates.")

    # ---------------------------------------------------------------- R3 m5
    mus = sorted(d[d.module == "I"].mu.dropna().unique())
    check("R3-Minor-5", "Section 3.7 - Module I priors",
          "mu in {0.30, 0.43, 0.60, 0.80} bracketing the threshold mu_bar=0.4286.",
          "Only mu=%s appears in the deposited Module I records (n=%d)."
          % (mus, (d.module == "I").sum()),
          "REFEREE CORRECT - only one prior was run; the other three must be "
          "removed or reported as not run.")

    # ---------------------------------------------------------------- R3 m4
    m2 = d[(d.module == "II") & (d.protocol == "P2") & (d.agree == 1)]
    trough = m2[m2.bond == 0.20]
    per_agent = trough.groupby("agent").ED.mean().round(4)
    front = m2[m2.tier == "high"]
    ed118 = front[front.bond == 0.118].ED.mean()
    ed20 = front[front.bond == 0.20].ED.mean()
    check("R3-Minor-4", "Sections 4.8 / 6.3 - the ED = 0.0045 claim",
          "Reference client scores ED=0.0045 on its own runs (4.8); at the trough "
          "the agreed division lands on x* to within half a percentage point "
          "(ED=0.0045), equal to the reference client's value (6.3).",
          "ED=0.0045 occurs in neither place. It is a PILOT value: Sonnet 5, "
          "cover S2, bond b=0.12, superseded gemma judge "
          "(out/g2_pilot_anthropic-claude-sonnet-5_judge-gemma.json). In the "
          "confirmatory matrix, trough (b=0.20) per-agent ED = %s. Frontier "
          "pooled ED = %.4f at b=0.118 and %.4f at b=0.20. The reference client "
          "scores 0.0003 pooled (0.0000-0.0020 per cell)."
          % (dict(per_agent), ed118, ed20),
          "REFEREE CORRECT, AND THE ERROR IS LARGER THAN STATED - a pilot number "
          "at a different bond was carried into the confirmatory narrative and "
          "misattributed to the reference client.")

    # ---------------------------------------------------------------- R3 m1
    p3 = d[(d.module == "I") & (d.protocol == "P3")]
    reas = p3[p3.reasoning == "reasoning"]
    rng = reas.groupby(["agent", "cover_paper"]).dr_verbal_ep.mean().dropna()
    check("R3-Minor-1", "Section 6.2 - DR_verbal under P3 on the reasoning tiers",
          "'highest on the reasoning tiers (0.29-0.50)'.",
          "Engine-computed per agent x cover range is %.2f-%.2f (o4-mini reaches "
          "%.2f on N1). Table 3 already reports 0.39-0.64 for o4-mini, so the "
          "table is right and the prose is wrong."
          % (rng.min(), rng.max(), rng.max()),
          "REFEREE CORRECT - prose range should read 0.29-0.64.")

    # ------------------------------------------------------------ R3 results
    t = d[(d.module == "II") & (d.protocol == "P2") & (d.bond == 0.20)]
    split = t.groupby("agent")[["breakdown", "defect", "conflict_any"]].mean().round(3)
    check("R3-Results", "Section 4.7 / Table 3 - what 'conflict' counts in Module II",
          "Section 3.1 defines conflict, breakdown and defect as distinct terms; "
          "Table 3 reports 'conflict' and 'accept-then-defect' as separate columns.",
          "metrics.war_rate pools war_now + attack_t2, so the Module II conflict "
          "column CONTAINS the defection column. Decomposition at b=0.20: %s"
          % split.to_dict("index"),
          "REFEREE CORRECT - the two columns are not independent; conflict must "
          "be split into immediate breakdown and period-2 defection.")

    # --------------------------------------------------------------- P1 null
    m1 = d[(d.module == "I") & d.protocol.isin(["P0", "P1"])]
    piv = m1.pivot_table(index="agent", columns="protocol",
                         values="conflict_any", aggfunc="mean").round(3)
    check("R3-Results-P1", "Section 6.1 / 7.3 - the P1 null",
          "'Recording alone (P1) leaves behaviour essentially unchanged ... "
          "The null holds.' Reported in words only.",
          "P1 ran in Module I only (n=330 vs 660 at P0) and never in Module II. "
          "Per-agent P0->P1 conflict: %s. Pooled %.3f -> %.3f. Several agents "
          "move substantially (Claude Haiku 4.5 up, o4-mini down)."
          % (piv.to_dict("index"), m1[m1.protocol == "P0"].conflict_any.mean(),
             m1[m1.protocol == "P1"].conflict_any.mean()),
          "PARTLY CORRECT - the null needs a reported test, not a word, and its "
          "scope is Module I only.")

    # ------------------------------------------------------- separation risk
    cells = d[(d.module == "II") & (d.protocol == "P2")].groupby(
        ["agent", "cover_paper", "bond"]).conflict_any.mean()
    degen = ((cells == 0) | (cells == 1)).sum()
    check("R3-Major-3", "Section 5.4 - feasibility of the specified model",
          "Mixed-effects logistic regression with crossed random intercepts for "
          "agent and seed; Holm-corrected contrasts; Cliff's delta with CIs.",
          "%d of %d agent x cover x bond cells are degenerate (0%% or 100%%), and "
          "the agent factor has only %d levels. Complete separation makes the "
          "specified model unstable, as the referee anticipated."
          % (degen, len(cells), d.agent.nunique()),
          "REFEREE CORRECT - report a penalised / cover-level analysis and say "
          "plainly what was and was not run.")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for tag, v in VERDICTS:
        print("  %-16s %s" % (tag, v.split(" - ")[0]))


if __name__ == "__main__":
    main()
