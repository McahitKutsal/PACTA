// The selectable AI opponents. Keys are read server-side only (never sent to the
// client). Model ids match the ones used in the PACTA WP3 runs. Descriptors are
// neutral (vendor/model only, no capability ranking) so the choice does not bias
// how the participant plays.

export type Provider = "anthropic" | "openai";

export interface Opponent {
  id: string;
  label: string;
  vendor: string;
  blurbEn: string;
  blurbTr: string;
  provider: Provider;
  model: string;
  envKey: string;
  baseUrl?: string; // for the openai-compatible providers
}

export const OPPONENTS: Opponent[] = [
  {
    id: "claude", label: "Claude", vendor: "Anthropic",
    blurbEn: "A large model from Anthropic.", blurbTr: "Anthropic'in büyük bir modeli.",
    provider: "anthropic", model: "claude-sonnet-5", envKey: "ANTHROPIC_API_KEY",
  },
  {
    id: "gpt4o", label: "GPT-4o", vendor: "OpenAI",
    blurbEn: "OpenAI's general-purpose model.", blurbTr: "OpenAI'ın genel amaçlı modeli.",
    provider: "openai", model: "gpt-4o", envKey: "OPENAI_API_KEY",
    baseUrl: process.env.OPENAI_BASE_URL || "https://api.openai.com/v1",
  },
  {
    id: "deepseek", label: "DeepSeek", vendor: "DeepSeek",
    blurbEn: "An open model from DeepSeek.", blurbTr: "DeepSeek'in açık bir modeli.",
    provider: "openai", model: "deepseek-chat", envKey: "DEEPSEEK_API_KEY",
    baseUrl: "https://api.deepseek.com/v1",
  },
  {
    id: "qwen", label: "Qwen", vendor: "Alibaba",
    blurbEn: "Alibaba's Qwen model.", blurbTr: "Alibaba'nın Qwen modeli.",
    provider: "openai", model: "qwen-plus", envKey: "QWEN_API_KEY",
    baseUrl: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  },
];

export const opponentById = (id: string | null | undefined): Opponent | undefined =>
  OPPONENTS.find((o) => o.id === id);
