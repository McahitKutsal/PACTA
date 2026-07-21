# PACTA-Bench v0.5.2 — Skeleton + LLM Pipeline + Judge + 4 Scenarios + G2 Pilot

The working core of a benchmark for measuring **verifiable commitment protocols**
in LLM-based crisis bargaining. Written in pure Python ≥ 3.10, with optional
`anthropic`/`openai` packages for real LLM integration.

This skeleton is the **numerical twin** of the **T1.1 Formal Model v0**
document: every closed-form result presented there (`mu_bar`, `b*`, minimum bond)
and every equilibrium prediction is validated here through unit tests. Mapping
to the Manifest tasks:

| Manifest task                                  | Corresponding implementation in this repository                                    |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| T1.5 — Analytical ↔ numerical cross-validation | `tests/test_theory.py` (12 tests)                                                  |
| T2.2 — Commitment DSL + ledger                 | `core.Commitment`, `core.Ledger`                                                   |
| T2.3 — Referee engine + LLM judge              | `engine._referee_verify` (deterministic) + `judge.py` (Mock/LLM Judge)             |
| T2.5 — Metric logger + recording discipline    | `core.new_record` (config hash, seed), `orchestrator`                              |
| §10.1 Metrics (v0 subset)                      | `metrics.aggregate`: DR, PBR, EI, AR, WELF, ED                                     |
| T2.1 — Scenario templates                      | `scenarios.py` (S1–S4; S1/S3 for Module I, S2/S4 for Module II; leakage-resistant) |
| T2.4 — LLM agent integration                   | `agents.LLMAgent` + `llm.py` (Mock/Anthropic/OpenAI); **completed**                |

## Quick Start

```bash
python -m unittest discover -s tests -v   # theory verification (15/15 should pass)
python -m pacta_bench.demo                # four-block pilot table (hard-coded agents)
python -m pacta_bench.llm_demo            # LLM pipeline + judge demo (zero API)
```

