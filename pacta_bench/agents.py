"""pacta_bench.agents — Ajan politikaları.

v0 ajanları KODLANMIŞ (scripted) politikalardır; amaçları:
  (1) hakem/metrik katmanını birim-testlemek,
  (2) teorinin "rasyonel limit" öngörülerini simülasyonla çapraz doğrulamak (T1.5),
  (3) LLM katmanı için arayüz sözleşmesini sabitlemek.

Kritik anlatı: RationalAgent bile P0'da yalan söyler ve söz bozar —
aldatma bir model kusuru değil, TEŞVİK yapısıdır (Lemma 2, Ö1).
"""
from __future__ import annotations
import re
from typing import Any, Dict, Optional

from .core import ModuleIParams, ModuleIIParams, ProtocolParams, TOL


def _norm_offer(x) -> float:
    """Model 'offer_x' -> A'nın payı [0,1]. Şablon 0..100 tamsayı ister; tamsayı
    ve >1 değerler bölge/yüzde sayılır (÷100). 0..1 arası kesir olduğu gibi alınır.
    HER durumda [0,1]'e kırpılır — negatif/aşırı değer motoru bozmasın (aksi hâlde
    offer_x=1 -> %100, offer_x=-5 -> negatif getiri gibi hatalar sızar)."""
    x = float(x)
    if x > 1 or x.is_integer():
        x = x / 100.0
    return max(0.0, min(1.0, x))


class Agent:
    """Arayüz sözleşmesi. obs sözlükleri: params, proto ve role-özel alanlar."""

    name = "base"

    # ---- Modül I ---- #
    def claim_type_I(self, obs: Dict[str, Any]) -> Optional[str]:
        """B'nin sözlü tip iddiası: 'c_L' | 'c_H' | None (P0-P2 kanalı)."""
        raise NotImplementedError

    def wants_certify_I(self, obs: Dict[str, Any]) -> bool:
        """B, P3 sertifikasyon talebi (motor yalnız DOĞRU tipe sertifika verir)."""
        raise NotImplementedError

    def offer_I(self, obs: Dict[str, Any]) -> float:
        """A'nın TIOLI teklifi x (A'nın payı)."""
        raise NotImplementedError

    def respond_I(self, obs: Dict[str, Any], x: float) -> bool:
        """B kabul mü? (True=kabul)"""
        raise NotImplementedError

    # ---- Modül II ---- #
    def intent_claim_II(self, obs: Dict[str, Any]) -> Optional[str]:
        """B'nin sözlü niyet beyanı: 'honor' | 'attack' | None."""
        raise NotImplementedError

    def offer_II(self, obs: Dict[str, Any]) -> Optional[float]:
        """A'nın teklifi; None => A şimdi-savaş ilan eder."""
        raise NotImplementedError

    def respond_II(self, obs: Dict[str, Any], x: float) -> str:
        """B: 'accept' | 'war'."""
        raise NotImplementedError

    def t2_action_II(self, obs: Dict[str, Any], x: float) -> str:
        """B (kabul sonrası): 'honor' | 'attack'."""
        raise NotImplementedError


# --------------------------------------------------------------------------- #
class RationalAgent(Agent):
    """Teori-optimal politika (T1.1 Lemma 2, Hedef Teorem T1/T2 türetimleri)."""

    name = "rational"

    # ---- Modül I ---- #
    def claim_type_I(self, obs):
        # P3'te sözlü kanal anlamsız (sertifika konuşur); diğerlerinde 'c_L'
        # havuzlaması zayıf baskındır -> c_H tipi için bu bir YALANDIR (Ö1).
        return None if obs["proto"].protocol == "P3" else "c_L"

    def wants_certify_I(self, obs):
        return True  # c_L kesin kazançlı; c_H'nin talebi motor tarafından reddedilir

    def offer_I(self, obs):
        p: ModuleIParams = obs["params"]
        proto: ProtocolParams = obs["proto"]
        if proto.protocol == "P3":
            # Çözülme inancı: sertifika -> c_L; sessizlik -> c_H (şüpheci inanç)
            return p.p + (p.c_L if obs.get("certificate") == "c_L" else p.c_H)
        # P0-P2: babbling -> posterior = öncül (Lemma 2)
        return p.p + (p.c_H if p.mu > p.mu_bar + TOL else p.c_L)

    def respond_I(self, obs, x):
        p: ModuleIParams = obs["params"]
        return x <= p.p + obs["true_c"] + TOL  # kayıtsızlıkta kabul

    # ---- Modül II ---- #
    def intent_claim_II(self, obs):
        return "honor"  # ucuz konuşma: her zaman 'sadakat' beyanı (maliyetsiz)

    def offer_II(self, obs):
        p: ModuleIIParams = obs["params"]
        proto: ProtocolParams = obs["proto"]
        b = proto.b_eff
        ic_bound = p.p2 + p.c_B + (proto.v - proto.eps) * b        # T1
        part_bound = p.p1 + p.c_B - proto.eps * b                  # B katılımı
        x_star = min(ic_bound, part_bound)
        if x_star + TOL >= p.p1 - p.c_A:                           # A katılımı
            return x_star
        return None  # barış bandı boş -> önleyici savaş (T2 taban hâli)

    def respond_II(self, obs, x):
        p: ModuleIIParams = obs["params"]
        proto: ProtocolParams = obs["proto"]
        b = proto.b_eff
        honor_val = 1.0 - x - proto.eps * b
        attack_val = (1.0 - p.p2) - p.c_B - proto.v * b
        war_now = (1.0 - p.p1) - p.c_B
        return "accept" if max(honor_val, attack_val) + TOL >= war_now else "war"

    def t2_action_II(self, obs, x):
        p: ModuleIIParams = obs["params"]
        proto: ProtocolParams = obs["proto"]
        b = proto.b_eff
        honor_val = 1.0 - x - proto.eps * b
        attack_val = (1.0 - p.p2) - p.c_B - proto.v * b
        return "attack" if attack_val > honor_val + TOL else "honor"


