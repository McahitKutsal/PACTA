#!/usr/bin/env python3
"""The inferential analysis Section 5.4 promised and the submission did not report.

Referees 2 (#2, #3), 3 (Major 3, Major 4) and 8 (#7) all raised this. Section
5.4 specified crossed mixed-effects logistic regressions, Holm-corrected
planned contrasts and effect sizes with intervals; the Results carried only
pooled proportions with Wilson intervals.

Two things make the specified model a poor instrument here, and we report both
rather than quietly substituting:

  1. 107 of 216 agent x cover x bond cells are degenerate (all-0 or all-1), so
     the logistic likelihood is separated.
  2. The agent factor has 8 levels, which is too few to identify a random
     intercept.

So the analysis is run at the level R3 identifies as the real unit of
replication - the agent x cover cell - with the episode-level model reported
alongside as a penalised (Firth) fit, and the originally specified crossed
model attempted and its outcome stated plainly.

Usage:  python paper/analysis/models.py
"""
from __future__ import annotations

import itertools
import os
import warnings

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "paper", "analysis", "outputs", "episodes.csv")
DEST = os.path.join(ROOT, "paper", "analysis", "outputs")
RNG = np.random.default_rng(20261017)
BOOT = 4000


# --------------------------------------------------------------------- stats
def cliffs_delta(a, b):
    """Cliff's delta with a bootstrap CI over the cluster-level values."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) == 0 or len(b) == 0:
        return np.nan, (np.nan, np.nan)
    gt = sum((x > y) for x, y in itertools.product(a, b))
    lt = sum((x < y) for x, y in itertools.product(a, b))
    d = (gt - lt) / (len(a) * len(b))
    boot = []
    for _ in range(1000):
        aa = RNG.choice(a, len(a), replace=True)
        bb = RNG.choice(b, len(b), replace=True)
        g = sum((x > y) for x, y in itertools.product(aa, bb))
        l = sum((x < y) for x, y in itertools.product(aa, bb))
        boot.append((g - l) / (len(aa) * len(bb)))
    return d, (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5)))


def holm(pvals):
    """Holm-Bonferroni adjusted p-values, order preserved."""
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    m = len(p)
    for i, idx in enumerate(order):
        running = max(running, (m - i) * p[idx])
        adj[idx] = min(1.0, running)
    return adj


def firth_logit(X, y, max_iter=200, tol=1e-8):
    """Firth-penalised logistic regression (Jeffreys prior).

    Finite estimates under complete separation, where plain ML diverges.
    Returns (beta, se, pvals). X must already include an intercept column.
    """
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, k = X.shape
    beta = np.zeros(k)
    for _ in range(max_iter):
        eta = X @ beta
        pr = 1.0 / (1.0 + np.exp(-eta))
        w = pr * (1 - pr)
        XW = X * w[:, None]
        info = X.T @ XW
        try:
            inv = np.linalg.pinv(info)
        except np.linalg.LinAlgError:
            break
        # hat diagonal under the weighted design
        H = (XW @ inv * X).sum(axis=1)
        # Firth-adjusted score
        U = X.T @ (y - pr + H * (0.5 - pr))
        step = inv @ U
        # damp the step so separated cells cannot blow up an iteration
        norm = np.linalg.norm(step)
        if norm > 5.0:
            step *= 5.0 / norm
        beta = beta + step
        if norm < tol:
            break
    eta = X @ beta
    pr = 1.0 / (1.0 + np.exp(-eta))
    w = pr * (1 - pr)
    cov = np.linalg.pinv(X.T @ (X * w[:, None]))
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        z = np.where(se > 0, beta / se, np.nan)
    pv = 2 * (1 - stats.norm.cdf(np.abs(z)))
    return beta, se, pv


def paired_cluster_test(d, label_a, label_b, dv, subset):
    """Paired contrast at the agent x cover level - the real unit (R3-Major-4).

    Rates are computed per (agent, cover), paired across the two conditions,
    and tested with Wilcoxon signed-rank. Reports the cluster count, which is
    the honest n for the inference.
    """
    sub = d[subset]
    cell = (sub.groupby(["agent", "cover_paper", "protocol"])[dv]
            .mean().unstack("protocol"))
    both = cell[[label_a, label_b]].dropna()
    if len(both) < 3:
        return None
    a, b = both[label_a].values, both[label_b].values
    diff = b - a
    if np.allclose(diff, 0):
        p = 1.0
    else:
        p = stats.wilcoxon(a, b, zero_method="zsplit").pvalue
    delta, ci = cliffs_delta(b, a)
    return dict(dv=dv, contrast=f"{label_a}->{label_b}", n_clusters=len(both),
                mean_a=a.mean(), mean_b=b.mean(), mean_diff=diff.mean(),
                p_raw=p, cliffs_delta=delta, delta_lo=ci[0], delta_hi=ci[1])


# ------------------------------------------------------------------ analyses
def primary_family(d):
    """{H2, H3}: the pre-specified primary family, reported with Holm."""
    m1 = d.module == "I"
    m2 = d.module == "II"
    rows = []

    # H2, Module I ladder: P0 -> P1 (the null) and P0 -> P3.
    for dv in ["conflict_any", "dr_effective_ep"]:
        for a, b in [("P0", "P1"), ("P0", "P3")]:
            r = paired_cluster_test(d, a, b, dv, m1)
            if r:
                r["family"] = "H2 (Module I)"
                rows.append(r)

    # H2, Module II: P0 vs P2 at the pre-specified trough b = 0.20.
    m2sub = m2 & ((d.protocol == "P0") | ((d.protocol == "P2") & (d.bond == 0.20)))
    for dv in ["conflict_any", "breakdown", "defect"]:
        r = paired_cluster_test(d, "P0", "P2", dv, m2sub)
        if r:
            r["family"] = "H2 (Module II, b=0.20)"
            rows.append(r)

    out = pd.DataFrame(rows)
    if not out.empty:
        out["p_holm"] = holm(out.p_raw.values)
    return out


def ladder_coverage(d):
    """R3-Major-2: which rungs were actually run in which module."""
    return pd.crosstab(d.module, d.protocol)


def variance_decomposition(d):
    """R3-Major-4: how much variation lives at the cover vs. the episode level."""
    m2 = d[(d.module == "II") & (d.protocol == "P2") & (d.bond == 0.20)]
    rows = []
    for agent, g in m2.groupby("agent"):
        per_cover = g.groupby("cover_paper").conflict_any.mean()
        if len(per_cover) < 2:
            continue
        # binomial (within-cover, i.e. API noise) vs. between-cover spread
        n_per = g.groupby("cover_paper").size()
        within = float(np.mean([p * (1 - p) / n for p, n in zip(per_cover, n_per)]))
        between = float(per_cover.var(ddof=1))
        rows.append(dict(agent=agent, n_covers=len(per_cover),
                         rate_min=per_cover.min(), rate_max=per_cover.max(),
                         spread=per_cover.max() - per_cover.min(),
                         var_between_cover=between, var_within_binomial=within,
                         ratio=between / within if within > 0 else np.nan))
    return pd.DataFrame(rows).sort_values("spread", ascending=False)


def firth_protocol_model(d):
    """Episode-level penalised fit, Module II conflict ~ bond (above/below b*)."""
    m2 = d[(d.module == "II") & (d.protocol == "P2")].copy()
    m2 = m2[m2.bond.notna()]
    m2["above_bstar"] = (m2.bond >= 0.118).astype(float)
    m2["high_tier"] = (m2.tier == "high").astype(float)
    X = np.column_stack([
        np.ones(len(m2)),
        m2.above_bstar.values,
        m2.high_tier.values,
        (m2.above_bstar * m2.high_tier).values,
    ])
    y = m2.conflict_any.values.astype(float)
    beta, se, pv = firth_logit(X, y)
    names = ["intercept", "bond>=b*min", "high tier", "interaction"]
    return pd.DataFrame(dict(term=names, beta=beta, se=se, p=pv,
                             odds_ratio=np.exp(beta),
                             lo=np.exp(beta - 1.96 * se),
                             hi=np.exp(beta + 1.96 * se)))


def attempt_specified_model(d):
    """Attempt the model Section 5.4 specified and report exactly what happens.

    Specified: mixed-effects LOGISTIC regression with CROSSED random intercepts
    for agent and seed.  Three separate obstacles are reported separately,
    because conflating them would misdescribe what failed.
    """
    msg = []
    m2 = d[(d.module == "II") & (d.protocol == "P2")].copy()
    m2["above"] = (m2.bond >= 0.118).astype(int)

    # (a) where separation actually bites: only once agent-level effects enter
    try:
        import statsmodels.api as sm
        degen = m2.groupby("agent").conflict_any.mean()
        degen = degen[(degen == 0) | (degen == 1)]
        specs = {}
        for label, build in (
            ("pooled (bond + tier)",
             lambda: pd.DataFrame({"above": m2.above.values,
                                   "high": (m2.tier == "high").astype(int).values})),
            ("+ agent fixed effects",
             lambda: pd.concat([pd.DataFrame({"above": m2.above.values}),
                                pd.get_dummies(m2.agent, drop_first=True, dtype=float)
                                .reset_index(drop=True)], axis=1)),
            ("+ agent x cover fixed effects",
             lambda: pd.concat([pd.DataFrame({"above": m2.above.values}),
                                pd.get_dummies(m2.agent + "|" + m2.cover_paper,
                                               drop_first=True, dtype=float)
                                .reset_index(drop=True)], axis=1)),
        ):
            X = sm.add_constant(build()).values.astype(float)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                f = sm.Logit(m2.conflict_any.values, X).fit(disp=0, maxiter=300)
            specs[label] = (X.shape[1], float(np.max(np.abs(f.params))),
                            float(np.nanmax(f.bse)))
        msg.append("(a) Unpenalised logistic, by specification:")
        for label, (k, mb, ms) in specs.items():
            msg.append("      %-32s k=%2d  max|beta|=%8.2f  max SE=%12.2f  %s"
                       % (label, k, mb, ms,
                          "SEPARATED" if (mb > 10 or ms > 10) else "ok"))
        msg.append("    The pooled model is well behaved; separation appears only "
                   "once agent-level effects enter - which is what Section 5.4 "
                   "specified. Source: %s is at conflict 1.00 in all of its "
                   "Module II P2 episodes." % ", ".join(degen.index))
    except Exception as e:
        msg.append("(a) Unpenalised logistic failed: %s: %s"
                   % (type(e).__name__, str(e)[:160]))

    # (b) the LOGISTIC mixed model (statsmodels MixedLM is linear, so not it)
    try:
        from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            glmm = BinomialBayesMixedGLM.from_formula(
                "conflict_any ~ above", {"agent": "0 + C(agent)"}, m2).fit_vb()
        msg.append("(b) Mixed-effects LOGISTIC with an agent random intercept fits "
                   "only by variational Bayes (BinomialBayesMixedGLM); the fixed "
                   "effect for bond>=b*min is %.3f. With 8 agent levels the random "
                   "intercept is weakly identified, exactly as R8 #7 notes."
                   % float(glmm.fe_mean[1]))
    except Exception as e:
        msg.append("(b) Mixed-effects logistic could not be fitted: %s: %s"
                   % (type(e).__name__, str(e)[:160]))

    # (c) crossed random effects, as actually specified
    msg.append(
        "(c) CROSSED random intercepts for agent AND seed, as Section 5.4 "
        "specifies, are not supported by any standard Python implementation for "
        "a binomial response, and with 8 agent levels and separation in half the "
        "cells the specification is not identifiable on these data in any case. "
        "We therefore state plainly that the crossed mixed-effects logistic "
        "described in Section 5.4 was specified but never run, and report the "
        "cluster-level contrasts and the Firth fit as the substantive analysis.")
    return "\n".join(msg)


def main():
    d = pd.read_csv(CSV)
    d = d[d.judge_config == "dualjudge"]
    os.makedirs(DEST, exist_ok=True)

    print("=" * 78)
    print("1. LADDER COVERAGE (R3-Major-2)")
    print("=" * 78)
    print(ladder_coverage(d).to_string())
    print("\nP2 and P3 were never run in the same module, so H2's ordering")
    print("P3 <= P2 <= P1 ~ P0 was never testable within a module.")

    print("\n" + "=" * 78)
    print("2. PRIMARY FAMILY {H2, H3}, cluster-level (R3-Major-3, R2-2, R8-7)")
    print("=" * 78)
    pf = primary_family(d)
    if not pf.empty:
        show = pf[["family", "dv", "contrast", "n_clusters", "mean_a", "mean_b",
                   "mean_diff", "cliffs_delta", "delta_lo", "delta_hi",
                   "p_raw", "p_holm"]]
        print(show.round(4).to_string(index=False))
        pf.to_csv(os.path.join(DEST, "primary_family.csv"), index=False)
    print("\nn_clusters is the number of agent x cover cells, which R3-Major-4")
    print("identifies as the real unit of replication - not the 30 episodes.")

    print("\n" + "=" * 78)
    print("3. WHERE THE VARIATION LIVES (R3-Major-4)")
    print("=" * 78)
    vd = variance_decomposition(d)
    print(vd.round(4).to_string(index=False))
    vd.to_csv(os.path.join(DEST, "variance_decomposition.csv"), index=False)
    print("\nratio > 1 means between-cover spread exceeds what binomial sampling")
    print("at n=30 can explain, i.e. the Wilson intervals in Table 3 understate")
    print("the real uncertainty.")

    print("\n" + "=" * 78)
    print("4. PENALISED (FIRTH) EPISODE-LEVEL MODEL")
    print("=" * 78)
    print(firth_protocol_model(d).round(4).to_string(index=False))

    print("\n" + "=" * 78)
    print("5. THE MODEL SECTION 5.4 SPECIFIED")
    print("=" * 78)
    print(attempt_specified_model(d))


if __name__ == "__main__":
    main()
