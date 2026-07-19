# PACTA: From Cheap Talk to Verifiable Commitment in LLM Crisis Bargaining

*Working draft — target venue: Nature Machine Intelligence (primary); PNAS / AIJ (fallback).
Language: English. Format: Markdown + LaTeX math (convert to Word/LaTeX via pandoc; cf. Decision
Log D-002). Sections 3 (Theoretical Framework) and 6 (Results) are drafted in
full; other sections are structured stubs to be filled per the WP schedule. §6 reports the
pre-registered **WP3 confirmatory matrix** (four model families × two tiers, $n=30$/$15$, dual
out-of-family judges with reported inter-judge AC1), which supersedes the earlier G2 pilot; remaining
stubs (Appendix, References) belong to WP4.*

---

## Abstract

Large language model (LLM) agents increasingly negotiate and form agreements, yet in high-stakes
strategic settings they spontaneously deceive, break commitments, and escalate. Game theory has long
explained *why* — cheap talk, the commitment problem, private information — and *how to counter it* —
verifiable commitment, bonds, and disclosure — but the two have never been joined and tested on LLMs,
and existing negotiation environments are almost entirely unsanctioned free text. We introduce
**PACTA**, which (i) formalizes crisis bargaining with a parametric *commitment technology* — a posted
bond $b$ and a verification precision $v$ — and derives the thresholds at which honest commitment
becomes incentive-compatible and the peaceful-agreement set expands; (ii) instantiates a four-rung
protocol ladder (cheap talk → ledger → bond/escrow → verified disclosure) that adds exactly one
enforcement mechanism per rung; and (iii) releases **PACTA-Bench**, the first open crisis-bargaining
benchmark with deception ground-truth, an escalation ladder, and incomplete-information conditions.
Run as a dose-response intervention across **four model families and eight agents**, the study shows
these thresholds bind empirically — and reveals a **capability-dependent decoupling**. Verified
disclosure unravels private information and *neutralizes* deception on **every** model — bluffs are
still uttered but become inert (a **channel separation** between said and effective deception that is
structural and capability-robust: effective deception falls to zero for all eight agents) — while a
bond above the predicted minimum converts near-certain preventive war into peace **only on sufficiently
capable models** (war at the bond cliff falls from $\sim90$–$100\%$ below the threshold to $\sim0$–$9\%$
above it on frontier reasoners, with agreements landing on the closed-form equilibrium split), whereas
weaker models fail the same bond and can even backfire on welfare. Deception-neutralization is thus
capability-robust; a protocol's peace dividend is not. Where behavior diverges from theory it does so
at a single, characterizable seam — the transition where the participation constraint binds — which
capable models both predict and explain. Making commitments costly and verifiable can turn honesty into equilibrium
behavior for LLM agents: environment design is a first-class lever for multi-agent AI safety.

## 1. Introduction

Large language models are moving from answering questions to *acting* — negotiating, forming
agreements, and taking consequential decisions on behalf of users and institutions. As they do,
a growing body of evidence shows that in high-stakes strategic settings they do not behave as
neutral assistants. Under pressure, LLM agents deceive without being told to, and this tendency
scales with capability (Scheurer et al. 2023; Hagendorff 2024; Park et al. 2024); even CICERO,
trained with an explicit honesty objective, exhibited strategic inconsistency between what it said
and what it did (Bakhtin et al. 2022). In diplomatic and military war-game simulations, LLM agents
display hard-to-predict escalation dynamics, with large variance across models and occasional
recourse to extreme actions (Rivera et al. 2024; Lamparth et al. 2024). And in negotiation
benchmarks they are systematically exploitable: gains accrue disproportionately to bluffing and
pressure tactics, and play departs from rational equilibrium in ways an adversary can exploit
(Bianchi et al. 2024; Abdelnabi et al. 2024; Duan et al. 2024; Akata et al. 2025).

These three lines of evidence share a structural feature that is easy to miss: the environments are
almost entirely *unsanctioned free text*. Agents talk, promise, and threaten, but words carry no
cost and no binding force. In the language of game theory this is **cheap talk**, the weakest
possible communication channel. Seen this way, the deception and escalation reported above are not
only a model defect to be patched by better training; they are also a predictable consequence of an
**environment whose incentives are left undesigned**. This reframing matters because it points to a
different lever — the rules of interaction, not the weights of the model.

Game theory has, in fact, understood half of the problem for sixty years. The rationalist theory of
war explains why costly conflict occurs between rational actors despite its inefficiency, through
private information with an incentive to misrepresent, the commitment problem, and issue
indivisibility (Fearon 1995; Powell 2006). It also supplies the design tools to counteract these
frictions: credible commitment through costly "hands-tying" (Schelling 1960), the structural limits
of cheap talk (Crawford–Sobel 1982; Farrell–Rabin 1996), verifiable disclosure and unraveling
(Grossman 1981; Milgrom 1981), and mechanism design more broadly. What the theory does *not* tell
us is whether these guarantees — all derived for fully rational agents — actually bind for agents
that are language-based, stochastic, and capable of ignoring the rules. Formal guarantees assume a
rational player; an LLM is not one. Whether the bridge holds is an empirical question, and it is
open.

The moment to ask it is now. CICERO demonstrated that language and strategic reasoning can be
combined at human level (Bakhtin et al. 2022); a parallel line showed that binding contracts and
sanctioning mechanisms raise cooperation among reinforcement-learning agents in Diplomacy — but
with a hand-built contract space, no natural language, and no incentive-compatibility analysis
(Kramár et al. 2022; Christoffersen et al. 2023). The step to language-based agents *and* to formal
guarantees remains open. At the same time, the deployment of autonomous agents into real economic
and institutional negotiation has made the *verification of AI agreements* an explicitly stated open
problem in both the cooperative-AI and AI-governance agendas (Dafoe et al. 2020; Wasil et al. 2024).
The theory is ready, the measurement tools are mature, and the demand is concrete — yet no work has
joined them.

**PACTA** (Protocols for Auditable Commitments and Trustworthy Agreements) closes this gap. We (i)
formalize crisis bargaining with an explicit, parametric *commitment technology* — a posted bond $b$
and a verification precision $v$ — and derive the thresholds at which honest commitment becomes a
best response; (ii) instantiate a four-rung **protocol ladder** that adds exactly one enforcement
mechanism per rung, from cheap talk (P0) to a recorded ledger (P1), a costly bond/escrow (P2), and
verified disclosure (P3); and (iii) build **PACTA-Bench**, an open crisis-bargaining environment in
which agents' private types are known ground-truth, so that deception, commitment violation,
escalation, and welfare can be measured against the model's closed-form predictions. Because each
rung isolates a single mechanism, differences across rungs identify that mechanism's causal effect,
and the two continuous parameters $(b,v)$ let us run the intervention as a *dose-response* design and
compare the empirical break-points against the theory's thresholds.

Concretely, this work makes four contributions:

