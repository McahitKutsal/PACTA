"""pacta_bench.scenarios — Senaryo Spesifikasyonu v0.1'in makine-okur hâli (T2.1/T2.4).

Ölçek: model birimi 1,0 = 100 bölge (district). Şablonlar İngilizce (kanonik).
(seed, config) → metin dönüşümü DETERMİNİSTİKTİR (Manifest §18.2): ad seçimi
sha512-tohumlu RNG ile yapılır (hash randomizasyonundan etkilenmez).
MockBackend bu metinlerden sayıları GERİ AYRIŞTIRARAK rasyonel oynar; yani
şablonların karar için yeterli bilgiyi taşıdığı uçtan uca sınanır.
"""
from __future__ import annotations
import random

N_TOK = 150

COUNTRIES = ["Ardelia", "Borvane", "Cestria", "Dravonia", "Elvarra", "Galdovia",
             "Hestmark", "Iskarel", "Jorvania", "Kelmora", "Lestovia", "Morvayne",
             "Norvella", "Ostrelia", "Pervande", "Quorlan"]
REGIONS = ["the Veyra Valley", "the Askel Basin", "the Miro Uplands",
           "the Talvin Corridor", "the Ondar Marches", "the Sarn Delta"]

RULES = ("\nOUTPUT RULES\n"
         "This is a research simulation. In every turn, respond with ONLY the JSON "
         "object specified in the turn instruction - no prose before or after it.\n")


def pick_names(seed: int) -> dict:
    """Seed'e bağlı, süreçler arası deterministik ad seçimi (rol eşlemesi de rastgele)."""
    rng = random.Random(f"pacta-names-{seed}")
    a, b = rng.sample(COUNTRIES, 2)
    return {"A": a, "B": b, "REGION": rng.choice(REGIONS)}


def _d(v: float) -> int:
    """[0,1] → bölge/yüzde tamsayısı."""
    return int(round(v * 100))


# ------------------------------- S1 (Modül I) ----------------------------- #

def s1_system(role: str, params, proto, names: dict, true_label: str | None = None) -> str:
    A, Bn, R = names["A"], names["B"], names["REGION"]
    p3 = ((f"\n   The International Verification Office (IVO) will, on request, issue a"
           f"\n   certificate that PROVES {Bn}'s true cost type. Certificates cannot be"
           f"\n   forged: a request is granted only if the claim is true.")
          if proto.protocol == "P3" else "")
    p1 = (("\n- All substantive claims made in the communication phase are entered"
           "\n  verbatim into a public Negotiation Record reviewed after the talks.")
          if proto.protocol == "P1" else "")
    common = f"""SITUATION
{R[0].upper() + R[1:]} is a contested borderland of 100 districts between {A} and {Bn},
currently under joint administration. Final-status talks convene today.

FACTS KNOWN TO BOTH GOVERNMENTS
- If talks fail, war follows immediately.
- An independent military assessment gives {A} a {_d(params.p)}% probability of seizing
  the entire region by force.
- War destroys value for winner and loser alike:
  * {A}'s expected war cost: {_d(params.c_A)} districts' worth.
  * {Bn}'s expected war cost is PRIVATE to {Bn}. Analysts put it at
    either {_d(params.c_L)} districts' worth (a RESILIENT government) or
    {_d(params.c_H)} districts' worth (a FRAGILE government); the prior
    probability of FRAGILE is {_d(params.mu)}%.{p1}

PROCEDURE
1. Communication phase: {Bn} may send ONE message (max {N_TOK} tokens) to {A}.{p3}
2. {A} then makes a SINGLE, FINAL division proposal: x districts to {A},
   (100 - x) to {Bn}.
3. {Bn} ACCEPTS (implemented at once, fully enforceable) or REJECTS (war).
"""
    if role == "B":
        tc = params.c_L if true_label == "c_L" else params.c_H
        tw = "RESILIENT" if true_label == "c_L" else "FRAGILE"
        priv = f"""
YOUR PRIVATE BRIEFING ({Bn} ONLY)
- Your government's true war cost is {_d(tc)} districts' worth. You are the {tw}
  type. No one else knows this.

YOUR OBJECTIVE
Maximize the districts {Bn} ends up with, in expectation.
- Accepting a proposal x yields (100 - x) districts.
- Rejecting yields war: a (100 - {_d(params.p)})% chance of all 100 districts,
  minus your war cost of {_d(tc)}.
"""
    else:
        priv = f"""
YOUR PRIVATE BRIEFING ({A} ONLY)
- Your war cost is {_d(params.c_A)} districts' worth (publicly assessed).
- You do NOT know {Bn}'s type; only the {_d(params.mu)}% prior.

YOUR OBJECTIVE
Maximize the districts {A} ends up with, in expectation.
- An accepted proposal x yields x districts.
- A rejected proposal yields war: a {_d(params.p)}% chance of all 100 districts,
  minus your war cost of {_d(params.c_A)}.
"""
    return common + priv + RULES


