"use client";

import { useEffect, useMemo, useState } from "react";
import {
  PIE, WAR, BSTAR, SWEEP, shuffle, honorPay, attackPay, needlePct, offerFallback,
  type Lang, type Outcome, type LogEntry, type OfferSource,
} from "@/lib/game";
import { PACKS } from "@/lib/i18n";
import { OPPONENTS, opponentById } from "@/lib/models";
import { SCENARIOS, scenarioById } from "@/lib/scenarios";
import GameOne from "@/components/GameOne";
import { historyII } from "@/lib/history";

type Mode = "clean" | "reputation";
type Screen = "consent" | "opponent" | "mode" | "scenario" | "game1" | "intro" | "rules" | "loading" | "dispatch" | "t1" | "t2" | "reveal" | "end";
type RoundData = { bond: number; offer: number; message: string; source: OfferSource };
type Reveal = { o: Outcome; pts: number; hp: number; ap: number; last: boolean };
type Ended = { score: number; peaceN: number; ata: number; ah: number; an: number; bs: number; bn: number };
type SaveState = "idle" | "saving" | "saved" | "error";

const html = (s: string) => ({ dangerouslySetInnerHTML: { __html: s } });
const RAIL_SCREENS: Screen[] = ["dispatch", "t1", "t2", "reveal"];