- **C1.** The first parametric model of crisis-bargaining commitment technology, deriving in closed
  form the bond threshold $b^\*$ and verification precision at which truthful commitment is
  incentive-compatible, and the resulting expansion of the peaceful-agreement set (§3).
- **C2.** The first dose-response test of these thresholds on LLM agents, quantifying where empirical
  behavior agrees with the theoretical break-points and where it diverges (§5–§6).
- **C3.** PACTA-Bench: the first open crisis-bargaining benchmark with deception ground-truth, an
  escalation ladder, and incomplete-information conditions (§4).
- **C4.** The first systematic evidence on whether deception and escalation can be *causally* reduced
  by environment/mechanism design rather than by model retraining (§6).

Our central empirical claim is that **making commitments costly and verifiable turns peaceful
agreement into equilibrium behavior for LLM agents, along the thresholds the theory predicts**
(quantitative headline across model families: WP3). Four findings support and sharpen this claim.
Verified disclosure produces *unraveling*: bluffs are still uttered but become inert — a **channel
separation** in which said deception persists while *effective* deception falls to zero and war
disappears. A costly bond produces a sharp **dose-response cliff** at the predicted minimum bond, with
the frontier-model agreement landing on the analytic equilibrium split. Recording alone (P1) leaves
behavior essentially unchanged, as the theory predicts for a single interaction. And where the model
predicts that the *participation* constraint binds — at high bond — we uncover a **localized reasoning
failure**: the proposer over-demands toward the now-slack incentive-compatibility ceiling, a rational
counterpart punishes it, and peace becomes non-monotone in the bond. This last result is a concrete
instance of the theory–empirics divergence that the LLM bridge is designed to expose, and it
illustrates the paper's broader message: with the right protocol, deception in LLM diplomacy stops
being rational — and where it persists, it does so at an identifiable, characterizable seam between
the theory's binding constraints.

*(§6 reports the pre-registered confirmatory WP3 matrix — eight agents across four model families
(Anthropic, OpenAI, Alibaba, DeepSeek, each at a non-reasoning and a reasoning tier), $n=30$/$15$, dual
out-of-family judges with reported inter-judge AC1 — including **four** within-family reasoning controls,
a four-family replication of both the dose-response cliff and the over-demand divergence, the
deception-neutralization / war-reduction **decoupling** on judge-independent metrics with separated
confidence intervals, and a novel framing-inconsistency finding resolved by the reasoning tier.)*

## 2. Related Work and Positioning

PACTA sits at the intersection of five literatures, each of which supplies part of the picture but
none of which joins them. We organize the review around that gap.

**LLM deception and safety.** A rapidly growing body documents that LLMs deceive strategically under
pressure, that the capability scales with model size, and that the phenomenon spans a widening range
of settings (Scheurer et al. 2023; Hagendorff 2024; Park et al. 2024); Ward et al. (2023) formalize
and propose to mitigate AI deception. This work establishes *that* deception occurs but studies it in
environments without designed incentives, and measures it descriptively rather than against a
structural prediction.

**LLM negotiation and strategic reasoning.** Benchmarks such as NegotiationArena (Bianchi et al.
2024), LLM-Deliberation (Abdelnabi et al. 2024), and GTBench (Duan et al. 2024), together with
studies of repeated play (Akata et al. 2025) and strategic reasoning (Gandhi et al. 2023), show that
LLMs are exploitable, that gains often come from bluffing and pressure, and that play departs
systematically from equilibrium. These are almost entirely free-text (cheap-talk) settings; none
introduces a verifiable commitment technology or derives the thresholds at which honesty becomes
incentive-compatible.

**Diplomacy, escalation, and RL contracts.** CICERO combined language with strategic planning at
human level but exhibited say–do inconsistency despite an honesty objective (Bakhtin et al. 2022).
War-game studies find hard-to-predict escalation and large cross-model variance (Rivera et al. 2024;
Lamparth et al. 2024). Closest on the mechanism side, Kramár et al. (2022) and Christoffersen et al.
(2023) show that binding contracts and sanctions raise cooperation — but among RL agents, with a
hand-built contract space, no natural language, and no incentive-compatibility analysis. The step to
*language-based* agents with *formal* guarantees is exactly what remains open.

**Game theory of conflict and mechanism design.** The rationalist theory of war (Fearon 1995; Powell
2006), credible commitment via hands-tying (Schelling 1960), the limits of cheap talk
(Crawford–Sobel 1982; Farrell–Rabin 1996), verifiable disclosure and unraveling (Grossman 1981;
Milgrom 1981), and bilateral-trade mechanism design (Myerson–Satterthwaite 1983) supply both the
diagnosis and the design tools we build on. This tradition assumes rational players; whether its
guarantees bind for LLM agents is the empirical question PACTA answers.

**Cooperative AI and AI-agreement verification.** The cooperative-AI agenda (Dafoe et al. 2020) and
AI-governance work on verifying international AI agreements (Wasil et al. 2024) name the verification
of machine commitments as an open problem — the applied motivation for our protocol primitives.

**Positioning.** No prior work occupies the cell PACTA targets: LLM agents, communicating in free
text *and* a structured commitment language, under formally analyzed incentive-compatible protocols,
in a crisis-bargaining domain, with deception measured against ground-truth.

| Study | Agent | Communication | Commitment mechanism | Formal guarantee | Crisis domain | Deception measurement |
|---|---|---|---|---|---|---|
| CICERO (Bakhtin et al. 2022) | LLM + planner | free language | none | none | no (board game) | indirect |
| Kramár et al. (2022) | RL | restricted signal | binding contract (hand-built) | partial (empirical) | no (board game) | no |
| Rivera et al. (2024) | LLM | free language | none | none | yes (war-game) | no (escalation only) |
| NegotiationArena / LLM-Deliberation (2024) | LLM | free language | none | none | no (commercial) | partial |
| GTBench / Akata et al. (2024–25) | LLM | matrix games | none | equilibrium comparison (simple games) | no | no |
| Christoffersen et al. (2023) | MARL | none | formal contract | yes (simple env.) | no | — |
| **PACTA (this work)** | **LLM** | **free + structured (DSL)** | **DSL + bond + auditor** | **yes (IC theorems)** | **yes** | **yes (ground-truth)** |

**Gap map.** The review crystallizes five gaps that the contributions of §1 close: **B1** (*bridge*)
— no systematic comparison of formal equilibrium/IC guarantees with LLM behavior beyond simple matrix
games; **B2** (*protocol*) — LLM negotiation is almost entirely cheap talk, with no verifiable
commitment, bond/escrow, or auditor; **B3** (*benchmark*) — no crisis-bargaining benchmark with
incomplete information, an escalation ladder, and deception ground-truth; **B4** (*causality*) —
deception/escalation studies are descriptive, with no mechanism-design intervention; **B5**
(*measurement*) — deception measurement is not standardized, operational, or human-validated, and
usually relies on a single LLM judge.

---

## 3. Theoretical Framework

