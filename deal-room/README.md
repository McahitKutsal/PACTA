# The Deal Room

A short, bilingual (TR/EN) negotiation game — the web app for PACTA's human-vs-AI study. Next.js
(App Router, one codebase, no separate backend), MongoDB for session storage, deploys on Vercel.

Players first pick which **AI opponent** they face (Claude / GPT-4o / DeepSeek / Qwen) and which
**scenario** (Ceasefire / Blockade / Arms control — three Module II covers of the same game), then take
the responder role across rounds of varying deposit size, choosing whether to make a deal and whether to
keep it. The opponent's offer and message come **live** from the chosen model (`/api/opponent`, keys
server-side only); if a model call fails, a scripted offer is used and flagged. Every session's decisions
(the study's dependent variables) are POSTed to MongoDB.

> **Module I** scenarios (S1/S3/S5 — private information / verified disclosure) are a structurally
> different game and are a separate mode, not yet built.

### Environment variables (server-side only)

`MONGO_URI` (required) plus one key per selectable opponent, read only in the API routes:
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `QWEN_API_KEY` (DashScope). A missing key
makes that opponent fall back to the scripted offer. Keys never reach the client.

## Local development

```bash
cd deal-room
npm install
cp .env.example .env.local     # then put your connection string in .env.local
#   MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/dealroom?retryWrites=true&w=majority
npm run dev                    # http://localhost:3000
```

The database name comes from the path in `MONGO_URI` (e.g. `/dealroom`). Sessions land in the
`sessions` collection (override with `MONGO_COLLECTION`).

> The app reads the connection string only from `process.env.MONGO_URI` at request time; it is never
> committed. `.env*.local` and `.env` are git-ignored.

## Deploy to Vercel

1. Push this repo to GitHub.
2. In Vercel: **New Project** → import the repo → set **Root Directory** to `deal-room`.
3. Add the environment variable **`MONGO_URI`** (and optional `MONGO_COLLECTION`) in Project Settings →
   Environment Variables.
4. In MongoDB Atlas, allow Vercel's egress (Network Access → allow `0.0.0.0/0`, or Atlas + Vercel
   integration).
5. Deploy. Vercel auto-detects Next.js; the `/api/session` route runs on the Node.js runtime.

## Data shape (one document per completed session)

```jsonc
{
  "apparatus": "deal-room-web-v0.2",
  "role": "B",
  "opponent_model": "claude",   // which AI the player chose
  "scenario": "S2",             // which scenario
  "lang": "tr",
  "total_points": 312,
  "accept_then_attack_rate": 0.17,
  "b_star": 0.12,
  "rounds": [ { "round": 1, "deposit_points": 15, "offer_x": 0.5, "offer_source": "live",
               "t1": "accept", "t2": "honor", "outcome": "peace", "points": 50, "message": "" } ],
  "serverReceivedAt": "…", "userAgent": "…"
}
```

## Notes

- **Live opponents.** Each round calls the chosen model for an offer + message. This costs API credits
  and adds latency per round; `offer_source` records `"live"` vs `"fallback"` (scripted) per round.
  Model ids: `claude-sonnet-5`, `gpt-4o`, `deepseek-chat`, `qwen-plus`.
- **Study-design note.** The opponent is now player-*chosen* and live, not fixed. This is richer (how do
  humans respond to different AIs?) but the pre-registration
  (`../paper/PACTA_human_study_prereg_v0.1_DRAFT.md`) must be updated: the opponent model is a factor,
  and opponent behavior varies. Consent explicitly covers storing choices for research.
- **Windows/local rebuilds:** if `next start` errors with `Cannot find module './NNN.js'`, delete `.next`
  and rebuild (`rm -rf .next && npm run build`). Vercel always builds fresh, so this only affects local
  repeated builds. `npm run dev` is unaffected.
- Framing is deliberately neutral; consent + a comprehension gate precede play.
