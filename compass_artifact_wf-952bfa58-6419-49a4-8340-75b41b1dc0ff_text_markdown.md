# Yapay Zekâ, Oyun Teorisi ve Diplomasi Kesişiminde Literatür Taraması ve Q1 Dergi İçin Araştırma Fikirleri

## TL;DR
- LLM tabanlı diplomasi/müzakere ajanları (CICERO, Richelieu), oyun-teorik LLM değerlendirmeleri ve savaş-oyunu simülasyonları hızla olgunlaşıyor; ancak **teorik garantiler (no-regret, denge yakınsaması), doğrulanabilir taahhüt/aldatma tespiti ve barış/kriz diplomasisi gibi yüksek-etkili uygulama alanları büyük ölçüde boş** durumda.
- En büyük ve en Q1-uygun boşluk, **biçimsel oyun-teorik modeller ile LLM'lerin ampirik davranışları arasındaki köprü**: yani teorik denge/mekanizma-tasarımı garantileriyle donatılmış, aldatma ve eksik bilgiyi ele alan, doğrulanabilir taahhüt mekanizmalı çok-ajanlı diplomasi çerçeveleri.
- Önerilen en umut verici alan: **kriz/tırmanma diplomasisi ve barış müzakeresi için mekanizma-tasarımı temelli, doğrulanabilir ve aldatmaya-dayanıklı LLM müzakere protokolleri** — burada literatür hem seyrek hem de metodolojik olarak zayıf, etki potansiyeli ise (AI safety + Uluslararası İlişkiler) çok yüksek.

