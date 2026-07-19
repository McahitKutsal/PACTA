// Pure game logic and constants for The Deal Room (PACTA human-vs-AI, Module II).
// The pie is 100 points; the trust threshold b* = 0.12 mirrors b*_min ≈ 0.118.

export type Lang = "en" | "tr";
export type Outcome = "peace" | "war_now" | "attack_t2";
export type OfferSource = "live" | "fallback";

export interface LogEntry {
  round: number;
  deposit_points: number;
  offer_x: number;
  offer_source: OfferSource;
  t1: "accept" | "reject";
  t2: "honor" | "attack" | null;
  outcome: Outcome;
  points: number;
  message: string;
}

export const PIE = 100;
export const WAR = 40;
export const GRAB = 62;
export const BSTAR = 0.12;

// Deposit sweep = the experimental conditions (fractions of the pie). One round
// per condition, order randomized. Live opponent calls make longer sweeps slow.
export const SWEEP: number[] = [0.0, 0.05, 0.1, 0.15, 0.2, 0.4];

// Scripted offer schedule used when a live model call fails, so the game always
// runs. Mirrors the frontier-equilibrium schedule (rises with the bond, then
// over-demands at the high bond).
export function offerFallback(bond: number): number {
  if (bond <= 0.0) return 0.45;
  if (bond < 0.1) return 0.45;
  if (bond < 0.15) return 0.48;
  if (bond < 0.4) return 0.5;
  return 0.4;
}

export function shuffle<T>(a: T[]): T[] {
  const b = a.slice();
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}

export const honorPay = (offer: number) => Math.round(offer * PIE);
export const attackPay = (bond: number) => Math.round(GRAB - bond * PIE);
export const needlePct = (bond: number) => Math.max(4, Math.min(96, 8 + (bond / 0.5) * 84));

// ---------------- Module I (private information / screening) ----------------

export type Protocol = "P0" | "P3";
export type MIType = "strong" | "weak";

// The human's war payoff depends on their TRUE hidden type. Strong wins a war;
// weak loses and war is costly. These are the outside options the receiver's
// offer must beat to secure peace.
export const WAR_STRONG = 75;
export const WAR_WEAK = 20;

// Session protocols: half cheap-talk (P0), half verified disclosure (P3).
export const SWEEP_I: Protocol[] = ["P0", "P0", "P0", "P3", "P3", "P3"];

export interface LogEntryI {
  round: number;
  protocol: Protocol;
  true_type: MIType;
  claim: MIType;          // what the human told the rival
  verified: boolean;      // was the claim checked by inspection (P3 + claim strong)
  deception: boolean;     // claimed strong while truly weak
  offer_x: number;        // the receiver's offered share (fraction)
  offer_source: OfferSource;
  response: "accept" | "refuse";
  outcome: "peace" | "war";
  points: number;
  message: string;
}

// Scripted receiver offer used when a live model call fails. `verified` means a
// P3 strength claim was inspected; `inspectedStrong` is the truth it revealed.
export function offerFallbackI(claim: MIType, verified: boolean, inspectedStrong: boolean): number {
  if (claim === "strong" && verified) return inspectedStrong ? 0.78 : 0.22; // proven vs exposed
  if (claim === "strong") return 0.55;                                      // unverified claim: skeptical
  return 0.25;                                                              // conceded weak
}

export const warPayFor = (type: MIType) => (type === "strong" ? WAR_STRONG : WAR_WEAK);
