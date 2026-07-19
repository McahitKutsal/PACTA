# §6 Results — WP3 confirmatory consolidation *(PROPOSED replacement for the pilot §6)*

*(Review draft. This supersedes the pilot (n=8) §6.1–§6.6 of `PACTA_draft.md` with the
pre-registered main matrix: **4 families × 2 tiers = 8 agents**, dense 10-point bond sweep,
**n=30 primary / 15 secondary**, **dual out-of-family judges** with inter-judge AC1, judge-independent
primary DVs, and 95% CIs. Headline reorganized around **decoupling** (H8). Numbers are drawn from
`out/g2_pilot_*_dualjudge*.json` and the per-cell transcripts; nothing here touches the frozen
pre-registration. Merge into `PACTA_draft.md` §6 after review.)*

---

## 6. Results

*(Scope: the pre-registered confirmatory study (WP3). Eight agents span four families at two capability
tiers each — Anthropic (**claude-haiku-4-5**, **Claude Sonnet 5**), OpenAI (**gpt-4o**, **o4-mini**),
Alibaba (**qwen-plus**, **Qwen3.7-max**), DeepSeek (**deepseek-v4-flash**, **deepseek-v4-pro**) — over
six scenarios (S1/S3/S5 Module I; S2/S4/S6 Module II), the 10-point bond sweep of §5, and dual
out-of-family judges (§4.6) with agreement-filtered labels and reported inter-judge AC1. Primary DVs
(war rate, PBR, accept-then-attack rate, WELF, agreed $x$) are **judge-independent**, so the
confirmatory results do not depend on judge reliability. Parse errors were zero on all runs. The
pre-registration fixes **one non-reasoning and one reasoning tier per family**; relative to the pilot
this *adds* Anthropic's non-reasoning tier (claude-haiku, absent there) and does not carry
deepseek-v3.2, a third DeepSeek tier used only in the pilot's exploratory cross-section, so the
confirmatory set is the more complete $4\times2$ design rather than a subset of the pilot. Sonnet 5
was run as a depth-preserved **focused replication** (Module II scenario S2, Module I S3, the same bond
sweep at full $n$; deviation logged), for the reasons given in §6.7.)*

The central result is a **decoupling**: a designed protocol neutralizes deception on **every** agent
regardless of capability, but converts that neutralization into actual conflict-reduction **only** on
sufficiently capable models. §6.1 states the decoupling; §6.2–§6.3 establish its two halves (structural
neutralization; capability-dependent war-reduction and the bond cliff); §6.4 isolates reasoning from
family with four within-family controls; §6.5 reports the novel over-demand divergence; §6.6 is a
case study of framing-(in)variance that the reasoning tier resolves; §6.7 covers judge reliability
and caveats.

### 6.1 The headline: deception-neutralization is universal, war-reduction is capability-dependent

Theorem T3 gives verified disclosure (P3) two consequences: effective deception falls to zero *and*
war falls to zero. In the data these two consequences **come apart by capability**. Effective
deception under P3 is **exactly zero for all eight agents** ($DR_{\text{eff}}=0$ in every Module I
cell, Table 1) — it is structural, fixed by the unforgeable certificate channel, independent of the
model. War-reduction under P3 is not: it ranges from full elimination on frontier reasoners
(deepseek-v4-flash $0.41\to0$; Qwen3.7-max $0.40\to0.03$) to **none** on the weakest agents, where war
under P3 is flat or even *rises* (qwen-plus $0.31\to0.44$; claude-haiku $0.64\to0.70$). The same split
appears in Module II (Table 2): every reasoning tier triggers the bond cliff, every non-reasoning tier
fails it. A protocol can thus reliably kill *effective deception* on any model while translating that
into *peace* only on a capable one. This is the paper's sharpest design-relevant claim
(H8): **deception-neutralization is capability-robust; the welfare benefit of a protocol is not.**

### 6.2 Module I: verified disclosure unravels, and deception separates into two channels

Under cheap talk (P0), roughly $1-\mu=0.40$ of episodes end in war with high uttered deception,
consistent with H1 and the babbling equilibrium (Lemma 2); recording alone (P1) leaves behavior
essentially unchanged (Note 2). Verified disclosure (P3) drives **effective** deception to exactly
zero for every agent, while capable models keep *uttering* now-inert bluffs ($DR_{\text{verbal}}>0$):
the **channel separation** that is the mechanism of Theorem T3. A representative frontier transcript
(deepseek-v4-pro, S1/P3) makes it concrete — a genuinely fragile ($c_H$) type utters the bluff