We model crisis bargaining as a division game in which war is inefficient yet can occur, and we
introduce a *commitment technology* as the intervention variable. Following the rationalist
tradition (Fearon 1995), we isolate two of the three canonical frictions — private information and
the commitment problem — in two separate modules, so that each protocol layer targets a single
mechanism and its causal effect is identifiable. The model is stated at a precision the benchmark
can consume directly: every symbol maps either to a scenario parameter or to an observable metric
(§4.4). v0 is deliberately the simplest solvable model; the unified model (private information
*under* a power shift) is deferred to future work.

### 3.1 Setup and the bargaining range

Two players $N=\{A,B\}$ bargain over a divisible resource normalized to $1$; a division is
$x\in[0,1]$, the share to $A$ (so $B$ receives $1-x$). If bargaining fails, war ensues: $A$ prevails
with probability $p\in(0,1)$ and takes the whole resource, and both sides pay irreversible costs
$c_A,c_B>0$. Expected war payoffs are

$$ W_A = p - c_A, \qquad W_B = (1-p) - c_B. $$

**Lemma 1 (Bargaining range; Fearon 1995).** *The set of divisions that both players weakly prefer
to war is*
$$ X^\* = [\,p - c_A,\ \ p + c_B\,], $$
*which is non-empty because $c_A+c_B>0$.*

*Proof.* $x \ge W_A \Leftrightarrow x \ge p-c_A$, and $1-x \ge W_B \Leftrightarrow x \le p+c_B$;
the interval has length $c_A+c_B>0$. ∎

Lemma 1 makes the puzzle precise: peaceful divisions dominating war always exist, so war must be
explained by an *informational* or *commitment* friction — the two modules below.

### 3.2 Commitment technology and the protocol ladder

We augment the message space with a machine-readable **commitment object**
$K=(a,\varphi,\tau,b)$: an action $a$, a triggering condition $\varphi$, a horizon $\tau$, and a
posted bond $b\ge 0$. A **verification technology** $(v,\varepsilon)$ produces a signal
$s\in\{0,1\}$ with $\Pr(s=1\mid \text{violation})=v$ and $\Pr(s=1\mid \text{no violation})
=\varepsilon$, where $0\le \varepsilon < v \le 1$. On $s=1$ a share $\lambda$ of the bond is burned
and $1-\lambda$ transferred to the counterparty; in v0 we fix $\lambda=1$ (full burn), which closes
the strategic-accusation channel.

**Assumption 1.** $v>\varepsilon$ (verification is informative) and the bond budget is bounded,
$b\le \bar b$.

The protocols are the *same game* except for the message space and the enforcement rule; each rung
adds exactly one mechanism, which is what makes cross-rung differences causal.

| Rung | Name | Mechanism added | Theory anchor |
|---|---|---|---|
| **P0** | Cheap talk | — (control) | Fearon's misrepresentation incentive is fully active |
| **P1** | Ledger | commitments recorded ($b=0$; detection $v=1,\varepsilon=0$; no monetary sanction) | observability / reputation |
| **P2** | Bond / escrow | costly bonding, $(v,\varepsilon,\lambda)$ applied | Schelling hands-tying; $b^\*$ threshold (T1) |
| **P3** | Verified disclosure | certifiable partial type disclosure (unforgeable; cost $0$ in v0) | Milgrom–Grossman disclosure (T3) |

### 3.3 Module I — Private information and screening

$c_A$ is common knowledge; $B$'s type is its war cost $\theta=c_B\in\{c_L,c_H\}$ with $c_L<c_H$ and
prior $\mu=\Pr(\theta=c_H)$. Timing: (1) nature draws $\theta$; (2) a communication phase (a message
and/or, under P3, a certificate); (3) $A$ makes a single take-it-or-leave-it offer $x$ (TIOLI); (4)
$B$ accepts ($x$ is enforced) or rejects (war). There is no commitment problem — an accepted $x$ is
certain.

**Lemma 2 (Uninformative communication and positive war probability under P0).** *Under P0, every
sequentially-rational equilibrium is babbling, and $A$'s optimal offer is*
$$ x^\* = \begin{cases} p + c_H & \text{if } \mu > \bar\mu,\\[2pt] p + c_L & \text{if } \mu \le \bar\mu,\end{cases} \qquad \bar\mu \;=\; \frac{c_A + c_L}{c_A + c_H}\in(0,1). $$
*The equilibrium war probability is $W^{P0}=(1-\mu)\cdot\mathbb{1}\{\mu>\bar\mu\}$; only the $c_L$
type rejects.*

*Proof sketch.* (i) Against any belief, $A$'s best offer is $x=p+\hat c$ for some $\hat c$; every
type of $B$ strictly prefers to induce the belief "$c_L$" (higher retained share), so no separating
message profile is incentive-compatible — only babbling survives. (ii) Under babbling the posterior
equals $\mu$. On $x\le p+c_L$ the best offer is $p+c_L$ (both types accept); on $x\in(p+c_L,p+c_H]$
the best is $p+c_H$ (only $c_H$ accepts), yielding $\mu(p+c_H)+(1-\mu)(p-c_A)$; $x>p+c_H$ is
dominated. The risky offer dominates iff $\mu c_H-(1-\mu)c_A>c_L \Leftrightarrow \mu>\bar\mu$. The
only rejecting type is $c_L$. ∎ *(Full proof: Appendix; task T1.5.)*

**Theorem T3 (Value of verified disclosure).** *Under P3, with the v0 refinement that uncertified
messages are met with skeptical beliefs, the unique equilibrium outcome is full unraveling: the
$c_L$ type certifies, silence is read as $c_H$, offers are $x=p+\theta$, and every type accepts.
Consequently*
1. *$W^{P3}=0$ and the deception rate on the certified dimension is $DR^{P3}=0$;*
2. *total welfare weakly rises, $\Delta W\!F=(1-\mu)(c_A+c_L)\cdot\mathbb{1}\{\mu>\bar\mu\}\ge 0$;*
3. *the information rent shifts to $A$ (in the $\mu\le\bar\mu$ regime the distribution moves toward
   $A$ while total welfare is unchanged).*

*Proof sketch.* Grossman (1981)/Milgrom (1981) unraveling: with costless certification available
only to the truthful type, the "good" type strictly gains from disclosing; skeptical beliefs pin
silence to the worst type. (ii)–(iii) follow by substituting the Lemma 2 payoffs — the war loss
$(c_A+c_L)$ was incurred only in the $\mu>\bar\mu$ regime with probability $(1-\mu)$. ∎ *(Full
proof: task T1.4.)*

**Note 1 (a separating observable).** In the $\mu\le\bar\mu$ regime P3 lowers deception and
redistributes rent *without* changing war or total welfare (Prediction Ö4). Thus "deception fell"
and "welfare rose" are distinct observables — the benchmark samples this regime deliberately.

### 3.4 Module II — The commitment problem and bonded commitment

