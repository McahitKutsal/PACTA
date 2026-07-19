# PACTA WP3 — Pre-Registration (FROZEN v1.0)

*OSF-style pre-registration for the confirmatory PACTA study (task T3.2). Drafted **after** the G2
pilot and **before** WP3 data collection. **Scientific content is FROZEN as of the date below**:
hypotheses (H1–H9), the model/scenario set (4 families × 2 tiers; 6 scenarios), the sampling plan
(n=30/15), the dual-judge scheme, the analysis, and the instrumentation. Any post-freeze deviation is
logged in the Decision Log with justification (R7). Only administrative OSF fields (author identity,
submission timestamp) are completed at upload; they do not alter the frozen scientific design.*

- **Study:** PACTA — From Cheap Talk to Verifiable Commitment in LLM Crisis Bargaining (WP3 confirmatory).
- **Registration venue / freeze date:** OSF (pre-registration); scientific freeze **2026-07-11**.
- **Authors:** [to fill at OSF upload — solo execution per D-004].
- **Bench version to pin:** PACTA-Bench v0.6.3 (frozen WP3 tag); every episode carries
  `config_hash`, `seed`, and pinned `model_version` (R7).
- **Model snapshots:** the pilot model strings are pinned (claude-sonnet-5 + a Haiku tier; gpt-4o +
  o4-mini; qwen-plus + qwen3.7-max; deepseek-v4-flash + deepseek-v4-pro); the **exact API-returned
  version is stamped per episode record** (R7), so the concrete snapshot is captured at run time even
  where a dated alias is not exposed.
- **Prior work this builds on:** G2 pilot (`out/g2_pilot_*.json`, `out/G2_sonnet5_analiz.md`,
  `out/G2_capability_vs_comprehension.md`); paper §3 (theory), §5 (design), §6 (pilot results).

---

## 1. Rationale and what the pilot already established

The G2 pilot (8 agents, 4 families, $n=8$/cell, descriptive) established the *directions and
break-point locations* that WP3 now tests **confirmatorily** with adequate power, $\kappa$-calibrated
judges, and a frozen model set. Pilot findings that become confirmatory targets:

1. **P3 unraveling + channel separation** — under verified disclosure, *effective* deception → 0
   (structural) and war falls; *said* deception persists. (All families showed DR_eff→0.)
2. **Module II dose-response cliff at $b^\*_{\min}\approx0.118$** — war $\approx1.0$ below, $\to0$
   above, for reasoning models; Sonnet 5 recovered the equilibrium split to $ED=0.0045$.
3. **Capability gradient** — the incentive-compatible (IC) response scales with **reasoning
   capability, not model family**; established by within-family reasoning controls in ≥2 families
   (Alibaba qwen-plus↔qwen3.7-max; DeepSeek v4-flash↔v4-pro; OpenAI gpt-4o↔o4-mini).
4. **Novel $b=0.40$ participation-binding over-demand** — war returns non-monotonically at high bond;
   replicated in 3 families (Sonnet 5, Qwen3.7-max, deepseek-v4-pro).
5. **Accept-then-attack rate** — a judge-independent capability metric; falls monotonically down the
   gradient (100→100→66→28→6→3%). The bottom-model failure is **non-integration of the incentive**,
   not miscomprehension (comprehension present in messages; defection bond-invariant).
6. **Welfare backfire** — for non-reasoning models the bond drives WELF *below* the war baseline
   (gpt-4o and qwen-plus share the law WELF $=0.80-0.9b$).

WP3 confirms 1–6 and, critically, does so **stratified by reasoning tier** — pooling across the
gradient would wash out capability-conditional effects (a design lesson from the pilot).

---

## 2. Research questions (unchanged from paper §5.3)

- **RQ1** Baseline: how much do LLM agents deceive / break commitments / escalate under cheap talk,
  vs the game-theoretic prediction?
- **RQ2** Protocol effect: to what extent and by what mechanism do recorded/costly/verifiable
  protocols reduce deception, violation, escalation, welfare loss?
- **RQ3** Theory–empirics bridge: under which $(b,v)$ conditions is honest commitment IC, and does
  behavior show the predicted break-point?
- **RQ4** Robustness: stability across adversarial opponents, prompt/persona variation, model family,
  and capability tier.

---

