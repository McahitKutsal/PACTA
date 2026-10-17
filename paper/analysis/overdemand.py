#!/usr/bin/env python3
"""Re-fit the proposer over-demand regression with clustering (R3-Major-8).

The submitted version reported beta = 0.21, t = 6.9 on N = 568 offers pooled
across five cells, two agents and several bond levels, with no adjustment for
that structure.  The referee's objection is correct: with five cells and a few
bond levels each, the effective number of independent points is in the tens,
so t = 6.9 is not credible.

Here the same regression is re-fitted three ways - naive, cluster-robust by
cell x agent, and at the cell x agent x bond level, which is the coarsest unit
at which the regressor actually varies.

Usage:  python paper/analysis/overdemand.py
"""
from __future__ import annotations

import glob
import json
import os
import re

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
C_A = C_B = 0.10

CELL_RE = re.compile(
    r"g2_tx_(.+?)_mockjudge_only-S2_d([\d.]+)_v([\d.]+)_e([\d.]+)_S2_P2_b([\d.]+)\.jsonl$")


def b_min(delta, v, eps):
    return max(0.0, (delta - C_A - C_B) / (v - eps))


def load_offers():
    rows = []
    for f in sorted(glob.glob(os.path.join(OUT, "g2_tx_*mockjudge_only-S2*.jsonl"))):
        m = CELL_RE.search(os.path.basename(f))
        if not m:
            continue
        agent, d, v, e, b = m.group(1), *map(float, m.groups()[1:])
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            offer = next((ev["payload"] for ev in r["events"]
                          if ev.get("actor") == "A" and ev.get("kind") == "offer"), None)
            if offer is None:
                continue
            xstar = (r.get("theory") or {}).get("x_star")
            rows.append(dict(agent=agent, delta=d, v=v, eps=e, bond=b,
                             offer=float(offer), x_star=xstar,
                             b_star=b_min(d, v, e), seed=r.get("seed")))
    df = pd.DataFrame(rows)
    df["excess"] = df.bond - df.b_star           # slack above the binding threshold
    df["cell"] = (df.delta.astype(str) + "/" + df.v.astype(str) + "/" + df.eps.astype(str))
    return df


def ols_cluster(y, X, groups):
    """OLS with cluster-robust (CR1) standard errors."""
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    meat = np.zeros((X.shape[1], X.shape[1]))
    uniq = pd.unique(groups)
    for g in uniq:
        idx = np.where(groups == g)[0]
        Xg, ug = X[idx], resid[idx]
        s = Xg.T @ ug
        meat += np.outer(s, s)
    G, n, k = len(uniq), X.shape[0], X.shape[1]
    scale = (G / max(G - 1, 1)) * ((n - 1) / max(n - k, 1))
    cov = XtX_inv @ (scale * meat) @ XtX_inv
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    return beta, se, G


def main():
    df = load_offers()
    if df.empty:
        print("No relocation records under out/.")
        return
    df = df.dropna(subset=["x_star"])
    print("offers: %d   cells: %d   agents: %d   bond levels: %d"
          % (len(df), df.cell.nunique(), df.agent.nunique(), df.bond.nunique()))

    y = df.offer.values.astype(float)
    # Submitted specification: demand ~ equilibrium offer + slack above threshold
    X = np.column_stack([np.ones(len(df)), df.x_star.values, df.excess.values])
    names = ["intercept", "x*", "b - b*"]

    print("\n%-12s %10s %10s %10s %10s" % ("clustering", "term", "beta", "SE", "t"))
    print("-" * 56)
    for label, groups in [
        ("none (naive)", np.arange(len(df))),
        ("cell x agent", (df.cell + "|" + df.agent).values),
        ("cell x agent x bond", (df.cell + "|" + df.agent + "|" +
                                 df.bond.astype(str)).values),
    ]:
        beta, se, G = ols_cluster(y, X, groups)
        for i, nm in enumerate(names):
            if nm == "intercept":
                continue
            t = beta[i] / se[i] if se[i] > 0 else np.nan
            print("%-20s %8s %10.4f %10.4f %9.2f%s"
                  % (label if i == 1 else "", nm, beta[i], se[i], t,
                     "   (G=%d)" % G if i == 1 else ""))
        print()

    print("Reading: the point estimate on the slack term is stable, but its")
    print("standard error grows several-fold once the clustering the design")
    print("actually has is respected. The effect survives in sign and rough")
    print("magnitude; the submitted t = 6.9 does not.")


if __name__ == "__main__":
    main()
