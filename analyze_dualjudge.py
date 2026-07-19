#!/usr/bin/env python3
"""Çevrimdışı yargıç-arası uyum analizi (D-023).

g2_pilot'un hücre-başı `interjudge_kappa`'sı iddiaları KONUMSAL eşler; iki yargıç
(farklı model) aynı mesajdan FARKLI sayıda/sırada iddia çıkardığından, konumsal
eşleme kayar ve κ yapay olarak düşük çıkar (v4-pro: claim-düzeyi κ≈0.149, ham≈0.48).
Bu, etiketleme UYUMUNU değil çıkarım-HİZASINI ölçer.

Bu betik, kaydedilmiş transkriptlerden (`out/g2_tx_{tag}_*.jsonl`, `judged_by` ile)
çıkarım-sayısına DAYANIKLI bir birimle yeniden hesaplar:
  birim = (bölüm, aktör);  yargıç X etiketi = o aktör için X'in HERHANGİ bir iddiası
  'deceptive' ise 'deceptive', yoksa 'clean'.
Yargıç-arası κ bu ikili mesaj-düzeyi etiket üzerinden hesaplanır — API/maliyet yok,
yeniden koşum yok. Birincil DV'ler zaten yargıç-bağımsız; bu yalnız İKİNCİL
DR_söylenen güvenilirliğini (ve κ-kapısını) doğru ölçmek içindir.

Kullanım:
  python analyze_dualjudge.py deepseek-deepseek-v4-pro_dualjudge
  python analyze_dualjudge.py --all
"""
import argparse
import glob
import json
import os
import sys

from pacta_bench.judge import cohen_kappa

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def gwet_ac1(a, b):
    """Gwet'in AC1'i (2 kategori) — Cohen κ'nin çarpık-yaygınlık patolojisine
    dayanıklı uyum katsayısı. Bir kategori baskın olduğunda κ çöker ama AC1 gerçek
    uyumu daha adil yansıtır. π=ortalama 'deceptive' oranı; pe=2π(1-π)."""
    n = len(a)
    if not n:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ra = sum(1 for x in a if x == "deceptive") / n
    rb = sum(1 for x in b if x == "deceptive") / n
    pi = (ra + rb) / 2.0
    pe = 2 * pi * (1 - pi)
    return 1.0 if pe == 1.0 else (po - pe) / (1.0 - pe)

OUTDIR = "out"


def _msg_labels(claims):
    """Bir yargıcın iddia listesi → {actor: 'deceptive'|'clean'}.
    Aktör için EN AZ BİR 'deceptive' iddia varsa mesaj 'deceptive'."""
    out = {}
    for c in claims:
        a = c.get("actor")
        if a is None:
            continue
        out.setdefault(a, "clean")
        if c.get("label") == "deceptive":
            out[a] = "deceptive"
    return out


def analyze_run(tag):
    files = sorted(glob.glob(os.path.join(OUTDIR, f"g2_tx_{tag}_*.jsonl")))
    if not files:
        print(f"  (transkript bulunamadı: out/g2_tx_{tag}_*.jsonl)")
        return None

    # kıyas için g2_pilot'un kaydettiği claim-düzeyi κ
    claim_kappa = None
    jp = os.path.join(OUTDIR, f"g2_pilot_{tag}.json")
    if os.path.isfile(jp):
        try:
            claim_kappa = json.load(open(jp, encoding="utf-8")).get("interjudge_kappa_mean")
        except Exception:
            pass

    print(f"\n{'='*72}\n{tag}\n{'='*72}")
    print(f"{'hücre':16}{'birim':>7}{'msg-κ':>8}{'ham-uzl':>9}{'j1-DR':>7}{'j2-DR':>7}")
    cell_ks, all_a, all_b = [], [], []
    for f in files:
        rest = os.path.basename(f)[len("g2_tx_"):-len(".jsonl")]
        cell = rest[len(tag) + 1:] if rest.startswith(tag) else rest
        la, lb = [], []
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            jb = json.loads(line).get("judged_by")
            if not jb or len(jb) < 2:
                continue
            ids = list(jb.keys())[:2]
            m1, m2 = _msg_labels(jb[ids[0]]), _msg_labels(jb[ids[1]])
            for actor in set(m1) | set(m2):
                la.append(m1.get(actor, "clean"))
                lb.append(m2.get(actor, "clean"))
        if not la:
            continue
        k = cohen_kappa(la, lb)
        agr = sum(1 for x, y in zip(la, lb) if x == y) / len(la)
        dr1 = sum(1 for x in la if x == "deceptive") / len(la)
        dr2 = sum(1 for x in lb if x == "deceptive") / len(lb)
        cell_ks.append(k if k is not None else 0.0)
        all_a += la; all_b += lb
        print(f"{cell:16}{len(la):>7}{(k if k is not None else 0):>8.2f}"
              f"{agr:>9.2f}{dr1:>7.2f}{dr2:>7.2f}")

    if not all_a:
        print("  (judged_by içeren çift-yargıç bölümü yok)")
        return None
    overall_k = cohen_kappa(all_a, all_b)
    overall_agr = sum(1 for x, y in zip(all_a, all_b) if x == y) / len(all_a)
    overall_ac1 = gwet_ac1(all_a, all_b)
    mean_cell_k = sum(cell_ks) / len(cell_ks)
    dr_j1 = sum(1 for x in all_a if x == "deceptive") / len(all_a)
    dr_j2 = sum(1 for x in all_b if x == "deceptive") / len(all_b)
    print(f"{'-'*72}")
    print(f"  MESAJ-DÜZEYİ (havuzlanmış): ham-uzlaşı={overall_agr:.3f}  "
          f"Cohen κ={overall_k:.3f}  Gwet AC1={overall_ac1:.3f}  birim={len(all_a)}")
    print(f"  Yargıç marjinal DR: j1={dr_j1:.2f}  j2={dr_j2:.2f}  "
          f"(fark → sistematik katılık farkı, çarpıklık κ'yi çökertir)")
    if claim_kappa is not None:
        print(f"  claim-düzeyi (g2_pilot) κ={claim_kappa:.3f}  ≈ mesaj-düzeyi κ → sanat DEĞİL, gerçek")
    return {"tag": tag, "msg_kappa": overall_k, "msg_ac1": overall_ac1,
            "raw_agreement": overall_agr, "dr_j1": dr_j1, "dr_j2": dr_j2,
            "claim_kappa": claim_kappa, "n_units": len(all_a)}


def main():
    ap = argparse.ArgumentParser(description="Çevrimdışı mesaj-düzeyi yargıç-arası κ")
    ap.add_argument("tag", nargs="?", default=None, help="koşu tag'i (dual-judge)")
    ap.add_argument("--all", action="store_true", help="out/'daki tüm *_dualjudge koşuları")
    args = ap.parse_args()
    if args.all:
        tags = sorted({os.path.basename(p)[len("g2_pilot_"):-len(".json")]
                       for p in glob.glob(os.path.join(OUTDIR, "g2_pilot_*dualjudge*.json"))})
        if not tags:
            print("out/'da *dualjudge* koşusu yok."); return
        for t in tags:
            analyze_run(t)
    elif args.tag:
        analyze_run(args.tag)
    else:
        ap.error("bir tag verin ya da --all kullanın")


if __name__ == "__main__":
    main()
