# PACTA Human-vs-AI Study — Pre-Registration (v0.1 DRAFT, NOT FROZEN)

**Status:** DRAFT for review. Freeze (v1.0) only after (a) design review, (b) IRB approval, and (c) an
internal apparatus pilot; then timestamp on OSF before any confirmatory data collection. Contributor:
[Researcher]. Companion to the frozen WP3 pre-registration (`PACTA_WP3_preregistration.md`) and the
design document (`PACTA_human_study_design_v0.1.md`). Apparatus:
`interface/pacta_bargaining_prototype.html`.

---

## 1. Background and research question

WP3 established, across four model families and eight LLM agents, that an LLM's incentive-compatibility
response to a designed commitment protocol **scales with reasoning capability** (a capability gradient),
with a **decoupling**: verified disclosure neutralizes deception on every model (structural), but only
capable models convert a bond above the predicted minimum into peace (behavioral). This study asks the
question the LLM matrix cannot:

> **Where do humans sit on that capability gradient, and does the bond mechanism produce the same
> dose-response cliff on humans as on frontier LLMs?**

It plays the **same Module II game** the LLM agents faced (identical parameters), with a human in the
responder role, so human behavior is measured on the **same judge-independent metrics** and placed on
the same axis as the eight LLM agents. Scope for v1 is **Module II (commitment / bonded commitment)**;
Module I (private information / verified disclosure) is deferred to v2.

## 2. Hypotheses

Confirmatory hypotheses are directional and pre-registered. HH-exp are exploratory (no confirmatory
claims). **Primary family: {HH2, HH3}.**

| ID | Statement | LLM analogue |
|---|---|---|
| **HH1** | Under **no deposit**, human play breaks down: low peace rate and high accept-then-attack rate. | H1 baseline |
| **HH2** *(primary)* | A **dose-response cliff**: peace and bond-honoring rise sharply as the deposit crosses $b^\*_{\min}$; the empirical break falls within the pre-registered **±25% band** of $b^\*_{\min}\approx0.118$. | H3 cliff |
| **HH3** *(primary)* | On the **capability gradient** (accept-then-attack rate and trough war rate), the human median falls **nearer the frontier reasoners than the non-reasoning bottom** (directional). | H7 gradient |
| **HH4** | Beyond $b^{\dagger}\approx0.33$, a **non-monotone return** of breakdown: the human rejection (war-now) rate at the over-demand deposit exceeds the trough. | H6 over-demand |
| **HH-exp** | Exploratory: human-specific deviations — honoring when attacking pays more (reciprocity/morality); effect of the optional one-line message; order/learning effects across rounds. | — |

## 3. Design

- **Module:** II (commitment / power-shift). Complete-information Powell setup; the responder is the
  *rising* power (its position strengthens over time), creating the temptation to accept then defect.
- **Human role:** **B (responder).** B makes the two decisions on which the gradient is defined:
  (t1) **accept or reject** A's offer; (t2, under a bond) **honor** the deal or **attack** (take more,
  forfeit the bond). This is exactly the axis the LLM agents were scored on (accept-then-attack).
- **Opponent (A):** a **fixed, deterministic scripted policy** calibrated to frontier-equilibrium
  proposer behavior (Appendix A), held constant across participants. A fixed opponent removes
  opponent-side variance as a confound, which is preferable for the "where do humans sit" question; a
  live-LLM opponent is a possible v2 robustness arm.
- **Parameters (identical to the WP3 Module II engine, frozen):** payoff pie normalized to 1 (shown to
  participants as **100 points**); $p_1=0.5$, power shift $\Delta=0.30$, war costs $c_A=c_B=0.10$;
  equilibrium split $x^\*\approx0.43$; minimum bond for peace $b^\*_{\min}\approx0.118$; participation
  ceiling $x_P=0.58$; IC→participation crossover $b^{\dagger}\approx0.33$.
- **Conditions (deposit level, within-subject):** six levels drawn from the frozen WP3 bond sweep —
  **{0 (no deposit), 0.05, 0.10, 0.15, 0.20, 0.40}** — spanning below $b^\*_{\min}$, across it, and the
  over-demand region. **k = 2 rounds per condition** (12 scored rounds), **order randomized** per
  participant, preceded by 1 unscored practice round.

## 4. Procedure and incentive-compatibility