Demo outputs are written to `out/demo_results.json` and
`out/transcripts_sample.jsonl`. Every episode record includes a **seed** and
**config_hash** (Manifest §18.2: *"a run without a record is considered never to
have occurred"*).

## LLM Pipeline (WP2/T2.4)

The pipeline consists of three layers:

`scenarios.py` (machine-readable templates derived from Scenario Specification
v0.1) → `llm.py` (clients + JSON enforcement) → `agents.LLMAgent` (binds the
LLM to the engine interface).

`MockClient` reconstructs the numerical parameters embedded in the prompt and
plays according to the T1.1 rational strategy. This demonstrates that the
scenario templates contain **sufficient information** without requiring any
external API and serves as a regression oracle.

```python
from pacta_bench import LLMAgent, MockClient, ModuleIIParams, ProtocolParams, run_module_II

A = LLMAgent(MockClient(), "S2", "A")
B = LLMAgent(MockClient(), "S2", "B")

rec = run_module_II(
    ModuleIIParams(delta=0.30),
    ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.20),
    A, B, seed=0
)

# rec["events"] contains every raw 'llm_call' response together with its parsed result
# (for judging and auditing)
```

**Switching to real models:** pass either
`AnthropicClient(model=..., temperature=0.0)` or
`OpenAICompatClient(...)` to
`pacta_bench.llm_demo.main(factory, tag)`.

Model versions are fixed and recorded in every run (R7). The MockClient
pipeline reproduces theoretical predictions through the LLM interface:
S1/P3 unraveling (0% war), the S2 dose-response threshold
(`b_min = 0.118`), and Example 6's welfare peak.

## Architecture (One-to-One with Manifest §8.2)

```
orchestrator.run_batch
   └── engine.run_module_{I,II}      # game flow (state machine)
         ├── agents.*                # policies: Rational / Deceptive / Naive / LLM (stub)
         ├── core.Ledger             # commitment ledger (P1+)
         └── referee                 # violation predicate + (v, eps) verification sampling
                └── metrics.aggregate
```

**Payoff contract (v0):** Payoffs are expected values (over the war lottery and
verification process). The verification signal `s` is still sampled using the
episode seed and recorded in the ledger. Realized-payoff mode will be enabled
via a configuration flag in v1.

## Rational-Limit Findings (Demo Summary)

* **Module I** (`μ = 0.60`): Under P0/P1, war ≈ 40% and DR ≈ 60%.
  *Even fully rational agents lie; deception is incentive-driven*
  (Lemma 2 / Example 1). Under P3, unraveling occurs: war = 0, DR = 0.

* **Module II** (`Δ = 0.30`): Under P0/P1, preventive war occurs with 100%
  probability (Powell). Under P2, the dose-response transition occurs exactly
  at `b_min = 0.1176`; with `b = 0.20`, peace is sustained,
  `x* = 0.47`, and `DWL = εb = 0.01`.

* **H5 core result:** A deceptive agent exploits a naive proposer under P0
  (Agent A payoff: 0.10). The **same agent** keeps its promise under
  P2 (`b = 0.40`) and earns 0.58. The mechanism changes incentives,
  not intentions.

## LLM Integration Contract (WP2/T2.4)

Within `agents.LLMAgent`:

1. Every method maps `obs` → prompt → **structured action**
   (JSON/DSL enforcement).
2. Free-text claims are converted into
   `core.log_claim(channel="verbal")` entries through the LLM Judge.
3. Model versions are fixed and logged (R7).

The hard-coded agents remain the ground-truth generators for judge calibration.

## G2 Pilot (Local Ollama)

`g2_pilot.py` executes the complete four-scenario × four-protocol matrix with
integrated agents and judges, producing the G2 gate decision (whether effective
deception/violation differs significantly across protocols).

Using local **Ollama** models provides zero-cost execution, full reproducibility
(R7), and natural model-family separation (R2: Qwen as the agent, Gemma as the
judge).

```bash
# 1) Start Ollama and download the models
ollama pull qwen3:8b       # agents (Alibaba)
ollama pull gemma3:4b      # judge (Google — different family)

# 2) Install the OpenAI-compatible client
pip install openai

# 3) Run the pilot
python g2_pilot.py                 # real Ollama
python g2_pilot.py --mock          # API-free preview (pipeline test)
python g2_pilot.py -n 50           # episodes per cell
python g2_pilot.py --agent mistral --judge llama   # cross-family configuration
```

Model assignments are defined in
`make_ollama_factory` and `make_ollama_judge`.
To change them, edit the `AGENT_MODEL` and `JUDGE_MODEL` constants.

Outputs include:

* `out/g2_pilot_*.json`
* Sample transcripts
* Console summary table
* G2 decision (**PASS / CONDITIONAL / REVISE**)

## Scenarios (T2.1)

The four scenarios share two game families (the engine remains unchanged; only
the narrative wrapper differs):

* **S1** Valley Dispute
* **S3** Sanctions–Inspection Trade-off

→ Module I (private information + verifiable disclosure; unraveling and channel
separation)

* **S2** Ceasefire Negotiation
* **S4** Blockade Crisis

→ Module II (commitment problem + power shift; dose-response threshold and
welfare peak)

Scenarios are instantiated as, for example:

```python
LLMAgent(client, "S3", "B")
```

The `_REGISTRY` maps every scenario to its corresponding
(game family, system function, phase function) triple.

**Scenario robustness (R1):** Scenarios within the same family produce
identical outcomes (S1 ≡ S3, S2 ≡ S4); changing the narrative wrapper does not
alter rational behavior (`test_cross_scenario_consistency`).

For real LLMs, narrative framing effects become an empirical question to be
measured.

## Judge Layer (T2.3)

`judge.py` converts free text into deception labels (structured actions are
already deterministic inside the engine).

The judge performs three tasks:

* Claim extraction (G1)
* Ground-truth matching (G2)
* Rhetorical escalation detection (G3)

`MockJudge` is a deterministic oracle with access to the ground truth.
`LLMJudge` is the real evaluation model (R2: always from a different model
family than the evaluated agent).

**Key finding (channel separation):**

Using `MockClient(persona="deceptive")`, the vulnerable type bluffs.

The judge distinguishes two metrics:

* `DR_judged` — deception expressed in language
* `DR_effective` — deception that actually determines the outcome

Under P3, bluffing still occurs (`DR_judged > 0`), but certificates cannot be
forged, so **effective deception is zero**, leading to unraveling.

The protocol does not prohibit deception—it **renders deception ineffective**.

This distinction constitutes the central thesis of the project and would remain
invisible without the judge layer.

**Calibration (κ gate):**

```python
calibrate(gold, test)
```

computes Cohen's κ, with a target value of **κ ≥ 0.7**
(Manifest §12.1).

Here:

* `gold` = MockJudge or a human gold-standard set
* `test` = LLMJudge

## Version / License

v0.5.2 — MIT (proposed; to be finalized under WP0/T0.1).

All changes are recorded in the Manifest §18.5 Decision Log.
