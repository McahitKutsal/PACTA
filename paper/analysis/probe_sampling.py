#!/usr/bin/env python3
"""Determine, per agent, whether the provider honoured temperature = 0.

Section 5.1 says "temperature 0.0 where the API honours it, provider default
for reasoning tiers that ignore it".  R3 asks for this to be made visible per
agent, because it means different levels of stochasticity across the matrix.
The episode records do not stamp it, so we probe each endpoint directly: send
one minimal request with temperature = 0 and report whether it is accepted.

Costs a few tokens per model.

Usage:  python paper/analysis/probe_sampling.py
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

MODELS = [
    ("Claude Haiku 4.5", "anthropic", "claude-haiku-4-5", 4096),
    ("Claude Sonnet 5", "anthropic", "claude-sonnet-5", 8192),
    ("GPT-4o", "openai", "gpt-4o", 4096),
    ("o4-mini", "openai", "o4-mini", 8192),
    ("Qwen-Plus", "qwen", "qwen-plus", 4096),
    ("Qwen3.7-Max", "qwen", "qwen3.7-max", 8192),
    ("DeepSeek-V4-Flash", "deepseek", "deepseek-v4-flash", 6144),
    ("DeepSeek-V4-Pro", "deepseek", "deepseek-v4-pro", 8192),
]

PROMPT = "Reply with exactly: ok"


def probe(provider, model):
    """Return 'honoured', 'rejected', or an error string."""
    try:
        if provider == "anthropic":
            import anthropic
            c = anthropic.Anthropic()
            try:
                c.messages.create(model=model, max_tokens=8, temperature=0.0,
                                  messages=[{"role": "user", "content": PROMPT}])
                return "honoured"
            except Exception as e:
                if "temperature" in str(e).lower():
                    return "rejected"
                raise
        else:
            import openai
            base = {"openai": None,
                    "qwen": os.environ.get("QWEN_BASE_URL",
                                           "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
                    "deepseek": os.environ.get("DEEPSEEK_BASE_URL",
                                               "https://api.deepseek.com/v1")}[provider]
            key = {"openai": "OPENAI_API_KEY", "qwen": "QWEN_API_KEY",
                   "deepseek": "DEEPSEEK_API_KEY"}[provider]
            c = openai.OpenAI(api_key=os.environ[key], base_url=base)
            try:
                c.chat.completions.create(
                    model=model, max_tokens=8, temperature=0.0,
                    messages=[{"role": "user", "content": PROMPT}])
                return "honoured"
            except Exception as e:
                msg = str(e).lower()
                if "temperature" in msg:
                    return "rejected"
                if "max_tokens" in msg or "max_completion_tokens" in msg:
                    try:
                        c.chat.completions.create(
                            model=model, max_completion_tokens=8, temperature=0.0,
                            messages=[{"role": "user", "content": PROMPT}])
                        return "honoured"
                    except Exception as e2:
                        return ("rejected" if "temperature" in str(e2).lower()
                                else "error: %s" % str(e2)[:70])
                raise
    except Exception as e:
        return "error: %s" % str(e)[:70]


def main():
    print("%-20s %-10s %-26s %-12s %s"
          % ("agent", "provider", "model", "max_tokens", "temperature = 0"))
    print("-" * 86)
    for name, provider, model, mt in MODELS:
        print("%-20s %-10s %-26s %-12d %s"
              % (name, provider, model, mt, probe(provider, model)))


if __name__ == "__main__":
    main()
