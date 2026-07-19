# PACTA — Human-vs-LLM Study & Interface: Design Document (v0.1)

*Design-first draft, per user decision (2026-07-19). No code yet. Purpose: pin the research question,
game design, screen flow, scoring, logged DVs, and consent/debrief so we can (1) build the apparatus,
(2) internally pilot it, (3) prepare IRB + pre-registration, (4) run the study. In-paper vs follow-up
scope is **deferred** (decide after the internal pilot). This doc reuses the frozen PACTA-Bench engine,
scenarios, protocols, and agent code; the interface is a frontend + logging layer over them.*

---

## 1. Research question & why it matters

WP3 established that **LLMs' incentive-compatibility response to the protocol ladder scales with reasoning
capability** (the gradient), with a **decoupling**: verified disclosure neutralizes deception on every
model (structural), but only capable models convert that into peace (behavioral). The human arm asks the
question the LLM matrix cannot:

> **Where do humans sit on that capability gradient, and does environment design produce the same
> response — bond cliff, channel separation, decoupling — on humans as on frontier LLMs?**

This bridges the paper's LLM findings back to the human-relevance claim §8 currently *disclaims*, and
tests whether "environment design makes honesty an equilibrium" holds for the ultimate target — human
strategic behavior. Sub-questions:

- **Placement.** Do humans honor bonds and avoid *accept-then-attack* like frontier reasoners, or defect
  like weak models — and does a distinct *human* pattern appear (reciprocity, trust, spite, morality
  beyond payoff)?
- **Cliff.** Do humans show the dose-response cliff at $b^\*_{\min}\approx0.118$?
- **Channel separation (P3).** Does verified disclosure neutralize *human* effective deception
  structurally (it should — the certificate is unforgeable regardless of who plays), and do humans
  *trust* the certificate enough to reach peace?
- **Over-demand (if humans also play the proposer).** At high bond, do humans over-demand past the
  participation ceiling $x_P=0.58$, like frontier models at the IC→participation transition?

## 2. Hypotheses (human analogues HH#, pre-registered before data)

| ID | Statement | Maps to |
|---|---|---|
| **HH1** | Under cheap talk (P0), human play shows substantial breakdown/exploitation (baseline war/defection). | H1 baseline |
| **HH2** | A bond above $b^\*_{\min}$ produces peace and bond-honoring; below it, breakdown — a dose-response cliff. | H3 cliff |
| **HH3** | Human *accept-then-attack* rate places humans on the LLM gradient (directional prediction: near the frontier, i.e. low). | H7 gradient |
| **HH4** | Under P3, human *effective* deception $\to0$ (structural) and peace rises (trust in the certificate). | H2/H8 channel sep. + decoupling |
| **HH5** *(if human plays proposer)* | At high bond humans over-demand past $x_P=0.58$ at a nonzero rate. | H6 over-demand |
| **HH-exp** | Exploratory: reciprocity / trust / punitive behaviors humans exhibit that LLMs do not (e.g. costly punishment of a bluffing opponent; bond-honoring beyond strict payoff). | — |

**Primary DVs are the same judge-independent ones as WP3** (§6): war rate, bond-honored vs attacked
(PBR analog), accept-then-attack rate, agreed $x$ vs equilibrium $x^\*$, war-now (rejection) rate,
human deception rate (Module I only). Process measures: decision times, comprehension-check score.

## 3. Game design

- **Module: II (commitment / bonded commitment)** — the most game-like rung and the crux of the
  capability gradient. Complete-information power-shift setup (Powell): B is the *rising* power, so the
  tension is whether to commit now vs exploit its future advantage. (Module I / private-information
  screening is a natural v2.)
- **Human role: B (responder).** B makes the two decisions where the gradient lives: (t1) accept or
  reject A's offer; (t2, under a bond) **honor** the deal or **attack** (grab more, forfeit the bond) —
  the accept-then-attack decision. This places the human on the same axis the LLM agents were scored on.
  *(Optional later condition: human as A (proposer) to test over-demand, HH5.)*
- **Opponent: a pinned frontier LLM as A (proposer),** via the existing agent code, held **fixed** so A
  plays near-equilibrium and the human's behavior is the variable. *(Optional later condition: a weak
  LLM opponent, to test whether humans exploit weak agents — mixed-motive question.)*