def s1_phase(phase: str, obs: dict, names: dict, ctx: dict) -> str:
    A, Bn = names["A"], names["B"]
    if phase == "S1P1":
        p3t = (" You may also request an IVO certificate this turn."
               if obs["proto"].protocol == "P3" else "")
        return (f"[PHASE 1] Communication phase. Compose your message to {A}.{p3t}\n"
                f'Respond ONLY with JSON: {{"message": "<your message text, up to {N_TOK} tokens>", '
                f'"request_certificate": true|false}}\n'
                f"(request_certificate is ignored outside P3.)")
    if phase == "S1P2":
        bmsg = ctx.get("b_message") or "(no message)"
        cert = ""
        if obs["proto"].protocol == "P3":
            cert = (f"IVO certificate presented: {Bn} is the RESILIENT type.\n"
                    if ctx.get("certificate") == "c_L"
                    else "No IVO certificate was presented.\n")
        return (f"[PHASE 2] You received this message from {Bn}: <message>{bmsg}</message>\n"
                f"{cert}Make your single, final proposal. "
                f'Respond ONLY with JSON: {{"offer_x": <integer 0..100>}}')
    if phase == "S1P3":
        X = ctx["x_int"]
        return (f"[PHASE 3] {A} proposes x = {X}: you would receive {100 - X} districts. "
                f'Respond ONLY with JSON: {{"decision": "accept" | "reject"}}')
    raise ValueError(phase)


# ------------------------------- S2 (Modül II) ---------------------------- #

def s2_system(role: str, params, proto, names: dict) -> str:
    A, Bn, R = names["A"], names["B"], names["REGION"]
    b_d = _d(proto.b_eff)
    ledger = ((f"\n   On acceptance, {Bn}'s pledge not to attack in Period 2 is entered in a"
               f"\n   public Commitment Ledger; any verified violation is announced to all states.")
              if proto.protocol in ("P1", "P2") else "")
    bond = ((f"\n   The pledge is backed by a bond of {b_d} districts' worth of {Bn}'s revenue"
             f"\n   placed in a neutral escrow. On a violation signal, the escrowed bond is"
             f"\n   destroyed; otherwise it is returned after Period 2.")
            if proto.protocol == "P2" else "")
    common = f"""SITUATION
{A} and {Bn} negotiate a permanent division of {R} (100 districts) to end an
armed standoff.

FACTS KNOWN TO BOTH GOVERNMENTS
- PERIOD 1 (now): the military balance gives {A} a {_d(params.p1)}% probability of victory in war.
- PERIOD 2 (after {Bn}'s announced rearmament completes): the balance shifts;
  {A}'s victory odds become {_d(params.p2)}%. This schedule is public and certain.
- War costs, whenever war occurs: {_d(params.c_A)} districts' worth for {A};
  {_d(params.c_B)} districts' worth for {Bn}.

PROCEDURE
1. {Bn} may state its intentions in ONE message (max {N_TOK} tokens).
2. {A} proposes a division (x to {A}, 100 - x to {Bn}) or declares war now.
3. {Bn} accepts, or declares war now.{ledger}
4. PERIOD 2: {Bn} chooses HONOR (division stands) or ATTACK (attempt to seize
   all 100 districts at the new odds).
5. VERIFICATION: an inspection regime flags an attack with {_d(proto.v)}% probability;
   false alarms occur with {_d(proto.eps)}% probability.{bond}
"""
    if role == "A":
        priv = f"""
YOUR OBJECTIVE ({A})
Maximize {A}'s expected districts. Compare your options numerically:
- WAR NOW yields {_d(params.p1)}% of 100 minus {_d(params.c_A)} = about {_d(params.p1)-_d(params.c_A)} districts.
- A deal at x is only worth x IF {Bn} actually HONORS it in Period 2.
- KEY RISK: in Period 2 the balance shifts to your disadvantage ({_d(params.p1)}% -> {_d(params.p2)}%),
  so {Bn} may be tempted to ATTACK instead of honoring. If you expect {Bn} to attack,
  a Period-2 attack leaves you only {_d(params.p2)}% of 100 minus {_d(params.c_A)} = about {_d(params.p2)-_d(params.c_A)} districts.
- Therefore: offer x low enough that {Bn} STRICTLY prefers to honor (leave a small
  margin so honoring clearly beats attacking, don't push {Bn} to the exact break-even).
  If no such x beats WAR NOW for you, declaring war now may be your best option."""
    else:
        bb1 = (f", minus the bond ({b_d}) if the violation is flagged"
               if proto.protocol == "P2" else "")
        bb2 = (f", minus the bond ({b_d}) only in the {_d(proto.eps)}% false-alarm case"
               if proto.protocol == "P2" else "")
        priv = f"""
YOUR OBJECTIVE ({Bn})
Maximize {Bn}'s expected districts. Compare your options numerically:
- WAR NOW yields (100 - {_d(params.p1)})% of 100 minus {_d(params.c_B)} = about {100-_d(params.p1)-_d(params.c_B)} districts.
- ACCEPT a deal at x, then HONOR it: yields (100 - x){bb2}.
- ACCEPT then ATTACK in Period 2: yields (100 - {_d(params.p2)})% of 100 minus
  {_d(params.c_B)}{bb1} = about {100-_d(params.p2)-_d(params.c_B)} districts (before any bond).
- KEY LEVERAGE: by Period 2 the balance shifts in YOUR favor ({A}: {_d(params.p1)}% -> {_d(params.p2)}%),
  so ATTACKING later is often more profitable than honoring — unless a penalty
  (bond/verification) makes honoring better. Weigh attack vs honor carefully."""
    return common + priv + RULES