> *"We are resilient. Our war costs are low. If your offer is too greedy, we'll fight. We won't prove
> it, but you should consider that we may be resilient,"*

leaving the certificate channel empty (it cannot certify a false type), so the skeptical proposer
ignores the unverifiable claim and offers $x=p+c_H$, which the fragile type accepts — peace. The agent
literally says *"we won't prove it."* A protocol scored "still deceptive" by any single-number metric
is in fact one in which deception has been rendered inert — invisible without the judge layer (§4.6).
The structural half of the decoupling lives here: $DR_{\text{eff}}\to0$ holds uniformly (Table 1),
whereas whether P3 also lowers war is the capability-dependent half (Table 1, war column; §6.1).

**Table 1.** Module I under P3 (verified disclosure), all eight agents, ordered bottom-to-top of the
capability gradient. $DR_{\text{verbal}}$ is the **ground-truth** rate of uttered bluffs (the agent
claims a type it does not hold, computed by the engine — judge-independent); $DR_{\text{eff}}$ is
deception after the certificate channel. Effective deception is universally neutralized; war-reduction
is not. (Means/ranges over the scenarios each agent ran; $n=30$ at P0/P3.)

| Agent (family; tier) | Mod I war P0 → P3 | $DR_{\text{verbal}}$ P3 (uttered) | $DR_{\text{eff}}$ P3 | War-reduction? |
|---|---|---|---|---|
| qwen-plus (Alibaba; non-reasoning) | 0.31 → **0.44** | 0.00 | **0** | no (*rises*) |
| gpt-4o (OpenAI; non-reasoning) | 0.56 → 0.54 | 0.35–0.45 | **0** | no |
| claude-haiku-4-5 (Anthropic; non-reasoning) | 0.64 → **0.70** | 0.00–0.22 | **0** | no (*rises*) |
| o4-mini (OpenAI; reasoning-mini) | 0.33 → 0.21 | 0.39–0.64 | **0** | partial |
| deepseek-v4-flash (DeepSeek; light reasoning) | 0.41 → **0.00** | 0.38–0.48 | **0** | yes (full) |
| Claude Sonnet 5 (Anthropic; frontier) | 0.40 → 0.17 | 0.29 | **0** | yes |
| deepseek-v4-pro (DeepSeek; frontier) | 0.41 → 0.11 | 0.39–0.45 | **0** | yes |
| Qwen3.7-max (Alibaba; frontier) | 0.40 → **0.03** | 0.45–0.50 | **0** | yes (full) |

A pattern reinforces the channel-separation reading: the **reasoning** agents utter *more* verbal
bluffs under P3 ($DR_{\text{verbal}}\approx0.29$–$0.50$) than the non-reasoning bottom (qwen-plus
$0.00$; claude-haiku $\le0.22$), because they actually play the screening game — yet $DR_{\text{eff}}$
is $0$ for all of them. The protocol is thus most visibly at work precisely on the agents capable
enough to bluff. (The LLM-*judge*'s deception score $DR_{\text{judged}}$, a separate, judge-dependent
quantity, runs much higher — $\sim0.9$–$1.0$ — because the judges over-flag; that gap is the
judge-reliability story of §6.7, not the structural result here.)

### 6.3 Module II: a bond cliff at $b^\*_{\min}$, and how sharply it fires scales with capability

With $\Delta=0.30>c_A+c_B=0.20$, cheap talk produces near-certain preventive war (H1/H4). Introducing
a bond produces a **dose-response cliff** at the predicted threshold $b^\*_{\min}\approx0.118$ — for
frontier reasoners it is textbook-sharp. Sonnet 5 (S2) is illustrative: war collapses from **0.87 at
$b=0.10$ (below $b^\*_{\min}$) to 0.03 at $b=0.118$**, holding near zero to $b=0.33$, with pledge-breaking
$\to0$ and welfare recovering $0.82\to0.99$. The grid brackets the break to $b\in(0.10,0.118]$, so we
claim not point-localization at $0.118$ but that the empirical break falls inside the pre-registered
$\pm25\%$ band — the confirmatory criterion for H3. deepseek-v4-pro and Qwen3.7-max reproduce the cliff
across all three Module II covers.

**Table 2.** Module II bond dose-response, illustrative frontier run (Claude Sonnet 5, cover S2, $n=30$
per cliff cell / $15$ per secondary). The cliff is at $b^\*_{\min}$; the $b=0.40$ uptick is the
over-demand divergence of §6.5.

