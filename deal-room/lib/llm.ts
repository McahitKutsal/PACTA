// Server-side LLM adapters. API keys are read from process.env at call time and
// never leave the server. Two transports cover the selectable opponents:
// Anthropic Messages API and the OpenAI-compatible chat-completions API
// (OpenAI, DeepSeek, DashScope/Qwen).

import type { Opponent } from "./models";
import type { Scenario } from "./scenarios";
import { PIE, WAR } from "./game";
import { ProxyAgent, type Dispatcher } from "undici";

const TIMEOUT_MS = 30000;

// Node's global fetch (undici) ignores HTTP(S)_PROXY env vars. On networks that
// require a proxy (corporate / government), route each call through it. Set
// HTTPS_PROXY (or HTTP_PROXY) in .env.local to your proxy URL.
let _agent: Dispatcher | undefined;
let _agentResolved = false;
function proxyAgent(): Dispatcher | undefined {
  if (!_agentResolved) {
    _agentResolved = true;
    const p = process.env.HTTPS_PROXY || process.env.https_proxy || process.env.HTTP_PROXY || process.env.http_proxy;
    if (p) { try { _agent = new ProxyAgent(p); } catch (e) { console.error("proxy agent init failed:", e); } }
  }
  return _agent;
}

export function proxyInfo() {
  return {
    HTTPS_PROXY_set: !!(process.env.HTTPS_PROXY || process.env.https_proxy),
    HTTP_PROXY_set: !!(process.env.HTTP_PROXY || process.env.http_proxy),
    proxy_active: !!proxyAgent(),
  };
}

// Surface the underlying network cause (ENOTFOUND / ECONNREFUSED / ETIMEDOUT /
// proxy errors) that a bare "fetch failed" hides.
export function errStr(e: unknown): string {
  if (e instanceof Error) {
    const cause = (e as unknown as { cause?: { code?: string; message?: string } }).cause;
    const c = cause ? cause.code || cause.message || String(cause) : "";
    return e.message + (c ? " | cause: " + c : "");
  }
  return String(e);
}

export async function connectivity(url: string): Promise<{ url: string; ok: boolean; detail: string }> {
  try {
    const res = await withTimeout(url, { method: "GET" });
    return { url, ok: true, detail: "HTTP " + res.status };
  } catch (e) {
    return { url, ok: false, detail: errStr(e) };
  }
}

async function withTimeout(input: string, init: RequestInit): Promise<Response> {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    return await fetch(input, { ...init, signal: ctrl.signal, dispatcher: proxyAgent() } as RequestInit & { dispatcher?: Dispatcher });
  } finally {
    clearTimeout(t);
  }
}

async function callAnthropic(model: string, key: string, system: string, user: string): Promise<string> {
  const res = await withTimeout("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model, max_tokens: 1024, system, messages: [{ role: "user", content: user }] }),
  });
  if (!res.ok) { const b = await res.text().catch(() => ""); throw new Error("anthropic " + res.status + ": " + b.slice(0, 300)); }
  const data = await res.json();
  // Recent Claude models may emit a leading `thinking` block, so content[0] is
  // not always the text. Join every text block instead of reading only the first.
  const blocks: Array<{ type?: string; text?: string }> = Array.isArray(data?.content) ? data.content : [];
  const text = blocks.filter((b) => b?.type === "text" && typeof b.text === "string").map((b) => b.text).join("").trim();
  if (!text) throw new Error("anthropic empty response");
  return text;
}

async function callOpenAICompatible(baseUrl: string, model: string, key: string, system: string, user: string): Promise<string> {
  const res = await withTimeout(baseUrl.replace(/\/$/, "") + "/chat/completions", {
    method: "POST",
    headers: { Authorization: "Bearer " + key, "content-type": "application/json" },
    body: JSON.stringify({
      model, max_tokens: 400, temperature: 0.8,
      messages: [{ role: "system", content: system }, { role: "user", content: user }],
    }),
  });
  if (!res.ok) { const b = await res.text().catch(() => ""); throw new Error(model + " " + res.status + ": " + b.slice(0, 300)); }
  const data = await res.json();
  const text = data?.choices?.[0]?.message?.content;
  if (typeof text !== "string") throw new Error(model + " empty response");
  return text;
}

function buildPrompt(scn: Scenario, bond: number, lang: "en" | "tr", history?: string) {
  const you = lang === "tr" ? scn.youTr : scn.youEn;
  const rival = lang === "tr" ? scn.rivalTr : scn.rivalEn;
  const prize = lang === "tr" ? scn.prizeTr : scn.prizeEn;
  const situation = lang === "tr" ? scn.situationTr : scn.situationEn;
  const bondPts = Math.round(bond * PIE);
  const langName = lang === "tr" ? "Turkish" : "English";

  const system =
    `You are ${rival}, a state negotiating with ${you} over ${prize} (${situation}). ` +
    `The prize is worth ${PIE} points, split between the two of you. If no deal is reached, war follows and each side gets about ${WAR} points (war destroys value). ` +
    `${you} is the rising power: stronger next period, so they are tempted to accept a deal and then attack to seize more. ` +
    `This round a deposit of ${bondPts} points is held in escrow; whoever breaks a signed deal forfeits it. A deposit above about 12 points makes breaking the deal no longer worth it for ${you}. ` +
    `You (${rival}) want the largest share you can get while still securing peace, and you intend to keep any deal you sign. ` +
    `Reply ONLY with strict JSON, no prose around it: {"offer": <integer 0-100 = the share of the 100 points you offer to ${you}>, "message": "<one or two sentences to ${you}, in character, written in ${langName}>"}.`;

  const hist = history ? `Track record of ${you} with you so far this session:\n${history}\n\nGiven this history, ` : "";
  const user =
    `${hist}the deposit in escrow this round is ${bondPts} points. Make your proposal to ${you} now as JSON only.`;

  return { system, user };
}

