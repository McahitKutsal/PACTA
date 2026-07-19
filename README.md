# PACTA-Bench v0.5.2 — İskelet + LLM Boru Hattı + Yargıç + 4 Senaryo + G2 Pilotu

LLM tabanlı kriz pazarlığında **doğrulanabilir taahhüt protokollerini** ölçen
benchmark'ın çalışan çekirdeği. Saf Python ≥ 3.10; gerçek LLM için opsiyonel `anthropic`/`openai` paketleri.

Bu iskelet, **T1.1 Formel Model v0** dokümanının sayısal ikizidir: oradaki her
kapalı-form değer (`mu_bar`, `b*`, asgari teminat) ve denge öngörüsü burada
birim testle doğrulanır. Manifest görev eşlemesi:

| Manifest görevi | Bu repodaki karşılık |
|---|---|
| T1.5 — analitik ↔ nümerik çapraz doğrulama | `tests/test_theory.py` (12 test) |
| T2.2 — Taahhüt DSL + defter | `core.Commitment`, `core.Ledger` |
| T2.3 — hakem motoru + LLM-yargıç | `engine._referee_verify` (deterministik) + `judge.py` (Mock/LLM yargıç) |
| T2.5 — metrik kaydedici + kayıt disiplini | `core.new_record` (config hash, seed), `orchestrator` |
| §10.1 metrikleri (v0 alt kümesi) | `metrics.aggregate`: DR, PBR, EI, AR, WELF, ED |
| T2.1 — senaryo şablonları | `scenarios.py` (S1–S4; S1/S3 Modül I, S2/S4 Modül II; sızıntı-korumalı) |
| T2.4 — LLM ajan bağlama | `agents.LLMAgent` + `llm.py` (Mock/Anthropic/OpenAI); **tamamlandı** |

## Hızlı başlangıç

```bash
python -m unittest discover -s tests -v   # teori doğrulaması (15/15 geçmeli)
python -m pacta_bench.demo                # 4 bloklu pilot tablo (kodlanmış ajanlar)
python -m pacta_bench.llm_demo            # LLM boru hattı + yargıç demosu (sıfır API)
```

Demo çıktıları `out/demo_results.json` ve `out/transcripts_sample.jsonl`
dosyalarına yazılır; her bölüm kaydı **seed + config_hash** taşır
(Manifest §18.2: "kaydı olmayan koşu yapılmamış hükmündedir").

## LLM boru hattı (WP2/T2.4)