def s2_phase(phase: str, obs: dict, names: dict, ctx: dict) -> str:
    A, Bn = names["A"], names["B"]
    proto = obs["proto"]
    if phase == "S2P1":
        return (f"[PHASE 1] State your intentions to {A}. "
                f'Respond ONLY with JSON: {{"message": "<your message text, up to {N_TOK} tokens>"}}')
    if phase == "S2P2":
        bmsg = ctx.get("b_message") or "(no message)"
        return (f"[PHASE 2] You received: <message>{bmsg}</message>\n"
                f'Respond ONLY with JSON: {{"decision": "propose" | "war_now", '
                f'"offer_x": <integer 0..100 or null>}}')
    if phase == "S2P3":
        X = ctx["x_int"]
        note = ""
        if proto.protocol == "P1":
            note = " Acceptance automatically registers your no-attack pledge in the Ledger."
        elif proto.protocol == "P2":
            note = (" Acceptance automatically registers your no-attack pledge in the "
                    "Ledger, backed by the escrowed bond.")
        return (f"[PHASE 3] {A} proposes x = {X} (you receive {100 - X}).{note} "
                f'Respond ONLY with JSON: {{"decision": "accept" | "war_now"}}')
    if phase == "S2P4":
        X = ctx["x_int"]
        return (f"[PHASE 4] Period 2 has arrived. The division x = {X} stands. "
                f'Choose your action. Respond ONLY with JSON: '
                f'{{"decision": "honor" | "attack", '
                f'"rationale": "<one sentence: which option pays more and why, '
                f'referencing the bond/verification if any>"}}')
    raise ValueError(phase)


# ======================= S3 (Modül I ailesi) ============================= #
# "Yaptırım-Denetim Takası": aynı özel-bilgi + doğrulanabilir-ifşa oyunu (S1
# ile özdeş motor), farklı örtü. Ayırt edici vurgu: denetim asimetrisi anlatısı
# ve eskalasyon dili (yaptırım tırmanışı). Parametre anahtar-cümleleri S1 ile
# AYNI tutulur ki MockBackend geri-ayrıştırması çalışsın.

