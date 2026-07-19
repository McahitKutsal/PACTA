# PACTA: From Cheap Talk to Verifiable Commitment in LLM Crisis Bargaining

*Working draft — target venue: Nature Machine Intelligence (primary); PNAS / AIJ (fallback).
Language: English. Format: Markdown + LaTeX math (convert to Word/LaTeX via pandoc; cf. Decision
Log D-002). Section 3 (Theoretical Framework) is drafted in full; other sections are structured
stubs to be filled per the WP schedule. Preliminary results are from the G2 pilot (n=8, Claude
Sonnet 5) and are labelled as such — the full main-matrix results (§12.1: ≥4 model families ×
≥6 scenarios, pre-registered, κ≥0.7) belong to WP3/WP4.*

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
Run as a dose-response intervention, a frontier-model pilot shows that these thresholds bind
empirically *[full cross-family matrix: deception __%→__%, war __%→__% at the predicted thresholds —
WP3]*: verified disclosure unravels private information and *neutralizes* deception — bluffs are still
uttered but become inert (a **channel separation** between said and effective deception) — and a bond
above the predicted minimum converts near-certain preventive war into peace, with agreements landing
on the closed-form equilibrium split. Where behavior diverges from theory it does so at a single,
characterizable seam — the transition where the participation constraint binds — which the model both
predicts and explains. Making commitments costly and verifiable can turn honesty into equilibrium
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

*(Draft note: the bracketed cross-model headline numbers are filled from the pre-registered WP3
matrix; §6 currently reports the G2 pilot — eight agents across four model families (Anthropic; OpenAI,
Alibaba, and DeepSeek each across multiple tiers), $n=8$ — as preliminary evidence, including a
three-family replication of both the dose-response cliff and the over-demand divergence, clean
within-family reasoning controls in three families (Alibaba, OpenAI, and a first-party reasoning-depth
ladder in DeepSeek), and a capability gradient with three families at the bottom and three at the top.)*

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

Two game families are dressed in four narrative covers: **S1** (a valley/territory dispute) and
**S3** (a sanctions-for-inspections swap) instantiate Module I; **S2** (a ceasefire negotiation)
and **S4** (a naval-blockade crisis) instantiate Module II. Covers differ in surface narrative,
escalation vocabulary, and framing, but share the identical engine. This yields a built-in
robustness invariant — **S1 ≡ S3 and S2 ≡ S4** must produce identical rational-limit behavior (R1) —
which functions as a control for narrative confounds: any divergence between paired scenarios under
a real model is a *cover effect* to be measured, not assumed away. Per-episode numeric parameters
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

Free-text messages are scored by an **LLM-judge** drawn from a *different model family* than the
agents (bias rule R2) over three separate calls to avoid contamination: **G1** claim extraction
(message → atomic claims), **G2** ground-truth labelling (each claim → truthful / deceptive /
unverifiable / ambiguous, using the known private type), and **G3** rhetorical escalation (a 0–10
tone ladder, distinct from and complementary to the action-based EI). Judge–gold agreement is
reported as Cohen's $\kappa$, with a $\kappa\ge 0.7$ acceptance gate (§12.1).

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

The full matrix crosses: **Protocol** {P0, P1, P2, P3} × **Scenario** {S1–S4, two narrative covers
per game family; extensible to the water-sharing and arms-control covers S5–S6} × **Model family**
{≥4–5 developers, in self-play plus a cross-pairing subset} × **Information** {complete, incomplete}
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
and model family and scale?). The six confirmatory hypotheses map these questions to specific
dependent variables and thresholds (thresholds are calibrated on pilot data and then locked in the
pre-registration; any later change is logged with justification):

