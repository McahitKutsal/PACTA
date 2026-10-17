#!/usr/bin/env python3
"""Analyse the three arms added in revision: honesty control, cross-play, covers.

N1  prompted-honesty control  (R1 control-group, R2, R8 #3)
N2  cross-play                (R3 Major 6, R8 #2)
N4  Claude Sonnet 5 on the two Module II covers it had not run  (R8 #5)

Every dependent variable compared here is computed by the engine or the
referee, never by a judge, so the new arms (run with --mock-judge) are directly
comparable with the dual-judge confirmatory baseline.  Verbal deception is the
engine's own check of a structured type declaration against the known private
type; conflict, breakdown and defection are engine outcomes.

Handles partial data: arms still running are reported as incomplete rather than
silently averaged over whatever has landed.

Usage:  python paper/analysis/new_arms.py
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "paper", "analysis", "outputs", "episodes.csv")

EXPECTED_N = 30


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def fisher(k1, n1, k2, n2):
    """Two-sided Fisher exact on the 2x2; returns p."""
    if min(n1, n2) == 0:
        return np.nan
    return stats.fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1]


# ------------------------------------------------------------------- N1
def honesty(d):
    print("=" * 78)
    print("N1  PROMPTED-HONESTY CONTROL  (P0 vs P0 + conduct instruction)")
    print("=" * 78)
    arm = d[d.arm == "honesty"]
    if arm.empty:
        print("no honesty-arm records yet")
        return
    # The baseline is the confirmatory matrix only: the judge-* and mockjudge
    # pilot runs share arm == "baseline" but are not the reported cells.
    base = d[(d.arm == "baseline") & (d.judge_config == "dualjudge")
             & (d.protocol == "P0")]

    rows = []
    for (agent, cover, module), g in arm.groupby(["agent", "cover_paper", "module"]):
        b = base[(base.agent == agent) & (base.cover_paper == cover)
                 & (base.module == module)]
        if b.empty:
            continue
        rec = dict(agent=agent, cover=cover, module=module,
                   n_base=len(b), n_arm=len(g),
                   complete="yes" if len(g) >= EXPECTED_N else "PARTIAL")
        # verbal deception (Module I only: the type declaration is what can lie)
        if module == "I":
            vb, va = b.dr_verbal_ep.dropna(), g.dr_verbal_ep.dropna()
            rec["DRverbal_base"] = vb.mean() if len(vb) else np.nan
            rec["DRverbal_arm"] = va.mean() if len(va) else np.nan
            rec["p_DRverbal"] = (stats.mannwhitneyu(vb, va).pvalue
                                 if len(vb) > 2 and len(va) > 2 else np.nan)
        rec["conflict_base"] = b.conflict_any.mean()
        rec["conflict_arm"] = g.conflict_any.mean()
        rec["p_conflict"] = fisher(int(b.conflict_any.sum()), len(b),
                                   int(g.conflict_any.sum()), len(g))
        if module == "II":
            rec["defect_base"] = b.defect.mean()
            rec["defect_arm"] = g.defect.mean()
        rows.append(rec)

    t = pd.DataFrame(rows)
    if t.empty:
        print("no matched baseline cells yet")
        return
    for module in ("I", "II"):
        sub = t[t.module == module]
        if sub.empty:
            continue
        print("\nModule %s" % module)
        cols = [c for c in ["agent", "cover", "n_base", "n_arm", "complete",
                            "DRverbal_base", "DRverbal_arm", "p_DRverbal",
                            "conflict_base", "conflict_arm", "p_conflict",
                            "defect_base", "defect_arm"] if c in sub.columns]
        print(sub[cols].round(3).to_string(index=False))

    print("\nReading: the instruction and the protocol act on different things.")
    print("Where it suppresses the type declaration it does so strongly, but")
    print("that is speech, not payoff - so breakdown and defection need not")
    print("follow it down.")


# ------------------------------------------------------------------- N2
def crossplay(d):
    print("\n" + "=" * 78)
    print("N2  CROSS-PLAY  (self-play diagonals vs the off-diagonal cells)")
    print("=" * 78)
    arm = d[d.arm == "crossplay"]
    if arm.empty:
        print("no cross-play records yet")
        return
    # Grouped by cover as well: with between-cover variance as large as it is
    # (Section 5.2), pooling three self-play covers against one cross-play
    # cover would not be like-for-like.
    for (module, proto, bond, cover), g in arm.groupby(
            ["module", "protocol", "bond", "cover_paper"]):
        print("\nModule %s, %s, b = %g, cover %s" % (module, proto, bond, cover))
        rows = []
        for (a, b_), cell in g.groupby(["agent_A", "agent_B"]):
            lo, hi = wilson(int(cell.conflict_any.sum()), len(cell))
            rows.append(dict(proposer=a, responder=b_, n=len(cell),
                             complete="yes" if len(cell) >= EXPECTED_N else "PARTIAL",
                             conflict=cell.conflict_any.mean(),
                             ci="[%.2f, %.2f]" % (lo, hi),
                             breakdown=cell.breakdown.mean(),
                             defect=cell.defect.mean(),
                             mean_offer=cell.offer_x.mean()))
        # the matching self-play cells from the confirmatory matrix
        for agent in sorted(set(g.agent_A) | set(g.agent_B)):
            self_cell = d[(d.arm == "baseline") & (d.judge_config == "dualjudge")
                          & (d.agent == agent) & (d.cover_paper == cover)
                          & (d.module == module) & (d.protocol == proto)
                          & (d.bond == bond)]
            if self_cell.empty:
                continue
            lo, hi = wilson(int(self_cell.conflict_any.sum()), len(self_cell))
            rows.append(dict(proposer=agent, responder=agent + " (self-play)",
                             n=len(self_cell), complete="yes",
                             conflict=self_cell.conflict_any.mean(),
                             ci="[%.2f, %.2f]" % (lo, hi),
                             breakdown=self_cell.breakdown.mean(),
                             defect=self_cell.defect.mean(),
                             mean_offer=self_cell.offer_x.mean()))
        print(pd.DataFrame(rows).round(3).to_string(index=False))

    role_attribution(d)


def role_attribution(d):
    """Which role carries the capability effect?

    With both off-diagonal cells run, conflict can be regressed on the
    proposer's identity and on the responder's identity separately.  Self-play
    is incapable of separating these, which is the substance of R3 Major 6.
    """
    print("\n" + "-" * 78)
    print("Role attribution: proposer identity vs responder identity")
    print("-" * 78)
    xp = d[d.arm == "crossplay"]
    sp = d[(d.arm == "baseline") & (d.judge_config == "dualjudge")]
    cells = []
    for (mod, proto, bond, cov), g in xp.groupby(
            ["module", "protocol", "bond", "cover_paper"]):
        for (A, B), c in g.groupby(["agent_A", "agent_B"]):
            cells.append(dict(mod=mod, proto=proto, bond=bond, cov=cov, A=A, B=B,
                              k=int(c.conflict_any.sum()), n=len(c)))
        for ag in sorted(set(g.agent_A) | set(g.agent_B)):
            s = sp[(sp.agent == ag) & (sp.cover_paper == cov)
                   & (sp.module == mod) & (sp.protocol == proto)
                   & (sp.bond == bond)]
            if len(s):
                cells.append(dict(mod=mod, proto=proto, bond=bond, cov=cov,
                                  A=ag, B=ag, k=int(s.conflict_any.sum()),
                                  n=len(s)))
    t = pd.DataFrame(cells)
    if t.empty:
        return
    for (mod, proto, bond), g in t.groupby(["mod", "proto", "bond"]):
        if g.A.nunique() < 2 or g.B.nunique() < 2:
            continue
        print("\nModule %s, %s, b = %g" % (mod, proto, bond))
        print((g.pivot_table(index="A", columns="B", values="k") / 30)
              .round(3).to_string())
        for role, col in (("responder", "B"), ("proposer", "A")):
            lv = sorted(g[col].unique())
            if len(lv) != 2:
                continue
            a, b = g[g[col] == lv[0]], g[g[col] == lv[1]]
            p = stats.fisher_exact([[int(a.k.sum()), int(a.n.sum() - a.k.sum())],
                                    [int(b.k.sum()),
                                     int(b.n.sum() - b.k.sum())]])[1]
            print("   by %-9s %s = %.3f vs %s = %.3f   Fisher p = %.3g"
                  % (role, lv[0], a.k.sum() / a.n.sum(),
                     lv[1], b.k.sum() / b.n.sum(), p))

    print("\nReading: 'weak agents are lowballed' is a claim about a pairing,")
    print("and self-play cannot test it. The off-diagonal cells can.")


# ------------------------------------------------------------------- N4
def sonnet_covers(d):
    print("\n" + "=" * 78)
    print("N4  CLAUDE SONNET 5 ACROSS MODULE II COVERS  (R8 #5)")
    print("=" * 78)
    s = d[(d.agent == "Claude Sonnet 5") & (d.module == "II")
          & (d.protocol == "P2")]
    if s.empty:
        print("no Module II records for Claude Sonnet 5")
        return
    t = s.groupby(["cover_paper", "bond"]).agg(
        n=("conflict_any", "size"), conflict=("conflict_any", "mean"),
        breakdown=("breakdown", "mean"), defect=("defect", "mean"),
        ED=("ED", "mean")).round(3)
    print(t.to_string())
    covers = sorted(s.cover_paper.unique())
    print("\ncovers present: %s" % ", ".join(covers))
    if len(covers) < 2:
        print("still single-cover; the R8 #5 caveat stands until N4 completes")
        return
    tr = s[s.bond == 0.20]
    if tr.cover_paper.nunique() >= 2:
        tab = tr.groupby("cover_paper")[["agree", "breakdown", "defect"]].sum()
        keep = tab.loc[:, tab.sum(axis=0) > 0]
        if keep.shape[1] >= 2 and keep.shape[0] >= 2:
            chi2, p, dof, _ = stats.chi2_contingency(keep.values)
            print("homogeneity across covers at b = 0.20: "
                  "chi2(%d) = %.2f, p = %.3g" % (dof, chi2, p))
        else:
            print("outcome identical across covers at b = 0.20 - "
                  "framing-invariant, no test needed")


def main():
    d = pd.read_csv(CSV)
    honesty(d)
    crossplay(d)
    sonnet_covers(d)


if __name__ == "__main__":
    main()