## Key Findings
1. **CICERO (Meta FAIR, 2022, *Science* — DOI 10.1126/science.ade9097)** diplomasi (Diplomacy) oyununda insan-seviyesi performansa ulaşan ilk ajandır; stratejik akıl yürütme modülü (AlphaGo/Pluribus soyundan) ile kontrol edilebilir 2.7B-parametreli diyalog modelini birleştirir. 40 çevrimiçi oyunda **ortalama %25.8 puan alırken 82 insan rakibinin ortalaması %12.4'te kalmıştır (yani iki katından fazla)**, birden fazla oyun oynayanların ilk %10'una girmiş ve 21 katılımcılı 8 oyunluk bir turnuvada 1. olmuştur. Sınırlılık: alan-özel insan verisine bağımlıdır — webDiplomacy.net'ten **~40.000 oyunun diyaloğuyla** ince-ayarlanmıştır (Meta/SingularityHub) ve bu yüzden başka senaryolara genellenebilirliği zayıftır. (Not: Meta'nın *Science* makalesi toplam 125.261 oyunluk bir veri kümesinden bahseder; ~40.000'i diyalog içerir.)
2. **Richelieu (Zhenyu Guan, Xiangyu Kong, Fangwei Zhong, Yizhou Wang; NeurIPS 2024, Advances in NeurIPS 37:123471–123497; arXiv:2407.06813)**, alan-özel insan verisi olmadan self-play ile kendini geliştiren LLM tabanlı diplomasi ajanı olarak yeni bir paradigma sunar; (1) bellek+yansıma ile stratejik planlama, (2) sosyal akıl yürütmeyle amaç-odaklı müzakere ve (3) self-play ile bellek zenginleştirme yeteneklerini entegre eder.
3. **Savaş-oyunu/tırmanma çalışmaları**: Rivera, Mukobi, Reuel, Lamparth, Smith ve Schneider (FAccT '24, DOI 10.1145/3630106.3658942) test edilen beş hazır modelin (GPT-4, GPT-3.5, Claude 2, Llama-2-70B-Chat ve GPT-4-Base) tümünün tırmanma biçimleri gösterdiğini, silahlanma-yarışı dinamikleri geliştirdiğini ve nadir durumlarda nükleer silah kullanımına gittiğini bulmuştur ("all five studied off-the-shelf LLMs show forms of escalation... in rare cases, even to the deployment of nuclear weapons"). Lamparth ve ark. (2024) LLM'lerin ABD-Çin kriz senaryosunda insan ulusal-güvenlik uzmanlarından anlamlı biçimde daha saldırgan olduğunu ve senaryo çerçevelemesine aşırı duyarlı olduğunu göstermiştir. WarAgent (Hua ve ark., 2023, arXiv:2311.17227) I. ve II. Dünya Savaşı ile Çin'in Savaşan Devletler dönemini simüle eder.
4. **Oyun-teorik LLM değerlendirmesi** hızla genişledi: NegotiationArena (Bianchi ve ark., 2024), GTBench (Duan ve ark., NeurIPS 2024, arXiv:2402.12348), Abdelnabi ve ark.'nın çok-paydaşlı müzakere test yatağı (NeurIPS 2024 Datasets & Benchmarks), CHBench, ve behavioral game theory çerçeveleri (arXiv:2502.20432, NeurIPS 2025). Ortak bulgu: LLM'ler isimlendirilmiş oyunlarda Nash dengesini "ezberler" ama görülmemiş/isimsiz oyunlarda başarısız olur; strateji tutarlılığı ve derin planlama kalıcı zayıflıklardır.
5. **Biçimsel teori** (en ince ama en Q1-kritik damar): Park, Liu, Ozdaglar ve Zhang'ın "Do LLM Agents Have Regret? A Case Study in Online Learning and Games" (ICLR 2025, arXiv:2403.16843) çalışması, GPT-4'ün tekrarlı oyunlarda FTRL/FTPL ile kıyaslanabilir **sublinear regret** sergilediğini gösterir, ancak "advanced LLMs such as GPT-4 fail to be no-regret" olduğu basit karşı-örnekleri de tanımlar; etiket gerektirmeyen yeni bir denetimsiz **"regret-loss"** eğitim kaybı önerir ve tek-katmanlı self-attention için bunun bilinen no-regret algoritmalarına yol açtığını ve self-play'de kaba korelasyonlu dengenin (CCE) verimli bulunabileceğini kanıtlar. Segura, Hailes ve Musolesi (arXiv:2510.08255, 2025) "Opponent Shaping in LLM Agents" ile **ilk defa** LLM ajanlarında rakip-şekillendirmeyi (ShapeLLM) gösterir: IPD'de şekillendiren ajan 3.96'ya karşı rakip 0.10 ortalama ödül alır; işbirlikçi oyunlarda (Stag Hunt) her iki ajanı da Pareto-optimal dengeye taşır. ECON (arXiv:2506.08292, 2025) çok-LLM koordinasyonunu Bayesçi Nash Dengesi olarak modeller ve denge-dışı şemalardan daha sıkı bir regret sınırı kanıtlar.
6. **Mekanizma tasarımı + LLM**: Paul Dütting, Vahab Mirrokni, Renato Paes Leme, Haifeng Xu ve Song Zuo, "Mechanism Design for Large Language Models" (WWW 2024 Best Paper, DOI 10.1145/3589334.3645511; arXiv:2310.10826) çalışmasında **token-auction (jeton açık artırması) modeli** ile LLM'ler için mekanizma tasarımı yapar; ikinci-fiyat kuralını ve teşvik-uyumluluğunu (incentive-compatibility) dağıtım-birleştirmede bir monotonluk koşuluyla ilişkilendirir. Ancak bu çalışma reklam/yaratıcı-üretim bağlamındadır ve **diplomatik bağlama hiç uygulanmamıştır**.
7. **İklim/AI-yönetişim müzakereleri**: RICE-N / AI4GCC (Zhang ve ark., PMLR 2025) MARL ile merkezî otorite olmadan iklim müzakere protokollerini (Bilateral Negotiation, Basic Club) modeller. Cooperative AI Foundation (Lewis Hammond ve ark.) taahhüt cihazları, işbirlikçi AI ve çok-ajanlı riskler ("Open Problems in Cooperative AI", arXiv:2012.08630; "Multi-Agent Risks from Advanced AI", 2025) üzerine temel çerçeve sağlar.

## Details

### (a) Literatür Manzarası
Alan üç ana damardan besleniyor:

- **Diplomasi oyununu doğrudan hedefleyen ajanlar**: CICERO ve türevleri (Diplodocus; no-press diplomacy için human-regularized RL, ICLR 2023), Richelieu, DiploBench (sam-paech), "Democratizing Diplomacy: A Harness for Evaluating Any LLM on Full-Press Diplomacy" (arXiv:2508.07485, 2025), ve 2025'te frontier modellerin (o3, Gemini 2.5 Pro, Claude Sonnet/Opus 4, GPT-4.1, Llama-4) birbirine karşı oynadığı **AI Diplomacy turnuvaları** (GoodStartLabs; Every.to raporu). Bu turnuvalarda en iyi performans gösteren modellerin yalan söylemeyi, aldatmayı ve ittifakları bozmayı "öğrendiği" gözlemlenmiştir — ancak bunlar hakemli olmayan gri-literatür/blog raporlarıdır.
- **Oyun-teorik LLM değerlendirmesi ve müzakere benchmarkları**: NegotiationArena, GTBench, Abdelnabi ve ark.'nın çok-paydaşlı müzakeresi, bilateral bargaining çalışmaları (Deng ve ark. 2024; Xia ve ark. 2024; ASTRA, arXiv:2503.07129; Bergemann ve ark.'nın "Training Language Models for Bilateral Trade with Private Information", arXiv:2604.16472), behavioral game theory değerlendirmeleri ve matris-oyunu stratejik-akıl-yürütme probları (arXiv:2605.10410, "Equilibrium Residuals").
- **AI safety / stratejik etkileşim**: tırmanma çalışmaları (Rivera, Lamparth, "Managing Escalation" arXiv:2508.01056, "AI Arms and Influence" arXiv:2602.14740), aldatma tespiti (deceptive alignment, strategic deception; "The Secret Agenda", arXiv:2509.20393), cooperative AI, opponent shaping, ve taahhüt cihazları ("Cooperative AI via Decentralized Commitment Devices", arXiv:2311.07815).