Flow: **consent → comprehension gate → practice → 12 randomized rounds → debrief.** Per round: A's
message and offer are shown; B accepts or rejects; if B accepts under a bond, B honors or attacks; the
outcome and points are shown. **Payoffs must be real:** total points map to a **performance bonus**
(base pay + bonus proportional to points), so participants are motivated to maximize their own share —
the incentive the theory assumes. War pays less than a kept peace; the bond is **forfeited on attack**;
over-demanding offers can be rejected. The apparatus presents all payoffs transparently and logs every
decision locally. **Framing is neutral:** instructions and between-round feedback are factual and
symmetric and never label an option as better; the opponent's messages are persuasive as **diegetic
stimulus** (disclosed to participants as part of the game's rules).

## 5. Variables

- **Independent variable:** deposit level (6 within-subject conditions).
- **Primary DVs (all judge-independent, from the interface log):**
  - **peace rate** (share of rounds ending in a kept deal),
  - **accept-then-attack rate** (attacked / accepted), the gradient-placement statistic,
  - **bond-honoring rate** (1 − PBR among accepted bonded deals),
  - **war rate** (share ending in war, whether war-now or attack),
  - **agreed split $x$** vs the closed-form $x^\*$ (equilibrium deviation).
- **Secondary/process:** war-now (rejection) rate, decision times, optional-message content,
  round order.
- **Exclusions (pre-registered):** participants who fail the comprehension gate after 3 attempts;
  incomplete sessions; attention-check failures; completion-time outliers (< 1/3 or > 3× the median).
  All exclusions reported with counts.

## 6. Sampling plan

- **Target N = 120** completers who pass the comprehension gate. **Fixed-N stopping rule** (no optional
  stopping / no peeking).
- **Power:** the within-subject cliff (HH2) is a large effect (peace rises from near 0 below $b^\*_{\min}$
  toward near 1 above it in capable play); N = 120 gives power > 0.95 for a mixed-model deposit effect.
  For gradient placement (HH3), N = 120 yields a proportion CI half-width of ≈ ±0.09 on the human
  accept-then-attack rate, comparable to the WP3 $n=30$ per-cell precision.
- **Recruitment:** an online panel (e.g. Prolific), adults, fluent in the session language (TR or EN),
  balanced where feasible. Compensation: fixed base + performance bonus.

## 7. Analysis plan

- **HH1 (baseline):** descriptive; test that under no-deposit the peace rate is low and the
  accept-then-attack rate high (one-sample tests against a neutral reference; report rates with CIs).
- **HH2 (cliff, primary):** mixed-effects logistic regression of *kept-peace* (and, separately,
  *bond-honored*) on deposit level, with a random intercept (and slope) per participant. Estimate the
  dose-response curve; locate the break with a pre-specified change-point / segmented fit and test that
  it falls within the **±25% band** of $b^\*_{\min}$. No point-localization claim (grid-limited).
- **HH3 (placement, primary):** compute each participant's accept-then-attack rate and trough
  (deposit = 0.20) war rate; summarize the human distribution (median + bootstrap CI) and **place it
  against the eight fixed LLM-agent values** from WP3. Confirmatory directional test: human median is
  closer to the frontier cluster than to the non-reasoning bottom.
- **HH4 (over-demand):** test that the rejection (war-now) rate at deposit = 0.40 exceeds the trough
  (deposit = 0.20) within participant (paired test).
- **HH-exp:** exploratory only — rate of honoring when attacking pays more; message-content coding;
  round-order / learning models. Reported as exploratory.
- **Multiplicity:** primary family {HH2, HH3}; control family-wise error (Holm). Secondary and
  exploratory analyses flagged as such.

## 8. Ethics

Binding (also committed in the paper's §8): **IRB approval before any data; informed consent; a design
that does not deceive the participant.** The opponent's in-game bluffing is a disclosed game mechanic
(like poker), not deception about the study. Participants are told the opponent is an AI. **Debrief**
after play states the purpose, the deception ground-truth, data use, and a contact. Data are anonymous
(no names), stored and released in aggregate; raw session logs under gated access. No model is
fine-tuned to deceive; scenarios are synthetic. Participation is voluntary with withdrawal at any time.
Compensation is fair (base + bonus).

## 9. Pilot, deviations, freeze

An internal apparatus pilot (self + a few testers, **no external data enters analysis**) validates UX,
comprehension, and clean logging before freeze. This document is a **DRAFT**; on freeze (v1.0) the
hypotheses, design, conditions, N, and analysis plan are locked and OSF-timestamped. Any post-freeze
change is logged as a dated deviation with rationale (as in the WP3 decision-log discipline).

## Appendix A — Fixed opponent (A) policy

Deterministic given the condition (and a fixed seed for any tie-breaking). A is the *declining* power
(proposer); it proposes a split and always honors (A is not the party tempted to defect — B is). A's
offered share to B, $x_A(b)$, follows the frozen frontier-equilibrium schedule: near $x^\*\approx0.43$
at low bond, rising modestly toward the participation region as the bond grows, and **over-demanding**
(offering B below its reservation, approaching $x_P$-binding) in the high-bond condition ($b=0.40$),
reproducing the H6 over-demand regime the LLM proposers exhibited. The exact per-condition schedule is
frozen in the apparatus config and reported in full with the results.

## Appendix B — Comprehension items (must pass to proceed)

Neutral checks of rules/payoffs (not strategy):
1. You make a deal, then break it — what happens to your deposit? *(correct: you lose it)*
2. You make a deal and keep it — what happens to your deposit? *(correct: you get it back)*
3. You refuse the offer and fight — about how many points do you get? *(correct: about 40)*