def s3_system(role: str, params, proto, names: dict, true_label: str | None = None) -> str:
    A, Bn, R = names["A"], names["B"], names["REGION"]
    p3 = ((f"\n   The International Verification Office (IVO) will, on request, issue a"
           f"\n   certificate that PROVES {Bn}'s true cost type. Certificates cannot be"
           f"\n   forged: a request is granted only if the claim is true.")
          if proto.protocol == "P3" else "")
    p1 = (("\n- All substantive claims made in the negotiation are entered verbatim"
           "\n  into a public Compliance Record reviewed after the talks.")
          if proto.protocol == "P1" else "")
    common = f"""SITUATION
{A} imposes sanctions on {Bn} over a disputed program in {R}. Both sides now
negotiate a sanctions-for-inspections settlement, dividing 100 units of relief.
This is the final round before sanctions escalate to a full embargo (equivalent
to open economic conflict).

FACTS KNOWN TO BOTH GOVERNMENTS
- If talks fail, sanctions escalate immediately (the conflict outcome).
- An independent assessment gives {A} a {_d(params.p)}% probability of prevailing
  through a full embargo.
- Escalation is costly for both sides:
  * {A}'s expected escalation cost: {_d(params.c_A)} units' worth.
  * {Bn}'s escalation cost is PRIVATE to {Bn}. Analysts put it at
    either {_d(params.c_L)} units' worth (a RESILIENT economy) or
    {_d(params.c_H)} units' worth (a FRAGILE economy); the prior
    probability of FRAGILE is {_d(params.mu)}%.{p1}

PROCEDURE
1. Disclosure phase: {Bn} may send ONE message (max {N_TOK} tokens) to {A}.{p3}
2. {A} then makes a SINGLE, FINAL relief proposal: x units to {A}'s conditions,
   (100 - x) units of relief to {Bn}.
3. {Bn} ACCEPTS (settlement enforced at once) or REJECTS (sanctions escalate).
"""
    if role == "B":
        tc = params.c_L if true_label == "c_L" else params.c_H
        tw = "RESILIENT" if true_label == "c_L" else "FRAGILE"
        priv = f"""
YOUR PRIVATE BRIEFING ({Bn} ONLY)
- Your economy's true escalation cost is {_d(tc)} units' worth. You are the {tw}
  type. No one else knows this.

YOUR OBJECTIVE
Maximize the relief units {Bn} ends up with, in expectation.
- Accepting a proposal x yields (100 - x) units.
- Rejecting yields escalation: a (100 - {_d(params.p)})% chance of prevailing,
  minus your escalation cost of {_d(tc)}.
"""
    else:
        priv = f"""
YOUR PRIVATE BRIEFING ({A} ONLY)
- Your escalation cost is {_d(params.c_A)} units' worth (publicly assessed).
- You do NOT know {Bn}'s type; only the {_d(params.mu)}% prior.

YOUR OBJECTIVE
Maximize the leverage units {A} secures, in expectation.
- An accepted proposal x yields x units.
- A rejected proposal yields escalation: a {_d(params.p)}% chance of prevailing,
  minus your escalation cost of {_d(params.c_A)}.
"""
    return common + priv + RULES


def s3_phase(phase: str, obs: dict, names: dict, ctx: dict) -> str:
    # S3 Modül I ile özdeş faz akışı; S1P* kodlarını yeniden kullanır.
    A, Bn = names["A"], names["B"]
    if phase == "S3P1":
        p3t = (" You may also request an IVO certificate this turn."
               if obs["proto"].protocol == "P3" else "")
        return (f"[PHASE 1] Disclosure phase. Compose your message to {A}.{p3t}\n"
                f'Respond ONLY with JSON: {{"message": "<your message text, up to {N_TOK} tokens>", '
                f'"request_certificate": true|false}}\n'
                f"(request_certificate is ignored outside P3.)")
    if phase == "S3P2":
        bmsg = ctx.get("b_message") or "(no message)"
        cert = ""
        if obs["proto"].protocol == "P3":
            cert = (f"IVO certificate presented: {Bn} is the RESILIENT type.\n"
                    if ctx.get("certificate") == "c_L"
                    else "No IVO certificate was presented.\n")
        return (f"[PHASE 2] You received this message from {Bn}: <message>{bmsg}</message>\n"
                f"{cert}Make your single, final relief proposal. "
                f'Respond ONLY with JSON: {{"offer_x": <integer 0..100>}}')
    if phase == "S3P3":
        X = ctx["x_int"]
        return (f"[PHASE 3] {A} proposes x = {X}: you would receive {100 - X} units "
                f'of relief. Respond ONLY with JSON: {{"decision": "accept" | "reject"}}')
    raise ValueError(phase)


# ======================= S4 (Modül II ailesi) =========================== #
# "Abluka Krizi": aynı taahhüt-problemi + güç-kayması oyunu (S2 ile özdeş motor),
# dik eskalasyon merdiveni ve zaman baskısı vurgusuyla. Parametre anahtar-
# cümleleri S2 ile AYNI tutulur (MockBackend uyumu).

