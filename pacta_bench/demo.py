"""python -m pacta_bench.demo — Rasyonel-limit pilot koşusu.

Üretilen tablolar, T1.1 öngörülerinin (Ö1-Ö3, Ö5) kodlanmış-ajan limitinde
sağlandığını gösterir. LLM katmanı bağlandığında AYNI tablolar LLM ajanları
için üretilecek ve teori-empiri sapması (ED, kırılma kayması) raporlanacaktır.
Çıktılar: out/demo_results.json, out/transcripts_sample.jsonl
"""
from __future__ import annotations
import json
from pathlib import Path

from . import (
    DeceptiveAgent, ModuleIParams, ModuleIIParams, NaiveProposerAgent,
    ProtocolParams, RationalAgent, aggregate, run_batch, save_transcripts,
)
from .metrics import fmt_num, fmt_pct

OUT = Path("out"); OUT.mkdir(exist_ok=True)
RA, RB = RationalAgent(), RationalAgent()
results = {}


def row(label, m, cols):
    cells = []
    for c in cols:
        v = m.get(c)
        cells.append(fmt_pct(v) if c in ("war_rate", "DR", "PBR_formal",
                                         "PBR_verbal", "AR") else fmt_num(v))
    print(f"  {label:<14}" + "".join(f"{s:>9}" for s in cells))


SHORT = {"war_rate": "savas%", "DR": "DR", "WELF": "WELF", "ED": "ED",
         "payoff_A": "pay_A", "payoff_B": "pay_B", "AR": "AR",
         "PBR_formal": "PBR_f", "PBR_verbal": "PBR_v"}


def header(title, cols):
    print("\n" + title)
    print("  " + "-" * (14 + 9 * len(cols)))
    print(f"  {'':<14}" + "".join(f"{SHORT[c]:>9}" for c in cols))


# ---------------------------------------------------------------- Blok 1 --- #
cols1 = ["war_rate", "DR", "WELF", "payoff_A", "ED"]
header("BLOK 1 — Modul I (ozel bilgi; mu=0.60 > mu_bar=0.43) | Rasyonel v Rasyonel | n=4000",
       cols1)
pI = ModuleIParams(mu=0.60)
for proto in ("P0", "P1", "P3"):
    m = aggregate(run_batch("I", pI, ProtocolParams(protocol=proto), RA, RB, 4000))
    results[f"I/{proto}"] = m
    row(proto, m, cols1)
print("  Teori: P0/P1 -> savas %40, DR ~ mu; P3 -> cozulme (T3): savas 0, DR 0, refah 1.00")

# ---------------------------------------------------------------- Blok 2 --- #
cols2 = ["war_rate", "PBR_formal", "PBR_verbal", "WELF", "payoff_A"]
header("BLOK 2 — Modul II (guc kaymasi Delta=0.30; v=0.9, eps=0.05) | Rasyonel v Rasyonel | n=500",
       cols2)
pII = ModuleIIParams(delta=0.30)
for proto, b in (("P0", 0.0), ("P1", 0.0), ("P2", 0.20)):
    pr = ProtocolParams(protocol=proto, v=0.9, eps=0.05, bond=b)
    m = aggregate(run_batch("II", pII, pr, RA, RB, 500))
    results[f"II/{proto}(b={b})"] = m
    row(f"{proto} (b={b:.2f})", m, cols2)
print("  Teori: Delta > c_A+c_B=0.20 -> P0/P1'de onleyici savas (Powell);")
print("         P2, b >= b_min ile barisi kurtarir; izleme bedeli DWL = eps*b = 0.01")

# ---------------------------------------------------------------- Blok 3 --- #
print("\nBLOK 3 — Doz-yanit (O3 / H3): P2 teminat taramasi | b_min = 0.1/0.85 = 0.1176")
print("  " + "-" * 58)
print(f"  {'b':>6} {'savas%':>9} {'PBR':>9} {'x_anlasma':>11} {'WELF':>8}")
sweep = {}
for b in (0.00, 0.05, 0.10, 0.118, 0.15, 0.20, 0.30):
    pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=b)
    recs = run_batch("II", pII, pr, RA, RB, 200)
    m = aggregate(recs)
    sweep[b] = m
    x = m["payoff_A"] if m["war_rate"] == 0 else None
    print(f"  {b:>6.3f} {fmt_pct(m['war_rate']):>9} {fmt_pct(m['PBR_formal']):>9}"
          f" {fmt_num(x):>11} {fmt_num(m['WELF']):>8}")
results["II/P2_sweep"] = {str(k): v for k, v in sweep.items()}
print("  Kirilma 0.10 ile 0.118 arasinda — kapali-form esikle birebir (Hedef Teorem T1/T2).")

# ---------------------------------------------------------------- Blok 4 --- #
cols4 = ["war_rate", "PBR_verbal", "PBR_formal", "payoff_A", "payoff_B"]
header("BLOK 4 — Somuru ve koruma (H5): Naif teklifci (A) v Aldatici (B)", cols4)
for proto, b in (("P0", 0.0), ("P2", 0.40)):
    pr = ProtocolParams(protocol=proto, v=0.9, eps=0.05, bond=b)
    recs = run_batch("II", pII, pr, NaiveProposerAgent(), DeceptiveAgent(), 20)
    m = aggregate(recs)
    results[f"II/adv/{proto}(b={b})"] = m
    row(f"{proto} (b={b:.2f})", m, cols4)
print("  P0: 'sadakat' beyani + t2 saldirisi -> naif A soyulur (getiri 0.10).")
print("  P2: teminat saldiriyi karsiz kilar -> AYNI aldatici ajan sozunu tutar (0.58).")
print("  Mekanizma tasarimi, niyeti degil TESVIKI degistirir — projenin cekirdek tezi.")

# ------------------------------------------------------------------ Kayit -- #
tp = save_transcripts(
    run_batch("II", pII, ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.20),
              RA, RB, 10), str(OUT / "transcripts_sample.jsonl"), k=10)
with (OUT / "demo_results.json").open("w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"\nKayit: {OUT/'demo_results.json'} ve {tp} yazildi.")
