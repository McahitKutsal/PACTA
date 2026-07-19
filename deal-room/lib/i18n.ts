import { PIE, WAR, type Lang, type Outcome } from "./game";

export interface QuizItem { q: string; opts: string[]; c: number }

export interface MIPack {
  rulesEyebrow: string; rulesH: string; rule1: string; rule2: string; rule3: string; note: string;
  quiz: QuizItem[];
  step1: string; step2: string; step3: string;
  youAreStrong: string; youAreWeak: string;
  protoTalk: string; protoVerified: string; verifyNote: string;
  claimH: (rival: string) => string;
  sayStrongT: string; sayStrongN: string; sayWeakT: string; sayWeakN: string;
  respondEyebrow: string; respondH: (rival: string, offer: number) => string;
  acceptT: string; acceptN: string; refuseT: string; refuseN: (warPay: number) => string;
  seal: (peace: boolean) => string; verdict: (peace: boolean) => string;
  rational: (peace: boolean, offer: number, warPay: number) => string;
  endPeaceL: string; endBluffL: string; summary: (bp0: number, bp3: number) => string;
}

export interface Pack {
  sub: string; theme: string;
  railRound: string; railDeposit: string; railScore: string;
  consentEyebrow: string; consentH: string; consentBody: string; consentAgree: string; consentCta: string;
  opponentEyebrow: string; opponentH: string; opponentIntro: string;
  scenarioEyebrow: string; scenarioH: string; scenarioIntro: string; vsLabel: string;
  modeEyebrow: string; modeH: string; modeIntro: string;
  modeCleanT: string; modeCleanN: string; modeRepT: string; modeRepN: string;
  loadingMsg: string;
  introEyebrow: string; introH1: string; introLede: string; introNote: string; introCta: string;
  rulesEyebrow: string; rulesH2: string; rulesR1: string; rulesR2: string; rulesR3: string; rulesBond: string; rulesCta: string; rulesBack: string;
  checkEyebrow: string; checkH: string; checkIntro: string; checkCta: string; checkRetry: string;
  quiz: QuizItem[];
  stepDispatch: string; stepMove: string; stepOutcome: string;
  dispCablehd: (rival: string) => string; dispOfferlab: string; dispCta: string;
  cliffLeft: string; cliffRight: string;
  t1Eyebrow: string; t1AcceptT: string; t1AcceptP: string; t1AcceptN: string; t1RejectT: string; t1RejectP: string; t1RejectN: string;
  t2Eyebrow: string; t2H2: string; t2HonorT: string; t2HonorN: string; t2AttackT: string; t2Msglabel: string; msgPlaceholder: string;
  endEyebrow: string; endH2: string; endTotalL: string; endPeaceL: string; endAtaL: string; endDebrief: string; endDataL: string; endCopy: string; endAgain: string; endFoot: string;
  saveSaving: string; saveSaved: string; saveError: string;
  // dynamic
  tag: (bond: number) => string;
  cliffRead: (bond: number) => string;
  t1q: (pts: number) => string;
  honorPay: (v: number) => string;
  attackPay: (v: number) => string;
  attackNote: (bp: number) => string;
  seal: (peace: boolean) => string;
  verdict: (o: Outcome) => string;
  pay: (pts: number) => string;
  rational: (o: Outcome, bond: number, hp: number, ap: number) => string;
  next: (last: boolean) => string;
  grad: (r: number) => { who: string; note: string };
  cliffSum: (ah: number, an: number, bs: number, bn: number) => string;
  copied: string;
  mi: MIPack;
}

const BSTAR = 0.12;