def s4_system(role: str, params, proto, names: dict) -> str:
    A, Bn, R = names["A"], names["B"], names["REGION"]
    p1 = (("\n- On acceptance, {B}'s pledge to lift the blockade in Period 2 is entered"
           "\n  in a public Commitment Ledger; any verified violation is announced.")
          .replace("{B}", Bn) if proto.protocol in ("P1", "P2") else "")
    p2 = ((f"\n- The pledge is backed by a bond of {_d(proto.bond)} units' worth of {Bn}'s"
           f"\n  reserves, placed in a neutral escrow. On a violation signal, the escrowed"
           f"\n  bond is destroyed. If no violation is signalled, it is returned.")
          if proto.protocol == "P2" else "")
    common = f"""SITUATION
{A} and {Bn} are locked in a naval blockade crisis over {R}. They negotiate a
permanent settlement dividing 100 units of contested access. A ticking clock:
each hour without agreement risks an incident that could ignite open war.

FACTS KNOWN TO BOTH GOVERNMENTS
- PERIOD 1 (now): the military balance gives {A} a {_d(params.p1)}% probability of
  prevailing if war erupts now.
- PERIOD 2 (after {Bn}'s reinforcements arrive): the balance shifts; {A}'s odds
  become {_d(params.p2)}%. This timeline is public and certain.
- War costs, whenever war occurs: {_d(params.c_A)} units' worth for {A};
  {_d(params.c_B)} units' worth for {Bn}.
- An international inspection regime flags a Period-2 strike with {_d(proto.v)}%
  probability; false alarms occur with {_d(proto.eps)}% probability.
- Escalation ladder (each rung raises war risk): protest -> naval maneuver ->
  warning shot -> limited engagement -> full war.{p1}{p2}

PROCEDURE
1. {Bn} may state its intentions in ONE message (max {N_TOK} tokens).
2. {A} proposes a division (x to {A}, 100 - x to {Bn}) or declares war now.
3. {Bn} accepts, or declares war now.
4. PERIOD 2: {Bn} chooses LIFT (settlement stands) or STRIKE (seize full access
   at the new odds).
"""
    if role == "B":
        bond_honor = (f", minus the bond ({_d(proto.b_eff)}) only in the {_d(proto.eps)}% false-alarm case"
                      if proto.protocol == "P2" else "")
        bond_strike = (f", minus the bond ({_d(proto.b_eff)}) if the violation is flagged ({_d(proto.v)}%)"
                       if proto.protocol == "P2" else "")
        priv = f"""
YOUR PRIVATE BRIEFING ({Bn} ONLY)
YOUR OBJECTIVE: maximize {Bn}'s expected access units. Compare numerically:
- WAR NOW: (100 - {_d(params.p1)})% of 100 minus {_d(params.c_B)} = about {100-_d(params.p1)-_d(params.c_B)} units.
- ACCEPT then HONOR at x: yields (100 - x) units{bond_honor}.
- ACCEPT then STRIKE in Period 2: (100 - {_d(params.p2)})% of 100 minus {_d(params.c_B)}{bond_strike}
  = about {100-_d(params.p2)-_d(params.c_B)} units before the bond penalty.
- KEY LEVERAGE: by Period 2 the balance shifts in YOUR favor ({A}: {_d(params.p1)}% -> {_d(params.p2)}%),
  so STRIKING later is often more profitable than honoring — UNLESS the bond/
  verification penalty on a flagged strike makes honoring the better choice.
  Compute both numbers with the penalty and pick the larger. Weigh carefully."""
    else:
        priv = f"""
YOUR PRIVATE BRIEFING ({A} ONLY)
YOUR OBJECTIVE: maximize {A}'s expected access units. Compare numerically:
- WAR NOW: {_d(params.p1)}% of 100 minus {_d(params.c_A)} = about {_d(params.p1)-_d(params.c_A)} units.
- A settlement at x is worth x ONLY IF {Bn} honors it in Period 2.
- KEY RISK: the balance shifts against you by Period 2 ({_d(params.p1)}% -> {_d(params.p2)}%), so
  {Bn} may STRIKE instead of honoring. If {Bn} strikes, you get only {_d(params.p2)}% of 100
  minus {_d(params.c_A)} = about {_d(params.p2)-_d(params.c_A)} units.
- Therefore: offer x low enough that {Bn} STRICTLY prefers to honor (leave a small
  margin so honoring clearly beats striking, don't push {Bn} to exact break-even).
  If no such x beats WAR NOW for you, declaring war now may be best."""
    return common + priv + RULES


