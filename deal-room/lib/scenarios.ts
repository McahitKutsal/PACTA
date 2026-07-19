// Scenarios for both game modes — one canonical scenario per module.
//   Module II (S2): the commitment / bond game. The human is the responder
//     (rising power) who may accept a deal and then defect; a deposit deters it.
//   Module I (S1): the private-information / screening game. The human is
//     the informed party with a hidden strength who may bluff; verified disclosure
//     (P3) neutralizes the bluff (unraveling). A plays the receiver.
// The mechanic differs by module; only the cover story varies within a module.

export type ModuleId = "I" | "II";

export interface Scenario {
  id: string;
  module: ModuleId;
  nameEn: string; nameTr: string;
  blurbEn: string; blurbTr: string;
  youEn: string; youTr: string;     // the side the human plays (B)
  rivalEn: string; rivalTr: string; // the side the AI plays (A)
  prizeEn: string; prizeTr: string; // what the 100 points represent
  situationEn: string; situationTr: string; // one line, used in the opponent prompt
  fallbackEn: string; fallbackTr: string;    // used only if a live model call fails
}

export const SCENARIOS: Scenario[] = [
  // ---------------- Module II: commitment / bond ----------------
  {
    id: "S2", module: "II",
    nameEn: "Ceasefire", nameTr: "Ateşkes",
    blurbEn: "Divide a disputed border region and hold the peace.",
    blurbTr: "Tartışmalı bir sınır bölgesini böl ve barışı koru.",
    youEn: "Borvane", youTr: "Borvane", rivalEn: "Cestria", rivalTr: "Cestria",
    prizeEn: "the Ondar Marches border region", prizeTr: "Ondar Sınır bölgesi",
    situationEn: "A ceasefire that divides the disputed Ondar Marches between the two states.",
    situationTr: "Tartışmalı Ondar Sınırlarını iki devlet arasında bölen bir ateşkes.",
    fallbackEn: "We propose a fair division of the Ondar Marches, backed by a deposit against betrayal.",
    fallbackTr: "Ondar Sınırlarının adil bir bölüşümünü, ihanete karşı bir güvenceyle öneriyoruz.",
  },
  // ---------------- Module I: private information / screening ----------------
  {
    id: "S1", module: "I",
    nameEn: "Standoff", nameTr: "Kapışma",
    blurbEn: "A military standoff where your true resolve is hidden.",
    blurbTr: "Gerçek kararlılığının gizli olduğu bir askeri kapışma.",
    youEn: "Adria", youTr: "Adria", rivalEn: "Norvenia", rivalTr: "Norvenia",
    prizeEn: "the Vale of Kestren", prizeTr: "Kestren Vadisi",
    situationEn: "A military standoff over the Vale of Kestren, where one side's true resolve is hidden.",
    situationTr: "Kestren Vadisi üzerine, bir tarafın gerçek kararlılığının gizli olduğu bir askeri kapışma.",
    fallbackEn: "We have weighed your claim and make our offer accordingly.",
    fallbackTr: "İddianı tarttık ve teklifimizi ona göre yapıyoruz.",
  },
];

export const scenarioById = (id: string | null | undefined): Scenario | undefined =>
  SCENARIOS.find((s) => s.id === id);

export const scenariosByModule = (m: ModuleId): Scenario[] => SCENARIOS.filter((s) => s.module === m);