## 3. Confirmatory hypotheses (LOCKED directions + thresholds)

Tested in the two weak forms the LLM bridge licenses (§3.5): **sign** of comparative statics and
**location** of regime changes — never point rationality. Thresholds below are calibrated on pilot
data and frozen here.

| Hyp. | RQ | Statement (direction) | Primary DV | Pre-registered threshold |
|---|---|---|---|---|
| **H1** | 1 | Under P0, deception & escalation prevalent | DR_eff, EI, war (P0) | $DR_{\text{eff}}>15\%$ **and** war $>0.3$ in ≥3 families (reasoning tier) |
| **H2** ⭐ | 2 | Ladder lowers *effective* deception/violation: P3 ⪯ P2 ⪯ P1 ≈ P0; said-deception may persist (channel separation) | $DR_{\text{eff}}$, PBR (judge-independent) | monotone drop in effective metric; Cliff's $\delta\ge0.3$ at critical transition |
| **H3** ⭐ | 3 | Violation/war drops sharply once $b\ge b^\*_{\min}$ | PBR–$b$, war–$b$; segmented regression | empirical break within $\pm25\%$ of $b^\*_{\min}=0.118$ (reasoning tier) |
| **H4** | 2 | Welfare/Pareto up, war down under P2+ (reasoning tier) | war rate, WELF, DWL | ≥50% relative war reduction under P2 ($b\ge b^\*$) vs P0 |
| **H5** | 4 | P2–P3 bound exploitation loss vs an adversary | EXPL (adversarial cells) | loss ≤ ½ of P0 loss |
| **H6** | 2–3 | Within peace zone welfare declines in $b$; non-monotone re-entry of war at high bond (participation-binding) | WELF–$b$, war–$b$ | slope $<0$ in peace zone; war re-entry near $b^{\dagger}\approx0.33$ |
| **H7** ⭐ | 4 | The IC response scales with **reasoning capability, not family**: within every vendor, the reasoning tier shows a sharper cliff / lower accept-then-attack than its non-reasoning tier | accept-then-attack rate; war–$b$ cliff depth | within-family monotone in tier in ≥3 of 4 families; between-family rank ~ reasoning tier, not vendor |
| **H8** | 2–3 | **Decoupling**: $DR_{\text{eff}}\to0$ under P3 for *all* models (structural), but war-reduction only for sufficiently capable models (capability-dependent) | $DR_{\text{eff}}$ (all) vs war (by tier) | $DR_{\text{eff}}=0$ under P3 for 100% of models; P3 war-reduction correlates with tier ($\rho>0$) |
| **H9** | 2 | **Welfare backfire**: for non-reasoning models WELF is non-increasing in $b$ and can fall below the P0 war baseline | WELF–$b$ (non-reasoning tier) | slope $\le0$; WELF$(b{=}0.40)<$ WELF(P0) in ≥2 non-reasoning models |

⭐ = **primary** confirmatory hypotheses (multiple-comparison family fixed to {H2, H3, H7}); all others
are secondary/confirmatory-supporting. A theory–empirics *divergence* (e.g. H6 over-demand) is a
reportable contribution, not a failure (gate G3).

**Primary DVs are judge-independent** (war rate, PBR, accept-then-attack, WELF, ED) so confirmatory
claims do not depend on judge calibration; $DR_{\text{said}}$ (judge-dependent) is secondary only.

---

## 4. Design

### 4.1 Factors (fractional factorial, power concentrated on primary cells)

- **Protocol:** P0, P1, P2 (bond sweep), P3.
- **Scenario (LOCKED at 6):** Module I — S1 (valley/territory), S3 (sanctions-for-inspections),
  **S5 (water-sharing: upstream/downstream, hidden water need/scarcity → screening)**; Module II —
  S2 (ceasefire), S4 (naval blockade), **S6 (arms-control: mutual-disarmament pledge under a power
  shift, verified)**. Three covers per module; the **S1≡S3≡S5** and **S2≡S4≡S6** rational-limit
  invariants (R1) control for narrative confounds. [Code: S5/S6 templates to implement before freeze.]