- **Parameters (from the frozen engine):** pie normalized to **100 points**; $p_1=0.5$, power shift
  $\Delta=0.30$, war costs $c_A=c_B=0.10$; equilibrium split $x^\*\approx0.43$; minimum bond for peace
  $b^\*_{\min}\approx0.118$; participation ceiling $x_P=0.58$. War destroys surplus (each side's war
  payoff $\approx40$ points, summing to $<100$).
- **Conditions (within-subject, randomized order, multiple rounds each):**
  1. **P0** — cheap talk, no bond (baseline).
  2. **P2, $b<b^\*_{\min}$** (e.g. $b=0.05$) — bond too small.
  3. **P2, $b\ge b^\*_{\min}$** (e.g. $b=0.15$–$0.20$) — bond sufficient (cliff test).
  4. **P2, high $b$** (e.g. $b=0.40$) — high-bond / over-demand regime.
  5. **P3** — verified disclosure (channel-separation test).

## 4. Incentive-compatibility (non-negotiable for validity)

The game must have **real stakes**, or it measures nothing strategic. Payoffs (points, 0–100) map to a
**performance bonus** (e.g. Prolific bonus ∝ total points). War pays less than peace (destruction); the
bond is **forfeited on attack**; over-demand risks rejection. Participants are told upfront that their
bonus depends on their score, so they are motivated to maximize their own share — exactly the incentive
the theory assumes. Fixed base pay + variable bonus.

## 5. Screen flow

1. **Landing → Consent** (IRB-approved; §6). Voluntary, data use, compensation, opponents are AI.
2. **Interactive tutorial** — teaches the rules in plain language (see §7): the pie, that war destroys
   value, the escrow bond, verified disclosure. **Comprehension check** (must pass to proceed) so we
   only analyze participants who understood the mechanics.
3. **Round loop** (repeated across conditions):
   1. *Setup screen:* "You are Borvane (B). The territory is worth 100 points. If war, you get ~40. This
      round: **bond = 15 points** — whoever breaks a made deal forfeits it."
   2. *Messaging:* the LLM (A) sends a proposal message; human B may reply (cheap talk).
   3. *Offer:* A offers B a share $x$. Human B: **accept / reject**.
   4. *If accepted under a bond →* t2 decision: human B chooses **honor** or **attack** (grab more,
      forfeit the bond) — the accept-then-attack choice.
   5. *Outcome + reveal:* peace/war, points earned, and the engagement hooks (§7): did the opponent
      bluff? what was the "rational" play? where did the bond sit vs the trust threshold (cliff meter)?
4. **Debrief** (§8) → optional demographics → payment.

## 6. Logged data (all judge-independent, mirrors WP3 §6)

Per round: condition (protocol, $b$), offer $x$, accept/reject, honor/attack, outcome
(agree / war-now / attack-t2), points, decision times, free-text messages (if enabled). Derived per
participant × condition: war rate, PBR (honor) rate, **accept-then-attack rate**, mean agreed $x$ vs
$x^\*$, war-now rate. Plus: comprehension-check score, session duration, device. **Human's placement on
the gradient** = accept-then-attack rate and trough war rate, plotted against the eight LLM agents.

## 7. Making it understandable *and* fun

**Translate the jargon (tutorial + tooltips):** "verified disclosure" → *"you can prove your true
strength with an inspection"*; "bond/escrow" → *"a deposit you lose if you break the deal"*; "power
shift" → *"you'll be stronger next round"*; "participation ceiling" → *"demand too much and they'll
walk"*. **Engagement hooks (all map to real findings):**

- **Betrayal reveal** — "They honored the deal." / "You were attacked!" (the accept-then-attack beat).
- **Cliff meter** — a gauge showing where the round's bond sat relative to the trust threshold
  $b^\*_{\min}$ ("your bond was just above the line — that's why the deal held").
- **Gradient placement** — end-of-session: *"You played like a frontier reasoner"* / *"…like a weak
  model"*, placing the participant on the same gradient as the LLMs (engaging **and** it is the science).
- Score/streak, short rounds (2–3 min), ~10–15 rounds (~25–30 min total).

