#!/usr/bin/env python3
"""WP3 çok-config orkestratörü (D-021).

Dondurulmuş ön-kaydın (paper/PACTA_WP3_preregistration.md, FROZEN v1.0) 8 config'ini
— 4 aile × 2 tier — sırayla `g2_pilot.py --dual-judge` ile koşar. Her config AYRI bir
alt-süreçtir: izole çıktı/log, biri başarısız olsa (kota/anahtar) diğerleri devam eder.

Hücre-başı n (birincil N_PRIMARY / ikincil N_SECONDARY, §5) g2_pilot'un varsayılanıdır
(-n verilmez). Çift-yargıç, ajan ailesine göre havuzdan otomatik seçilir (§4.2):
  - Anthropic/OpenAI ajan → yargıçlardan biri Gemini → GEMINI_API_KEY gerekir.
  - Alibaba/DeepSeek ajan → yargıçlar gpt-4o-mini + claude-haiku → OPENAI + ANTHROPIC.

Kullanım:
  python wp3_run.py                      # 8 config, çift-yargıç, tam matris (n=30/15)
  python wp3_run.py --only II            # alt küme (g2_pilot'a iletilir)
  python wp3_run.py --configs qwen3.7-max,deepseek-v4-pro   # config alt kümesi
  python wp3_run.py --dry-run            # komutları yazdır, koşma
  python wp3_run.py -n 3 --only S6       # ucuz smoke (tek-tip n=3)
"""
import argparse
import subprocess
import sys
import time

# (agent bayrağı, model, max_tokens). Reasoning tier'lar daha çok düşünme-token'ı yer.
# NOT: snapshot ID'leri freeze'de pinlenir; kayıt-başı gerçek sürüm damgalanır (R7).
CONFIGS = [
    ("--anthropic", "claude-haiku-4-5",  4096),   # Anthropic — non-reasoning tier
    ("--anthropic", "claude-sonnet-5",   8192),   # Anthropic — reasoning
    ("--openai",    "gpt-4o",            4096),    # OpenAI — non-reasoning
    ("--openai",    "o4-mini",           8192),    # OpenAI — reasoning (mini)
    ("--qwen",      "qwen-plus",         4096),    # Alibaba — non-reasoning
    ("--qwen",      "qwen3.7-max",       8192),    # Alibaba — reasoning
    ("--deepseek",  "deepseek-v4-flash", 6144),    # DeepSeek — light reasoning
    ("--deepseek",  "deepseek-v4-pro",   8192),    # DeepSeek — reasoning
]


def main():
    try:  # Windows cp1252 konsolunda Türkçe karakter/✓ çökmesini önle
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="WP3 8-config orkestrator (cift-yargic)")
    ap.add_argument("--only", default=None,
                    help="g2_pilot --only'a iletilir (I | II | 'S2,S4').")
    ap.add_argument("-n", type=int, default=None,
                    help="tek-tip n override (smoke). Verilmezse WP3 hücre-başı 30/15.")
    ap.add_argument("--configs", default=None,
                    help="virgülle model alt kümesi (ör. qwen3.7-max,deepseek-v4-pro).")
    ap.add_argument("--dry-run", action="store_true", help="komutları yazdır, koşma.")
    args = ap.parse_args()

    want = {s.strip() for s in args.configs.split(",")} if args.configs else None
    configs = [c for c in CONFIGS if (want is None or c[1] in want)]
    if not configs:
        print(f"HATA: --configs eşleşmedi. Geçerli: {[c[1] for c in CONFIGS]}", file=sys.stderr)
        sys.exit(2)

    ntxt = "30/15 (WP3 hücre-başı)" if args.n is None else str(args.n)
    print(f"WP3 orkestratör — {len(configs)} config, çift-yargıç, n={ntxt}")
    print("Not: Anthropic/OpenAI ajan config'leri yargıç havuzunda Gemini kullanır "
          "→ GEMINI_API_KEY gerekir.\n")

    results = []
    for i, (flag, model, mtok) in enumerate(configs, 1):
        cmd = [sys.executable, "g2_pilot.py", flag, model, "--dual-judge",
               "--save-transcripts", "--max-tokens", str(mtok)]
        if args.only:
            cmd += ["--only", args.only]
        if args.n is not None:
            cmd += ["-n", str(args.n)]
        print(f"{'='*70}\n[{i}/{len(configs)}] {model}\n  $ {' '.join(cmd)}\n{'='*70}")
        if args.dry_run:
            results.append((model, "DRY-RUN"))
            continue
        t0 = time.time()
        rc = subprocess.call(cmd)
        dt = (time.time() - t0) / 60.0
        status = "OK" if rc == 0 else f"HATA(rc={rc})"
        results.append((model, f"{status}  {dt:.0f}dk"))
        print(f"\n[{i}/{len(configs)}] {model} → {status} ({dt:.1f} dk)\n")

    print(f"{'='*70}\nWP3 ÖZET ({len(configs)} config)")
    for model, st in results:
        print(f"  {model:22} {st}")
    print("Çıktılar: out/g2_pilot_*_dualjudge*.json (+ transkriptler, loglar).")
    # herhangi bir config başarısızsa çıkış kodu 1 (izleme/CI için)
    if any("HATA" in st for _, st in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