- **Model family × tier (frozen set):** each family run at a **non-reasoning** and a **reasoning**
  tier where available, to give a within-family control (H7):

  | Family | Non-reasoning tier | Reasoning tier |
  |---|---|---|
  | Anthropic | Claude Haiku 4.5 | Claude Sonnet 5 |
  | OpenAI | gpt-4o | o4-mini (or o-series reasoning) |
  | Alibaba | qwen-plus | qwen3.7-max |
  | DeepSeek | deepseek-v4-flash | deepseek-v4-pro |

  **LOCKED at 4 families** (Anthropic, OpenAI, Alibaba, DeepSeek) — gives up to four within-family
  reasoning controls (H7), of which three are already demonstrated in the pilot. This is **below the
  paper's current §12.1 bar of ≥5 families**, which is therefore to be revised to **≥4** (see §10 /
  Decision Log); the core "reasoning-not-family" claim rests on the within-family controls, not on
  family count, so 4 families is sufficient for it. Self-play primary; a cross-pairing subset for
  R2/robustness. [LOCK at freeze: exact model snapshot IDs.]
- **Bond sweep (P2):** $b\in\{0,\,0.05,\,0.10,\,0.118,\,0.15,\,0.20,\,0.25,\,0.33,\,0.40,\,0.50\}$,
  **densified around $b^\*_{\min}=0.118$ and $b^{\dagger}\approx0.33$** (both matter: cliff + over-demand).
- **Verification sweep (secondary):** $(v,\varepsilon)\in\{(0.9,0.05),(0.6,0.3),(1.0,0)\}$ incl. the
  discriminating boundary cell $(0.6,0.3)$; hard shift $\Delta=0.45$ (D-005).
- **Information:** {complete, incomplete}. **Power:** {symmetric, asymmetric}.

### 4.2 Judges and R2 (LOCKED — dual judge)

Judge family ≠ agent family (R2). Because primary DVs are judge-independent, judge choice cannot drive
confirmatory results; the judges are needed only for $DR_{\text{said}}$ and rhetoric (secondary).

**Dual independent judges on every episode**, drawn from a three-judge pool —
{**GPT-4o-mini** (OpenAI), **Claude Haiku 4.5** (Anthropic), **deepseek-chat** (DeepSeek)}. For each
agent, the two judges are the pool members whose family ≠ the agent's family (R2), so both are always
out-of-family:

| Agent family | Judge 1 | Judge 2 |
|---|---|---|
| OpenAI | Claude Haiku 4.5 | deepseek-chat |
| Anthropic | GPT-4o-mini | deepseek-chat |
| Alibaba | GPT-4o-mini | Claude Haiku 4.5 |
| DeepSeek | GPT-4o-mini | Claude Haiku 4.5 |

> **Post-freeze deviation (pre-data for the affected configs):** the third pool member was changed
> Gemini 2.x Flash → Qwen-plus (D-022, no `GEMINI_API_KEY`) → **deepseek-chat (DeepSeek)** (D-028). The
> *design* is unchanged — two independent, out-of-family judges per episode with inter-judge κ (R2);
> only the third pool slot's vendor changed, **before any OpenAI/Anthropic-agent data was collected**
> (the third slot is only ever used to judge OpenAI/Anthropic agents; the completed DeepSeek + Alibaba
> configs used {GPT-4o-mini, Claude Haiku} and are unaffected). Keys: OPENAI + ANTHROPIC + DEEPSEEK.

Both judges label every episode; the **inter-judge Cohen's $\kappa$ is reported per cell** (§7), and the
secondary said-deception metric uses the agreement-filtered label (claims on which the two judges agree).
Each judge must also pass $\kappa\ge0.7$ against the gold set (§7); a judge failing the gate is replaced
by the third pool member and, if none passes, that family's said-deception numbers are withheld.
(Doubles judge cost — accepted for the strongest said-deception reliability. Primary DVs unaffected.)

---

## 5. Sampling plan and power analysis

**Effect sizes from the pilot** (proportion contrasts, arcsine $h$):

- H3 cliff (war $\approx1.0$ below vs $\approx0$ above $b^\*$, reasoning tier): $h\approx\pi$
  (near-maximal) → $n=5$ gives power $>0.99$. **Vastly over-powered.**
- H2 effective-deception drop (P0 $\approx0.7\to$ P3 $=0$): structural/deterministic → tiny $n$.
- **Binding constraint = smallest effect of interest**: the gradient's adjacent-tier war-rate
  differences and the $b=0.40$ over-demand magnitude. To detect a war-rate difference of $\Delta p=0.25$
  around $p=0.4$ ($h\approx0.50$) at power $0.80$, $\alpha=0.05$ two-sided: $n\approx31$/cell.