## 8. Consent, debrief, ethics (IRB; §8 of the paper commits to this)

The paper's §8 already binds us: **IRB approval, informed consent, and a design that does not deceive
participants.** Concretely:

- **Consent up front:** the study concerns negotiation/commitment behavior; opponents are **AI** (no
  human-vs-AI deception); voluntary; data use/anonymization; compensation.
- **In-game bluffing is a disclosed game mechanic** (like poker) — the *opponent* may bluff, and the
  participant knows this is part of the rules. We never deceive the participant *about the study itself*.
- **Debrief after:** purpose, the deception ground-truth, how the data is used, contact.
- Anonymized storage; consent for aggregate release; exclude non-consenting/failed-comprehension data.
- No fine-tuning of any model to deceive; published scenarios synthetic (already true).

## 9. Sample & power (to firm up in the pre-reg)

Large within-subject effects (the cliff) need modest $N$; placing humans on the gradient with tight CIs
wants more. Rough target **$N\approx100$–$150$** (power 0.80 for the cliff and for a gradient-placement
CI comparable to the WP3 $n=30$ cells), several rounds per condition per participant. Recruitment via a
platform (e.g. Prolific); budget ≈ $N$ × session-time × rate + bonuses — to be estimated in the prereg.

## 10. Sequencing

- **Phase 0 (now):** this design doc → review + resolve §11 open decisions.
- **Phase 1 (build + internal pilot):** apparatus as a playable, incentive-instrumented interface —
  first with a **scripted/heuristic opponent** (zero backend, validate UX/mechanics/logging), then wired
  to a **live LLM** via the existing agent code. Internal pilot (self + a few testers) for UX,
  comprehension, and clean logging — **apparatus testing only, no data enters the paper** (no IRB yet).
- **Phase 2 (IRB + pre-registration):** protocol, consent, power analysis, analysis plan (mirroring the
  WP3 prereg discipline).
- **Phase 3 (run):** recruit, collect, analyze, place humans on the gradient; then decide in-paper vs
  follow-up.

## 11. Open design decisions (need the user)

1. **Human role:** B only (cleanest, v1), or B **and** A (adds the over-demand test HH5, but doubles
   conditions/length)?
2. **Opponent:** fixed frontier only (clean human placement), or **also a weak model** (tests whether
   humans exploit weak agents — richer, but adds conditions)?
3. **Module:** II only for v1, or also **Module I** (private-information screening — tests human
   deception + P3 channel separation on the *said* side, but a very different UI)?
4. **Messaging:** **free-text** human messages (richer, more human, but need a judge/moderation layer),
   or **structured choices** only (cleaner, safer, faster)?
5. **Platform / N / budget:** Prolific vs MTurk vs university pool; target $N$; bonus scheme.
6. **In-paper vs follow-up:** deferred by decision — revisit after Phase 1 pilot.

**v1 defaults — LOCKED (user, 2026-07-19):** human = **B only**; opponent = **fixed frontier** (scripted
heuristic for the Phase-1 prototype, live LLM once wired); **Module II only**; **structured choices** for
the accept/reject/honor/attack decisions with an **optional single free-text message** per round;
platform/N deferred to the prereg; in-paper vs follow-up deferred to after the Phase-1 pilot.
→ **Phase 1 build (in progress):** self-contained HTML prototype (`interface/pacta_bargaining_prototype.html`),
scripted opponent, DV logging + session export, engagement hooks (betrayal reveal, cliff meter, gradient
placement). **Bilingual TR/EN** (browser-default). **Neutral experimenter framing** (no value-laden nudges
in instructions/feedback; opponent dispatches stay persuasive as diegetic stimulus; between-round feedback
is factual/symmetric). **Consent notice + 3-question comprehension gate** added (comprehension tests
rules/payoffs, not strategy). Remaining for study-readiness: real IRB consent text, demographics, and
platform integration. **Note on a live-LLM opponent:** it cannot run inside the published artifact (CSP
blocks external calls) and would need a backend/web-app; a fixed scripted opponent is also methodologically
cleaner (removes opponent variance) for the "where do humans sit on the gradient" question, so it may be
the right choice for v1 regardless.