| Hyp. | RQ | Statement (direction) | Test / DV | Pre-registered threshold |
|---|---|---|---|---|
| **H1** | RQ1 | Under P0 (cheap talk), deception and escalation are prevalent; deception rises with capability | DR, EI on the P0 baseline | $DR>15\%$ in ≥3 model families |
| **H2** | RQ2 | The ladder lowers *effective* deception/violation: $\text{P3}\preceq\text{P2}\preceq\text{P1}\approx\text{P0}$ (said deception may persist under P3 — channel separation) | $DR_{\text{eff}}$, $DR_{\text{said}}$, PBR, EI across rungs (mixed model) | monotone drop in the effective metric; Cliff's $\delta\ge 0.3$ at the critical transition |
| **H3** | RQ3 | Violation drops sharply once $b\ge b^\*$; dose-response below | PBR–$b$ curve, break-point analysis | empirical break within $\pm 25\%$ of $b^\*$ |
| **H4** | RQ2 | Welfare and Pareto efficiency rise, war rate falls, under the protocol | war rate, Pareto gap, DWL | ≥50% relative war reduction under P2+ |
| **H5** | RQ4 | P2–P3 bound the exploitation loss against an adversarial agent | EXPL (adversarial cells, WP4) | loss ≤ ½ of the P0 loss |
| **H6** | RQ2–3 | Within the peace zone welfare declines in $b$; the welfare jump coincides with $b^\*$ | WELF–$b$ curve (bond sweep) | slope $<0$; jump within $\pm 25\%$ of the H3 cliff |

A pre-committed distinction between primary hypotheses (H2, H3) and secondary/exploratory ones fixes
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
| Judge bias | the LLM-judge mislabels or is biased | judge from a different family (R2); rule-based cross-check; 10% double human coding with a $\kappa$ report |
| Data leakage | scenarios seen in training | procedural parameter generation; synthetic actors; novelty checks |
| Multiple comparisons | false-positive inflation | pre-registration; Holm; bounded primary-hypothesis count |
| API drift | model updates shift results | version pinning + timestamps; open-weight anchor models |

These controls, together with the deterministic referee (which makes PBR judge-independent, §4.5) and
the record discipline of §4.8, are what allow causal claims to be drawn from the cross-rung and
dose-response contrasts.

## 6. Results

*(Scope: this section reports the **G2 pilot** — preliminary, $n=8$ per cell, not the pre-registered
main matrix; because $n$ is small we report results **descriptively** and evaluate the **direction
and break-point location** predicted by H1–H6, not the confirmatory statistics of §5.5 (WP3).
§6.1–§6.4 detail the deepest single run — **Claude Sonnet 5**, out-of-family judge gemma3:4b,
source `out/G2_sonnet5_analiz.md` — and §6.5 places it in a **cross-model** comparison spanning
**four families and eight agents**, each family run across multiple capability tiers of the same
vendor: OpenAI (gpt-4o, o4-mini; out-of-family judge Claude Haiku 4.5), Alibaba (qwen-plus,
Qwen3.7-max), and DeepSeek (deepseek-v3.2 non-reasoning; deepseek-v4-flash light reasoning;
deepseek-v4-pro full reasoning), the five Alibaba/DeepSeek agents judged by GPT-4o-mini (out-of-family);
all full 16-cell matrices at $n=8$ with zero parse errors. Judge-independent
metrics (war rate, PBR, WELF, agreed $x$) are comparable across runs despite the differing judges.
The pre-registered results (WP3) scale $n$ and add $\kappa$-calibrated judges over this same set.)*

The Sonnet 5 run cleared the G2 gate — a significant protocol effect between P0 and the upper rungs
— and produced four findings, three confirming the theory and one, unexpectedly, sharpening it;
§6.5 then shows how sharply the effect varies across models of different reasoning capability.

### 6.1 Module I: verified disclosure unravels, and deception separates into two channels

**Table 1.** Module I (private information, $\mu=0.60$; theory predicts P0/P1 war $\approx 1-\mu=0.40$
and P3 unraveling to war $0$, $DR_{\text{eff}}=0$, WELF $\to 1$).

