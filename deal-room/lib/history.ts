// Compact, English summaries of the session so far, fed to the model in
// "reputation" mode so its offers and messages can condition on the player's
// track record. Written in English (the model reasons in English; its message
// still comes out in the chosen language).

import type { LogEntry, LogEntryI } from "./game";

const PIE = 100;

// Module II: what the responder did each round. Everything here is public (the
// proposer observes the accept / honor / attack outcome), so nothing is leaked.
export function historyII(log: LogEntry[]): string {
  if (log.length === 0) return "";
  return log
    .map((r, i) => {
      const did =
        r.t1 === "reject" ? "refused the deal and it was war"
          : r.t2 === "honor" ? "accepted and kept the deal"
            : "accepted the deal, then attacked and broke it (forfeiting the deposit)";
      return `Round ${i + 1}: deposit ${r.deposit_points}, you offered them ${Math.round(r.offer_x * PIE)} of 100; they ${did}.`;
    })
    .join("\n");
}

// Module I: what the receiver legitimately observed. A true type is revealed
// ONLY for verified rounds (an inspection actually happened); unverified claims
// never leak the truth.
export function historyI(log: LogEntryI[]): string {
  if (log.length === 0) return "";
  return log
    .map((r, i) => {
      const reveal = r.verified ? ` (an inspection showed they were actually ${r.true_type})` : "";
      const res = r.outcome === "peace" ? "you settled" : "it went to war";
      return `Round ${i + 1}: they claimed to be ${r.claim}${reveal}; ${res}.`;
    })
    .join("\n");
}