Üç katman: `scenarios.py` (Senaryo Spes. v0.1'in makine-okur şablonları) →
`llm.py` (istemciler + JSON zorlama) → `agents.LLMAgent` (motor sözleşmesine
bağlar). `MockClient` prompt metninden sayıları geri okuyup T1.1-rasyonel oynar;
böylece **şablonların yeterli bilgi taşıdığını** dış API olmadan kanıtlar ve
regresyon oracle'ı olur.

```python
from pacta_bench import LLMAgent, MockClient, ModuleIIParams, ProtocolParams, run_module_II
A = LLMAgent(MockClient(), "S2", "A"); B = LLMAgent(MockClient(), "S2", "B")
rec = run_module_II(ModuleIIParams(delta=0.30),
                    ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.20), A, B, seed=0)
# rec["events"] içinde her 'llm_call' ham yanıtı + parse sonucunu taşır (yargıç/denetim)
```

**Gerçek modele geçiş:** `AnthropicClient(model=..., temperature=0.0)` veya
`OpenAICompatClient(...)` fabrikası `pacta_bench.llm_demo.main(factory, tag)`'e
verilir. Model sürümü sabitlenir ve her kayda damgalanır (R7). MockClient boru
hattı, teori kırılmalarını LLM ajan arayüzüyle yeniden üretir:
S1/P3 çözülme (savaş %0), S2 doz-yanıt kırılması (b_min=0.118'de), Ö6 refah tepesi.

## Mimari (Manifest §8.2 ile bire bir)

```
orchestrator.run_batch
   └── engine.run_module_{I,II}      # oyun akışı (durum makinesi)
         ├── agents.*                # politika: Rational / Deceptive / Naive / LLM(stub)
         ├── core.Ledger             # taahhüt defteri (P1+)
         └── hakem                   # ihlal yüklemi + (v, eps) doğrulama örneklemesi
                └── metrics.aggregate
```

**Getiri sözleşmesi (v0):** getiriler beklenen değerdir (savaş piyangosu ve
doğrulama üzerinden); doğrulama sinyali `s` yine de tohumlu örneklenip deftere
işlenir. Gerçekleşme modu v1'de bayrakla açılacaktır.

## Rasyonel-limit bulguları (demo özeti)

* **Modül I** (μ=0.60): P0/P1 → savaş ≈ %40, DR ≈ %60 — *rasyonel ajan bile
  yalan söyler; aldatma teşvik yapısıdır* (Lemma 2 / Ö1). P3 → çözülme: savaş 0, DR 0.
* **Modül II** (Δ=0.30): P0/P1 → %100 önleyici savaş (Powell). P2 → doz-yanıt
  kırılması tam `b_min = 0.1176`'da; b=0.20'de barış, x*=0.47, DWL=εb=0.01.
* **H5 çekirdeği:** aldatıcı ajan P0'da naif teklifçiyi soyar (A: 0.10);
  **aynı ajan** P2 (b=0.40) altında sözünü tutar (A: 0.58). Mekanizma niyeti
  değil teşviki değiştirir.

## LLM entegrasyon sözleşmesi (WP2/T2.4)

`agents.LLMAgent` doldurulurken: (1) her metot `obs` → istem → **yapılandırılmış
eylem** (JSON/DSL zorlaması); (2) serbest-metin iddialar LLM-yargıç ile
`core.log_claim(channel="verbal")` etiketlerine çevrilir; (3) model sürümü
sabitlenir ve kayda geçer (R7). Kodlanmış ajanlar, yargıç kalibrasyonu için
ground-truth üretici olarak kalır.

## G2 pilotu (yerel Ollama ile)

`g2_pilot.py` dört senaryo × dört protokol matrisini ajan+yargıç bağlı koşar ve
G2 kapı kararını üretir (protokoller arası etkin aldatma/ihlal farkı anlamlı mı).
Yerel **Ollama** modelleriyle sıfır maliyet, tam tekrarlanabilirlik (R7), doğal
aile ayrımı (R2: ajan Qwen, yargıç Gemma).

```bash
# 1) Ollama çalışsın; modelleri çek
ollama pull qwen3:8b       # ajanlar (Alibaba)
ollama pull gemma3:4b      # yargıç (Google — farklı aile)
# 2) OpenAI-uyumlu endpoint için
pip install openai
# 3) pilotu koş
python g2_pilot.py                 # gerçek Ollama
python g2_pilot.py --mock          # API'siz önizleme (boru hattı testi)
python g2_pilot.py -n 50           # hücre başına bölüm sayısı
python g2_pilot.py --agent mistral --judge llama   # farklı aile çifti (çapraz-model)
```

Model atamaları `make_ollama_factory` / `make_ollama_judge` içinde; değiştirmek
için oradaki `AGENT_MODEL` / `JUDGE_MODEL` düzenlenir. Çıktı: `out/g2_pilot_*.json`
+ örnek transkript + konsol tablosu + G2 kararı (GEÇ/KOŞULLU/REVİZE).

## Senaryolar (T2.1)

Dört senaryo, iki oyun ailesini paylaşır (motor değişmez, örtü değişir):
- **S1** Vadi Anlaşmazlığı · **S3** Yaptırım-Denetim Takası → Modül I (özel bilgi
  + doğrulanabilir ifşa; çözülme, kanal ayrışması)
- **S2** Ateşkes Masası · **S4** Abluka Krizi → Modül II (taahhüt problemi + güç
  kayması; doz-yanıt kırılması, refah tepesi)

`LLMAgent(client, "S3", "B")` gibi kurulur; `_REGISTRY` her senaryoyu (aile,
sistem-fn, faz-fn) üçlüsüne bağlar. **Senaryo-sağlamlığı (R1):** aynı aile
senaryoları birebir aynı sonucu verir (S1≡S3, S2≡S4) — anlatı örtüsü rasyonel
davranışı değiştirmez (`test_cross_scenario_consistency`). Gerçek LLM'de örtü
etkisi ölçülecek asıl ampirik sorudur.

## Yargıç katmanı (T2.3)

`judge.py` serbest metni aldatma etiketlerine çevirir (yapılandırılmış eylemler
zaten motorda deterministik). Üç görev: iddia çıkarımı (G1), ground-truth eşleme
(G2), retorik eskalasyon (G3). `MockJudge` ground-truth'u bilen deterministik
oracle; `LLMJudge` gerçek model (R2: değerlendirilenden farklı aile).

**Ana bulgu (kanal ayrışması):** `MockClient(persona="deceptive")` ile kırılgan
tip blöf yapar. Yargıç iki metriği ayırır: `DR_judged` (söylenen aldatma) ve
`DR_effective` (sonucu belirleyen kanal). P3'te blöf söylenir (DR_judged>0) ama
sertifika sahtelenemez olduğundan **etkin aldatma 0** ve çözülme olur — protokol
aldatmayı yasaklamaz, *işlevsizleştirir*. Bu ayrım, projenin merkezi tezidir ve
yargıç katmanı olmadan görünmez.

**Kalibrasyon (κ kapısı):** `calibrate(gold, test)` → Cohen's κ; hedef ≥ 0.7
(Manifest §12.1). `gold`=MockJudge/insan altın-set, `test`=LLMJudge.

## Sürüm / lisans

v0.5.2 — MIT (öneri; WP0/T0.1'de kesinleştirilecek). Değişiklikler Manifest
§18.5 Karar Günlüğü'ne işlenir.