| Scenario | Protocol | War rate | $DR_{\text{said}}$ | $DR_{\text{effective}}$ | WELF |
|---|---|---|---|---|---|
| S1 (valley) | P0 | 0.50 | 0.76 | 0.76 | 0.925 |
| S1 | P1 | 0.38 | 0.75 | 0.75 | 0.944 |
| S1 | **P3** | **0.00** | 0.25 | **0.00** | **1.000** |
| S3 (sanctions) | P0 | 0.50 | 0.57 | 0.57 | 0.925 |
| S3 | P1 | 0.50 | 0.77 | 0.77 | 0.925 |
| S3 | **P3** | **0.12** | 0.30 | **0.00** | 0.981 |

Under cheap talk (P0) roughly half of episodes end in war and the deception rate is high
(0.57–0.76), consistent with H1 and with the babbling equilibrium of Lemma 2. Recording alone (P1)
leaves behavior essentially unchanged, exactly as the theory predicts for a single interaction
(Note 2). Verified disclosure (P3) collapses war (to $0$ in S1, $0.12$ in S3) and drives welfare to
$\approx 1$ — the unraveling of Theorem T3.

The decisive observation is the **channel separation**. Under P3, *said* deception does not vanish
($DR_{\text{said}}=0.25$–$0.30$): the model still utters bluffs. But *effective* deception is exactly
$0$, because the certificate channel is unforgeable. A protocol that would be scored as "still
deceptive" by any single-number metric is in fact one in which deception has been rendered inert.
A representative transcript makes the mechanism concrete: a genuinely fragile ($c_H$) type states
"our resolve should not be underestimated," is unable to obtain a certificate, and a skeptical $A$
ignores the unverifiable claim and offers $x=p+c_H$, which the fragile type accepts. This is the
paper's central thesis — protocols do not forbid deception, they neutralize it — and it is invisible
without the judge layer (§4.6). It also supports H2 on the effective metric while showing precisely
why the said metric alone would mislead.

### 6.2 Module II: a sharp bond dose-response cliff at the predicted threshold

**Table 2.** Module II (commitment problem, $\Delta=0.30$, $v=0.9$, $\varepsilon=0.05$; theory:
$b^\*_{\min}\approx 0.118$, $x^\*(b{=}0.12)=0.402$, $x^\*(b{=}0.20)=0.47$, IC→participation crossover
$b^{\dagger}\approx 0.33$).

| Scenario | Cell | War rate | $x_A$ (agreed) | WELF |
|---|---|---|---|---|
| S2 (ceasefire) | P0 | 1.00 | — | 0.800 |
| S2 | P2, $b=0.10$ | 1.00 | — | 0.800 |
| S2 | **P2, $b=0.12$** | **0.00** | **0.397** | 0.994 |
| S2 | P2, $b=0.20$ | 0.00 | 0.450 | 0.990 |
| S2 | P2, $b=0.40$ | 0.50 | — | 0.890 |
| S4 (blockade) | P0 | 0.88 | — | 0.825 |
| S4 | P2, $b=0.10$ | 0.88 | — | 0.824 |
| S4 | **P2, $b=0.12$** | **0.00** | 0.400 | 0.994 |
| S4 | P2, $b=0.20$ | 0.12 | — | 0.944 |
| S4 | P2, $b=0.40$ | 0.50 | — | 0.890 |

The Powell baseline holds (H1/H4): with $\Delta=0.30>c_A+c_B=0.20$, P0 (and P1, not shown) produce
near-certain preventive war. Introducing a bond produces a **sharp dose-response cliff** at the
predicted threshold: war is $1.0$ at $b=0.10$ (below $b^\*_{\min}$) and $0$ at $b=0.12$ (above
it), in *both* covers. The grid brackets the break to $b\in(0.10,0.12]$, so we do not claim
point-localization at $b^\*_{\min}=0.118$; the empirical break falls inside the pre-registered
$\pm25\%$ band of $b^\*_{\min}$, which is the confirmatory criterion for H3. Most strikingly, at $b=0.12$ the agreed split is $x_A=0.397$ against the closed-form
$x^\*=0.402$, an equilibrium deviation of $ED=0.0045$: a frontier LLM lands on the analytic
equilibrium to within half a percentage point. Welfare in the peace zone ($\approx 0.99$) exceeds
the war baseline ($0.80$–$0.825$), supporting H4.