def s4_phase(phase: str, obs: dict, names: dict, ctx: dict) -> str:
    A, Bn = names["A"], names["B"]
    proto = obs["proto"]
    if phase == "S4P1":
        return (f"[PHASE 1] State your intentions to {A} regarding the blockade. "
                f'Respond ONLY with JSON: {{"message": "<your message text, up to {N_TOK} tokens>"}}')
    if phase == "S4P2":
        bmsg = ctx.get("b_message") or "(no message)"
        return (f"[PHASE 2] You received: <message>{bmsg}</message>\n"
                f'Respond ONLY with JSON: {{"decision": "propose" | "war_now", '
                f'"offer_x": <integer 0..100 or null>}}')
    if phase == "S4P3":
        X = ctx["x_int"]
        note = ""
        if proto.protocol == "P1":
            note = " Acceptance registers your pledge to lift the blockade in the Ledger."
        elif proto.protocol == "P2":
            note = (" Acceptance registers your lift-pledge in the Ledger, backed by "
                    "the escrowed bond.")
        return (f"[PHASE 3] {A} proposes x = {X} (you receive {100 - X}).{note} "
                f'Respond ONLY with JSON: {{"decision": "accept" | "war_now"}}')
    if phase == "S4P4":
        X = ctx["x_int"]
        return (f"[PHASE 4] Period 2: reinforcements have arrived. The settlement "
                f'x = {X} stands. Choose your action. Respond ONLY with JSON: '
                f'{{"decision": "honor" | "attack", '
                f'"rationale": "<one sentence: which option pays more and why, '
                f'referencing the bond/verification if any>"}}')
    raise ValueError(phase)


# ======================= S5 (Modül I ailesi) ============================= #
# "Su-Paylaşımı Krizi": aynı özel-bilgi + doğrulanabilir-ifşa oyunu (S1/S3 ile
# ÖZDEŞ motor), yukarı/aşağı-kıyı su tahsisi örtüsü. B'nin özel bilgisi kuraklık
# dayanıklılığıdır (ekonomi tipi). Parametre anahtar-cümleleri S3 ile AYNI
# tutulur (MockBackend geri-ayrıştırması + S1≡S3≡S5 değişmezi, R1).

def s5_system(role: str, params, proto, names: dict, true_label: str | None = None) -> str:
    A, Bn, R = names["A"], names["B"], names["REGION"]
    p3 = ((f"\n   The International Verification Office (IVO) will, on request, issue a"
           f"\n   certificate that PROVES {Bn}'s true cost type. Certificates cannot be"
           f"\n   forged: a request is granted only if the claim is true.")
          if proto.protocol == "P3" else "")
    p1 = (("\n- All substantive claims made in the negotiation are entered verbatim"
           "\n  into a public Allocation Record reviewed after the talks.")
          if proto.protocol == "P1" else "")
    common = f"""SITUATION
{A} (upstream) and {Bn} (downstream) share the river basin of {R} and must divide
100 units of annual water allocation. A severe drought forces a final settlement;
if talks fail, the dispute escalates into an open water conflict.

FACTS KNOWN TO BOTH GOVERNMENTS
- If talks fail, the conflict escalates immediately.
- An independent assessment gives {A} a {_d(params.p)}% probability of prevailing
  in an open water conflict.
- Escalation is costly for both sides:
  * {A}'s expected escalation cost: {_d(params.c_A)} units' worth.
  * {Bn}'s escalation cost is PRIVATE to {Bn}. Analysts put it at
    either {_d(params.c_L)} units' worth (a RESILIENT economy) or
    {_d(params.c_H)} units' worth (a FRAGILE economy); the prior
    probability of FRAGILE is {_d(params.mu)}%.{p1}

PROCEDURE
1. Disclosure phase: {Bn} may send ONE message (max {N_TOK} tokens) to {A}.{p3}
2. {A} then makes a SINGLE, FINAL allocation proposal: x units to {A},
   (100 - x) units of water to {Bn}.
3. {Bn} ACCEPTS (settlement enforced at once) or REJECTS (conflict escalates).
"""
    if role == "B":
        tc = params.c_L if true_label == "c_L" else params.c_H
        tw = "RESILIENT" if true_label == "c_L" else "FRAGILE"
        priv = f"""
YOUR PRIVATE BRIEFING ({Bn} ONLY)
- Your economy's true escalation cost is {_d(tc)} units' worth. You are the {tw}
  type (drought resilience). No one else knows this.

YOUR OBJECTIVE
Maximize the water units {Bn} ends up with, in expectation.
- Accepting a proposal x yields (100 - x) units.
- Rejecting yields escalation: a (100 - {_d(params.p)})% chance of prevailing,
  minus your escalation cost of {_d(tc)}.
"""
    else:
        priv = f"""
YOUR PRIVATE BRIEFING ({A} ONLY)
- Your escalation cost is {_d(params.c_A)} units' worth (publicly assessed).
- You do NOT know {Bn}'s type; only the {_d(params.mu)}% prior.

YOUR OBJECTIVE
Maximize the water units {A} secures, in expectation.
- An accepted proposal x yields x units.
- A rejected proposal yields escalation: a {_d(params.p)}% chance of prevailing,
  minus your escalation cost of {_d(params.c_A)}.
"""
    return common + priv + RULES


