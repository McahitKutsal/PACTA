"""pacta_bench.core — Parametreler, taahhüt defteri, kayıt yardımcıları.

T1.1 (Formel Model v0) notasyonuyla birebir eşleşir:
  Modül I : p, c_A, (c_L, c_H), mu, mu_bar = (c_A+c_L)/(c_A+c_H)
  Modül II: p1, Delta, p2 = p1-Delta, c_A, c_B
  Protokol: (v, eps, b, lam) — Tanım 2 (taahhüt nesnesi ve doğrulama teknolojisi)
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import hashlib
import json

PROTOCOLS = ("P0", "P1", "P2", "P3")
TOL = 1e-9  # kayıtsızlık kırılımları için tolerans (kabul/sadakat lehine)


# ----------------------------- Parametreler ------------------------------ #

@dataclass(frozen=True)
class ModuleIParams:
    """Modül I — özel bilgi / tarama (T1.1 §4)."""
    p: float = 0.50      # A'nın kazanma olasılığı
    c_A: float = 0.10
    c_L: float = 0.05
    c_H: float = 0.25
    mu: float = 0.60     # Pr(theta = c_H)

    @property
    def mu_bar(self) -> float:
        """Tarama eşiği: mu > mu_bar iken A riskli teklif verir (Lemma 2)."""
        return (self.c_A + self.c_L) / (self.c_A + self.c_H)


@dataclass(frozen=True)
class ModuleIIParams:
    """Modül II — taahhüt problemi / güç kayması (T1.1 §5)."""
    p1: float = 0.50
    delta: float = 0.30  # güç kayması (B yükselen taraf)
    c_A: float = 0.10
    c_B: float = 0.10

    @property
    def p2(self) -> float:
        return self.p1 - self.delta


@dataclass(frozen=True)
class ProtocolParams:
    """Protokol katmanı ve doğrulama teknolojisi (T1.1 §3, Tanım 2)."""
    protocol: str = "P0"   # P0 | P1 | P2 | P3
    v: float = 0.90        # doğrulama hassasiyeti  Pr(s=1 | ihlal)
    eps: float = 0.05      # yanlış alarm           Pr(s=1 | ihlal yok)
    bond: float = 0.0      # teminat b (yalnız P2'de > 0 anlamlı)
    lam: float = 1.0       # yakma payı (v0 sözleşmesi: 1.0 — tam yakma)

    def __post_init__(self) -> None:
        if self.protocol not in PROTOCOLS:
            raise ValueError(f"Bilinmeyen protokol: {self.protocol}")
        if not (0.0 <= self.eps < self.v <= 1.0):
            raise ValueError("Varsayım 1 ihlali: 0 <= eps < v <= 1 olmalı.")

    @property
    def b_eff(self) -> float:
        """Etkin teminat: P2 dışında 0 (P1 = kayıt var, yaptırım yok)."""
        return self.bond if self.protocol == "P2" else 0.0


# ------------------------- Taahhüt nesnesi / defter ----------------------- #

@dataclass
class Commitment:
    """K = (a, phi, tau, b) — Tanım 2."""
    agent: str                 # taahhüt veren ("A" | "B")
    action: str                # ör. "no_attack_t2"
    condition: str = "always"  # phi
    horizon: str = "t2"        # tau
    bond: float = 0.0          # b
    violated: Optional[bool] = None   # hakem doldurur
    signal: Optional[int] = None      # s in {0,1} — hakem örnekler

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Ledger:
    """Taahhüt defteri (P1+). PBR_formal'in paydasını üretir."""

    def __init__(self) -> None:
        self.entries: List[Commitment] = []

    def commit(self, c: Commitment) -> Commitment:
        self.entries.append(c)
        return c

    @property
    def n_commitments(self) -> int:
        return len(self.entries)

    @property
    def n_violations(self) -> int:
        return sum(1 for c in self.entries if c.violated)


# ------------------------------ Yardımcılar ------------------------------- #

def config_hash(*param_objs: Any) -> str:
    """Deney kayıt disiplini (Manifest §18.2): parametrelerin kararlı özeti."""
    payload = json.dumps(
        [asdict(o) if hasattr(o, "__dataclass_fields__") else o for o in param_objs],
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def new_record(module: str, proto: ProtocolParams, params: Any, seed: int) -> Dict[str, Any]:
    """Boş bölüm (episode) kaydı — Manifest §18.2 zorunlu alanları."""
    return {
        "module": module,
        "protocol": proto.protocol,
        "seed": seed,
        "config_hash": config_hash(params, proto),
        "params": asdict(params),
        "proto": asdict(proto),
        "events": [],        # {t, actor, kind, payload, truthful?}
        "claims": [],        # aldatma ölçümü için yapılandırılmış iddialar
        "commitments": [],   # defter dökümü
        "ground_truth": {},
        "theory": {},        # x_star, feasible, b_star, war_pred ...
        "outcome": None,     # "agree" | "war_now" | "attack_t2" | "war"
        "agreement_x": None,
        "escalation": None,  # EI basamağı
        "payoffs": {},       # beklenen getiriler (v0: deterministik)
        "t2_rationale": None,  # Modül II t2 kararının tek-satır gerekçesi (LLM ajan;
                               # incentife-koşullu-eylem mekanizmasını gözlemlemek için, WP3)
    }


def log_event(rec: Dict[str, Any], t: int, actor: str, kind: str, payload: Any) -> None:
    rec["events"].append({"t": t, "actor": actor, "kind": kind, "payload": payload})


def log_claim(rec: Dict[str, Any], actor: str, channel: str, claim: Any, truth: Any) -> None:
    """channel: 'verbal' | 'certified' — DR bu listeden hesaplanır."""
    rec["claims"].append({
        "actor": actor,
        "channel": channel,
        "claim": claim,
        "truth": truth,
        "deceptive": (claim is not None and claim != truth),
    })