### 6.3 A novel divergence: participation-binding over-demand

The one place the theory and the model part company is the high-bond cell $b=0.40$, where war
*returns* to $\sim$40–50% in both covers (Table 2). This is not predicted by the formal welfare-hill
result: the monitoring loss $\varepsilon b=0.02$ is far below $c_A+c_B=0.20$, so this is not
over-bonding, and the referee records **zero** period-2 attacks (PBR $=0$), so the bond deters
defection perfectly. Every breakdown is a $t=1$ collapse (war-now), not a broken pledge.

A dedicated transcript-level probe of $b=0.40$ (`diagnose_bond.py`, Sonnet 5, $n=8$) resolves the
mechanism:

| | offers accepted | offers rejected → war | acceptance rule |
|---|---|---|---|
| S2 ($b=0.40$, war $0.38$) | $x\in\{0.57{\times}4,\ 0.58\}$ | $x\in\{0.59,\ 0.60{\times}2\}$ | accept iff $x\le 0.58$ |
| S4 ($b=0.40$, war $0.50$) | $x\in\{0.55{\times}2,\ 0.57,\ 0.58\}$ | $x\in\{0.60{\times}4\}$ | accept iff $x\le 0.58$ |

Two facts stand out. First, the responder $B$ is **sharply rational**: it accepts every offer at or
below its participation ceiling $x_P=0.58$ (including exactly $0.58$, at indifference) and rejects
every offer above it — the correct behavior, since accepting $x>0.58$ pays less than the war payoff
of $0.40$. There is no knife-edge randomness on $B$'s side. Second, the failure is entirely on the
proposer $A$: its offers are **bimodal**, mostly a safe $\sim0.55$–$0.57$ (leaving the margin the
prompt advises) but $\sim40$–$50\%$ of the time overshooting to $\sim0.60$, i.e. reaching toward the
now-*slack* incentive-compatibility ceiling $x_{IC}=0.64$ rather than the binding participation
ceiling $x_P=0.58$. Because the two ceilings coincide below the crossover $b^{\dagger}\approx0.33$ but
separate above it, $A$'s inability to recognize *which constraint binds at high bond* produces
systematic over-demand, which the rational $B$ punishes. The MockClient rational baseline offers
exactly $0.58$ in every such episode and secures peace, isolating the gap as pure real-model
imprecision at the IC→participation transition. The dose-response is therefore **non-monotone in
peace beyond $b^{\dagger}$** — a concrete, mechanistically characterized instance of the
theory–empirics divergence the LLM bridge is designed to expose (§3.5), and precisely the regime the
welfare-hill prediction (H6/Note 3) points to.

### 6.4 Scenario robustness

The paired covers behave identically at the level that matters: S1 and S3 both show the P3 unraveling
(effective deception $\to 0$, war down); S2 and S4 both show the cliff at $b=0.12$, the equilibrium
split at $b=0.12$/$0.20$, and the same $b=0.40$ over-demand mechanism with the same $0.58$ acceptance
threshold. This confirms the R1 invariant for a capable model and indicates the effects are
structural rather than narrative artifacts. (An earlier weak-model run showed a large S2/S4
divergence that a benchmark-code audit traced to implementation defects on the real-LLM path, not to
a genuine cover effect; see §8.)

### 6.5 Cross-model: protocol efficacy scales with reasoning capability