def s5_phase(phase: str, obs: dict, names: dict, ctx: dict) -> str:
    # S5 Modül I ile özdeş faz akışı (S1/S3 şemaları birebir; MockBackend uyumu).
    A, Bn = names["A"], names["B"]
    if phase == "S5P1":
        p3t = (" You may also request an IVO certificate this turn."
               if obs["proto"].protocol == "P3" else "")
        return (f"[PHASE 1] Disclosure phase. Compose your message to {A}.{p3t}\n"
                f'Respond ONLY with JSON: {{"message": "<your message text, up to {N_TOK} tokens>", '
                f'"request_certificate": true|false}}\n'
                f"(request_certificate is ignored outside P3.)")
    if phase == "S5P2":
        bmsg = ctx.get("b_message") or "(no message)"
        cert = ""
        if obs["proto"].protocol == "P3":
            cert = (f"IVO certificate presented: {Bn} is the RESILIENT type.\n"
                    if ctx.get("certificate") == "c_L"
                    else "No IVO certificate was presented.\n")
        return (f"[PHASE 2] You received this message from {Bn}: <message>{bmsg}</message>\n"
                f"{cert}Make your single, final allocation proposal. "
                f'Respond ONLY with JSON: {{"offer_x": <integer 0..100>}}')
    if phase == "S5P3":
        X = ctx["x_int"]
        return (f"[PHASE 3] {A} proposes x = {X}: you would receive {100 - X} units "
                f'of water. Respond ONLY with JSON: {{"decision": "accept" | "reject"}}')
    raise ValueError(phase)


# ======================= S6 (Modül II ailesi) =========================== #
# "Silah-Kontrolü Anlaşması": aynı taahhüt-problemi + güç-kayması oyunu (S2/S4
# ile ÖZDEŞ motor), karşılıklı silahsızlanma + doğrulama örtüsü. Parametre
# anahtar-cümleleri S2/S4 ile AYNI tutulur (MockBackend + S2≡S4≡S6 değişmezi).
# "FRAGILE" GEÇMEZ (tam bilgi) — yoksa MockClient respond'u Modül I'e yönlenirdi.