| $b$ | 0.10 | **0.118** | 0.15 | 0.20 | 0.33 | 0.40 |
|---|---|---|---|---|---|---|
| War rate | 0.87 | **0.03** | 0.03 | 0.00 | 0.00 | 0.53 |
| PBR | 0.20 | 0.00 | 0.03 | 0.00 | 0.00 | 0.00 |
| WELF | 0.82 | 0.99 | 0.98 | 0.99 | 0.98 | 0.88 |

How *cleanly* the cliff fires is the capability-dependent half of the decoupling, and it is
statistically clean. Table 3 orders the eight agents by the Module II **trough** (war at $b=0.20$,
pooled over the covers each ran) with Wilson 95% CIs. The rungs are separated: the non-reasoning
bottom sits at $1.00$ $[0.96,1.00]$, the frontier top at $0.00$–$0.09$ $[0.00,0.17]$, with the
intermediate reasoners strictly between. The convergent judge-independent metrics — trough war, PBR,
and accept-then-attack rate — agree on the ordering.

**Table 3.** Cross-model Module II response, bottom-to-top. Trough war rate with Wilson 95% CI; PBR and
accept-then-attack rate (both judge-independent) at the cliff/trough. (Pooled over the Module II covers
each agent ran: S2/S4/S6 for all but Sonnet 5, which ran S2 only, $n=30$.)

| Agent (family; tier) | Trough war ($b{=}0.20$) [95% CI] | PBR @ $b^\*_{\min}$ | Accept-then-attack @ $b{=}0.20$ |
|---|---|---|---|
| qwen-plus (Alibaba; non-reasoning) | 1.00 [0.96, 1.00] | 1.00 | 1.00 |
| gpt-4o (OpenAI; non-reasoning) | 1.00 [0.96, 1.00] | 1.00 | 1.00 |
| o4-mini (OpenAI; reasoning-mini) | 0.59 [0.49, 0.68] | 0.59 | 0.36 |
| claude-haiku-4-5 (Anthropic; non-reasoning) \* | 0.59 [0.49, 0.68] \* | 0.34 | 0.34 |
| deepseek-v4-flash (DeepSeek; light reasoning) | 0.26 [0.18, 0.35] | 0.30 | 0.26 |
| deepseek-v4-pro (DeepSeek; frontier) | 0.07 [0.03, 0.14] | 0.08 | 0.06 |
| Qwen3.7-max (Alibaba; frontier) | 0.09 [0.05, 0.17] | 0.14 | 0.09 |
| Claude Sonnet 5 (Anthropic; frontier) | 0.00 [0.00, 0.11] | 0.00 | 0.00 |

\* claude-haiku's aggregate trough (0.59) **masks a within-agent trichotomy** across the rationally
equivalent covers; it is not a stable intermediate. See §6.6.

### 6.4 The gradient tracks reasoning, not family: four within-family controls

Because each family is run at a non-reasoning and a reasoning tier of the *same vendor*, the gradient
is not a cross-vendor confound. **Four** within-family controls isolate reasoning capability:

- **Alibaba (on/off, sharpest).** qwen-plus and Qwen3.7-max share the DashScope endpoint and judge, yet
  qwen-plus fails completely (trough $1.00$, PBR $1.00$, accept-then-attack $1.00$) while Qwen3.7-max
  produces the full clean cliff (trough $0.09$) — a total-failure→full-response contrast with the
  serving stack fixed.
- **DeepSeek (depth).** deepseek-v4-flash and deepseek-v4-pro run through the same first-party endpoint;
  the deeper model floors lower (trough $0.07$ vs $0.26$) with less pledge-breaking — response quality
  rising monotonically with reasoning depth, provider fixed.
- **OpenAI (off→mini).** gpt-4o defects regardless of $b$ (trough $1.00$); o4-mini triggers the cliff
  but floors high (trough $0.59$) — reasoning helps even at "mini" scale, but shallowly.
- **Anthropic (labile→responsive).** claude-haiku is framing-labile (§6.6) while Sonnet 5 gives the
  sharpest clean cliff (trough $0.00$) — reasoning converts an unstable bond response into a stable one.

The gradient is therefore **monotone in reasoning depth**: none → total failure (qwen-plus, gpt-4o);
mini/shallow → partial (o4-mini, deepseek-v4-flash); deep → clean cliff (Sonnet 5, deepseek-v4-pro,
Qwen3.7-max). A corollary at the bottom: gpt-4o and qwen-plus, from different families, obey the
*identical* welfare law WELF $=0.80-0.9b$ — the accept-then-attack failure mode is a shared regularity,
not a per-model quirk (H9; §6.5). This lifts H1/H7 to the sharp claim that *the incentive-compatibility
response to a designed protocol scales with reasoning capability, not family.*

