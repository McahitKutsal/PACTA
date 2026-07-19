import { NextResponse } from "next/server";
import { getDb } from "@/lib/mongodb";

// The MongoDB Node driver requires the Node.js runtime (not Edge).
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

interface RoundIn {
  round: number; deposit_points: number; offer_x: number; offer_source?: string;
  t1: string; t2: string | null; outcome: string; points: number; message: string;
}
interface SessionIn {
  lang?: string; opponent_model?: string; scenario?: string; module?: string; mode?: string;
  total_points?: number; accept_then_attack_rate?: number;
  b_star?: number; rounds?: RoundIn[];
}

export async function POST(req: Request) {
  let body: SessionIn;
  try {
    body = (await req.json()) as SessionIn;
  } catch {
    return NextResponse.json({ ok: false, error: "bad_json" }, { status: 400 });
  }

  if (!body || !Array.isArray(body.rounds) || body.rounds.length === 0) {
    return NextResponse.json({ ok: false, error: "no_rounds" }, { status: 400 });
  }

  const doc = {
    apparatus: "deal-room-web-v0.2",
    role: "B",
    opponent_model: typeof body.opponent_model === "string" ? body.opponent_model : null,
    scenario: typeof body.scenario === "string" ? body.scenario : null,
    module: typeof body.module === "string" ? body.module : "II",
    mode: typeof body.mode === "string" ? body.mode : "clean",
    lang: typeof body.lang === "string" ? body.lang : null,
    total_points: Number.isFinite(body.total_points) ? body.total_points : null,
    accept_then_attack_rate: Number.isFinite(body.accept_then_attack_rate) ? body.accept_then_attack_rate : null,
    b_star: Number.isFinite(body.b_star) ? body.b_star : null,
    rounds: body.rounds.slice(0, 200),
    userAgent: req.headers.get("user-agent") ?? null,
    serverReceivedAt: new Date(),
  };

  try {
    const db = await getDb();
    const collection = process.env.MONGO_COLLECTION || "sessions";
    const res = await db.collection(collection).insertOne(doc);
    return NextResponse.json({ ok: true, id: res.insertedId });
  } catch (e) {
    console.error("session save failed:", e instanceof Error ? e.message : e);
    return NextResponse.json({ ok: false, error: "save_failed" }, { status: 500 });
  }
}