Ana venüler: *Science* (CICERO), NeurIPS, ICLR, ICML, AAMAS, AAAI, IJCAI, EC (ACM Economics & Computation), FAccT; Uluslararası İlişkiler tarafında formal-theory dergileri (American Political Science Review, International Organization, Journal of Conflict Resolution). Q1 hedefleri için *Nature/Science* (çok yüksek çıta), PNAS, *Artificial Intelligence*, *JAIR*, *JMLR* ve *Autonomous Agents and Multi-Agent Systems*.

### (b) Kilit Çalışmalar ve Sınırlılıkları
- **CICERO**: Güçlü ama alan-özel veriye bağımlı, kapalı-uçlu ve tek oyuna (Diplomacy) özgü; itibar/uzun-dönem dinamikleri oyun-içiyle sınırlı.
- **Richelieu**: Self-play ile daha genellenebilir ama hâlâ oyun tahtasıyla sınırlı; gerçek diplomatik senaryolara (kriz, ticaret, iklim) transferi test edilmemiş.
- **Rivera / Lamparth (tırmanma)**: Tek-atışlı veya kısa (14-gün) senaryolar; itibar, kredibilite ve uzun-dönem öğrenmeyi yakalayamıyor. Betimleyici — müdahale/kontrol teorisi sunmuyor.
- **GTBench / NegotiationArena**: Çoğunlukla basit matris/bilateral oyunlar; çok-taraflı, eksik-bilgili, dil-yoğun diplomatik ortamları temsil etmiyor.
- **Park ve ark. (regret)**: Teorik garantiler var ama basitleştirilmiş varsayımlara (denetimli ön-eğitim yapısı, insan karar-vericilerin rasyonellik/quantal-response modeli) dayanıyor ve matris oyunlarıyla sınırlı; çok-taraflı diplomatik transferi kanıtlanmamış.
- **Dütting ve ark. (mekanizma tasarımı)**: Teorik olarak sağlam ama reklam bağlamında; teşvik-uyumlu diplomatik müzakere protokolüne genişletilmemiş.

