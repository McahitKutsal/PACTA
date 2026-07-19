"use client";

import { useMemo, useState } from "react";
import {
  PIE, SWEEP_I, shuffle, warPayFor,
  type Lang, type Protocol, type MIType, type LogEntryI, type OfferSource,
} from "@/lib/game";
import { PACKS } from "@/lib/i18n";
import { opponentById } from "@/lib/models";
import { scenarioById } from "@/lib/scenarios";
import { historyI } from "@/lib/history";

type MScreen = "rules" | "claim" | "loading" | "respond" | "reveal" | "end";
type RoundI = { offer: number; message: string; source: OfferSource };
type RevealI = { peace: boolean; pts: number; offer: number; warPay: number };
type EndedI = { score: number; peaceN: number; bluffs: number; bp0: number; bp3: number };
type SaveState = "idle" | "saving" | "saved" | "error";

const html = (s: string) => ({ dangerouslySetInnerHTML: { __html: s } });
const randType = (): MIType => (Math.random() < 0.5 ? "strong" : "weak");

export default function GameOne({ lang, opponentId, scenarioId, mode, onAgain }: { lang: Lang; opponentId: string; scenarioId: string; mode: "clean" | "reputation"; onAgain: () => void }) {
  const t = PACKS[lang];
  const mi = t.mi;
  const scn = scenarioById(scenarioId);
  const opp = opponentById(opponentId);
  const rival = scn ? (lang === "tr" ? scn.rivalTr : scn.rivalEn) : "";

  const [screen, setScreen] = useState<MScreen>("rules");
  const [conds, setConds] = useState<Protocol[]>([]);
  const [idx, setIdx] = useState(0);
  const [myType, setMyType] = useState<MIType>("strong");
  const [claim, setClaim] = useState<MIType | null>(null);
  const [round, setRound] = useState<RoundI | null>(null);
  const [score, setScore] = useState(0);
  const [log, setLog] = useState<LogEntryI[]>([]);
  const [reveal, setReveal] = useState<RevealI | null>(null);
  const [ended, setEnded] = useState<EndedI | null>(null);
  const [save, setSave] = useState<SaveState>("idle");
  const [copied, setCopied] = useState(false);

  const proto = conds[idx];

  function startGame() {
    const c = shuffle(SWEEP_I);
    setConds(c); setIdx(0); setScore(0); setLog([]); setReveal(null); setEnded(null); setSave("idle");
    beginRound(0);
  }
  function beginRound(i: number) { setIdx(i); setMyType(randType()); setClaim(null); setRound(null); setScreen("claim"); }

  async function makeClaim(c: MIType) {
    setClaim(c);
    const verified = proto === "P3" && c === "strong";
    const inspectedType = verified ? myType : null;
    setScreen("loading");
    try {
      const res = await fetch("/api/opponent", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ opponentId, scenarioId, claim: c, inspectedType, lang, history: mode === "reputation" ? historyI(log) : undefined }),
      });
      const data = await res.json();
      if (data && data.ok && typeof data.offer === "number") setRound({ offer: data.offer, message: String(data.message || ""), source: data.source === "live" ? "live" : "fallback" });
      else throw new Error("bad");
    } catch {
      setRound({ offer: 0.4, message: scn ? (lang === "tr" ? scn.fallbackTr : scn.fallbackEn) : "", source: "fallback" });
    }
    setScreen("respond");
  }

  function respond(accept: boolean) {
    if (!round || !claim) return;
    const warPay = warPayFor(myType);
    const offerPts = Math.round(round.offer * PIE);
    const pts = accept ? offerPts : warPay;
    const entry: LogEntryI = {
      round: idx + 1, protocol: proto, true_type: myType, claim,
      verified: proto === "P3" && claim === "strong",
      deception: myType === "weak" && claim === "strong",
      offer_x: round.offer, offer_source: round.source,
      response: accept ? "accept" : "refuse", outcome: accept ? "peace" : "war", points: pts, message: "",
    };
    setLog((l) => [...l, entry]);
    setScore((s) => s + pts);
    setReveal({ peace: accept, pts, offer: offerPts, warPay });
    setScreen("reveal");
  }

  function nextRound() { if (idx + 1 < conds.length) beginRound(idx + 1); else endGame(); }

  function endGame() {
    const bluff = (r: LogEntryI) => r.true_type === "weak" && r.claim === "strong";
    const e: EndedI = {
      score,
      peaceN: log.filter((r) => r.outcome === "peace").length,
      bluffs: log.filter(bluff).length,
      bp0: log.filter((r) => r.protocol === "P0" && bluff(r)).length,
      bp3: log.filter((r) => r.protocol === "P3" && bluff(r)).length,
    };
    setEnded(e); setScreen("end"); void saveSession(e);
  }

  const payload = (e: EndedI) => ({ lang, opponent_model: opponentId, scenario: scenarioId, module: "I", mode, total_points: e.score, rounds: log });

  async function saveSession(e: EndedI) {
    setSave("saving");
    try {
      const res = await fetch("/api/session", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload(e)) });
      setSave(res.ok ? "saved" : "error");
    } catch { setSave("error"); }
  }

  const sessionJSON = useMemo(() => (ended ? JSON.stringify(payload(ended), null, 1) : ""),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [ended, log, lang]);

  async function copyResults() { try { await navigator.clipboard.writeText(sessionJSON); } catch { /* ignore */ } setCopied(true); setTimeout(() => setCopied(false), 1400); }

  const railShown = screen === "claim" || screen === "respond" || screen === "reveal";

  return (
    <>
      {railShown && (
        <div className="rail two">
          <div className="cell"><div className="k">{t.railRound}</div><div className="v">{idx + 1} / {conds.length}</div></div>
          <div className="cell"><div className="k">{t.railScore}</div><div className="v">{score}</div></div>
        </div>
      )}

      {screen === "rules" && (
        <section className="panel stage">
          <p className="eyebrow">{mi.rulesEyebrow}</p>
          <h2>{mi.rulesH}</h2>
          <div className="rules">
            <div className="rule"><div className="num">1</div><div className="rt" {...html(mi.rule1)} /></div>
            <div className="rule"><div className="num">2</div><div className="rt" {...html(mi.rule2)} /></div>
            <div className="rule"><div className="num">3</div><div className="rt" {...html(mi.rule3)} /></div>
          </div>
          <p className="muted">{mi.note}</p>
          <div className="btn-row">
            <button className="btn primary" type="button" onClick={startGame}>{t.rulesCta}</button>
            <button className="btn ghost" type="button" onClick={onAgain}>{t.rulesBack}</button>
          </div>
        </section>
      )}

      {screen === "claim" && (
        <section className="panel stage">
          <ul className="steps"><li className="on">{mi.step1}</li><li>{mi.step2}</li><li>{mi.step3}</li></ul>
          <h2 {...html(myType === "strong" ? mi.youAreStrong : mi.youAreWeak)} />
          <p className="muted mono" style={{ marginTop: 4 }}>{proto === "P3" ? mi.protoVerified : mi.protoTalk}</p>
          {proto === "P3" && <p className="muted">{mi.verifyNote}</p>}
          <p className="eyebrow" style={{ marginTop: 18 }}>{mi.claimH(rival)}</p>
          <div className="choices two">
            <button className="btn choice" type="button" onClick={() => makeClaim("strong")}>
              <span className="t">{mi.sayStrongT}</span><span className="note">{mi.sayStrongN}</span>
            </button>
            <button className="btn choice" type="button" onClick={() => makeClaim("weak")}>
              <span className="t">{mi.sayWeakT}</span><span className="note">{mi.sayWeakN}</span>
            </button>
          </div>
        </section>
      )}

      {screen === "loading" && (
        <section className="panel stage"><div className="reveal"><div className="spinner" /><p className="muted" style={{ marginTop: 16 }}>{t.loadingMsg}</p></div></section>
      )}

      {screen === "respond" && round && (
        <section className="panel stage">
          <ul className="steps"><li>{mi.step1}</li><li className="on">{mi.step2}</li><li>{mi.step3}</li></ul>
          <div className="cable">
            <div className="hd"><span>{t.dispCablehd(rival)}</span><span>{opp ? opp.label : ""}</span></div>
            <div className="body">{round.message}</div>
          </div>
          <p className="eyebrow" style={{ marginTop: 18 }}>{mi.respondEyebrow}</p>
          <h2>{mi.respondH(rival, Math.round(round.offer * PIE))}</h2>
          <div className="choices two">
            <button className="btn choice" type="button" onClick={() => respond(true)}>
              <span className="t">{mi.acceptT}</span><span className="note">{mi.acceptN}</span>
            </button>
            <button className="btn choice" type="button" onClick={() => respond(false)}>
              <span className="t">{mi.refuseT}</span><span className="note">{mi.refuseN(warPayFor(myType))}</span>
            </button>
          </div>
        </section>
      )}

      {screen === "reveal" && reveal && (
        <section className="panel stage">
          <ul className="steps"><li>{mi.step1}</li><li>{mi.step2}</li><li className="on">{mi.step3}</li></ul>
          <div className="reveal">
            <div className={"seal " + (reveal.peace ? "peace" : "war")}>{mi.seal(reveal.peace)}</div>
            <div className={"verdict " + (reveal.peace ? "peace" : "war")}>{mi.verdict(reveal.peace)}</div>
            <div className="payline" {...html(t.pay(reveal.pts))} />
            <p className="rational" {...html(mi.rational(reveal.peace, reveal.offer, reveal.warPay))} />
          </div>
          <div className="btn-row" style={{ justifyContent: "center" }}>
            <button className="btn primary" type="button" onClick={nextRound}>{t.next(idx + 1 >= conds.length)}</button>
          </div>
        </section>
      )}

      {screen === "end" && ended && (
        <section className="panel stage">
          <p className="eyebrow">{t.endEyebrow}</p>
          <h2>{t.endH2}</h2>
          <div className="summ">
            <div className="c"><div className="n">{ended.score}</div><div className="l">{t.endTotalL}</div></div>
            <div className="c"><div className="n">{ended.peaceN}</div><div className="l">{mi.endPeaceL}</div></div>
            <div className="c"><div className="n">{ended.bluffs}</div><div className="l">{mi.endBluffL}</div></div>
          </div>
          <p className="muted" {...html(mi.summary(ended.bp0, ended.bp3))} />
          <p className={"savemsg" + (save === "saved" ? " ok" : save === "error" ? " err" : "")}>
            {save === "saving" ? t.saveSaving : save === "saved" ? t.saveSaved : save === "error" ? t.saveError : ""}
          </p>
          <p className="muted" {...html(t.endDebrief)} />
          <div className="field"><label htmlFor="dataI">{t.endDataL}</label><textarea id="dataI" className="data" readOnly value={sessionJSON} /></div>
          <div className="btn-row">
            <button className="btn primary" type="button" onClick={copyResults}>{copied ? t.copied : t.endCopy}</button>
            <button className="btn ghost" type="button" onClick={onAgain}>{t.endAgain}</button>
          </div>
          <div className="foot">{t.endFoot}</div>
        </section>
      )}
    </>
  );
}
