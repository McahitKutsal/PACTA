"""b=0.40 katılım-kısıtı kırılganlığı TANISI — ucuz, yargıçsız, transkriptli.

Sonnet-5 pilotunda b=0.40'ta savaş %50'ye sıçradı (hem S2 hem S4). Teori bunu
'aşırı-teminat' olarak açıklamıyor (ε·b=0.02 ≪ c_A+c_B=0.20); mekanizma katılım
kısıtının bağlaması: b*≈0.333 üstünde x*=x_P ve B tam KAYITSIZLIK noktasında
(kabul getirisi = savaş getirisi). Bu betik her bölümde A'nın teklifini, B'nin
kabul/ret ve t2 kararını basıp kırılganlığın KAYNAĞINI ayırır:
  - A, x_P'nin üstünde mi teklif ediyor?  -> AŞIRI TALEP (B haklı olarak reddeder)
  - A ~x_P teklif edip B reddediyor mu?    -> BIÇAK-SIRTI REDDİ (knife-edge)
  - B kabul edip t2'de saldırıyor mu?      -> teminat caydıramadı

Yargıç YOK (mekanizma motor kararlarından okunur) -> gemma yüklenmez, daha hızlı+ucuz.
Kullanım:
  python diagnose_bond.py                         # Haiku 4.5, b=0.40, n=8, S2+S4
  python diagnose_bond.py --bond 0.20             # karşılaştırma (IC bağlar, güvenilir barış)
  python diagnose_bond.py --model claude-sonnet-5 # daha pahalı teyit
"""
from __future__ import annotations
import argparse
from pathlib import Path

from g2_pilot import load_dotenv
from pacta_bench import (
    LLMAgent, AnthropicClient, ModuleIIParams, ProtocolParams,
    run_module_II, aggregate, save_transcripts,
)

OUT = Path("out"); OUT.mkdir(exist_ok=True)


def _ev(rec, kind):
    """Bölümdeki ilk `kind` olayının payload'u (yoksa None)."""
    return next((e["payload"] for e in rec["events"] if e.get("kind") == kind), None)


def main() -> None:
    load_dotenv()
    ap = argparse.ArgumentParser(description="b=0.40 kırılganlık tanısı (Haiku, yargıçsız)")
    ap.add_argument("--model", default="claude-haiku-4-5",
                    help="Anthropic modeli (varsayılan Haiku 4.5 — ucuz + temperature=0 determinist)")
    ap.add_argument("--bond", type=float, default=0.40)
    ap.add_argument("--delta", type=float, default=0.30)
    ap.add_argument("-n", type=int, default=8)
    args = ap.parse_args()

    p = ModuleIIParams(delta=args.delta)
    pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=args.bond)
    x_ic = p.p2 + p.c_B + (pr.v - pr.eps) * args.bond
    x_p = p.p1 + p.c_B - pr.eps * args.bond
    x_star = min(x_ic, x_p)
    binding = "KATILIM (x_P) — B kayıtsızlık noktasında" if x_p < x_ic else "IC (x_IC) — B'nin artı payı var"
    crossover = 0.30 / 0.90  # x_IC == x_P çözümü (delta=0.30, v-eps=0.85, eps=0.05)

    print(f"\nmodel={args.model}  bond={args.bond}  delta={args.delta}  n={args.n}")
    print(f"teori: x_IC={x_ic:.3f}  x_P={x_p:.3f}  x*={x_star:.3f}  |  bağlayıcı kısıt: {binding}")
    print(f"       (kesişim b*≈{crossover:.3f}; b bunun üstünde -> knife-edge; altında -> güvenilir)")

    def mk(scn: str, role: str) -> LLMAgent:
        return LLMAgent(AnthropicClient(model=args.model, temperature=0.0, max_tokens=4096), scn, role)

    for scn in ("S2", "S4"):
        recs = [run_module_II(p, pr, mk(scn, "A"), mk(scn, "B"), seed=s) for s in range(args.n)]
        print(f"\n=== {scn}  P2 b={args.bond} ===")
        print(f"  {'seed':>4} {'A_teklif':>9} {'B_yanıt':>9} {'B_t2':>7} {'sonuç':>10}  tanı")
        for i, r in enumerate(recs):
            offer = _ev(r, "offer")
            declared = any(e.get("kind") == "declare_war" for e in r["events"])
            resp = _ev(r, "respond") or "-"
            t2 = _ev(r, "t2_action") or "-"
            if declared:
                offer_s, note = "WAR_NOW", "A savaş ilan etti (teklif yok)"
            elif isinstance(offer, (int, float)):
                offer_s = f"{offer:.3f}"
                if r["outcome"] == "war_now" and resp == "war":
                    note = ("A>x_P: AŞIRI TALEP" if offer > x_p + 1e-6
                            else "~x_P: BIÇAK-SIRTI REDDİ (B kayıtsızlıkta reddetti)")
                elif r["outcome"] == "attack_t2":
                    note = "B kabul→SALDIRI (teminat caydıramadı)"
                else:
                    note = "barış"
            else:
                offer_s, note = "-", "?"
            print(f"  {i:>4} {offer_s:>9} {str(resp):>9} {str(t2):>7} {r['outcome']:>10}  {note}")
        m = aggregate(recs)
        print(f"  -> war={m['war_rate']:.2f}  xA={m['payoff_A']:.3f}  WELF={m['WELF']:.3f}")
        tag = args.model.replace("/", "-").replace(":", "-")
        path = save_transcripts(recs, str(OUT / f"diag_{scn}_b{args.bond}_{tag}.jsonl"), k=args.n)
        print(f"  transkript: {path}")

    print("\nYorum: 'AŞIRI TALEP' baskınsa -> A güçlü teminatta B'yi katılım sınırının ötesine "
          "itiyor.\n       'BIÇAK-SIRTI REDDİ' baskınsa -> denge B'nin kayıtsızlık noktasında ve "
          "gerçek model\n       marjsız teklifi güvenilir kapatamıyor (senaryo promptunun 'marj bırak' uyarısı).")


if __name__ == "__main__":
    main()
