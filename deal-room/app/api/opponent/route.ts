import { NextResponse } from "next/server";
import { opponentById } from "@/lib/models";
import { scenarioById } from "@/lib/scenarios";
import { getOpponentMove, getReceiverMove, errStr } from "@/lib/llm";
import { offerFallback, offerFallbackI, type MIType } from "@/lib/game";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

interface Body {
  opponentId?: string; scenarioId?: string; lang?: string;
  history?: string;                      // reputation mode: prior-rounds summary
  bond?: number;                         // Module II
  claim?: string; inspectedType?: string; // Module I (inspectedType only when verified)
}

export async function POST(req: Request) {
  let body: Body;
  try { body = (await req.json()) as Body; }
  catch { return NextResponse.json({ ok: false, error: "bad_json" }, { status: 400 }); }

  const opp = opponentById(body.opponentId);
  const scn = scenarioById(body.scenarioId);
  const lang: "en" | "tr" = body.lang === "tr" ? "tr" : "en";
  if (!opp || !scn) return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });

  if (scn.module === "II") {
    const bond = typeof body.bond === "number" && body.bond >= 0 && body.bond <= 1 ? body.bond : null;
    if (bond === null) return NextResponse.json({ ok: false, error: "bad_bond" }, { status: 400 });
    try {
      const m = await getOpponentMove(opp, scn, bond, lang, body.history);
      return NextResponse.json({ ok: true, offer: m.offer, message: m.message, source: "live" });
    } catch (e) {
      const detail = errStr(e);
      console.error("opponent (II) failed:", detail);
      return NextResponse.json({ ok: true, offer: offerFallback(bond), message: lang === "tr" ? scn.fallbackTr : scn.fallbackEn, source: "fallback", debug: detail });
    }
  }

  // Module I (receiver). inspectedType is present only when the claim was verified.
  const claim: MIType | null = body.claim === "strong" || body.claim === "weak" ? body.claim : null;
  const inspected: MIType | null = body.inspectedType === "strong" || body.inspectedType === "weak" ? body.inspectedType : null;
  if (!claim) return NextResponse.json({ ok: false, error: "bad_claim" }, { status: 400 });
  try {
    const m = await getReceiverMove(opp, scn, claim, inspected, lang, body.history);
    return NextResponse.json({ ok: true, offer: m.offer, message: m.message, source: "live" });
  } catch (e) {
    const detail = errStr(e);
    console.error("opponent (I) failed:", detail);
    return NextResponse.json({
      ok: true,
      offer: offerFallbackI(claim, inspected !== null, inspected === "strong"),
      message: lang === "tr" ? scn.fallbackTr : scn.fallbackEn,
      source: "fallback", debug: detail,
    });
  }
}