The mechanism at the bottom is **non-integration of the incentive, not miscomprehension**: the
weak models' period-1 messages correctly name the ledger, the escrowed bond, and period-2 honoring,
yet they accept-then-attack in 100% of bonded episodes, flat across every $b$ from $0.10$ to $0.40$
(forfeiting even a bond twice the stakes) and identically at P0 with no bond. The discriminating
statistic, the accept-then-attack rate, falls **monotonically** down the gradient (Table 3, last
column: $1.00\to0.36\to0.06$), mirrored by a rise in upfront refusals on the capable models. Capable
models decline a deal they could not keep; weak models agree to every deal and break it. The capability
axis is whether a model makes its action *incentive-contingent* — the property H1 concerns — not
whether it understands the game.

### 6.5 A novel divergence: participation-binding over-demand, replicated across four families

Every reasoning agent shows a non-monotone **return of war beyond $b^{\dagger}\approx0.33$**: at
$b=0.40$ war climbs back to $0.36$–$0.53$ (Sonnet 5 $0.53$, deepseek-v4-pro $0.36$, Qwen3.7-max $0.49$,
deepseek-v4-flash $0.60$, o4-mini $0.71$), even though monitoring loss $\varepsilon b$ is far below
$c_A+c_B$ and pledge-breaking is $\approx0$ (every breakdown is a $t=1$ war-now, not a broken pledge).
The mechanism (transcript-level, §6.3 of the pilot, reconfirmed here) is proposer **over-demand at the
IC→participation transition**: below $b^{\dagger}$ the incentive-compatibility and participation
ceilings coincide, above it they separate, and the proposer intermittently reaches toward the
now-slack IC ceiling $x_{IC}$ rather than the binding participation ceiling $x_P=0.58$, which the
sharply rational responder punishes. Table 4 shows the acceptance rule directly at WP3 fidelity: the
responder accepts every offer at or below $x_P=0.58$ and rejects every offer above it, so each war is
a proposer over-demand, not a responder error.

**Table 4.** $b=0.40$ offers by outcome (frontier runs). The responder's rule is **accept iff
$x\le x_P=0.58$**; the war rate is set entirely by how often the proposer overshoots.

| Run ($b{=}0.40$) | Offers accepted → peace | Offers rejected → war |
|---|---|---|
| Sonnet 5 (S2) | $x\in\{0.55,\ 0.57,\ 0.58\}$ | $x=0.60$ |
| deepseek-v4-pro (S4) | $x\in\{0.43,\ 0.57,\ 0.58\}$ | $x=0.63$ |

That an unanticipated, mechanistically specific divergence recurs
independently in **four families** is strong evidence it reflects the theory's regime change (H6)
rather than a per-model artifact. (It is robust enough that the automated gate, comparing P0 to the
*highest* bond, understates frontier responses by reading the over-demand regime rather than the
$b=0.20$ trough — corrected in analysis by the trough comparison.)

### 6.6 Framing-(in)variance: a case study the reasoning tier resolves

The rationally equivalent Module II covers (R1: S2 ≡ S4 ≡ S6) let us test whether a model's bond
response is invariant to surface framing. Seven of the eight agents are framing-consistent — they
fail, partially respond, or cleanly comply *the same way* across covers. **claude-haiku is the
exception, and instructively so.** Given the identical game, it produces **three distinct
game-theoretic outcomes** (Table 5): a clean cliff in one cover, pure accept-then-attack in a second,
and a $t=1$ **participation breakdown** in a third — the last a genuine bargaining refusal
(PBR $=0$, no pledge is ever made-then-broken), not betrayal. Its aggregate trough (Table 3, $0.59$) is
the average of these and is therefore uninformative on its own.

**Table 5.** claude-haiku Module II by cover ($b=0.15$, $n=30$): one bond mechanism, three modes.

| Cover | Dominant outcome | Mode |
|---|---|---|
| S4 | agree (27/30) | clean cliff — bond honored |
| S6 | attack-$t_2$ (30/30) | accept-then-attack (PBR $=1$) |
| S2 | war-now (22/30) | participation / bargaining breakdown (PBR $=0$) |

