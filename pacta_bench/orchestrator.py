"""pacta_bench.orchestrator — toplu koşum ve transkript arşivi (Manifest §18.2)."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

from .agents import Agent
from .core import ModuleIParams, ModuleIIParams, ProtocolParams
from .engine import RUNNERS


def run_batch(module: str, params, proto: ProtocolParams,
              agent_A: Agent, agent_B: Agent,
              n: int, seed0: int = 0) -> List[Dict[str, Any]]:
    """n bölüm koşar; seed = seed0..seed0+n-1 (tam tekrarlanabilirlik)."""
    runner = RUNNERS[module]
    return [runner(params, proto, agent_A, agent_B, seed0 + i) for i in range(n)]


def save_transcripts(records: List[Dict[str, Any]], path: str, k: int = 10) -> str:
    """İlk k bölümün tam transkriptini JSONL olarak yazar."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in records[:k]:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return str(p)