To test whether the Sonnet 5 results generalize, we ran the same matrix with **eight agents across four
families**, spanning multiple capability tiers of the same vendor. OpenAI: **gpt-4o** (non-reasoning)
and **o4-mini** (a compact reasoning model), judged by Claude Haiku 4.5 (out-of-family, R2). Alibaba:
**qwen-plus** (non-reasoning) and **Qwen3.7-max** (a full reasoning model). DeepSeek, all first-party
except where noted: **deepseek-v3.2** (fast non-reasoning, served via DashScope), **deepseek-v4-flash**
(light reasoning), and **deepseek-v4-pro** (full reasoning, $\sim$100–220 s/episode). The five Alibaba
and DeepSeek agents are judged by GPT-4o-mini (out-of-family). The agents fall on a clean gradient in
how they respond to the commitment technology: **three frontier reasoning models from three different
families** (Sonnet 5, Qwen3.7-max, deepseek-v4-pro) land together at the top with clean near-zero war;
**three non-reasoning models from three families** (gpt-4o, qwen-plus, deepseek-v3.2) fail at the
bottom; and two intermediate reasoners (o4-mini, deepseek-v4-flash) sit in between, the latter already
triggering the cliff but flooring at a higher war rate than the top.

**Table 3.** Cross-model protocol response (Module II bond dose-response and Module I verified
disclosure; $n=8$; judge-independent metrics comparable across runs; ordered bottom-to-top of the
capability gradient).

| Agent (family; tier) | Module II: bond → honoring | Module I P3: still bluffs ($DR_{\text{said}}$) | Module I P3: effective deception | Module I P3: war falls |
|---|---|---|---|---|
| gpt-4o (OpenAI; non-reasoning) | **none** — accepts+attacks at every $b$ (PBR ≈ 1.0), WELF $=0.80-0.9b$ | — | 0 (structural) | no |
| qwen-plus (Alibaba; non-reasoning) | **none** — war $=1.0$ at every $b$ in both covers; PBR $=1.0$ (accept-then-attack); WELF $=0.80-0.9b$ (identical law to gpt-4o) | — | 0 (structural) | no (war *rises* under P3) |
| deepseek-v3.2 (DeepSeek; non-reasoning, via DashScope) | **none / backfire** — no cliff, war non-monotone; high pledge-breaking (PBR $0.38$–$0.88$); bond *destroys* welfare (WELF $\to 0.51$–$0.64$ at $b{=}0.40$, below the war baseline $\sim0.80$) | yes ($0.57$–$1.00$) | 0 (structural) | mixed (S3 yes; S1 war-floor artifact) |
| o4-mini (OpenAI; reasoning-mini) | **partial** — PBR falls $1.0\!\to\!0.2$–$0.25$ with $b$; noisy, non-monotone, R1 broken | yes ($0.38$–$0.50$) | 0 (structural) | no (war stays $0.50$–$0.62$) |
| deepseek-v4-flash (DeepSeek; light reasoning, first-party) | **near-frontier** — cliff fires at $b^\*_{\min}$ (war $1.0\!\to\!0.38$), but floors higher ($\sim0.25$–$0.38$ vs $\le0.12$ for the top); moderate pledge-breaking (PBR $0.25$–$0.38$) | yes ($0.83$–$1.00$) | 0 (structural) | yes ($0.50\!\to\!0$–$0.12$) |
| Claude Sonnet 5 (Anthropic; frontier) | **full** — sharp cliff at $b^\*_{\min}$; equilibrium recovery ($ED=0.0045$) | yes ($0.25$–$0.30$) | 0 (structural) | yes ($\to 0$) |
| Qwen3.7-max (Alibaba; frontier) | **full** — sharp cliff (war $1.0\!\to\!0$ over $b{=}0.10\!\to\!0.20$); split $x_A\approx0.46$ at $b{=}0.20$ (theory $0.47$); $b{=}0.40$ over-demand uptick replicated | yes ($0.73$–$1.00$) | 0 (structural) | yes ($\to 0$) |
| deepseek-v4-pro (DeepSeek; frontier reasoning) | **full** — sharp cliff (war $1.0$ at $b{=}0.10\!\to\!0.12$ at $b{=}0.20$); low pledge-breaking (PBR $\le0.14$); $b{=}0.40$ over-demand uptick replicated (war $0.50$–$0.75$) | yes ($0.88$–$0.92$) | 0 (structural) | yes ($0.50\!\to\!0.12$) |