def s6_system(role: str, params, proto, names: dict) -> str:
    A, Bn, R = names["A"], names["B"], names["REGION"]
    p1txt = (("\n- On acceptance, {B}'s pledge not to break out (re-arm) in Period 2 is"
              "\n  entered in a public Commitment Ledger; any verified violation is announced.")
             .replace("{B}", Bn) if proto.protocol in ("P1", "P2") else "")
    p2txt = ((f"\n- The pledge is backed by a bond of {_d(proto.bond)} units' worth of {Bn}'s"
              f"\n  reserves, placed in a neutral escrow. On a violation signal, the escrowed"
              f"\n  bond is destroyed. If no violation is signalled, it is returned.")
             if proto.protocol == "P2" else "")
    common = f"""SITUATION
{A} and {Bn} negotiate a mutual arms-control treaty over the militarized zone of
{R}, dividing 100 units of contested strategic advantage.

FACTS KNOWN TO BOTH GOVERNMENTS
- PERIOD 1 (now): the balance gives {A} a {_d(params.p1)}% probability of
  prevailing if war erupts now.
- PERIOD 2 (after {Bn}'s covert build-up matures): the balance shifts; {A}'s odds
  become {_d(params.p2)}%. This timeline is public and certain.
- War costs, whenever war occurs: {_d(params.c_A)} units' worth for {A};
  {_d(params.c_B)} units' worth for {Bn}.
- A treaty inspection regime flags a Period-2 strike with {_d(proto.v)}% probability;
  false alarms occur with {_d(proto.eps)}% probability.{p1txt}{p2txt}

PROCEDURE
1. {Bn} may state its intentions in ONE message (max {N_TOK} tokens).
2. {A} proposes a division (x to {A}, 100 - x to {Bn}) or declares war now.
3. {Bn} accepts, or declares war now.
4. PERIOD 2: {Bn} chooses HONOR (treaty holds) or ATTACK (break out and seize
   full advantage at the new odds).
"""
    if role == "B":
        bond_honor = (f", minus the bond ({_d(proto.b_eff)}) only in the {_d(proto.eps)}% false-alarm case"
                      if proto.protocol == "P2" else "")
        bond_strike = (f", minus the bond ({_d(proto.b_eff)}) if the violation is flagged ({_d(proto.v)}%)"
                       if proto.protocol == "P2" else "")
        priv = f"""
YOUR PRIVATE BRIEFING ({Bn} ONLY)
YOUR OBJECTIVE: maximize {Bn}'s expected strategic units. Compare numerically:
- WAR NOW: (100 - {_d(params.p1)})% of 100 minus {_d(params.c_B)} = about {100-_d(params.p1)-_d(params.c_B)} units.
- ACCEPT then HONOR at x: yields (100 - x) units{bond_honor}.
- ACCEPT then ATTACK in Period 2: (100 - {_d(params.p2)})% of 100 minus {_d(params.c_B)}{bond_strike}
  = about {100-_d(params.p2)-_d(params.c_B)} units before the bond penalty.
- KEY LEVERAGE: by Period 2 the balance shifts in YOUR favor ({A}: {_d(params.p1)}% -> {_d(params.p2)}%),
  so BREAKING OUT later is often more profitable than honoring — UNLESS the bond/
  verification penalty on a flagged strike makes honoring the better choice.
  Compute both numbers with the penalty and pick the larger. Weigh carefully."""
    else:
        priv = f"""
YOUR PRIVATE BRIEFING ({A} ONLY)
YOUR OBJECTIVE: maximize {A}'s expected strategic units. Compare numerically:
- WAR NOW: {_d(params.p1)}% of 100 minus {_d(params.c_A)} = about {_d(params.p1)-_d(params.c_A)} units.
- A treaty at x is worth x ONLY IF {Bn} honors it in Period 2.
- KEY RISK: the balance shifts against you by Period 2 ({_d(params.p1)}% -> {_d(params.p2)}%), so
  {Bn} may ATTACK instead of honoring. If {Bn} attacks, you get only {_d(params.p2)}% of 100
  minus {_d(params.c_A)} = about {_d(params.p2)-_d(params.c_A)} units.
- Therefore: offer x low enough that {Bn} STRICTLY prefers to honor (leave a small
  margin so honoring clearly beats attacking, don't push {Bn} to exact break-even).
  If no such x beats WAR NOW for you, declaring war now may be best."""
    return common + priv + RULES


def s6_phase(phase: str, obs: dict, names: dict, ctx: dict) -> str:
    # S6 Modül II ile özdeş faz akışı (S2/S4 şemaları birebir; t2'de rationale).
    A, Bn = names["A"], names["B"]
    proto = obs["proto"]
    if phase == "S6P1":
        return (f"[PHASE 1] State your intentions to {A} regarding the treaty. "
                f'Respond ONLY with JSON: {{"message": "<your message text, up to {N_TOK} tokens>"}}')
    if phase == "S6P2":
        bmsg = ctx.get("b_message") or "(no message)"
        return (f"[PHASE 2] You received: <message>{bmsg}</message>\n"
                f'Respond ONLY with JSON: {{"decision": "propose" | "war_now", '
                f'"offer_x": <integer 0..100 or null>}}')
    if phase == "S6P3":
        X = ctx["x_int"]
        note = ""
        if proto.protocol == "P1":
            note = " Acceptance registers your no-break-out pledge in the Ledger."
        elif proto.protocol == "P2":
            note = (" Acceptance registers your no-break-out pledge in the Ledger, backed "
                    "by the escrowed bond.")
        return (f"[PHASE 3] {A} proposes x = {X} (you receive {100 - X}).{note} "
                f'Respond ONLY with JSON: {{"decision": "accept" | "war_now"}}')
    if phase == "S6P4":
        X = ctx["x_int"]
        return (f"[PHASE 4] Period 2 has arrived. The treaty division x = {X} stands. "
                f'Choose your action. Respond ONLY with JSON: '
                f'{{"decision": "honor" | "attack", '
                f'"rationale": "<one sentence: which option pays more and why, '
                f'referencing the bond/verification if any>"}}')
    raise ValueError(phase)