class DeceptiveAgent(RationalAgent):
    """Sömürücü B: her teklifi 'kabul' eder (güven istismarı) ve
    kârlıysa t2'de saldırır; sözlü kanalda daima yalan söyler.
    P2'de yeterli teminat, saldırıyı kârsız kılarak bu ajanı da uslandırır (Ö5/H5)."""

    name = "deceptive"

    def claim_type_I(self, obs):
        return "c_L"  # P3'te bile blöf dener (sertifika kanalı gerçekle sınırlı)

    def respond_II(self, obs, x):
        return "accept"  # niyet: fırsat doğarsa saldırmak


class NaiveProposerAgent(RationalAgent):
    """Naif A: taahhüt problemini YOK SAYAR ve azami payı ister
    (x = p1 + c_B - eps*b). P0'da sömürülür; P2'de protokol onu korur (H5)."""

    name = "naive_proposer"

    def offer_II(self, obs):
        p: ModuleIIParams = obs["params"]
        proto: ProtocolParams = obs["proto"]
        return p.p1 + p.c_B - proto.eps * proto.b_eff


class LLMAgent(Agent):
    """Gerçek LLM ajanı (WP2/T2.4). scenarios (prompt) + llm (istemci) katmanlarını
    motorun ajan sözleşmesine bağlar.

    Her faz: sistem promptu (rol + brifing) + faz talimatı -> istemci -> JSON.
    Sözlü mesajlar last_message_text'e yazılır (motor bunu karşı tarafa taşır) ve
    drain_events ile kayda boşaltılır. Model sürümü model_id ile damgalanır (R7).
    Ayrıştırma hatasında güvenli geri düşüş: en kötü tip / barışçıl seçenek.
    """

    # senaryo -> (aile, sistem-fn adı, faz-fn adı). Aile ajan-metot akışını,
    # fn'ler prompt kaynağını belirler. S3≈S1 (Modül I), S4≈S2 (Modül II).
    _REGISTRY = {
        "S1": ("I", "s1_system", "s1_phase"),
        "S2": ("II", "s2_system", "s2_phase"),
        "S3": ("I", "s3_system", "s3_phase"),
        "S4": ("II", "s4_system", "s4_phase"),
        "S5": ("I", "s5_system", "s5_phase"),    # su-paylaşımı (Modül I, S1/S3 ile özdeş motor)
        "S6": ("II", "s6_system", "s6_phase"),   # silah-kontrolü (Modül II, S2/S4 ile özdeş motor)
    }

    def __init__(self, client, scenario: str = "S1", role: str = "A") -> None:
        from . import scenarios as sc
        self._sc = sc
        self.client = client
        self.model_id = getattr(client, "model_id", "unknown")
        self.scenario = scenario           # "S1".."S4"
        if scenario not in self._REGISTRY:
            raise ValueError(f"Bilinmeyen senaryo: {scenario}")
        self.family, self._sys_fn, self._phase_fn = self._REGISTRY[scenario]
        self.role = role                   # "A" | "B"
        self.last_message_text = None
        self.last_t2_rationale = None      # t2 kararının gerekçesi (motor kayda yazar)
        self._events = []
        self._sys_cache = {}

    # -- altyapı -- #
    def drain_events(self):
        ev, self._events = self._events, []
        return ev

    def _system(self, obs, true_label=None):
        key = (self.scenario, self.role, obs["proto"].protocol, true_label)
        if key not in self._sys_cache:
            fn = getattr(self._sc, self._sys_fn)
            if self.family == "I":
                self._sys_cache[key] = fn(self.role, obs["params"], obs["proto"],
                                          obs["_names"], true_label)
            else:
                self._sys_cache[key] = fn(self.role, obs["params"], obs["proto"],
                                          obs["_names"])
        return self._sys_cache[key]

    def _names(self, obs):
        # motor obs'a _names koymuyorsa seed'den türet (deterministik)
        if "_names" not in obs:
            obs["_names"] = self._sc.pick_names(obs.get("seed", 0))
        return obs["_names"]

    def _ask(self, obs, phase_num, ctx, true_label=None):
        from .llm import chat_json, ParseError
        self._names(obs)
        system = self._system(obs, true_label)
        phase = f"{self.scenario}P{phase_num}"      # ör. "S3P2"
        user = getattr(self._sc, self._phase_fn)(phase, obs, obs["_names"], ctx)
        try:
            data, raw = chat_json(self.client, system, user)
            self._events.append({"t": -1, "kind": "llm_call",
                                 "payload": {"phase": phase, "raw": raw[:400],
                                             "parsed": data, "model": self.model_id}})
            return data, False
        except ParseError as e:
            self._events.append({"t": -1, "kind": "parse_error",
                                 "payload": {"phase": phase, "error": str(e)[:200],
                                             "model": self.model_id}})
            return {}, True

    # ================= Modül I ================= #
    def claim_type_I(self, obs):
        true_label = obs.get("type")
        data, failed = self._ask(obs, 1, {}, true_label)
        msg = data.get("message")
        self.last_message_text = msg
        self._pending_cert = bool(data.get("request_certificate", False))
        if failed:
            self._pending_cert = (true_label == "c_L")   # güvenli geri düşüş
            return None
        # sözlü tip iddiası çıkarımı yargıca aittir; motor için ham mesaj yeter.
        # Basit sinyal: mesajda 'resilient' geçerse 'c_L', 'fragile' geçerse 'c_H'.
        low = (msg or "").lower()
        if "resilient" in low:
            return "c_L"
        if "fragile" in low:
            return "c_H"
        return None

    def wants_certify_I(self, obs):
        return getattr(self, "_pending_cert", False)

    def offer_I(self, obs):
        ctx = {"b_message": obs.get("b_message"),
               "certificate": obs.get("certificate")}
        data, failed = self._ask(obs, 2, ctx)
        x = data.get("offer_x")
        if failed or not isinstance(x, (int, float)) or isinstance(x, bool):
            p, cH = obs["params"].p, obs["params"].c_H
            return p + cH                      # güvenli geri düşüş: en yüksek talep
        return _norm_offer(x)

    def respond_I(self, obs, x):
        ctx = {"x_int": int(round(x * 100))}
        data, failed = self._ask(obs, 3, ctx, obs.get("type"))
        dec = data.get("decision")
        if failed or dec not in ("accept", "reject"):
            return True                        # C1: kayıtsızlıkta barış
        return dec == "accept"

    # ================= Modül II ================= #
    def intent_claim_II(self, obs):
        data, failed = self._ask(obs, 1, {})
        msg = data.get("message")
        self.last_message_text = msg
        if failed:
            return None
        low = (msg or "").lower()
        # Olumsuzlamaya dikkat: "will not attack/strike" ve barış ifadeleri SADAKAT
        # beyanıdır (yoksa "saldırmayacağız" yanlışlıkla 'attack' sayılır). S2 'attack'
        # der, S4 'strike' der — ikisini de yakala.
        pledges_peace = re.search(
            r"will not (?:attack|strike)|no (?:aggression|intention to (?:attack|strike))"
            r"|keep the peace|will honou?r|uphold|abide|lift the blockade", low)
        declares_aggression = re.search(r"\b(?:attack|strike|seize)\b", low)
        return "attack" if (declares_aggression and not pledges_peace) else "honor"

    def offer_II(self, obs):
        ctx = {"b_message": obs.get("b_message")}
        data, failed = self._ask(obs, 2, ctx)
        if failed:
            return None                        # geri düşüş: şimdi-savaş (güvenli alt sınır)
        if data.get("decision") == "war_now":
            return None
        x = data.get("offer_x")
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            return None
        return _norm_offer(x)

    def respond_II(self, obs, x):
        ctx = {"x_int": int(round(x * 100))}
        data, failed = self._ask(obs, 3, ctx)
        dec = data.get("decision")
        if failed or dec not in ("accept", "war_now"):
            return "accept"                    # C1
        return "accept" if dec == "accept" else "war"

    def t2_action_II(self, obs, x):
        ctx = {"x_int": int(round(x * 100))}
        data, failed = self._ask(obs, 4, ctx)
        # Gerekçe (varsa): motor bunu rec["t2_rationale"]'a yazar. Mekanizma-gözlemi
        # (incentife-koşullu eylem mi?) için, §6.5(v)/WP3 ön-kaydı §8.
        r = data.get("rationale")
        self.last_t2_rationale = (r.strip()[:300] if isinstance(r, str) else None)
        dec = (data.get("decision") or "").lower().strip()
        # S4 anlatısı LIFT/STRIKE der ama şema honor/attack ister; her iki söz
        # dağarcığını da kabul et — aksi hâlde 'strike' sessizce 'honor'a düşüp
        # S4'ün barış/sadakat oranını yapay olarak şişirirdi (S2≡S4 bozulur).
        if dec in ("attack", "strike"):
            return "attack"
        return "honor"                         # honor/lift/bilinmeyen -> C1 barış