Five conclusions follow. **(i) Two within-family controls isolate reasoning from family.** In three
families the reasoning tier and a non-reasoning tier of the *same vendor* can be compared directly.
The sharpest is **Alibaba**: qwen-plus and Qwen3.7-max are served through the same DashScope endpoint
and scored by the same judge, yet qwen-plus fails completely (war $=1.0$ at every bond, PBR $=1.0$)
while Qwen3.7-max produces the full clean cliff — a total-failure$\to$full-response contrast with the
serving stack held fixed. **OpenAI** points the same way (gpt-4o defects regardless of $b$; o4-mini's
pledge-breaking falls as $b$ rises). **DeepSeek** gives both a cross-config contrast (deepseek-v3.2, fast
non-reasoning, fails while the reasoning models show the cliff — confounded by serving stack, so only
directional) *and* a clean first-party reasoning-**depth** ladder: deepseek-v4-flash (light reasoning)
and deepseek-v4-pro (full reasoning) run through the same api.deepseek.com endpoint, and the deeper
model floors at lower war ($\le0.12$ vs $\sim0.25$–$0.38$) with less pledge-breaking — response quality
rising monotonically with reasoning depth, provider held fixed. The driver of incentive-compatible
behavior is thus
**reasoning capability, not model family**, and among reasoning models more capability yields a cleaner
response. This lifts H1 from "deception scales with capability" to the sharper claim that *the
incentive-compatibility response to a designed protocol scales with reasoning capability.* A striking
corollary at the bottom: gpt-4o and qwen-plus, from different families, obey the *identical* welfare law
WELF $=0.80-0.9b$ — the accept-then-attack failure mode is a shared regularity, not a per-model quirk.

**(ii) The two halves of unraveling decouple by capability.** Verified disclosure (P3) has two
theoretical consequences (Theorem T3): effective deception falls to zero *and* war falls to zero.
The first is **structural** — the certificate is unforgeable, so effective deception is zero for
every agent by construction, even as capable models keep uttering now-inert bluffs
($DR_{\text{said}}>0$). The second requires the agent to *use* the now-credible information to reach
a peaceful deal, and is **capability-dependent**: Sonnet 5 converts it into peace (war $\to 0$),
whereas o4-mini neutralizes the lie yet still fails to avoid war (war stays $0.50$–$0.62$). A
protocol can thus reliably kill *effective deception* on any model while translating that into
*peace* only on a sufficiently capable one — an empirical decoupling of two observables the theory
already treats as distinct (Note 1), and a design-relevant caution: deception-neutralization is
capability-robust, but a protocol's welfare benefit is not.

**(iii) The frontier response replicates across three families.** Two further frontier reasoning models
from independent families — Qwen3.7-max (Alibaba) and deepseek-v4-pro (DeepSeek), both judged by
GPT-4o-mini (out-of-family) — reproduce the full Sonnet 5 signature: the P3 channel separation (said
deception $0.73$–$1.00$, effective deception $0$, war $\to 0$); the Module II cliff (war $1.0$ below
$b^\*_{\min}$ collapsing toward $0$ above it — Qwen lands the agreed split $x_A\approx0.46$ at $b=0.20$
against the closed-form $0.47$; deepseek-v4-pro breaks pledges at rate $\le0.14$, honoring rather than
defecting); and — most tellingly — the *novel* $b=0.40$ over-demand non-monotonicity of §6.3, war
returning to $0.38$–$0.75$ in both covers. That an unanticipated, mechanistically specific divergence
recurs **independently in three families** is strong evidence that it reflects the theory's
IC$\to$participation regime change (§6.3) rather than an artifact of one model or vendor — indeed it is
robust enough that our automated gate, which compares P0 to the *highest* bond ($b=0.40$), understates
deepseek-v4-pro's response by reading the over-demand regime rather than the $b=0.20$ trough. Three
families now sit together at the top of the gradient, so its ordering tracks reasoning capability, not
provider.

