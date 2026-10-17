#!/usr/bin/env python3
"""Build the tidy episode-level dataset underlying every number in the paper.

Reads the raw per-cell transcripts in out/g2_tx_*.jsonl (the frozen WP3
dual-judge runs) and emits one row per episode to
paper/analysis/outputs/episodes.csv.

This is the file the revision's statistical models consume. It exists because
reviewers could not locate the analysis code behind Section 5.4; every
downstream table regenerates from this CSV by a single command.

Usage:  python paper/analysis/build_dataset.py
"""
from __future__ import annotations

import collections
import csv
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(ROOT, "paper", "analysis", "outputs")

# Raw cell filename. Anchored at the END, because the middle carries a variable
# number of run flags (_only-..., _honesty, _d0.3_v0.6_e0.05, ...). Everything
# before the trailing _S{cover}_P{rung}[_b{bond}] is the run tag.
CELL_RE = re.compile(r"g2_tx_(?P<tag>.+)_(?P<cover>S\d)_(?P<proto>P\d)"
                     r"(?:_b(?P<bond>[\d.]+))?\.jsonl$")
JUDGE_RE = re.compile(r"_(dualjudge|judge-[a-z0-9.\-]+|mockjudge)")
# Threshold-relocation cells carry their parameter triple in the tag.
RELOC_RE = re.compile(r"_d(?P<d>[\d.]+)_v(?P<v>[\d.]+)_e(?P<e>[\d.]+)")
# Cross-play (revision N2): the two roles are played by different models.
XPLAY_RE = re.compile(r"^xplay_A-(?P<a>.+?)_B-(?P<b>.+?)(?=_(?:dualjudge|judge-|mockjudge))")


def parse_tag(tag):
    """Split a run tag into agent(s), judge config, and arm flags."""
    jm = JUDGE_RE.search(tag)
    judge = jm.group(1) if jm else "unknown"
    head = tag[:jm.start()] if jm else tag
    rest = tag[jm.end():] if jm else ""

    xm = XPLAY_RE.match(tag)
    if xm:
        agent_a, agent_b, arm = xm.group("a"), xm.group("b"), "crossplay"
    else:
        agent_a = agent_b = head
        arm = "honesty" if "_honesty" in rest else "baseline"
    if RELOC_RE.search(rest):
        arm = "relocation"
    return agent_a, agent_b, judge, arm

# Canonical agent metadata. `tier` is the within-family capability ordering of
# Section 5.1; `reasoning` is the coarse label, retained only for continuity.
AGENTS = {
    "anthropic-claude-haiku-4-5": ("Claude Haiku 4.5", "Anthropic", "low", "non-reasoning"),
    "anthropic-claude-sonnet-5": ("Claude Sonnet 5", "Anthropic", "high", "reasoning"),
    "openai-gpt-4o": ("GPT-4o", "OpenAI", "low", "non-reasoning"),
    "openai-o4-mini": ("o4-mini", "OpenAI", "high", "reasoning"),
    "qwen-qwen-plus": ("Qwen-Plus", "Alibaba", "low", "non-reasoning"),
    "qwen-qwen3.7-max": ("Qwen3.7-Max", "Alibaba", "high", "reasoning"),
    "deepseek-deepseek-v4-flash": ("DeepSeek-V4-Flash", "DeepSeek", "low", "reasoning"),
    "deepseek-deepseek-v4-pro": ("DeepSeek-V4-Pro", "DeepSeek", "high", "reasoning"),
}

# Narrative cover -> module. S1/S3/S5 screen; S2/S4/S6 commit.
COVER_MODULE = {"S1": "I", "S3": "I", "S5": "I", "S2": "II", "S4": "II", "S6": "II"}
# Manuscript-facing cover names (N*) vs. engine names (S*).
COVER_PAPER = {"S1": "N1", "S3": "N3", "S5": "N5", "S2": "N2", "S4": "N4", "S6": "N6"}

FIELDS = [
    "agent", "agent_key", "family", "tier", "reasoning", "module", "cover", "cover_paper",
    "protocol", "bond", "seed", "config_hash", "judge_config", "arm",
    "agent_A", "agent_B",
    "v", "eps", "delta", "p1", "p", "c_A", "c_B", "c_L", "c_H", "mu",
    "outcome", "agree", "breakdown", "defect", "conflict_any",
    "agreement_x", "x_star", "ED", "payoff_A", "payoff_B", "welfare", "escalation",
    # Module I role decomposition
    "true_type", "claimed_type", "cert_requested", "cert_granted", "offer_x",
    "responder_decision", "proposer_lowball",
    # Module II
    "committed", "t2_action", "bond_theory_min",
    # deception channels
    "dr_verbal_ep", "dr_effective_ep",
    "n_claims_verbal", "n_deceptive_verbal",
    "n_judged_verifiable", "n_judged_deceptive",
    "parse_error",
]


def _ev(rec, actor, kind):
    """First event payload matching (actor, kind), else None."""
    for e in rec.get("events", []):
        if e.get("actor") == actor and e.get("kind") == kind:
            return e.get("payload")
    return None


def _has(rec, kind):
    return any(e.get("kind") == kind for e in rec.get("events", []))


