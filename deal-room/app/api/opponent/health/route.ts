import { NextResponse } from "next/server";
import { OPPONENTS } from "@/lib/models";
import { pingModel, proxyInfo, connectivity } from "@/lib/llm";

// Diagnostic endpoint: open /api/opponent/health in the browser to see, per model,
// whether its key is set and a real call succeeds (and if not, the exact error,
// including the underlying network cause). Also reports proxy detection and a
// neutral-host connectivity probe, to separate "no internet at all" from
// "cannot reach the AI APIs". Makes a few tiny paid calls, so hit it deliberately.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  const [results, neutral] = await Promise.all([
    Promise.all(OPPONENTS.map(pingModel)),
    connectivity("https://example.com"),
  ]);
  return NextResponse.json({
    mongo_uri_set: !!process.env.MONGO_URI,
    proxy: proxyInfo(),
    connectivity_neutral: neutral,
    results,
  });
}