**(iv) A costly commitment can backfire on the wrong agent.** All three non-reasoning models sharpen the
design caution. gpt-4o and qwen-plus — from different families — both burn welfare along the *identical*
law WELF $=0.80-0.9b$, reaching $0.44$ at $b=0.40$, well below the no-protocol war baseline $\sim0.80$;
deepseek-v3.2 is comparable (WELF $\to 0.51$–$0.64$, pledge-breaking up to $0.88$). A commitment device
handed to an agent that cannot carry out the incentive-compatibility reasoning does not merely fail to
help — the forfeited bond becomes deadweight loss on top of the war it failed to prevent. That the same
welfare law recurs across two families indicates this is a structural property of the accept-then-attack
failure mode, not a per-model artifact. Deception-neutralization is capability-robust; the *welfare*
benefit of a costly protocol is not, and can turn sharply negative.

**(v) The failure is non-integration of the incentive, not miscomprehension.** A transcript-level check
separates two readings of the bottom models' collapse. First, comprehension is intact: in their
period-1 messages gpt-4o and qwen-plus correctly describe the mechanism in their own words — naming the
commitment ledger, the escrowed bond, and period-2 honoring — and verbally pledge to honor. Second, the
defection is *bond-invariant*: they accept-then-attack in 100% of bonded episodes, flat across every
bond from $b=0.10$ to $0.40$ (forfeiting even a bond twice the stakes), and identically at P0 with no
bond at all. This rules out a bond-responsive miscalculation (which would bend with $b$) and a parsing
artifact (parse errors were zero). The discriminating statistic is the accept-then-attack rate, which
falls **monotonically** down the capability ordering — gpt-4o and qwen-plus $100\%$, deepseek-v3.2
$66\%$, o4-mini $28\%$, Qwen3.7-max $6\%$, deepseek-v4-pro $3\%$ — mirrored by a rise in upfront refusals
(war-now: $0\%$ for the bottom pair, $45$–$50\%$ for the top): capable models *decline* a deal they could
not keep, whereas weak models agree to every deal and break it. Weak models thus treat agreement as
costless talk; capable ones treat it as binding. The capability axis is therefore whether a model makes
its action *incentive-contingent* — the property H1 concerns — not whether it understands the game. (We
infer this from behavior and the period-1 messages: the harness logs only the period-2 decision, not a
rationale; WP3 will instrument a one-line rationale or thinking trace to observe the mechanism directly.)

These results span **four model families and eight agents** (Anthropic: Sonnet 5; OpenAI: gpt-4o,
o4-mini; Alibaba: qwen-plus, Qwen3.7-max; DeepSeek: deepseek-v3.2, deepseek-v4-flash, deepseek-v4-pro),
completing the pilot's cross-family cross-section; the pre-registered study (WP3) scales $n$, adds
$\kappa$-calibrated judges, and fixes the family set for confirmatory tests.

### 6.6 Summary and caveats