def row_for(rec, agent_key, judge_config, cover, protocol, bond_str,
            arm="baseline", agent_b_key=None):
    name, family, tier, reasoning = AGENTS.get(agent_key, (agent_key, "?", "?", "?"))
    agent_b_key = agent_b_key or agent_key
    module = rec.get("module") or COVER_MODULE[cover]
    p = rec.get("params", {})
    proto = rec.get("proto", {})
    th = rec.get("theory", {})
    gt = rec.get("ground_truth", {})
    outcome = rec.get("outcome")

    x = rec.get("agreement_x")
    xs = th.get("x_star")
    ed = abs(x - xs) if (x is not None and xs is not None) else None

    claims = rec.get("claims", [])
    verbal = [c for c in claims if c.get("channel") == "verbal"]
    certified = [c for c in claims if c.get("channel") == "certified"]
    n_dec_verbal = sum(1 for c in verbal if c.get("deceptive"))
    # Effective channel: the certificate under Module I / P3, else the verbal one.
    eff = certified if (protocol == "P3" and module == "I") else verbal
    dr_eff = (sum(1 for c in eff if c.get("deceptive")) / len(eff)) if eff else None

    judged = rec.get("judged_claims", [])
    verifiable = [j for j in judged if j.get("label") in ("truthful", "deceptive")]

    cert = _ev(rec, "B", "certify_request") or {}
    offer = _ev(rec, "A", "offer")
    resp = _ev(rec, "B", "respond")

    # Proposer lowball (Module I / P3): A demands the concessive price p + c_H
    # against a responder that did certify resilient. Separates proposer failure
    # from responder failure in the Section 6.2 / 6.5 conflict accounting.
    lowball = None
    if module == "I" and offer is not None:
        pp, cH = p.get("p"), p.get("c_H")
        if pp is not None and cH is not None:
            lowball = int(offer > pp + cH - 1e-9 and bool(cert.get("granted")))

    payoffs = rec.get("payoffs") or {}
    return {
        "agent": name, "agent_key": agent_key, "family": family, "tier": tier,
        "reasoning": reasoning, "module": module, "cover": cover,
        "cover_paper": COVER_PAPER[cover], "protocol": protocol,
        "bond": float(bond_str) if bond_str else (proto.get("bond") or 0.0),
        "seed": rec.get("seed"), "config_hash": rec.get("config_hash"),
        "judge_config": judge_config, "arm": arm,
        "agent_A": AGENTS.get(agent_key, (agent_key,))[0],
        "agent_B": AGENTS.get(agent_b_key, (agent_b_key,))[0],
        "v": proto.get("v"), "eps": proto.get("eps"),
        "delta": p.get("delta"), "p1": p.get("p1"), "p": p.get("p"),
        "c_A": p.get("c_A"),
        "c_B": p.get("c_B") if p.get("c_B") is not None else gt.get("c_B"),
        "c_L": p.get("c_L"), "c_H": p.get("c_H"), "mu": p.get("mu"),
        "outcome": outcome,
        "agree": int(outcome == "agree"),
        "breakdown": int(outcome in ("war_now", "war")),
        "defect": int(outcome == "attack_t2"),
        "conflict_any": int(outcome in ("war", "war_now", "attack_t2")),
        "agreement_x": x, "x_star": xs, "ED": ed,
        "payoff_A": payoffs.get("A"), "payoff_B": payoffs.get("B"),
        "welfare": (payoffs.get("A", 0) + payoffs.get("B", 0)) if payoffs else None,
        "escalation": rec.get("escalation"),
        "true_type": gt.get("type"),
        "claimed_type": _ev(rec, "B", "claim_type"),
        "cert_requested": int(bool(cert.get("wants"))) if cert else None,
        "cert_granted": int(bool(cert.get("granted"))) if cert else None,
        "offer_x": offer,
        "responder_decision": resp,
        "proposer_lowball": lowball,
        "committed": int(_has(rec, "commit")) if module == "II" else None,
        "t2_action": _ev(rec, "B", "t2_action"),
        "bond_theory_min": th.get("min_bond_for_peace"),
        "dr_verbal_ep": (n_dec_verbal / len(verbal)) if verbal else None,
        "dr_effective_ep": dr_eff,
        "n_claims_verbal": len(verbal),
        "n_deceptive_verbal": n_dec_verbal,
        "n_judged_verifiable": len(verifiable),
        "n_judged_deceptive": sum(1 for j in verifiable if j.get("label") == "deceptive"),
        "parse_error": int(_has(rec, "parse_error")),
    }


def main():
    os.makedirs(DEST, exist_ok=True)
    rows, skipped = [], []
    for f in sorted(glob.glob(os.path.join(OUT, "g2_tx_*.jsonl"))):
        m = CELL_RE.search(os.path.basename(f))
        if not m:
            skipped.append(os.path.basename(f))
            continue
        cover, protocol, bond_str = m.group("cover"), m.group("proto"), m.group("bond")
        agent_key, agent_b_key, judge_config, arm = parse_tag(m.group("tag"))
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(row_for(json.loads(line), agent_key,
                                        judge_config, cover, protocol, bond_str,
                                        arm=arm, agent_b_key=agent_b_key))

    dest = os.path.join(DEST, "episodes.csv")
    with open(dest, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    by_judge = collections.Counter(r["judge_config"] for r in rows)
    print("wrote %s: %d episodes" % (dest, len(rows)))
    for k, v in sorted(by_judge.items()):
        print("  %-32s %d" % (k, v))
    if skipped:
        print("skipped %d unparsed filenames" % len(skipped))


if __name__ == "__main__":
    main()