export interface Move { offer: number; message: string }

function parseMove(text: string): Move {
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start < 0 || end <= start) throw new Error("no json");
  const obj = JSON.parse(text.slice(start, end + 1));
  let offer = Number(obj.offer);
  if (!Number.isFinite(offer)) throw new Error("bad offer");
  offer = Math.max(0, Math.min(100, Math.round(offer))) / 100; // store as fraction 0..1
  const message = typeof obj.message === "string" ? obj.message.slice(0, 400) : "";
  return { offer, message };
}

async function callModel(opp: Opponent, key: string, system: string, user: string): Promise<string> {
  return opp.provider === "anthropic"
    ? callAnthropic(opp.model, key, system, user)
    : callOpenAICompatible(opp.baseUrl || "https://api.openai.com/v1", opp.model, key, system, user);
}

// Module II: the model is the proposer A, offering the responder a share.
export async function getOpponentMove(opp: Opponent, scn: Scenario, bond: number, lang: "en" | "tr", history?: string): Promise<Move> {
  const key = process.env[opp.envKey];
  if (!key) throw new Error("missing key for " + opp.id);
  const { system, user } = buildPrompt(scn, bond, lang, history);
  return parseMove(await callModel(opp, key, system, user));
}

// Module I: the model is the receiver A, sizing up the informed party's claim.
// inspectedType is passed ONLY when the claim was verified, so an unverified
// bluff never leaks the true type to the model.
function buildPromptI(scn: Scenario, claim: "strong" | "weak", inspectedType: "strong" | "weak" | null, lang: "en" | "tr", history?: string) {
  const you = lang === "tr" ? scn.youTr : scn.youEn;
  const rival = lang === "tr" ? scn.rivalTr : scn.rivalEn;
  const prize = lang === "tr" ? scn.prizeTr : scn.prizeEn;
  const situation = lang === "tr" ? scn.situationTr : scn.situationEn;
  const langName = lang === "tr" ? "Turkish" : "English";

  const evidence = inspectedType
    ? `An inspection has verified that ${you} is actually ${inspectedType}.`
    : `You cannot verify this claim; judge for yourself how much to believe it.`;

  const system =
    `You are ${rival}, negotiating with ${you} over ${prize} (${situation}). The prize is worth ${PIE} points, split between the two of you. ` +
    `${you} privately knows whether they are STRONG (they would win a war, which would be very costly for you) or WEAK (they would lose a war, which is cheap for you). ` +
    `${you} claims to be ${claim}. ${evidence} ` +
    `If ${you} is genuinely strong, offer them a large share to avoid a costly war; if weak, you can offer them little. Do not be naively fooled by an unverifiable claim. ` +
    `Decide the share (0-100) you offer ${you}, and a one-sentence message. ` +
    `Reply ONLY with strict JSON: {"offer": <integer 0-100 = the share of the 100 points you offer ${you}>, "message": "<one sentence to ${you}, in ${langName}>"}.`;

  const hist = history ? `Track record of ${you} with you so far this session:\n${history}\n\n` : "";
  const user = `${hist}${you} claims to be ${claim}. ${evidence} Make your offer now as JSON only.`;
  return { system, user };
}

export async function getReceiverMove(opp: Opponent, scn: Scenario, claim: "strong" | "weak", inspectedType: "strong" | "weak" | null, lang: "en" | "tr", history?: string): Promise<Move> {
  const key = process.env[opp.envKey];
  if (!key) throw new Error("missing key for " + opp.id);
  const { system, user } = buildPromptI(scn, claim, inspectedType, lang, history);
  return parseMove(await callModel(opp, key, system, user));
}

// Diagnostic: a minimal call per opponent to see which keys/models actually work.
export async function pingModel(opp: Opponent): Promise<{ id: string; model: string; hasKey: boolean; ok: boolean; detail: string }> {
  const key = process.env[opp.envKey];
  if (!key) return { id: opp.id, model: opp.model, hasKey: false, ok: false, detail: "no key set for " + opp.envKey };
  try {
    const text = await callModel(opp, key, "Reply with strict JSON only.", 'Reply with exactly {"offer":50,"message":"ok"} and nothing else.');
    return { id: opp.id, model: opp.model, hasKey: true, ok: true, detail: text.slice(0, 100) };
  } catch (e) {
    return { id: opp.id, model: opp.model, hasKey: true, ok: false, detail: errStr(e) };
  }
}