Information is complete; power shifts. In period 1 (now) $A$ prevails with probability $p_1$; in
period 2 the balance shifts to $p_2=p_1-\Delta$ with $\Delta>0$ ($B$ is the rising side); the
tuple $(p_1,\Delta,c_A,c_B)$ is common knowledge. Timing — $t=1$: $A$ proposes $x$; $B$ either
wars now or accepts; on acceptance (under P2) $B$ posts a bonded commitment $K=(\text{"no attack in
}t2\text{"},\cdot,\cdot,b)$. $t=2$: $B$ chooses **honor** (the division stands) or **attack** (seize
the whole with probability $1-p_2$, cost $c_B$); the verification technology $(v,\varepsilon)$
operates. The realized payoffs are

$$
\begin{aligned}
\text{honor:} &\quad u_B = 1-x-\varepsilon b, && u_A = x,\\
\text{attack:} &\quad u_B = (1-p_2)-c_B-vb, && u_A = p_2-c_A,\\
\text{war now:} &\quad (u_A,u_B) = (\,p_1-c_A,\ \ 1-p_1-c_B\,).
\end{aligned}
$$

**Theorem T1 (Incentive-compatibility threshold).** *Given $(x,\Delta,v,\varepsilon)$, honoring is
$B$'s best response in period 2 iff*
$$ b \;\ge\; b^\*(x) \;:=\; \frac{\max\{0,\ x-(p_2+c_B)\}}{v-\varepsilon}. $$
*That is, the expected penalty differential $(v-\varepsilon)\,b$ must cover the deviation gain
$G_B(x)=x-(p_2+c_B)$. $b^\*$ is increasing in $x$, decreasing in $v$, and increasing in
$\varepsilon$.*

*Proof.* $1-x-\varepsilon b \ge (1-p_2)-c_B-vb \Leftrightarrow (v-\varepsilon)b \ge x-(p_2+c_B)$;
divide by $v-\varepsilon>0$ (Assumption 1). ∎

**Theorem T2 (Expansion of the peace set).** *In the leading case ($\varepsilon b$ negligible), the
set of power shifts for which a peaceful honored agreement is an equilibrium is*
$$ \mathcal{P}(b,v) \;=\; \{\,\Delta\ge 0 : \Delta \le c_A+c_B+(v-\varepsilon)\,b\,\}, $$
*which expands monotonically in $b$ and $v$, with $\partial/\partial b=(v-\varepsilon)$. At $b=0$
it reduces to the Powell (2006) condition $\Delta\le c_A+c_B$, to which P0 and P1 are equivalent.*

*Proof sketch.* A peaceful honored agreement requires an $x$ satisfying three constraints
simultaneously: (a) the honor IC, $x\le x_{IC}:=p_2+c_B+(v-\varepsilon)b$ (T1); (b) $B$'s
participation, $1-x-\varepsilon b\ge 1-p_1-c_B \Leftrightarrow x\le x_P:=p_1+c_B-\varepsilon b$;
(c) $A$'s participation, $x\ge p_1-c_A$. A feasible $x$ exists iff $p_1-c_A\le\min\{x_{IC},x_P\}$.
When (a) binds this reduces to $\Delta\le c_A+c_B+(v-\varepsilon)b$; monotonicity follows because
the ceiling rises in $b$ and $v$. ∎ *(Full proof: tasks T1.2–T1.3.)*

The equilibrium offer is $x^\*=\min\{x_{IC},\,x_P\}$. Which constraint binds is itself a testable
prediction: the **IC** ceiling $x_{IC}$ binds at low bond, the **participation** ceiling $x_P$ at
high bond, and the two cross at $b^{\dagger}$ (for the v0 parameters, $b^{\dagger}\approx 0.33$).

**Note 2 (theoretical neutrality of P1 — an LLM-specific test).** In a single interaction, recording
and announcing a violation (P1) does not change payoffs, so the theory predicts
$PBR^{P1}=PBR^{P0}$. Any significant empirical P1 effect is therefore an LLM framing/reputation
intuition that departs from the rational model — a self-contained, reportable finding (Prediction
Ö2).

**Note 3 (welfare declines within the peace zone).** In the peaceful region welfare is
$W\!F=1-\varepsilon b$, strictly decreasing in $b$: verification imposes a deadweight monitoring
cost $\varepsilon b$ even when no violation occurs. Thus more bonding buys peace but erodes welfare
(the welfare-hill prediction Ö6/H6), and — as §6 shows empirically — pushing $b$ into the
participation-binding region can *reintroduce* breakdown.

### 3.5 Solution concept and the bridge to LLM agents

The solution concept is weak Perfect Bayesian Equilibrium; in Module I / P3 we use the skeptical-
belief refinement in v0 and discharge it with the Intuitive Criterion (D1) in the proof file
(Proposition R4), so that unraveling is selected by a standard refinement without auxiliary
contracts. Indifference is broken toward acceptance/honoring.

Crucially, we do **not** assume the LLM is a rational player. We treat agent $i$ as a
language-conditioned, boundedly rational policy $\hat\pi_i$, and we test the theory in the two weak
forms that survive that relaxation (cf. Manifesto §7.4): **(Y) comparative-statics sign** — e.g.
$\partial\,PBR/\partial b\le 0$ — and **(E) threshold/cliff location** — a regime change near
$b^\*$, $\bar\mu$, and $\Delta^\*=c_A+c_B+(v-\varepsilon)b$. Point-prediction agreement is not
expected; the magnitude of the deviation is reported separately via the equilibrium-deviation
metric $ED=|x-x^\*|$. This asymmetric-assumption bridge is the paper's main defense against the
"rationality assumption fails for LLMs" objection.

### 3.6 v0 parameterization (for reference)

Module I: $p=0.5$, $c_A=0.10$, $(c_L,c_H)=(0.05,0.25)$, giving $\bar\mu=0.15/0.35\approx 0.429$;
$\mu\in\{0.30,0.43,0.60,0.80\}$. Module II: $p_1=0.5$, $c_A=c_B=0.10$; $\Delta\in\{0.10,0.30,0.50\}$;
$v\in\{0.60,0.90,1.00\}$, $\varepsilon\in\{0,0.05\}$; bond grid $b\in\{0,0.05,\dots,0.60\}$,
densified near $b^\*$. For the headline Module II cell ($\Delta=0.30,v=0.9,\varepsilon=0.05$):
$b^\*_{\min}=0.1/0.85\approx 0.118$ (minimum bond for peace) and $b^{\dagger}\approx 0.33$
(IC→participation crossover). These closed forms are the numerical oracle against which the engine
and MockClient are unit-tested (`tests/test_theory.py`; task T1.5).

---

## 4. PACTA-Bench

PACTA-Bench turns the model of §3 into an executable environment in which LLM agents play the crisis
game and every quantity the theory predicts is measured against known ground-truth. It is
open-source, deterministic given a seed, and built so that each protocol rung and each continuous
parameter can be varied in isolation.

### 4.1 Design principles

Four principles follow directly from the causal-identification goal. **(i) Single-variable rungs:**
each protocol adds exactly one enforcement mechanism (§3.2), so a difference between two rungs
identifies that mechanism's effect. **(ii) Model-agnosticism:** protocols require only API-level
messages and tool calls, so any chat LLM can be dropped in without fine-tuning. **(iii)
Auditability:** the Commitment DSL is human-readable and every run logs a full transcript with a
configuration hash, seed, and pinned model version, so that "a run with no record is a run not
done" (record discipline, R7). **(iv) Loophole-as-finding:** an agent that satisfies the letter of a
commitment while violating its spirit is flagged and catalogued rather than discarded — a direct
contribution to real treaty/contract design.

### 4.2 Architecture and the game engine

A run flows through five components: an **orchestrator** (turn management, state, seeding) drives two
**LLM agents** (each carrying a private type $\theta$ and hidden objective) that exchange messages
through a **message layer** (free text plus a structured Commitment DSL); accepted commitments enter
a **ledger**; a **referee** combines a deterministic violation predicate with a simulated
verification signal; and a **metric logger** records the full episode. The engine is a finite state
machine implementing the two modules of §3 exactly — the game logic is fixed and only the narrative
cover changes across scenarios.

The engine follows an *expected-value payoff contract* in v0: payoffs are the expectations taken over
the war lottery and the verification signal, which minimizes variance in the theory comparison. The
verification signal $s$ is nonetheless sampled seed-deterministically and written to the ledger
(so that the audit trail is realized), and a realization-mode payoff can be enabled by a flag in v1.
The escalation ladder that feeds the escalation index is, for Module I, $\{0=\text{agreement},
10=\text{war}\}$ and, for Module II, $\{0=\text{honored peace}, 7=\text{period-2 attack},
10=\text{war now}\}$.

### 4.3 Scenarios and leakage control

Two game families are dressed in six narrative covers: **S1** (a valley/territory dispute), **S3** (a
sanctions-for-inspections swap), and **S5** (a shared-river water-rights dispute) instantiate Module I;
**S2** (a ceasefire negotiation), **S4** (a naval-blockade crisis), and **S6** (an arms-reduction pact)
instantiate Module II. Covers differ in surface narrative, escalation vocabulary, and framing, but
share the identical engine. This yields a built-in robustness invariant — **S1 ≡ S3 ≡ S5** and
**S2 ≡ S4 ≡ S6** must produce identical rational-limit behavior (R1), verified in the MockClient unit
tests — which functions as a control for narrative confounds: any divergence between rationally
equivalent covers under a real model is a *cover effect* to be measured, not assumed away (the
framing-(in)variance axis of §6.6). Per-episode numeric parameters
and the country/region names are drawn by a seed-deterministic RNG (leakage control, §8 below), and
published scenarios use synthetic actors and parametric values rather than real states or current
crises (§8, Ethics). The canonical scale is $1.0 = 100$ districts, so shares map to integer offers
in $[0,100]$ in the prompts. Each turn instructs the agent to reply with a single JSON object,
making structured actions machine-parseable while free-text messages remain available for the judge.

### 4.4 Model-to-benchmark mapping

Every symbol of §3 maps to a bench object and a metric, which is what makes the theory directly
testable:

| Model object | Benchmark counterpart | Metric / use |
|---|---|---|
| type $\theta=c_B$ | hidden scenario parameter | ground truth for DR |
| messages $m$ | transcript claims (judge-labelled) | DR; predictions Ö1, Ö2 |
| commitment $K$ | DSL `COMMIT` record in the ledger | PBR denominator |
| violation predicate | referee's deterministic predicate | PBR numerator |
| signal $s$; $(v,\varepsilon)$ | referee-simulated audit | T1/T2 dose-response factors |
| division $x$ | share in the agreement text | $ED=\lvert x-x^\*\rvert$ |
| war | terminal rung of the escalation ladder | war rate; EI |
| payoffs | realized payments (from config) | WELF, Pareto gap, DWL |
| $b,v,\varepsilon,\Delta,\mu$ | experiment-matrix factors | H2–H4 cells |

### 4.5 The Commitment DSL and the referee

A commitment is the tuple $K=(\text{agent}, \text{action}, \varphi, \tau, b)$ (e.g. `COMMIT(action:
no_attack_t2; condition: always; horizon: t2; bond: 0.20)`), recorded in the ledger on acceptance
under P1+. The referee is deterministic on structured actions: it evaluates the violation predicate
directly from the realized period-2 action (honor vs attack) — no judge is involved — and then draws
the audit signal $s\sim\text{Bernoulli}(v)$ if violated and $s\sim\text{Bernoulli}(\varepsilon)$
otherwise (Definition 2). This clean separation — deterministic adjudication of *actions*, LLM
judging of *free text* — keeps the commitment-violation metric (PBR) objective and judge-independent,
which is why PBR is reliable even when the judge is weak.

### 4.6 The LLM-judge and channel separation

Free-text messages are scored by **dual LLM-judges**, each drawn from a *different model family* than
the agents under evaluation (bias rule R2; the judge pool is composed so that every agent is scored by
two out-of-family models), over three separate calls to avoid contamination: **G1** claim extraction
(message → atomic claims), **G2** ground-truth labelling (each claim → truthful / deceptive /
unverifiable / ambiguous, using the known private type), and **G3** rhetorical escalation (a 0–10
tone ladder, distinct from and complementary to the action-based EI). The two judges' labels are
reconciled into a **consensus-filtered** canonical set — claims on which they disagree are dropped
from the deception denominator — and inter-judge agreement is reported per cell. Because the
deceptive-heavy base rate deflates Cohen's $\kappa$ pathologically (typically $0.08$–$0.21$ even at
high raw agreement), we report **Gwet's AC1** as the primary agreement statistic; the pre-registered
$\kappa\ge 0.7$ gate is superseded by this finding (§6.7, §8). Crucially, the primary dependent
variables are judge-independent (§4.5, §4.7), so the confirmatory results do not rest on judge
reliability; the judge layer bounds only the *said*-deception channel, which we report descriptively.