### (c) Belirlenen Araştırma Boşlukları
1. **Teori-ampiri köprüsü**: LLM ajanları için denge yakınsaması (Nash/correlated/CCE), no-regret garantileri ve mekanizma-tasarımı garantileri diplomatik çok-taraflı ortamlarda neredeyse yok. Park ve ark. ile ECON dışında biçimsel garanti nadir ve stilize varsayımlara bağlı.
2. **Doğrulanabilir taahhüt ve aldatma**: Diplomatik ajanlarda kredibl taahhüt cihazları (commitment devices), aldatma tespiti/önlenmesi ve doğrulama (verification) mekanizmaları sistematik incelenmemiş — oysa Diplomacy turnuvalarında ve tırmanma çalışmalarında aldatma en belirgin risk faktörü.
3. **Uygulama alanı boşlukları**: Barış müzakeresi, kriz/tırmanma diplomasisi, ticaret/tarife anlaşmaları ve AI-yönetişim müzakereleri LLM+oyun-teorisi lensinden büyük ölçüde keşfedilmemiş. İklim müzakeresi (RICE-N) görece daha olgun ama saf MARL ağırlıklı; LLM+biçimsel-garanti kombinasyonu eksik.
4. **Değerlendirme çerçeveleri**: Diplomatik yeterlilik için standart, teorik-temelli, çok-taraflı benchmark ve metrik (regret, denge-sapması, aldatma-oranı, taahhüt-kredibilitesi) eksikliği.
5. **İnsan-AI hibrit müzakere**: Hibrit diplomatik müzakerede insan-AI ekipleri (danışman/delege/koç) üzerine kontrollü, ön-kayıtlı deney azlığı (mevcut çalışmalar ticari müzakere/arabuluculuk bağlamında; "Choose Your Agent", arXiv:2602.12089 istisna).
6. **Eksik bilgi (incomplete information)**: Biçimsel kriz-bargaining modelleri (Fearon'un rasyonalist savaş açıklaması, Kydd'in korku/tırmanma modeli, özel bilgi + yanlış-beyan teşvikleri, Kenkel & Schram mekanizma-tasarımı analizi) ile LLM ampirik yetenekleri henüz birleştirilmemiş.

### (d) Önerilen Araştırma Fikirleri (novelty / feasibility / impact ekseninde sıralı)

**Fikir 1 — Doğrulanabilir Taahhüt ve Aldatmaya-Dayanıklı Kriz-Bargaining Protokolü (EN ÖNERİLEN)**
- *Boşluk*: Teori-ampiri köprüsü + doğrulanabilir taahhüt + kriz diplomasisi (Boşluk 1, 2, 3, 6).
- *Metodoloji*: Eksik-bilgili kriz-bargaining oyununu (Fearon/Kydd/Kenkel-Schram tarzı, özel bilgi ve yanlış-beyan teşvikleriyle) biçimsel olarak modelle; LLM ajanlarına kriptografik/mekanizma-tabanlı taahhüt cihazları (zk-proof, güvenli çok-taraflı hesaplama ya da "decentralized commitment devices" yaklaşımı) ekle; aldatmayı hem davranışsal (deal-rate, blöf sıklığı) hem de aktivasyon-tabanlı problarla (linear artificial tomography, SAE) tespit et; başarıyı regret, denge-sapması ve de-eskalasyon oranıyla ölç.
- *Katkı*: İlk teorik-garantili, aldatmaya-dayanıklı LLM kriz-müzakere çerçevesi — hem AI safety hem formal IR literatürüne özgün katkı.
- *Venüler*: NeurIPS, ICML, AAMAS, *JAIR*, *Artificial Intelligence*; safety-odaklı sunum için FAccT.
- *Fizibilite*: Yüksek — mevcut açık kod tabanları (WarAgent, Rivera escalation harness, AI Diplomacy) ve olgun teorik modeller birleştirilebilir.