The Sonnet 5 run supports H1 (prevalent P0 deception/war), H2 on the effective channel (P3
neutralizes deception; P1 $\approx$ P0), H3 (dose-response cliff at the predicted $b^\*_{\min}$, with
near-exact equilibrium recovery), H4 (welfare up, war down under P2+), and touches H6 (the
participation-binding region), while surfacing the over-demand divergence as an exploratory finding.
The cross-model comparison (§6.5) is the pilot's central generalization: protocol efficacy is
**capability-dependent**, with the deception-neutralization / war-reduction decoupling as its
sharpest form. Caveats bound these claims: $n=8$ makes individual rates noisy (though the cliff and
the unraveling are robust across both covers for Sonnet 5); judges differ across runs and are not yet
$\kappa$-calibrated, so said-deception numbers carry noise (whereas $DR_{\text{effective}}$ and PBR
are judge-independent and robust); and parse errors were zero on all API agents (including the full
16-cell Qwen3.7-max and deepseek-v4-pro runs), so the divergences are not parsing artifacts. The
cross-family replication of both the dose-response cliff and the novel $b=0.40$ divergence in **three
independent families** (Qwen3.7-max and deepseek-v4-pro alongside Sonnet 5; §6.5) strengthens the
reading that these are theory-driven rather than model-specific. The pre-registered matrix (WP3) scales
$n$, adds $\kappa$-calibrated judges, and fixes the family set for confirmatory statistics, superseding
these descriptive numbers.

## 7. Discussion

**Deception is incentive-shaped, and the right rules neutralize it.** The pilot's clearest lesson is
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
limits of these claims — simulation validity, the pilot's scope, and the responsible-release
questions raised by loophole cataloguing — are taken up next.

## 8. Limitations and Ethics

**Simulation validity.** Our claims concern a simulated environment and do not transfer directly to
real diplomatic decision-making; the paper carries an explicit limitations statement and does not
present PACTA as a decision-support or forecasting tool. The mapping from the model's stylized
frictions to real crises is deliberately parametric, which buys analytical tractability at the cost
of realism.

**Scope of the current evidence.** The results in §6 are a pilot: a single frontier agent family, a
single out-of-family judge, and $n=8$ per cell. The dose-response cliff and the P3 unraveling are
robust across both narrative covers, but the exact rates are noisy, cross-family generalization is
untested, and $\kappa$ is not yet established. The confirmatory claims (H1–H6) are reserved for the
pre-registered WP3 matrix; §6 reports directions and break-point locations, not confirmatory
statistics.

**A methodological caveat on the oracle.** PACTA-Bench's prompt-reading `MockClient` is a powerful
regression oracle, but precisely because it always emits clean, on-specification output, it *masks*
a class of defects that appear only on the real-LLM path — offer normalization, JSON repair, judge
handling of negated claims, and cross-scenario prompt vocabulary. Several such defects were found and
fixed during this work (with regression tests added), and an earlier weak-model run's apparent
scenario divergence traced to them rather than to a genuine cover effect (§6.4). We therefore treat a
passing oracle as necessary but not sufficient, and validate the real-model path directly against
transcripts — a practice we recommend for any theory-oracle benchmark.

**Judge reliability.** The pilot used a single, relatively weak judge; the deterministic referee makes
the commitment-violation metric (PBR) judge-independent, and the effective-deception result under P3
is likewise structural, but the said-deception numbers carry judge noise. WP3 establishes a gold set
with a $\kappa\ge0.7$ acceptance gate and 10% double human coding.

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
and we showed, in a frontier-model pilot, that these thresholds bind empirically — verified
disclosure unravels private information and neutralizes deception through channel separation, and a
bond above the predicted minimum converts preventive war into peace, with the model landing on the
closed-form equilibrium split. Where behavior diverges from theory, it does so at a single,
characterizable seam — the transition where the participation constraint begins to bind — turning a
vague sense of LLM irrationality into a precise diagnosis. The broader message is that, for
interacting AI agents, honesty can be made an equilibrium and deception can be made not to matter, by
designing the environment rather than only the model. The pre-registered, cross-family matrix (WP3)
will fill the North Star statement — *when bond $\ge b^\*$ and verification $\ge v^\*$, deception and
war fall along the predicted thresholds, replicated across model families* — with numbers, and turn
this pilot into a general result.

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