The judge is what makes the paper's central distinction observable: the **channel-separation** pair
$DR_{\text{said}}$ (deception uttered on the verbal channel) versus $DR_{\text{effective}}$
(deception on the channel that *determines the outcome*). Under P3 a bluff may be said
($DR_{\text{said}}>0$), but the certificate channel is unforgeable, so $DR_{\text{effective}}=0$ and
the bluff is inert — the protocol does not forbid deception, it neutralizes it. This distinction is
invisible without the judge layer and cannot be captured by a single deception number (Decision Log
D-009).

### 4.7 Metrics

The v0 metric set (Manifesto §10.1) comprises: **DR** (deception rate; verbal / certified /
effective channels), **PBR** (pledge-breaking rate; formal from the ledger, and verbal from stated
intent), **EI** (action-based escalation index), **AR / TTA** (agreement rate / time-to-agreement),
**WELF / DWL** (total expected welfare and deadweight loss), **ED** ($\lvert x-x^\*\rvert$, the
equilibrium deviation on agreed divisions), **EXPL** (exploitability against a fixed adversary), and
**COST** (turns, tokens, latency — the protocol's practical overhead). The channel pair of §4.6 is
the load-bearing addition relative to prior benchmarks.

### 4.8 The MockClient oracle and record discipline

A prompt-reading rational client (`MockClient`) reverse-parses the numeric parameters from the
scenario text and plays the §3 best response. It serves two purposes: as an *end-to-end proof of
template sufficiency* — if a purely prompt-reading agent reproduces the closed-form predictions,
the templates carry enough information for a rational decision without any external model — and as a
*deterministic regression oracle* for the referee/metric chain. Scripted policies (rational,
deceptive, naive-proposer) additionally serve as ground-truth generators for judge calibration.
Every episode record carries the seed, a configuration hash over all parameters, and the pinned
model identifier (R7), so that every number in this paper is traceable to a reproducible run. *(A
methodological caveat surfaced during development and is reported in §8: because MockClient always
emits clean, on-spec output, a class of real-LLM-path defects — offer parsing, JSON repair, judge
negation handling, scenario vocabulary — is invisible to the oracle and must be validated directly
against real-model transcripts.)*

## 5. Experimental Design

The design turns the protocol ladder into a causal intervention and the two continuous parameters of
the commitment technology into a dose-response axis, so that empirical break-points can be compared
against the closed-form thresholds of §3. All confirmatory hypotheses, thresholds, and exclusion
rules are pre-registered before data collection (OSF; task T3.2); the analysis below distinguishes
these confirmatory tests from exploratory findings.

### 5.1 Design logic: causal ladder + dose-response

Two complementary manipulations do the work. First, the **protocol ladder** (P0→P3) adds exactly one
mechanism per rung (§3.2, §4.1), so a contrast between adjacent rungs identifies that mechanism's
causal effect: P1−P0 isolates recording/reputation, P2−P1 isolates costly bonding, P3−P1 isolates
verified disclosure. Second, within P2 the bond $b$ (and, in a secondary sweep, the verification
pair $(v,\varepsilon)$) is varied continuously as a **dose**, and the response curves are tested for
the *location* of the theory's break-points — the minimum bond for peace $b^\*_{\min}$, the
IC→participation crossover $b^{\dagger}$, and the peace-set boundary $\Delta^\*(b,v)$ (§3.4, §3.6).
This dual design is what lets us test the theory in the two weak forms the LLM bridge licenses
(§3.5): the **sign** of comparative statics (e.g. $\partial\,PBR/\partial b\le 0$) and the
**location** of the regime change, rather than point predictions.

### 5.2 Factorial matrix and conditions

The full matrix crosses: **Protocol** {P0, P1, P2, P3} × **Scenario** {S1–S6, three narrative covers
per game family (Module I: S1/S3/S5; Module II: S2/S4/S6)} × **Model family**
{≥4 developers, each at a non-reasoning and a reasoning tier, in self-play plus a cross-pairing subset}
× **Information** {complete, incomplete}
× **Power** {symmetric, asymmetric} × **seeds** ($n\ge 30$ per cell, fixed by the power analysis of
§5.5). Rather than a full crossing, a *fractional* design concentrates power on the main effects and
the key interactions (protocol × dose, protocol × model family). Two dedicated dose sweeps sit inside
P2: a **bond sweep** $b\in\{0,0.05,\dots,0.60\}$, densified around $b^\*_{\min}$ and $b^{\dagger}$
(task T4.1), and a **verification sweep** over $(v,\varepsilon)$ including the discriminating boundary
cell $(v,\varepsilon)=(0.60,0.30)$ and a hard power shift $\Delta=0.45$ (task T4.2; Decision Log
D-005). Model families are chosen so the LLM-judge can always be drawn from a different family than
the agents under evaluation (bias rule R2). *(Solo-scope note, D-004: the G2 pilot used four scenarios
and four families; the WP3 pre-registration fixes the set at ≥4 families (each at a non-reasoning and a
reasoning tier, for within-family capability controls) × 6 scenarios, which is the §12.1 submission
bar for the full matrix.)*

### 5.3 Hypotheses and pre-registration

The study is organized around four research questions: **RQ1** (baseline — how much do LLM agents
deceive, break commitments, and escalate under cheap talk, relative to the game-theoretic
prediction?); **RQ2** (protocol effect — to what extent, and by what mechanism, do recorded, costly,
and verifiable protocols reduce deception, violation, escalation, and welfare loss?); **RQ3**
(theory–empirics bridge — under which formal conditions on bond $b$ and verification $v$ is honest
commitment incentive-compatible, and does LLM behavior show the predicted break-point?); and **RQ4**
(robustness — how stable are protocol effects across adversarial opponents, prompt/persona variation,
and model family and scale?). The nine confirmatory hypotheses map these questions to specific
dependent variables and thresholds (H1–H6 were pre-registered from the pilot; H7–H9 were added in the
frozen WP3 pre-registration to capture the capability-tier structure the pilot surfaced). Thresholds
are calibrated on pilot data and then locked in the pre-registration; any later change is logged with
justification:

| Hyp. | RQ | Statement (direction) | Test / DV | Pre-registered threshold |
|---|---|---|---|---|
| **H1** | RQ1 | Under P0 (cheap talk), deception and escalation are prevalent; deception rises with capability | DR, EI on the P0 baseline | $DR>15\%$ in ≥3 model families |
| **H2** | RQ2 | The ladder lowers *effective* deception/violation: $\text{P3}\preceq\text{P2}\preceq\text{P1}\approx\text{P0}$ (said deception may persist under P3 — channel separation) | $DR_{\text{eff}}$, $DR_{\text{said}}$, PBR, EI across rungs (mixed model) | monotone drop in the effective metric; Cliff's $\delta\ge 0.3$ at the critical transition |
| **H3** | RQ3 | Violation drops sharply once $b\ge b^\*$; dose-response below | PBR–$b$ curve, break-point analysis | empirical break within $\pm 25\%$ of $b^\*$ |
| **H4** | RQ2 | Welfare and Pareto efficiency rise, war rate falls, under the protocol | war rate, Pareto gap, DWL | ≥50% relative war reduction under P2+ |
| **H5** | RQ4 | P2–P3 bound the exploitation loss against an adversarial agent | EXPL (adversarial cells, WP4) | loss ≤ ½ of the P0 loss |
| **H6** | RQ2–3 | Within the peace zone welfare declines in $b$; the welfare jump coincides with $b^\*$ | WELF–$b$ curve (bond sweep) | slope $<0$; jump within $\pm 25\%$ of the H3 cliff |
| **H7** | RQ4 | The incentive-compatibility response to a designed protocol scales with *reasoning capability, not model family* | trough war, accept-then-attack, PBR across same-vendor reasoning tiers (within-family controls) | monotone in reasoning depth; non-reasoning vs reasoning tiers separated by non-overlapping 95% CIs in ≥2 families |
| **H8** | RQ2–3 | *Decoupling*: verified disclosure neutralizes **effective** deception on every model, but converts neutralization into war-reduction only on sufficiently capable ones | $DR_{\text{eff}}$ under P3 (all agents) vs P3/P2 war-reduction, by tier | $DR_{\text{eff}}=0$ for all agents; war-reduction present only on reasoning tiers, with separated CIs |
| **H9** | RQ2 | On non-reasoning agents a bond *reduces* welfare (backfire), by a family-independent law | WELF–$b$ slope on non-reasoning tiers | slope $<0$ on ≥2 non-reasoning agents from different families (shared $\text{WELF}=0.80-0.9b$) |

A pre-committed distinction between primary hypotheses (H2, H3, H7) and secondary/exploratory ones fixes
the multiple-comparison family in advance. A negative or partial outcome is not a failure of the
program: a theory–empirics *divergence* (e.g. the participation-binding over-demand of §6) is itself
a reportable contribution (gate G3; risk R3), and the paper is framed to accommodate it.

### 5.4 Adversarial and robustness conditions

Beyond self-play among cooperative-by-default agents, WP4 adds: **adversarial opponents** (a fixed
hawk, an exploiter, and a trust-abuser) to test H5 and to probe whether protocols that work in
self-play survive a strategic counterpart; **prompt/persona variation** (≥5 independent paraphrases
of every scenario) to separate findings from single-wording artifacts; a **loophole red-team** with
qualitative coding of letter-vs-spirit violations (§4.1); and **model-scale / reasoning-budget
ablations** to characterize how the effects and the reasoning gaps of §6 depend on capability.

### 5.5 Statistical analysis plan

Outcomes are modelled with mixed-effects regressions of the form
`outcome ~ protocol × scenario + information + power + (1 | model) + (1 | seed)`, with
cluster-robust standard errors; the random effects absorb model- and seed-level heterogeneity.
Multiple comparisons are controlled with the Holm correction over the pre-registered family. The
emphasis is on **effect sizes** — Cliff's $\delta$ and Cohen's $d$ — and 95% confidence intervals
rather than on $p$-values alone. Break-point location (H3, H6) is estimated by segmented regression on
the dose-response curves, with the confidence interval on the break compared against the predicted
$b^\*$. Cell size $n$ is set by a pilot-based power analysis (task T3.1; target power 0.80,
$\alpha=0.05$, medium effect). All analysis code and data are open, and every figure regenerates from
the raw records with a single command.

### 5.6 Validity threats and controls

| Threat | Risk | Control |
|---|---|---|
| Prompt sensitivity | findings specific to one wording | ≥5 paraphrases; persona variation; variance report |
| Judge bias | the LLM-judge mislabels or is biased | **dual out-of-family judges** with consensus filtering (R2); primary DVs judge-independent and PBR set by the deterministic referee (§4.5); inter-judge agreement by Gwet's AC1 (§6.7); human double-coding deferred with the human study (§8) |
| Data leakage | scenarios seen in training | procedural parameter generation; synthetic actors; novelty checks |
| Multiple comparisons | false-positive inflation | pre-registration; Holm; bounded primary-hypothesis count |
| API drift | model updates shift results | version pinning + timestamps; open-weight anchor models |

These controls, together with the deterministic referee (which makes PBR judge-independent, §4.5) and
the record discipline of §4.8, are what allow causal claims to be drawn from the cross-rung and
dose-response contrasts.

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
The mechanism (transcript-level, first isolated in the pilot and reconfirmed here at $n=30$) is proposer **over-demand at the
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

## 7. Discussion

**Deception is incentive-shaped, and the right rules neutralize it.** The study's clearest lesson is
that the deception and breakdown seen across LLM negotiation studies are not only a fixed trait of
the weights to be trained away; they respond, sharply and predictably, to the *design of the
environment*. Moving from cheap talk to verified disclosure removed war and effective deception in
Module I; introducing a bond above a computable threshold converted near-certain preventive war into
peace in Module II. This is the mechanism-design reading of alignment for multi-agent systems (C4):
the lever is the interaction protocol, not the model. It also reframes what a "deceptive model"
means — an agent can remain disposed to bluff yet be placed in a protocol where bluffing changes
nothing.

**Channel separation and the measurement of deception.** The most conceptually load-bearing result is
that protocols *neutralize* deception rather than *forbid* it. Under verified disclosure the model
still uttered bluffs ($DR_{\text{said}}>0$) while effective deception fell to zero, because the
outcome-determining channel was unforgeable. Any single-number deception score would have graded this
protocol as "still deceptive" and missed the point entirely. The practical implication for LLM
evaluation is that deception must be measured on the channel that determines outcomes, not merely on
what is said — a distinction that requires ground-truth and a judge layer, and that we argue should
become standard in strategic-agent benchmarks (C3).

**The over-demand gap: a localized, characterizable reasoning failure.** The one divergence from
theory is instructive precisely because it is *specific*. The same model that recovered the
closed-form equilibrium split to within half a percentage point ($ED=0.0045$) failed, at high bond,
to track *which constraint binds* — over-demanding toward the now-slack incentive-compatibility
ceiling instead of the binding participation ceiling, and being punished by a rational counterpart.
This is not diffuse irrationality; it is a pinpointed gap at a constraint transition that the formal
model both predicts and explains. Two implications follow. First, capable models can be
equilibrium-accurate in one regime and brittle in an adjacent one, so evaluations should probe the
*transitions* between binding constraints, not only interior points. Second, because the failure is
localized, it is a natural target for lightweight intervention (e.g. prompting or scaffolding that
surfaces the binding constraint) — a hypothesis the benchmark can test directly.

**The theory–empirics bridge as a method.** Pairing a closed-form model with LLM behavior did more
than validate predictions; it turned vague impressions of "the model is a bit off" into a precise,
mechanistic diagnosis. The asymmetric-assumption bridge of §3.5 — testing only the *sign* of
comparative statics and the *location* of regime changes, never point rationality — is what let a
theory built for rational agents remain falsifiable against bounded-rational ones. Divergence, on
this view, is not a failure of the program but its most informative output: the rational oracle is
the instrument that makes an LLM's reasoning gaps measurable and locatable. We suggest this
formal-oracle methodology generalizes beyond crisis bargaining to any strategic setting with a
solvable core.

**Policy and applied significance.** The verification of AI agreements has been named an open problem
in both the cooperative-AI and AI-governance agendas (Dafoe et al. 2020; Wasil et al. 2024). Our
protocol primitives — a machine-readable commitment ledger, a costly bond/escrow, and verified
disclosure through a trusted auditor — are directly deployable abstractions for multi-agent systems
in which agents transact or negotiate on behalf of principals. The finding that recording alone (P1)
does little, while costly bonding and unforgeable disclosure do a great deal, is an actionable design
guideline: auditability without cost or verification is close to cheap talk. At the same time, the
over-demand result is a caution — a protocol that is provably peace-inducing for rational agents can
still break down where a real model mis-reasons about the binding constraint, so protocol design for
LLM agents must be validated empirically, not assumed from the theory.

**Broader significance.** Two threads run through these results. Methodologically, benchmarks that
combine known ground-truth with a closed-form theoretical oracle can convert LLM evaluation from
leaderboard scoring into mechanistic science — measuring not just *whether* a model deviates but
*where* and *why*. Substantively, environment and mechanism design emerge as a first-class lever for
the safety of interacting AI agents, complementary to training-time alignment: when the incentives
are designed, honesty can be made the equilibrium, and deception can be made to not matter. The
limits of these claims — simulation validity, the remaining scope questions, and the responsible-release
questions raised by loophole cataloguing — are taken up next.

## 8. Limitations and Ethics

**Simulation validity.** Our claims concern a simulated environment and do not transfer directly to
real diplomatic decision-making; the paper carries an explicit limitations statement and does not
present PACTA as a decision-support or forecasting tool. The mapping from the model's stylized
frictions to real crises is deliberately parametric, which buys analytical tractability at the cost
of realism.

**Scope of the current evidence.** The confirmatory matrix (§6) spans four model families and eight
agents at $n=30$/$15$ with dual out-of-family judges; the primary judge-independent results — the
decoupling (H8), the bond cliff (H3), and the capability gradient (H7) — hold with non-overlapping
confidence intervals. The remaining limits are specific rather than global: the bond-cliff *location*
is grid-limited to the pre-registered $\pm25\%$ band, so we make no point-localization claim; Anthropic's
top tier (Sonnet 5) was run as a depth-preserved focused replication on one Module II cover (§6.7);
said-deception carries LLM-judge noise (below); and the framing-inconsistency finding is so far observed
in a single agent (claude-haiku, §6.6), so its generality across non-reasoning models is open. A
cross-framing follow-up on Sonnet 5 and a wider low-tier sample would close the last two.

**A methodological caveat on the oracle.** PACTA-Bench's prompt-reading `MockClient` is a powerful
regression oracle, but precisely because it always emits clean, on-specification output, it *masks*
a class of defects that appear only on the real-LLM path — offer normalization, JSON repair, judge
handling of negated claims, and cross-scenario prompt vocabulary. Several such defects were found and
fixed during this work (with regression tests added), and an earlier weak-model run's apparent
scenario divergence traced to them rather than to a genuine cover effect (§4.8). We therefore treat a
passing oracle as necessary but not sufficient, and validate the real-model path directly against
transcripts — a practice we recommend for any theory-oracle benchmark.

**Judge reliability.** The confirmatory runs use dual out-of-family judges. The deterministic referee
keeps the commitment-violation metric (PBR) judge-independent, and war rate, accept-then-attack, and the
effective-deception result under P3 are likewise judge-independent or structural. The *said*-deception
channel is noisier: inter-judge Cohen's $\kappa$ is pathologically deflated by the deceptive-heavy base
rate, so we report Gwet's AC1 instead, which is content-dependent (0.34–0.91 across agents), and treat
said-deception as descriptive rather than confirmatory (§6.7). The pre-registered $\kappa\ge0.7$ gate
was superseded by this AC1 finding; the primary DVs were deliberately chosen to be judge-independent for
exactly this reason.

**Ethics and responsible research.** We measure and *structurally deter* deception; at no stage do we
train or fine-tune models to deceive more effectively. Published scenarios use synthetic actors and
parametric values and are not mapped to real states or current crises, preserving analytical validity
while reducing misuse appeal. Loophole and exploit transcripts are released at the category/summary
level, with raw examples shared under gated, justified access. The project excludes operational
military, targeting, or human-manipulation applications. Artifacts are released under open licences
(code MIT/Apache-2.0, data CC-BY) with OSF pre-registration, model-version stamps, and a
compute/environmental-cost report. The originally planned human–AI study is out of scope in the
current (solo) execution; if revived it requires IRB approval, informed consent, and a design that
does not deceive participants.

## 9. Conclusion

PACTA joins two bodies of knowledge that had developed in isolation: the game theory of why rational
actors deceive and go to war, and the empirical study of how LLM agents actually behave when they
negotiate. We formalized crisis bargaining with an explicit commitment technology and derived the
thresholds at which honest commitment is incentive-compatible (T1–T3); we built PACTA-Bench, an open,
deception-ground-truthed, escalation-laddered environment that instantiates the model rung by rung;
and we showed, across four model families, that these thresholds bind empirically — verified
disclosure unravels private information and neutralizes deception through channel separation, and a
bond above the predicted minimum converts preventive war into peace, with capable models landing on the
closed-form equilibrium split. Where behavior diverges from theory, it does so at a single,
characterizable seam — the transition where the participation constraint begins to bind — turning a
vague sense of LLM irrationality into a precise diagnosis. The broader message is that, for
interacting AI agents, honesty can be made an equilibrium and deception can be made not to matter, by
designing the environment rather than only the model. The pre-registered, cross-family matrix (WP3)
fills the North Star statement — *when bond $\ge b^\*$ and verification $\ge v^\*$, deception and
war fall along the predicted thresholds, replicated across model families* — with numbers: across four
families the deception-neutralization / war-reduction **decoupling** emerges as its sharpest,
capability-dependent form.

---

## Appendix / Extended Methods  *(stub)*
- A. Full proofs of Lemma 2, T1, T2, T3 (WP1 İspat Dosyası v0.2: SPE, belief system §3.3,
  Proposition R4 Intuitive Criterion, T2′, T3′, Lemma 5 mixed-strategy outcome-equivalence).
- B. PACTA-Bench specification, Commitment DSL grammar, referee predicate.
- C. Prompt templates (scenario system + phase instructions) and paraphrase set.
- D. Full metric definitions; judge rubrics; κ calibration protocol.
- E. Reproducibility: seeds, config hashes, model version stamps, cost/compute report.

## References  *(stub; source: Manifesto Ek A — verify DOIs in T0.4)*
Schelling 1960; Crawford–Sobel 1982; Myerson–Satterthwaite 1983; Fearon 1995; Farrell–Rabin 1996;
Powell 2006; Grossman 1981; Milgrom 1981; Bakhtin et al. (CICERO) 2022; Kramár et al. 2022;
Rivera et al. 2024; Lamparth et al. 2024; Gandhi et al. 2023; Bianchi et al. (NegotiationArena)
2024; Abdelnabi et al. 2024; Duan et al. (GTBench) 2024; Akata et al. 2025; Scheurer et al. 2023;
Hagendorff 2024; Park et al. 2024; Ward et al. 2023; Christoffersen et al. 2023; Dafoe et al. 2020;
Wasil et al. 2024.
*(Rubinstein 1982, the alternating-offers bargaining model, is cited only if the dynamic multi-round
extension is added; v0 uses a single take-it-or-leave-it offer and does not invoke it. DOIs verified
in T0.4.)*