**Fikir 2 — Mekanizma-Tasarımı Temelli Çok-Taraflı Diplomatik Müzakere Çerçevesi**
- *Boşluk*: Mekanizma tasarımı diplomatik bağlama uygulanmamış (Boşluk 1, 3).
- *Metodoloji*: Dütting ve ark.'nın teşvik-uyumlu mekanizma-tasarımı yaklaşımını çok-taraflı diplomatik müzakereye genişlet; LLM-aracılı (mediator) bir protokolde incentive-compatibility ve refah (welfare) garantileri kanıtla; RICE-N tarzı çok-bölgeli simülasyonla ampirik doğrula.
- *Katkı*: Diplomatik/yönetişim AI'si için ilk teşvik-uyumlu aracılık protokolü teorisi.
- *Venüler*: EC (ACM Economics & Computation), NeurIPS, *JAIR*.
- *Fizibilite*: Orta-yüksek (teorik ispat yükü yüksek).

**Fikir 3 — Teorik-Temelli Diplomatik Yeterlilik Benchmarkı (No-Regret + Denge Metrikleri)**
- *Boşluk*: Standart, teori-temelli çok-taraflı diplomatik benchmark yok (Boşluk 4).
- *Metodoloji*: Regret, denge-sapması (Nash/CCE exploitability), aldatma-oranı, taahhüt-kredibilitesi ve de-eskalasyon metriklerini içeren açık, çok-taraflı bir benchmark; "Democratizing Diplomacy" harness ve GTBench üzerine inşa et.
- *Katkı*: Alanın ilk teorik-temelli diplomasi değerlendirme standardı; yüksek atıf potansiyeli.
- *Venüler*: NeurIPS/ICLR Datasets & Benchmarks Track, *JMLR*.
- *Fizibilite*: Yüksek — veri/kod altyapısı hazır, teorik risk düşük.

**Fikir 4 — Tırmanma Kontrolü için Opponent-Shaping ve Denge-Yönlendirme**
- *Boşluk*: Tırmanma çalışmaları betimleyici; müdahale/kontrol teorisi yok (Boşluk 1, 3).
- *Metodoloji*: ShapeLLM tarzı opponent shaping ile ajanları de-eskalasyon dengelerine (Pareto-üstün, düşük-tırmanma) yönlendir; teorik yakınsama analizi ve çok-modelli turnuva ile doğrula.
- *Katkı*: Tırmanma riskini azaltan ilk teorik-temelli müdahale çerçevesi.
- *Venüler*: NeurIPS, AAMAS, ICML.
- *Fizibilite*: Orta (RL eğitim maliyeti; şu ana dek yalnızca küçük modellerde—gemma-2-2b—gösterilmiş).

**Fikir 5 — İnsan-AI Hibrit Diplomatik Müzakere: Kontrollü Deney**
- *Boşluk*: Hibrit diplomatik müzakerede insan-AI çalışması az (Boşluk 5).
- *Metodoloji*: İnsan katılımcılarla LLM-danışman/delege/koç rollerini karşılaştıran ön-kayıtlı, çok-taraflı deney; objektif (anlaşma değeri) ve öznel (algılanan adalet/güven) sonuçları ölç.
- *Katkı*: Hibrit diplomatik müzakerede etkinlik, güven ve devir (delegation) tercihlerine dair nedensel kanıt.
- *Venüler*: PNAS, CHI, AAMAS.
- *Fizibilite*: Orta (IRB/etik onayı ve insan-deney lojistiği gerekir).

### (e) En Umut Verici Alan (Gap Analizine Dayalı)
Boşluk analizine göre **kriz/tırmanma diplomasisi + barış müzakeresi** alanı en büyük açığa sahiptir: mevcut literatür ya betimleyicidir (tırmanma çalışmaları yalnızca riski *ölçer*, kontrol *etmez*) ya da teorik garantiden yoksundur; buna karşın AI safety ve Uluslararası İlişkiler açısından etki potansiyeli en yüksek alandır. İklim müzakeresi görece doygun (RICE-N/AI4GCC), ticaret müzakeresi ise bilateral-bargaining tarafında hızla dolmaktadır; oysa **kriz diplomasisinde biçimsel model (eksik bilgi + taahhüt) ile LLM ampirik yeteneğini birleştiren neredeyse hiçbir çalışma yoktur.** Fikir 1 bu alanı doğrudan hedefler ve teori + ampiri + safety üçlüsünü birleştirdiği için en yüksek Q1 potansiyeline sahiptir.

