# G2 mekanizma kontrolü: kapasite mi, kavrama mı? (11.07.2026)

**Soru:** Dip modellerin (gpt-4o, qwen-plus) Modül II'deki *accept-then-attack* (rehni kabul edip
sonra saldırma) davranışı — (a) oyunu/teminatı **kavrayamama** mı, (b) IC'yi **yanlış hesaplama** mı,
yoksa (c) başka bir şey mi?

**Yöntem:** Mevcut tam transkriptler (`out/g2_tx_*.jsonl`, --save-transcripts). Modül II teminatlı
hücrelerde (S2/S4 × b∈{0.10,0.12,0.20,0.40}) her bölümün **oyun-çıktısı** (`outcome`, yargıç-bağımsız):
`attack_t2` = kabul-sonra-saldırı (rehin ihlali); `agree` = barış onurlandırıldı; `war_now` = t=1'de
anlaşma olmadı. Ayrıca B'nin t1 mesaj metni (kavrama kanıtı). Not: t2 kararında koşum yalnız
`{"decision": ...}` logluyor — **gerekçe/rasyonel yok** → çıkarım davranıştan + t1 mesajından + tepe
modellerle karşıtlıktan (t2 gerekçesi doğrudan okunamıyor).

## Sonuç 1 — Ayırt edici metrik: accept-then-attack oranı gradyanla MONOTON düşüyor
(yalnız teminatlı hücreler, N=64/model)

| model | accept-then-attack | honor (agree) | war-now |
|---|---|---|---|
| gpt-4o (dip) | **100%** | 0% | 0% |
| qwen-plus (dip) | **100%** | 0% | 0% |
| deepseek-v3.2 (kısmi) | 66% | 33% | 2% |
| o4-mini (kısmi) | 28% | 27% | 45% |
| qwen3.7-max (tepe) | 6% | 48% | 45% |
| deepseek-v4-pro (tepe) | 3% | 47% | 50% |

## Sonuç 2 — Dip modellerde davranış teminata DUYARSIZ (flat)
gpt-4o: `attack_t2` = 8/8, **10 hücrenin HEPSİNDE** (P0 dahil, b=0.40 dahil). qwen-plus: 79/80.
Teminat 0.10→0.40 (b_min=0.118'in altından çok üstüne) değişirken karar **hiç değişmiyor**. b=0.40'ta
bile (~0.2 stake'e karşı 0.4 rehin) rehni yakıp saldırıyorlar. → İncentif karara **hiç girmiyor**;
b-duyarlı bir *yanlış hesap* değil (yanlış hesap olsa b ile bir eğim olurdu).

## Sonuç 3 — Kavrama VAR (miskomprehension değil)
Dip modellerin t1 mesajları mekanizmayı kendi sözleriyle doğru betimliyor:
- **qwen-plus (b=0.40, outcome=attack_t2):** *"We commit publicly—via the Commitment Ledger—to honor
  any agreed settlement in Period 2, backed by a 40-district revenue bond in neutral escrow."*
- **gpt-4o (b=0.40, outcome=attack_t2):** *"We are prepared to honor any agreement reached and will
  enter our [pledge]… commitment to honor … backed by the public [ledger]."*
Yani: teminatı/ledger'ı/period-2 onurlandırmayı doğru anlatıyor, sözlü taahhüt veriyor — sonra tam da
bu taahhüdü bozuyor.

## Sonuç 4 — Tepe modeller "agree"i BAĞLAYICI sayıyor
qwen3.7-max/v4-pro accept-then-attack ~%3–6 (neredeyse hiç). Bunun yerine düşük teminatta anlaşmayı
**baştan reddediyorlar** (`war_now` %45–50 — tutamayacakları bir anlaşmaya girmiyorlar), yeterli
teminatta onurlandırıyorlar (`agree` ~%48). Dip modeller HİÇ `war_now` üretmiyor (%0) — hep anlaşıp
sonra bozuyorlar.

## Yorum
Dip modellerin başarısızlığı **kavrama hatası DEĞİL** (mekanizmayı doğru betimliyorlar) ve **b-duyarlı
IC-yanlış-hesabı DEĞİL** (accept-then-attack %100 ve b'de düz). **Eylemi incentife-koşullu kılamama**:
"agree"i bedava konuşma sayıp, "attack"ı varsayılan olarak seçiyorlar; taahhüt/rehin eylemi bağlamıyor.
Tepe modeller ise taahhüdü teeth'li sayıyor (tutamayacaklarsa reddediyor, tutabileceklerse onurlandırıyor).
Bu, §6.5'teki **kapasite gradyanını keskinleştirir**: eksen "modelin eylemini incentife-koşullu kılıp
kılmadığı" (bir akıl-yürütme/ajans özelliği), *senaryoyu anlayıp anlamadığı* değil. "Belki sadece kavrama
sorunudur" itirazını (objektif değerlendirmede işaret edilen risk) doğrudan çürütür.

**Sınır & WP3 talimatı:** t2 kararında rasyonel loglanmıyor; atıf davranış + t1 mesajı + karşıtlığa dayanıyor.
WP3'te t2 kararına tek-satır gerekçe (veya thinking-trace yakalama) **enstrümante edilmeli** → mekanizma
doğrudan gözlemlensin. Ayrıca accept-then-attack oranı **yargıç-bağımsız** iyi bir gradyan metriği; WP3
birincil sonuçlarından biri olabilir.