**Pre-registered $n$ (LOCKED — full matrix):** **$n=30$ per primary cell** (cliff region
$b\in\{0.10,0.118,0.15,0.20\}$ and P0/P3 for each model×scenario) — powers $h\ge0.51$ (war-rate diffs
$\ge\!\sim0.25$ around $p=0.4$) at $0.80$, and vastly over-powers the primary cliff/channel effects
(near-maximal $h$). **$n=15$ per secondary cell** (P1, other bond points, verification sweep) — powers
$h\ge0.72$ (large effects only; adequate for exploratory sweeps). *Trade-off noted: the finest gradient
distinctions ($\Delta p<0.25$) may be under-powered at $n=30$; these are reported descriptively with CIs
and, where needed, pooled across covers.* Mixed-effects random intercepts (§6) absorb model/seed
heterogeneity; this is a per-contrast proportion power calc, standard for pre-registration.

**Compute estimate:** ~42 cells/model (Module I: 3 scenarios × {P0,P1,P3} = 9; Module II: 3 scenarios ×
{P0 + 10-point bond sweep} = 33), **8 model configs** (4 families × 2 tiers) → **~7–8k core
self-play episodes** at blended $n$ (30/15), each ~3–5 LLM calls. Information/power/adversarial strata
(WP4) apply to a subset. **Reasoning-tier models dominate wall-clock and cost** (e.g. deepseek-v4-pro
100–220 s/episode) — schedule/stagger and run overnight; the resilient harness (fail-fast + retry/skip)
supports long unattended runs.

**Stopping rule:** fixed $n$ per cell (no optional stopping); a cell is complete when it reaches its
target of *successfully parsed* episodes.

---

## 6. Analysis plan

- **Model:** mixed-effects regression `outcome ~ protocol * scenario + information + power +
  reasoning_tier + (1 | model) + (1 | seed)`, cluster-robust SEs. **Capability-stratified**: primary
  effects estimated *within* reasoning tier and with `reasoning_tier` as a moderator (pooling across
  the gradient is pre-specified as inappropriate — pilot lesson).
- **Multiple comparisons:** Holm correction over the frozen primary family {H2, H3, H7}.
- **Effect sizes:** Cliff's $\delta$, Cohen's $d$, arcsine $h$ with 95% CIs — emphasized over $p$.
- **Break-point (H3, H6):** segmented / change-point regression on the war–$b$ and PBR–$b$ curves;
  the break-CI is compared against $b^\*_{\min}=0.118$ (H3) and re-entry near $b^{\dagger}=0.33$ (H6).
- **Gradient (H7):** accept-then-attack rate and cliff-depth regressed on reasoning tier; within-family
  paired contrasts (non-reasoning vs reasoning) reported per vendor.
- **Equilibrium accuracy:** $ED=|x-x^\*|$ distribution per cell; MockClient rational baseline as the
  $ED\to0$ reference.

---

## 7. Metrics (locked) and judge calibration

- **Primary (judge-independent):** war rate, PBR (deterministic referee), **accept-then-attack rate**
  (new, first-class), WELF/DWL, $ED$, escalation index (action-based).
- **Secondary (judge-dependent):** $DR_{\text{said}}$, rhetoric index — gated behind $\kappa\ge0.7$,
  and computed from the **agreement-filtered** label of the two judges (§4.2).
- **$\kappa$ gate (two-level, dual-judge):** (i) **judge-vs-gold** — gold set from scripted policies
  (rational / deceptive / naive) + **10% double human coding**; each of the two judges must reach
  Cohen's $\kappa\ge0.7$ vs gold or be replaced by the third pool member. (ii) **inter-judge** — the two
  judges' $\kappa$ is reported per cell as a reliability check; claims where they disagree are excluded
  from the said-deception numerator/denominator. A cell whose inter-judge $\kappa<0.7$ has its
  said-deception metric flagged low-confidence (primary DVs unaffected — they are judge-independent).

---

## 8. Instrumentation locked before data collection (from the pilot)