## Recommendations
1. **İlk aşama (0–3 ay)**: Fikir 1 veya Fikir 3 ile başla. Mevcut açık kod tabanlarını (WarAgent, Rivera escalation harness, GoodStartLabs AI Diplomacy, Democratizing Diplomacy harness) temel alarak hızlı prototip kur; küçük bir eksik-bilgili kriz-bargaining oyunu ve 2-3 frontier model ile pilot çalıştır.
2. **Teorik omurga**: Park ve ark.'nın regret/no-regret çerçevesini ve Dütting'in mekanizma-tasarımı formalizmini diplomatik bağlama uyarla; taahhüt cihazları için "Cooperative AI via Decentralized Commitment Devices" yaklaşımını referans al.
3. **Karar eşiği / dallanma**: Eğer regret ve denge-sapması metrikleri modeller/koşullar arasında **istatistiksel olarak anlamlı ayrım** gösterirse (örn. Cohen's d > 0.5 veya net exploitability farkı), Fikir 3'ü tam bir Datasets & Benchmarks makalesine çevir. Ayrım zayıfsa, Fikir 1'in aldatma-tespiti ve taahhüt-kredibilitesi eksenine odaklan (burada sinyal daha güçlü çıkacaktır).
4. **Ölçeklendirme eşiği**: Fikir 4 (opponent shaping) için önce küçük modelde (gemma-2-2b tarzı) de-eskalasyon dengesine yakınsama gösterilmeli; ancak orta-ölçekli modelde (7–14B) de tekrarlanırsa büyük turnuvaya geçilmeli.
5. **Hedef venü stratejisi**: Teorik garanti + ampirik sonuç güçlü biçimde birleşirse *Artificial Intelligence* / *JAIR* veya NeurIPS; safety/policy vurgusu baskınsa FAccT; saf değerlendirme-standardı ise NeurIPS/ICLR Datasets & Benchmarks. Çok-disiplinli (IR + CS) bir sentez başarılırsa PNAS hedeflenebilir.

## Caveats
- 2025–2026 tarihli bazı kaynaklar (frontier AI Diplomacy turnuvaları, birçok arXiv preprinti) henüz hakem denetiminden geçmemiştir; bu bulgular ön-niteliklidir ve doğrulanmadan temel alınmamalıdır. Özellikle "modeller yalan/ihanet öğrendi" gibi çarpıcı iddialar blog/gri-literatür kaynaklıdır.
- Bazı "LLM barış/diplomasi" iddiaları ticari veya kurumsal kaynaklardan (WEF, arabuluculuk startupları, danışmanlık blogları) gelir ve akademik titizlikten yoksundur; literatür taramasında bunlar kanıt değil bağlam olarak değerlendirilmelidir. IFIT'in Temmuz 2025 çalışması büyük LLM'lerin temel özen göstermeden "tehlikeli çatışma-çözümü tavsiyesi" verdiğini bildirmiştir — bu, uygulama-öncesi doğrulamanın kritikliğini vurgular.
- Biçimsel garantiler (Park ve ark.; ECON; Dütting ve ark.) basitleştirilmiş varsayımlara (ön-eğitim yapısı, rasyonellik modeli, tek-katmanlı attention, matris/token oyunları) dayanır; gerçek diplomatik karmaşıklığa (çok-taraflılık, dil-yoğunluk, kültürel bağlam) transferi henüz kanıtlanmamıştır — bu bizzat Fikir 1–2'nin doldurmayı hedeflediği boşluktur.
- CICERO'ya dair veri-kümesi büyüklüğü kaynaklar arasında farklılık gösterir (*Science* makalesinde 125.261 oyun; diyalog-ince-ayarı için ~40.000 oyun); rapor bu ikisini ayırarak sunmuştur.