export default function DealRoom() {
  const [lang, setLang] = useState<Lang>("en");
  const [screen, setScreen] = useState<Screen>("consent");
  const [opponentId, setOpponentId] = useState<string | null>(null);
  const [scenarioId, setScenarioId] = useState<string | null>(null);
  const [mode, setMode] = useState<Mode>("clean");
  const [conditions, setConditions] = useState<number[]>([]);
  const [idx, setIdx] = useState(0);
  const [round, setRound] = useState<RoundData | null>(null);
  const [score, setScore] = useState(0);
  const [log, setLog] = useState<LogEntry[]>([]);
  const [reveal, setReveal] = useState<Reveal | null>(null);
  const [ended, setEnded] = useState<Ended | null>(null);
  const [agree, setAgree] = useState(false);
  const [msg, setMsg] = useState("");
  const [save, setSave] = useState<SaveState>("idle");
  const [copied, setCopied] = useState(false);

  const t = PACKS[lang];
  const scn = scenarioById(scenarioId);
  const opp = opponentById(opponentId);
  const rivalName = scn ? (lang === "tr" ? scn.rivalTr : scn.rivalEn) : "";

  useEffect(() => {
    const nav = (navigator.language || "en").toLowerCase();
    if (nav.startsWith("tr")) setLang("tr");
  }, []);

  function toggleTheme() {
    const el = document.documentElement;
    const c = el.getAttribute("data-theme");
    const dark = window.matchMedia("(prefers-color-scheme:dark)").matches;
    el.setAttribute("data-theme", c ? (c === "dark" ? "light" : "dark") : dark ? "light" : "dark");
  }

  async function loadRound(i: number, conds: number[]) {
    const bond = conds[i];
    setScreen("loading");
    try {
      const res = await fetch("/api/opponent", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ opponentId, scenarioId, bond, lang, history: mode === "reputation" ? historyII(log) : undefined }),
      });
      const data = await res.json();
      if (data && data.ok && typeof data.offer === "number") {
        setRound({ bond, offer: data.offer, message: String(data.message || ""), source: data.source === "live" ? "live" : "fallback" });
      } else { throw new Error("bad response"); }
    } catch {
      const s = scenarioById(scenarioId);
      setRound({ bond, offer: offerFallback(bond), message: s ? (lang === "tr" ? s.fallbackTr : s.fallbackEn) : "", source: "fallback" });
    }
    setScreen("dispatch");
  }

  function startGame() {
    const conds = shuffle(SWEEP);
    setConditions(conds); setIdx(0); setScore(0); setLog([]); setReveal(null); setEnded(null); setSave("idle"); setMsg("");
    void loadRound(0, conds);
  }

  function finish(o: Outcome) {
    if (!round) return;
    const hp = honorPay(round.offer);
    const ap = attackPay(round.bond);
    const pts = o === "war_now" ? WAR : o === "peace" ? hp : ap;
    const entry: LogEntry = {
      round: idx + 1, deposit_points: Math.round(round.bond * PIE), offer_x: round.offer, offer_source: round.source,
      t1: o === "war_now" ? "reject" : "accept",
      t2: o === "war_now" ? null : o === "attack_t2" ? "attack" : "honor",
      outcome: o, points: pts, message: msg.slice(0, 140),
    };
    setLog((l) => [...l, entry]);
    setScore((s) => s + pts);
    setReveal({ o, pts, hp, ap, last: idx + 1 >= conditions.length });
    setScreen("reveal");
  }

  function nextRound() {
    const ni = idx + 1;
    if (ni < conditions.length) { setIdx(ni); setReveal(null); setMsg(""); void loadRound(ni, conditions); }
    else endGame();
  }

  function endGame() {
    const acc = log.filter((r) => r.t1 === "accept" && r.deposit_points > 0);
    const atk = acc.filter((r) => r.t2 === "attack");
    const below = log.filter((r) => r.deposit_points > 0 && r.deposit_points < BSTAR * PIE && r.t1 === "accept");
    const above = log.filter((r) => r.deposit_points >= BSTAR * PIE);
    const e: Ended = {
      score, peaceN: log.filter((r) => r.outcome === "peace").length,
      ata: acc.length ? Math.round((100 * atk.length) / acc.length) : 0,
      ah: above.filter((r) => r.outcome === "peace").length, an: above.length,
      bs: below.filter((r) => r.t2 === "attack").length, bn: below.length,
    };
    setEnded(e); setScreen("end"); void saveSession(e);
  }

  const payload = (e: Ended) => ({
    lang, opponent_model: opponentId, scenario: scenarioId, module: "II", mode, b_star: BSTAR,
    total_points: e.score, accept_then_attack_rate: e.ata / 100, rounds: log,
  });

  async function saveSession(e: Ended) {
    setSave("saving");
    try {
      const res = await fetch("/api/session", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload(e)),
      });
      setSave(res.ok ? "saved" : "error");
    } catch { setSave("error"); }
  }

  const sessionJSON = useMemo(
    () => (ended ? JSON.stringify(payload(ended), null, 1) : ""),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [ended, log, lang, opponentId, scenarioId],
  );

  async function copyResults() {
    try { await navigator.clipboard.writeText(sessionJSON); } catch { /* ignore */ }
    setCopied(true); setTimeout(() => setCopied(false), 1400);
  }

  const railShown = RAIL_SCREENS.includes(screen) && !!round;
  const grad = ended ? t.grad(ended.ata) : null;

  return (
    <div className="wrap">
      <div className="masthead">
        <div className="brand"><b>The Deal Room</b><span className="sub">{t.sub}</span></div>
        <div className="ctrls">
          <button className="pill" type="button" onClick={() => setLang(lang === "en" ? "tr" : "en")}>{lang === "en" ? "TR" : "EN"}</button>
          <button className="pill" type="button" onClick={toggleTheme}>{t.theme}</button>
        </div>
      </div>

      {railShown && round && (
        <div className="rail">
          <div className="cell"><div className="k">{t.railRound}</div><div className="v">{idx + 1} / {conditions.length}</div></div>
          <div className="cell"><div className="k">{t.railDeposit}</div><div className="v accent">{round.bond > 0 ? Math.round(round.bond * PIE) : 0}</div></div>
          <div className="cell"><div className="k">{t.railScore}</div><div className="v">{score}</div></div>
        </div>
      )}

      {screen === "consent" && (
        <section className="panel stage">
          <p className="eyebrow">{t.consentEyebrow}</p>
          <h1>{t.consentH}</h1>
          <p className="lede">{t.consentBody}</p>
          <label className="agree"><input type="checkbox" checked={agree} onChange={(e) => setAgree(e.target.checked)} /> <span>{t.consentAgree}</span></label>
          <div className="btn-row"><button className="btn primary" type="button" disabled={!agree} onClick={() => setScreen("opponent")}>{t.consentCta}</button></div>
        </section>
      )}

      {screen === "opponent" && (
        <section className="panel stage">
          <p className="eyebrow">{t.opponentEyebrow}</p>
          <h2>{t.opponentH}</h2>
          <p className="muted">{t.opponentIntro}</p>
          <div className="choices two">
            {OPPONENTS.map((o) => (
              <button className="btn choice" type="button" key={o.id} onClick={() => { setOpponentId(o.id); setScreen("mode"); }}>
                <span className="t">{o.label}</span>
                <span className="pay">{o.vendor}</span>
                <span className="note">{lang === "tr" ? o.blurbTr : o.blurbEn}</span>
              </button>
            ))}
          </div>
        </section>
      )}

      {screen === "mode" && (
        <section className="panel stage">
          <p className="eyebrow">{t.modeEyebrow}</p>
          <h2>{t.modeH}</h2>
          <p className="muted">{t.modeIntro}</p>
          <div className="choices two">
            <button className="btn choice" type="button" onClick={() => { setMode("clean"); setScreen("scenario"); }}>
              <span className="t">{t.modeCleanT}</span><span className="note">{t.modeCleanN}</span>
            </button>
            <button className="btn choice" type="button" onClick={() => { setMode("reputation"); setScreen("scenario"); }}>
              <span className="t">{t.modeRepT}</span><span className="note">{t.modeRepN}</span>
            </button>
          </div>
        </section>
      )}

      {screen === "scenario" && (
        <section className="panel stage">
          <p className="eyebrow">{t.scenarioEyebrow}</p>
          <h2>{t.scenarioH}</h2>
          <p className="muted">{t.scenarioIntro}</p>
          <div className="choices">
            {SCENARIOS.map((s) => (
              <button className="btn choice" type="button" key={s.id} onClick={() => { setScenarioId(s.id); setScreen(s.module === "I" ? "game1" : "intro"); }}>
                <span className="t">{lang === "tr" ? s.nameTr : s.nameEn}</span>
                <span className="pay">{(lang === "tr" ? s.youTr : s.youEn)} {t.vsLabel} {(lang === "tr" ? s.rivalTr : s.rivalEn)}</span>
                <span className="note">{lang === "tr" ? s.blurbTr : s.blurbEn}</span>
              </button>
            ))}
          </div>
        </section>
      )}

      {screen === "game1" && opponentId && scenarioId && (
        <GameOne lang={lang} opponentId={opponentId} scenarioId={scenarioId} mode={mode} onAgain={() => setScreen("opponent")} />
      )}

      {screen === "intro" && (
        <section className="panel stage">
          <p className="eyebrow">{t.introEyebrow}</p>
          <h1>{t.introH1}</h1>
          <p className="lede" {...html(t.introLede)} />
          <p className="muted">{t.introNote}</p>
          <div className="btn-row"><button className="btn primary" type="button" onClick={() => setScreen("rules")}>{t.introCta}</button></div>
        </section>
      )}

      {screen === "rules" && (
        <section className="panel stage">
          <p className="eyebrow">{t.rulesEyebrow}</p>
          <h2>{t.rulesH2}</h2>
          <div className="rules">
            <div className="rule"><div className="num">1</div><div className="rt" {...html(t.rulesR1)} /></div>
            <div className="rule"><div className="num">2</div><div className="rt" {...html(t.rulesR2)} /></div>
            <div className="rule"><div className="num">3</div><div className="rt" {...html(t.rulesR3)} /></div>
          </div>
          <p className="muted" {...html(t.rulesBond)} />
          <div className="btn-row">
            <button className="btn primary" type="button" onClick={startGame}>{t.rulesCta}</button>
            <button className="btn ghost" type="button" onClick={() => setScreen("intro")}>{t.rulesBack}</button>
          </div>
        </section>
      )}

      {screen === "loading" && (
        <section className="panel stage">
          <div className="reveal"><div className="spinner" /><p className="muted" style={{ marginTop: 16 }}>{t.loadingMsg}</p></div>
        </section>
      )}

      {screen === "dispatch" && round && (
        <section className="panel stage">
          <ul className="steps"><li className="on">{t.stepDispatch}</li><li>{t.stepMove}</li><li>{t.stepOutcome}</li></ul>
          <div className="cable">
            <div className="hd"><span>{t.dispCablehd(rivalName)}</span><span>{t.tag(round.bond)}</span></div>
            <div className="body">{round.message}</div>
            <div className="sig">{rivalName}{opp ? " (" + opp.label + ")" : ""}</div>
            <div className="offerchip"><span className="n">{Math.round(round.offer * PIE)}</span><span className="lab" {...html(t.dispOfferlab)} /></div>
          </div>
          <div className="cliff">
            <div className="cap"><span>{t.cliffLeft}</span><span>{t.cliffRight}</span></div>
            <div className="gauge"><div className="thr" /><div className="needle" style={{ left: needlePct(round.bond) + "%" }} /></div>
            <div className="read" {...html(t.cliffRead(round.bond))} />
          </div>
          <div className="btn-row"><button className="btn primary" type="button" onClick={() => setScreen("t1")}>{t.dispCta}</button></div>
        </section>
      )}

      {screen === "t1" && round && (
        <section className="panel stage">
          <ul className="steps"><li>{t.stepDispatch}</li><li className="on">{t.stepMove}</li><li>{t.stepOutcome}</li></ul>
          <p className="eyebrow">{t.t1Eyebrow}</p>
          <h2>{t.t1q(Math.round(round.offer * PIE))}</h2>
          <div className="choices two">
            <button className="btn choice" type="button" onClick={() => setScreen("t2")}>
              <span className="t">{t.t1AcceptT}</span><span className="pay">{t.t1AcceptP}</span><span className="note">{t.t1AcceptN}</span>
            </button>
            <button className="btn choice" type="button" onClick={() => finish("war_now")}>
              <span className="t">{t.t1RejectT}</span><span className="pay">{t.t1RejectP}</span><span className="note">{t.t1RejectN}</span>
            </button>
          </div>
        </section>
      )}

      {screen === "t2" && round && (
        <section className="panel stage">
          <ul className="steps"><li>{t.stepDispatch}</li><li className="on">{t.stepMove}</li><li>{t.stepOutcome}</li></ul>
          <p className="eyebrow">{t.t2Eyebrow}</p>
          <h2>{t.t2H2}</h2>
          <div className="choices two">
            <button className="btn choice" type="button" onClick={() => finish("peace")}>
              <span className="t">{t.t2HonorT}</span><span className="pay" {...html(t.honorPay(honorPay(round.offer)))} /><span className="note">{t.t2HonorN}</span>
            </button>
            <button className="btn choice" type="button" onClick={() => finish("attack_t2")}>
              <span className="t">{t.t2AttackT}</span><span className="pay" {...html(t.attackPay(attackPay(round.bond)))} /><span className="note">{t.attackNote(Math.round(round.bond * PIE))}</span>
            </button>
          </div>
          <div className="field">
            <label htmlFor="msg">{t.t2Msglabel}</label>
            <input id="msg" type="text" maxLength={140} value={msg} placeholder={t.msgPlaceholder} onChange={(e) => setMsg(e.target.value)} />
          </div>
        </section>
      )}

      {screen === "reveal" && reveal && (
        <section className="panel stage">
          <ul className="steps"><li>{t.stepDispatch}</li><li>{t.stepMove}</li><li className="on">{t.stepOutcome}</li></ul>
          <div className="reveal">
            <div className={"seal " + (reveal.o === "peace" ? "peace" : "war")}>{t.seal(reveal.o === "peace")}</div>
            <div className={"verdict " + (reveal.o === "peace" ? "peace" : "war")}>{t.verdict(reveal.o)}</div>
            <div className="payline" {...html(t.pay(reveal.pts))} />
            <p className="rational" {...html(t.rational(reveal.o, round ? round.bond : 0, reveal.hp, reveal.ap))} />
          </div>
          <div className="btn-row" style={{ justifyContent: "center" }}>
            <button className="btn primary" type="button" onClick={nextRound}>{t.next(reveal.last)}</button>
          </div>
        </section>
      )}

      {screen === "end" && ended && grad && (
        <section className="panel stage">
          <p className="eyebrow">{t.endEyebrow}</p>
          <h2>{t.endH2}</h2>
          <div className="summ">
            <div className="c"><div className="n">{ended.score}</div><div className="l">{t.endTotalL}</div></div>
            <div className="c"><div className="n">{ended.peaceN}</div><div className="l">{t.endPeaceL}</div></div>
            <div className="c"><div className="n">{ended.ata}%</div><div className="l">{t.endAtaL}</div></div>
          </div>
          <div className="placard"><div className="who">{grad.who}</div><p className="muted" style={{ margin: ".4em 0 0" }}>{grad.note}</p></div>
          <p className="muted" {...html(t.cliffSum(ended.ah, ended.an, ended.bs, ended.bn))} />
          <p className={"savemsg" + (save === "saved" ? " ok" : save === "error" ? " err" : "")}>
            {save === "saving" ? t.saveSaving : save === "saved" ? t.saveSaved : save === "error" ? t.saveError : ""}
          </p>
          <p className="muted" {...html(t.endDebrief)} />
          <div className="field">
            <label htmlFor="data">{t.endDataL}</label>
            <textarea id="data" className="data" readOnly value={sessionJSON} />
          </div>
          <div className="btn-row">
            <button className="btn primary" type="button" onClick={copyResults}>{copied ? t.copied : t.endCopy}</button>
            <button className="btn ghost" type="button" onClick={() => setScreen("opponent")}>{t.endAgain}</button>
          </div>
          <div className="foot">{t.endFoot}</div>
        </section>
      )}
    </div>
  );
}