1. **t2 decision rationale.** The period-2 honor/attack decision must log a **one-line rationale**
   (and, where the API exposes it, the reasoning/thinking trace), so the incentive-integration
   mechanism (§6.5(v)) is directly observable rather than inferred. *(Closes the pilot's stated
   limitation.)*
2. **`evaluate_g2` trough-fix.** The gate must compare P0 to the **minimum war over the bond sweep**
   (the peace trough), not to the highest bond $b=0.40$ — otherwise the (now 3-family-replicated)
   over-demand regime causes the gate to *understate* a genuine full response (observed for
   deepseek-v4-pro). Applies to the automated verdict only; does not affect raw metrics.
3. **Accept-then-attack rate** added to the aggregate/metric logger as a first-class output.
4. **Resilience/record discipline**: fail-fast on permanent API errors (auth/quota), per-episode
   retry/skip on transient errors, `config_hash`+`seed`+`model_version` on every record (R7), full
   transcripts (`--save-transcripts`).
5. **Per-cell checkpoint/resume** (D-021/D-022) for the multi-week run: each cell is persisted to
   `out/g2_ckpt_{tag}.jsonl` as it completes; a crashed/interrupted config resumes from the last
   completed cell on re-run (same command), so the loss from a crash in a ~37 h config is one cell, not
   the whole config. Checkpoint auto-deletes on successful completion.
6. **8-config orchestrator** (`wp3_run.py`): runs the 4-family × 2-tier matrix as isolated
   subprocesses (`--dual-judge`), so a failure in one config does not stop the others; supports
   `--configs`/`--only`/`--dry-run` for family-by-family execution.

*(Items 1–3 are code changes to land and unit-test before the freeze; see §10.)*

---

## 9. Exclusions, robustness, deviations

- **Exclusions:** episodes with parse failure after retry are excluded and re-drawn to hit target $n$
  (parse errors were 0 across all API agents in the pilot, so this is expected to be rare); cells
  where an API returns a permanent error (model unavailable) are dropped and logged.
- **Robustness (WP4):** ≥5 prompt/persona paraphrases per scenario; adversarial opponents (hawk,
  exploiter, trust-abuser) for H5; loophole red-team with letter-vs-spirit coding.
- **Deviations:** any change after the freeze is recorded in the Decision Log with rationale (R7);
  the pre-registration version and freeze date are stamped into every output record.

---

## 10. Status: locked vs still-open

**Locked (this revision):**
- **4 families** — Anthropic, OpenAI, Alibaba, DeepSeek — each at a non-reasoning and a reasoning tier
  (up to 4 within-family controls, H7; 3 already shown in the pilot). *Below the paper's current §12.1
  ≥5-family bar → §12.1 to be revised to ≥4 (open item 1).*
- **6 scenarios** — S1/S3/S5 (Module I), S2/S4/S6 (Module II); 3 covers per module.
- **Sampling** — $n=30$ primary / $n=15$ secondary; fixed $n$, no optional stopping.

**Done (landed with regression tests; 57/57 green):**
- ✓ Paper §12.1 (+ top note + §5.2) aligned from "≥5 families" to "≥4 families".
- ✓ **Instrumentation (§8) all landed:** (a) t2-rationale logging (`rec["t2_rationale"]`; t2_action
  event kept a string for judge compatibility); (b) `evaluate_g2` trough-fix (P0 vs the bond-sweep war
  trough, not $b=0.40$); (c) `accept_then_attack_rate` added to `aggregate()` (judge-independent,
  Module II); (d) S5 (water-sharing, Module I) + S6 (arms-control, Module II) scenario templates, with
  S1≡S3≡S5 and S2≡S6 rational-limit invariant tests passing under MockClient.

**Resolved at freeze (2026-07-11):**
- ✓ **Judge scheme** — dual independent out-of-family judges on every episode (§4.2), inter-judge $\kappa$
  reported, two-level $\kappa\ge0.7$ gate (§7).
- ✓ **Venue / freeze date** — OSF; scientific freeze 2026-07-11.
- ✓ **Model snapshots** — pilot model strings pinned; exact API version stamped per record (R7).

**Administrative only (completed at OSF upload; does not alter the frozen design):**
- Author identity and the OSF submission timestamp.

**Status: FROZEN.** WP3 execution (a separate step) instantiates this spec: extend the runner to the
6-scenario × 8-config × (n=30/15) matrix with the dual-judge pass, then run.