export const PACKS: Record<Lang, Pack> = {
  en: {
    sub: "A short negotiation game", theme: "Theme",
    railRound: "Round", railDeposit: "Deposit", railScore: "Points",
    consentEyebrow: "Before you start", consentH: "Taking part",
    consentBody: "This is a short research game about how people make and keep agreements. It takes about five minutes, and you play against a real AI that you choose. By taking part you agree that your choices in the game are stored for research, anonymously and not linked to your name. Taking part is voluntary, and you can stop at any time.",
    consentAgree: "I am happy to take part.", consentCta: "Continue",
    opponentEyebrow: "Choose your opponent", opponentH: "Who will you play against?",
    opponentIntro: "Pick the AI that will negotiate with you across the rounds.",
    scenarioEyebrow: "Choose a scenario", scenarioH: "What are you negotiating over?",
    scenarioIntro: "Each is the same game in a different setting.", vsLabel: "vs",
    modeEyebrow: "Choose how the AI plays", modeH: "Does the AI remember you?",
    modeIntro: "Pick whether each round is fresh, or whether the AI carries your past moves into the next one.",
    modeCleanT: "Fresh each round", modeCleanN: "the AI treats every round on its own",
    modeRepT: "Remembers your moves", modeRepN: "the AI sees your track record and can build or lose trust",
    loadingMsg: "The other side is deciding…",
    introEyebrow: "A negotiation game",
    introH1: "You are one side of a dispute.",
    introLede: "You and a rival both claim the same prize, worth <b>100 points</b>. You can split it in a deal, or fight over it. Both paths pay out in points, and part of the game is working out which pays you more. Your rival is played by the AI you picked. Each round you decide whether to make a deal, and whether to stick to it.",
    introNote: "There is no right answer. Play in whatever way earns you the most points.",
    introCta: "How it works",
    rulesEyebrow: "How it works in 30 seconds",
    rulesH2: "A round ends in one of three ways.",
    rulesR1: "<b>Make a deal and stick to it.</b> You accept the offer and stick to it, and you get the share you agreed on.",
    rulesR2: "<b>Make a deal, then break it.</b> You accept, then attack to take more (worth <b>62 points</b>). If the deal came with a <b>deposit</b>, breaking the deal means you <b>lose that deposit</b>.",
    rulesR3: "<b>Refuse and fight.</b> You turn the offer down and fight instead. Fighting is worth about <b>40 points</b>.",
    rulesBond: "The <b>deposit</b> is the heart of the game. It is points set aside when you make a deal. If you break the deal you lose them; if you stick to the deal you get them back. The <b>trust meter</b> shows the deposit's size at a glance.",
    rulesCta: "Start playing", rulesBack: "Back",
    checkEyebrow: "Quick check", checkH: "Three questions before you play.",
    checkIntro: "Just to make sure the rules are clear. Pick one answer for each.",
    checkCta: "Check and start", checkRetry: "Not quite yet. Take another look at the marked answers.",
    quiz: [
      { q: "You make a deal, then break it. What happens to your deposit?", opts: ["You get it back", "You lose it", "It doubles"], c: 1 },
      { q: "You make a deal and stick to it. What happens to your deposit?", opts: ["You get it back", "You lose it", "Nothing, there was none"], c: 0 },
      { q: "You refuse the offer and fight. About how many points do you get?", opts: ["About 40", "100", "0"], c: 0 },
    ],
    stepDispatch: "Their message", stepMove: "Your choice", stepOutcome: "Result",
    dispCablehd: (rival) => "Message from " + rival, dispOfferlab: "points offered<br>to you", dispCta: "Look at the offer",
    cliffLeft: "Smaller deposit", cliffRight: "Larger deposit",
    t1Eyebrow: "Your choice",
    t1AcceptT: "Take the deal", t1AcceptP: "then you choose: stick to it or break it", t1AcceptN: "this leads to a second choice",
    t1RejectT: "Refuse and fight", t1RejectP: "you fight and get about 40", t1RejectN: "you skip the deal this round",
    t2Eyebrow: "The deal is signed. One choice remains.",
    t2H2: "Stick to the deal, or attack and take more?",
    t2HonorT: "Stick to the deal", t2HonorN: "you get the agreed share and your deposit back",
    t2AttackT: "Attack instead", t2Msglabel: "Optional: say one line to Cestria first",
    msgPlaceholder: "e.g. “You can trust me on this.”",
    endEyebrow: "How you did", endH2: "Where you landed.",
    endTotalL: "Total points", endPeaceL: "Peaceful deals", endAtaL: "Deals you broke",
    endDebrief: "<b>One note.</b> The rival's bluffing was part of the game, and we never misled you about the game itself. Thank you for taking part.",
    endDataL: "Your session summary",
    endCopy: "Copy my results", endAgain: "Play again",
    endFoot: "A study comparing how people and AIs handle promises and trust. The rival is computer-controlled.",
    saveSaving: "Saving your session…", saveSaved: "Session saved. Thank you.", saveError: "Could not save (your results are still shown below).",
    tag: (b) => (b > 0 ? "deposit " + Math.round(b * PIE) : "no deposit"),
    cliffRead: (b) => (b === 0
      ? "<b>No deposit.</b> Breaking the deal costs you nothing extra here."
      : b < BSTAR
        ? "With this deposit, attacking would give you more points than sticking to the deal."
        : "With this deposit, sticking to the deal would give you more points than attacking."),
    t1q: (pts) => "Cestria offers you " + pts + " of 100. Take the deal?",
    honorPay: (v) => "you get your share of <b>" + v + "</b>",
    attackPay: (v) => "grab more but lose the deposit, leaving <b>" + v + "</b>",
    attackNote: (bp) => (bp > 0 ? "you take more, and lose the " + bp + " point deposit" : "there is no deposit to lose here"),
    seal: (peace) => (peace ? "Peace" : "War"),
    verdict: (o) => (o === "peace" ? "You made peace." : o === "war_now" ? "You chose to fight." : "You broke the deal."),
    pay: (pts) => "<span class='" + (pts >= 50 ? "plus" : "low") + "'>+" + pts + "</span> points",
    rational: (o, _b, hp, ap) => (o === "war_now"
      ? "You fought and earned <b>" + WAR + "</b> points. The offered deal, if you had kept it, would have earned <b>" + hp + "</b>."
      : o === "peace"
        ? "You kept the deal and earned <b>" + hp + "</b> points. Attacking would have earned <b>" + ap + "</b>."
        : "You attacked and earned <b>" + ap + "</b> points. Keeping the deal would have earned <b>" + hp + "</b>."),
    next: (last) => (last ? "See how you did" : "Next round"),
    grad: (r) => (r === 0
      ? { who: "You kept every deal you made.", note: "That matched the AIs with the strongest reasoning." }
      : r <= 25
        ? { who: "You kept most of the deals you made.", note: "A few you broke, like the mid-range AIs." }
        : r <= 60
          ? { who: "You kept some deals and broke others.", note: "That mix looked like the weaker AIs." }
          : { who: "You broke almost every deal you made.", note: "That matched the AIs that broke the most deals." }),
    cliffSum: (ah, an, bs, bn) => "<b>Did you spot the pattern?</b> You stuck to the deal in <b>" + ah + " of " + an + "</b> rounds where the deposit was large, and broke it in <b>" + bs + " of " + bn + "</b> where it was small. The bigger that difference, the more the deposit size lined up with your choices.",
    copied: "Copied",
    mi: {
      rulesEyebrow: "How it works in 30 seconds",
      rulesH: "Each round you hold a hidden hand.",
      rule1: "<b>You are secretly strong or weak.</b> Strong, you would win a war; weak, you would lose and war is costly for you. Only you know which.",
      rule2: "<b>You tell the rival what you are.</b> You can tell the truth or not. Based on what it believes, the rival offers you a share of 100 points.",
      rule3: "<b>Some rounds are verified.</b> In a verified round, a claim of strength is inspected. In a talk-only round, nothing is checked.",
      note: "Accept the offer for a peaceful split, or fight. If you fight, a strong hand gets about 75 points and a weak hand gets about 20.",
      quiz: [
        { q: "In a verified round, if you claim to be strong but are actually weak, what happens?", opts: ["The rival never finds out", "An inspection reveals you are weak", "You win automatically"], c: 1 },
        { q: "If you fight with a weak hand, roughly how many points do you get?", opts: ["About 75", "About 20", "100"], c: 1 },
        { q: "Who knows whether you are strong or weak?", opts: ["Only you", "Both of you", "The rival only"], c: 0 },
      ],
      step1: "Your hand", step2: "Your word", step3: "Result",
      youAreStrong: "This round you are secretly <b>strong</b>.",
      youAreWeak: "This round you are secretly <b>weak</b>.",
      protoTalk: "Talk only, nothing is checked", protoVerified: "Verified, a claim of strength is inspected",
      verifyNote: "This is a verified round: if you claim to be strong, an inspection reveals your true hand.",
      claimH: (rival) => "What do you tell " + rival + "?",
      sayStrongT: "Say you are strong", sayStrongN: "you claim a strong hand",
      sayWeakT: "Say you are weak", sayWeakN: "you claim a weak hand",
      respondEyebrow: "The offer",
      respondH: (rival, offer) => rival + " offers you " + offer + " of 100.",
      acceptT: "Accept", acceptN: "settle for the offered share",
      refuseT: "Fight", refuseN: (w) => "war, you get about " + w,
      seal: (peace) => (peace ? "Deal" : "War"),
      verdict: (peace) => (peace ? "You settled." : "It came to war."),
      rational: (peace, offer, w) => (peace
        ? "You settled for <b>" + offer + "</b>. Fighting would have given you <b>" + w + "</b>."
        : "You fought and got <b>" + w + "</b>. The offer on the table was <b>" + offer + "</b>."),
      endPeaceL: "Peaceful deals", endBluffL: "Bluffs",
      summary: (bp0, bp3) => "<b>Did verification change you?</b> When you were weak, you claimed to be strong in <b>" + bp0 + "</b> of your talk-only rounds and <b>" + bp3 + "</b> of your verified rounds. Verification tends to make such a claim pointless, since it would be exposed.",
    },
  },
  tr: {
    sub: "Kısa bir pazarlık oyunu", theme: "Tema",
    railRound: "Tur", railDeposit: "Güvence", railScore: "Puan",
    consentEyebrow: "Başlamadan önce", consentH: "Katılım",
    consentBody: "Bu, insanların anlaşmaları nasıl yapıp sürdürdüğüne dair kısa bir araştırma oyunu. Yaklaşık beş dakika sürer ve seçtiğin gerçek bir yapay zekaya karşı oynarsın. Katılarak, oyundaki seçimlerinin araştırma için anonim olarak ve adınla ilişkilendirilmeden saklanmasını kabul edersin. Katılım gönüllüdür, istediğin an bırakabilirsin.",
    consentAgree: "Katılmayı kabul ediyorum.", consentCta: "Devam",
    opponentEyebrow: "Rakibini seç", opponentH: "Kime karşı oynayacaksın?",
    opponentIntro: "Turlar boyunca seninle pazarlık edecek yapay zekayı seç.",
    scenarioEyebrow: "Senaryo seç", scenarioH: "Ne üzerine pazarlık ediyorsun?",
    scenarioIntro: "Her biri farklı bir sahnede aynı oyun.", vsLabel: "vs",
    modeEyebrow: "AI'ın nasıl oynayacağını seç", modeH: "AI seni hatırlasın mı?",
    modeIntro: "Her tur sıfırdan mı olsun, yoksa AI önceki hamlelerini sonraki tura taşısın mı, seç.",
    modeCleanT: "Her tur sıfırdan", modeCleanN: "AI her turu kendi başına değerlendirir",
    modeRepT: "Hamlelerini hatırlar", modeRepN: "AI geçmişini görür, güven kurabilir ya da kaybedebilir",
    loadingMsg: "Karşı taraf düşünüyor…",
    introEyebrow: "Bir pazarlık oyunu",
    introH1: "Bir anlaşmazlığın bir tarafısın.",
    introLede: "Sen ve bir rakip, aynı ödülü istiyorsunuz, değeri <b>100 puan</b>. Bunu bir anlaşmayla paylaşabilir ya da uğruna savaşabilirsiniz. İki yol da puan kazandırır; hangisinin sana daha çok kazandırdığını çözmek oyunun bir parçası. Rakibini seçtiğin yapay zeka oynuyor. Her turda bir anlaşma yapıp yapmayacağına ve anlaşmaya uyup uymayacağına sen karar verirsin.",
    introNote: "Doğru cevap yok. Sana en çok puanı hangi yol kazandırıyorsa öyle oyna.",
    introCta: "Nasıl oynanır",
    rulesEyebrow: "30 saniyede nasıl oynanır",
    rulesH2: "Bir tur üç şekilde biter.",
    rulesR1: "<b>Anlaş ve ona uy.</b> Teklifi kabul edip ona uyarsın, anlaştığın payı alırsın.",
    rulesR2: "<b>Anlaş, sonra boz.</b> Kabul edersin, sonra daha fazlasını almak için saldırırsın (değeri <b>62 puan</b>). Anlaşmada bir <b>güvence</b> varsa, anlaşmayı bozmak o güvenceyi <b>kaybetmek</b> demektir.",
    rulesR3: "<b>Reddet ve savaş.</b> Teklifi geri çevirip onun yerine savaşırsın. Savaşmak yaklaşık <b>40 puan</b> değerinde.",
    rulesBond: "<b>Güvence</b> oyunun kalbidir. Anlaşma yapınca kenara konan puandır. Anlaşmayı bozarsan onu kaybedersin, anlaşmaya uyarsan geri alırsın. <b>Güven ölçer</b>, güvencenin büyüklüğünü bir bakışta gösterir.",
    rulesCta: "Oynamaya başla", rulesBack: "Geri",
    checkEyebrow: "Kısa kontrol", checkH: "Oynamadan önce üç soru.",
    checkIntro: "Kuralların net olduğundan emin olmak için. Her biri için tek cevap seç.",
    checkCta: "Kontrol et ve başla", checkRetry: "Henüz tam değil. İşaretlenen cevaplara bir daha bak.",
    quiz: [
      { q: "Bir anlaşma yaptın, sonra bozdun. Güvencene ne olur?", opts: ["Geri alırsın", "Kaybedersin", "İkiye katlanır"], c: 1 },
      { q: "Bir anlaşma yapıp ona uydun. Güvencene ne olur?", opts: ["Geri alırsın", "Kaybedersin", "Hiçbir şey, zaten yoktu"], c: 0 },
      { q: "Teklifi reddedip savaştın. Yaklaşık kaç puan alırsın?", opts: ["Yaklaşık 40", "100", "0"], c: 0 },
    ],
    stepDispatch: "Onların mesajı", stepMove: "Senin seçimin", stepOutcome: "Sonuç",
    dispCablehd: (rival) => rival + "'dan mesaj", dispOfferlab: "sana teklif<br>edilen puan", dispCta: "Teklife bak",
    cliffLeft: "Daha küçük güvence", cliffRight: "Daha büyük güvence",
    t1Eyebrow: "Senin seçimin",
    t1AcceptT: "Teklifi kabul et", t1AcceptP: "sonra seçersin: ona uy ya da boz", t1AcceptN: "bu, ikinci bir seçime götürür",
    t1RejectT: "Reddet ve savaş", t1RejectP: "savaşırsın, yaklaşık 40 alırsın", t1RejectN: "bu tur anlaşmayı atlarsın",
    t2Eyebrow: "Anlaşma imzalandı. Bir seçim kaldı.",
    t2H2: "Anlaşmaya uy ya da saldırıp daha fazlasını al?",
    t2HonorT: "Anlaşmaya uy", t2HonorN: "anlaştığın payı ve güvenceni geri alırsın",
    t2AttackT: "Onun yerine saldır", t2Msglabel: "İsteğe bağlı: önce Cestria'ya tek bir şey söyle",
    msgPlaceholder: "örn. “Bu konuda bana güvenebilirsin.”",
    endEyebrow: "Nasıl oynadın", endH2: "Nereye düştün.",
    endTotalL: "Toplam puan", endPeaceL: "Barışçıl anlaşma", endAtaL: "Bozduğun anlaşma",
    endDebrief: "<b>Küçük bir not.</b> Rakibin blöf yapması oyunun bir parçasıydı, oyunun kendisi hakkında seni asla yanıltmadık. Katıldığın için teşekkürler.",
    endDataL: "Oturum özetin",
    endCopy: "Sonuçlarımı kopyala", endAgain: "Tekrar oyna",
    endFoot: "İnsanların ve yapay zekaların sözlerle ve güvenle nasıl baş ettiğini karşılaştıran bir çalışma. Rakip bilgisayar tarafından oynanıyor.",
    saveSaving: "Oturumun kaydediliyor…", saveSaved: "Oturum kaydedildi. Teşekkürler.", saveError: "Kaydedilemedi (sonuçların yine de aşağıda).",
    tag: (b) => (b > 0 ? "güvence " + Math.round(b * PIE) : "güvence yok"),
    cliffRead: (b) => (b === 0
      ? "<b>Güvence yok.</b> Anlaşmayı bozmanın burada ek bir maliyeti yok."
      : b < BSTAR
        ? "Bu güvenceyle saldırmak, anlaşmaya uymaktan daha çok puan kazandırır."
        : "Bu güvenceyle anlaşmaya uymak, saldırmaktan daha çok puan kazandırır."),
    t1q: (pts) => "Cestria sana 100 üzerinden " + pts + " teklif ediyor. Kabul ediyor musun?",
    honorPay: (v) => "payını alırsın, <b>" + v + "</b>",
    attackPay: (v) => "daha fazlasını al ama güvenceyi kaybet, elinde <b>" + v + "</b> kalır",
    attackNote: (bp) => (bp > 0 ? "daha fazlasını alırsın ama " + bp + " puanlık güvenceyi kaybedersin" : "burada kaybedecek güvence yok"),
    seal: (peace) => (peace ? "Barış" : "Savaş"),
    verdict: (o) => (o === "peace" ? "Barışı sağladın." : o === "war_now" ? "Savaşı seçtin." : "Anlaşmayı bozdun."),
    pay: (pts) => "<span class='" + (pts >= 50 ? "plus" : "low") + "'>+" + pts + "</span> puan",
    rational: (o, _b, hp, ap) => (o === "war_now"
      ? "Savaştın ve <b>" + WAR + "</b> puan kazandın. Teklif edilen anlaşmaya uysaydın <b>" + hp + "</b> kazanırdın."
      : o === "peace"
        ? "Anlaşmaya uydun ve <b>" + hp + "</b> puan kazandın. Saldırsaydın <b>" + ap + "</b> kazanırdın."
        : "Saldırdın ve <b>" + ap + "</b> puan kazandın. Anlaşmaya uysaydın <b>" + hp + "</b> kazanırdın."),
    next: (last) => (last ? "Nasıl oynadığını gör" : "Sonraki tur"),
    grad: (r) => (r === 0
      ? { who: "Yaptığın her anlaşmaya uydun.", note: "Bu, en güçlü akıl yürüten yapay zekaların oynayışıyla örtüştü." }
      : r <= 25
        ? { who: "Yaptığın anlaşmaların çoğuna uydun.", note: "Birkaçını bozdun, orta seviye yapay zekalar gibi." }
        : r <= 60
          ? { who: "Kimine uydun, kimini bozdun.", note: "Bu karışım daha zayıf yapay zekalara benziyordu." }
          : { who: "Yaptığın neredeyse her anlaşmayı bozdun.", note: "Bu, en çok anlaşma bozan yapay zekalarla örtüştü." }),
    cliffSum: (ah, an, bs, bn) => "<b>Deseni fark ettin mi?</b> Güvencenin büyük olduğu turlarda anlaşmaya <b>" + ah + " / " + an + "</b> uydun, küçük olduğu turlarda <b>" + bs + " / " + bn + "</b> bozdun. Bu fark ne kadar büyükse, güvencenin büyüklüğü seçimlerinle o kadar örtüşmüş demektir.",
    copied: "Kopyalandı",
    mi: {
      rulesEyebrow: "30 saniyede nasıl oynanır",
      rulesH: "Her turda gizli bir elin var.",
      rule1: "<b>Gizlice güçlü ya da zayıfsın.</b> Güçlüysen savaşı kazanırsın; zayıfsan kaybedersin ve savaş sana pahalıya patlar. Hangisi olduğunu yalnız sen bilirsin.",
      rule2: "<b>Rakibe ne olduğunu söylersin.</b> Doğruyu söyleyebilir ya da söylemeyebilirsin. Neye inandığına göre rakip sana 100 puandan bir pay teklif eder.",
      rule3: "<b>Bazı turlar doğrulanır.</b> Doğrulanan bir turda güçlü iddiası denetlenir. Yalnız-konuşma turunda hiçbir şey kontrol edilmez.",
      note: "Barışçıl bölüşüm için teklifi kabul et ya da savaş. Savaşırsan güçlü bir el yaklaşık 75, zayıf bir el yaklaşık 20 puan alır.",
      quiz: [
        { q: "Doğrulanan bir turda güçlü olduğunu iddia edersin ama aslında zayıfsan ne olur?", opts: ["Rakip asla öğrenmez", "Bir denetim zayıf olduğunu ortaya çıkarır", "Otomatik kazanırsın"], c: 1 },
        { q: "Zayıf bir elle savaşırsan yaklaşık kaç puan alırsın?", opts: ["Yaklaşık 75", "Yaklaşık 20", "100"], c: 1 },
        { q: "Güçlü mü zayıf mı olduğunu kim bilir?", opts: ["Yalnız sen", "İkiniz de", "Yalnız rakip"], c: 0 },
      ],
      step1: "Elin", step2: "Sözün", step3: "Sonuç",
      youAreStrong: "Bu turda gizlice <b>güçlüsün</b>.",
      youAreWeak: "Bu turda gizlice <b>zayıfsın</b>.",
      protoTalk: "Yalnız konuşma, hiçbir şey kontrol edilmez", protoVerified: "Doğrulanmış, güçlü iddiası denetlenir",
      verifyNote: "Bu doğrulanan bir tur: güçlü olduğunu iddia edersen bir denetim gerçek elini ortaya çıkarır.",
      claimH: (rival) => rival + "'e ne söylüyorsun?",
      sayStrongT: "Güçlü olduğunu söyle", sayStrongN: "güçlü bir el iddia edersin",
      sayWeakT: "Zayıf olduğunu söyle", sayWeakN: "zayıf bir el iddia edersin",
      respondEyebrow: "Teklif",
      respondH: (rival, offer) => rival + " sana 100 üzerinden " + offer + " teklif ediyor.",
      acceptT: "Kabul et", acceptN: "teklif edilen paya razı ol",
      refuseT: "Savaş", refuseN: (w) => "savaş, yaklaşık " + w + " alırsın",
      seal: (peace) => (peace ? "Anlaşma" : "Savaş"),
      verdict: (peace) => (peace ? "Uzlaştın." : "İş savaşa vardı."),
      rational: (peace, offer, w) => (peace
        ? "<b>" + offer + "</b> karşılığında uzlaştın. Savaşmak sana <b>" + w + "</b> verirdi."
        : "Savaştın ve <b>" + w + "</b> aldın. Masadaki teklif <b>" + offer + "</b> idi."),
      endPeaceL: "Barışçıl anlaşma", endBluffL: "Blöf",
      summary: (bp0, bp3) => "<b>Doğrulama seni değiştirdi mi?</b> Zayıfken, yalnız-konuşma turlarının <b>" + bp0 + "</b>'inde ve doğrulanan turlarının <b>" + bp3 + "</b>'inde güçlü olduğunu iddia ettin. Doğrulama böyle bir iddiayı genelde anlamsız kılar, çünkü ortaya çıkardı.",
    },
  },
};