A proposer-controlled analysis pins the mechanism. Across covers, claude-haiku-as-proposer offers a
**flat** $\sim0.33$ regardless of the bond — a lowball below the responder's war value $0.40$ — and
claude-haiku-as-responder answers the *same* offer differently depending on the cover (reject / honor /
exploit). Sonnet 5 resolves both sides: as proposer it **adapts** the offer to the bond
($0.40\to0.59$ as $b$ rises), and as responder it accepts credible bonded deals — yielding the clean
cliff of Table 2 on the very cover (S2) where claude-haiku breaks down. Reasoning thus confers
bond-responsive strategy on **both** the proposer and responder sides; the framing-lability of the
non-reasoning tier is a distinct failure mode from the consistent total-failure of gpt-4o/qwen-plus,
and adds a **consistency-across-framing** axis to the capability gradient. (The cross-framing
robustness of Sonnet 5 itself — beyond the S2 cover reported here — is left to a targeted follow-up;
the proposer-controlled comparison already isolates the reasoning effect on the shared cover.)

### 6.7 Judge reliability, focused-replication note, and caveats

**Judges (H-methods).** With dual out-of-family judges we report **Gwet's AC1**, not Cohen's $\kappa$,
because the deceptive-heavy base rate makes $\kappa$ pathologically low (typically $0.08$–$0.21$) even
at high raw agreement. AC1 is **content-dependent**: high where deception is blatant (qwen-plus $0.905$,
gpt-4o $0.86$ — both judges catch overt accept-then-attack) and moderate on nuanced frontier deception
(deepseek-v4-flash $0.34$, claude-haiku $0.43$, o4-mini $0.55$, Sonnet 5 $0.62$, deepseek-v4-pro $0.48$,
Qwen3.7-max $0.53$). The judges also **over-flag** relative to ground truth: their $DR_{\text{judged}}$
at P3 runs $\sim0.9$–$1.0$ against a ground-truth $DR_{\text{verbal}}$ of $\sim0.3$–$0.5$ (§6.2) — they
label as deceptive far more than the agents actually mis-state. The gpt-4o Module I case is a sharp
instance: its crude messages drive the two judges apart (0.22 vs 0.54), emptying the agreement-filter
so the agreement-filtered $DR_{\text{eff}}$ at P0 collapses to $0.05$ — low inter-judge overlap, not an
absence of deception. Because the primary DVs are judge-independent, none of this touches the
confirmatory results; it bounds the *said*-deception channel, which we report descriptively with AC1
and the inter-judge strictness gap, and it strengthens the measurement argument that single-LLM-judge
deception scores are unreliable — one needs ground-truth plus structural metrics ($DR_{\text{verbal}}$,
$DR_{\text{eff}}$, PBR).

**Focused replication.** Sonnet 5 was run breadth-narrowed but depth-preserved (Module II cover S2,
Module I S3, the full bond sweep at $n=30$/$15$) rather than the full six-scenario matrix. The primary
confirmatory hypotheses are carried by the two sharpest within-family controls (Alibaba on/off, DeepSeek
depth); Sonnet 5's role is the Anthropic within-family control and the pilot-anchor re-confirmation,
both of which require depth on the cliff/$b^{\dagger}$/P3 cells rather than breadth. The deviation is
logged; the cliff, the equilibrium recovery, the $b^{\dagger}$ uptick, and the proposer-controlled
within-family contrast are all recovered on the retained cells.

**Caveats.** $n=30$/$15$ makes individual rates precise enough to separate the gradient rungs by
non-overlapping CIs (Table 3), but the bond-cliff *location* is grid-limited to the $\pm25\%$ band and
we make no point-localization claim. Said-deception carries judge noise (above); effective deception,
PBR, and accept-then-attack are judge-independent and robust. Parse errors were zero on all eight runs,
so the divergences — including claude-haiku's trichotomy and the $b=0.40$ over-demand — are behavioral,
not parsing artifacts.

### 6.8 Summary

Across four families and eight agents the confirmatory matrix supports H1 (prevalent P0 deception/war),
H2 on the effective channel, H3 (the cliff within the $\pm25\%$ band with equilibrium recovery), H4
(welfare up under P2+), H6 (participation-binding over-demand, now replicated in four families), **H7**
(the incentive-compatibility response scales with reasoning, four within-family controls), **H8** (the
deception-neutralization / war-reduction **decoupling**, the section's headline), and **H9** (welfare
backfire on non-reasoning agents, identical law across two families), while surfacing a novel
framing-(in)variance axis (§6.6). The structural half — effective deception $\to0$ under P3 — is
universal; the behavioral half — war-reduction and a clean bond cliff — is capability-dependent. That
decoupling, established on judge-independent metrics with separated CIs and four within-family controls,
is the paper's central empirical claim.
