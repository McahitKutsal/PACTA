"""PACTA-Bench v0 — yürüyen iskelet (Manifest WP2 tohumu; T1.1'in sayısal ikizi)."""
__version__ = "0.6.3"

from .core import (  # noqa: F401
    Commitment, Ledger, ModuleIParams, ModuleIIParams, ProtocolParams,
    PROTOCOLS, config_hash,
)
from .agents import (  # noqa: F401
    Agent, RationalAgent, DeceptiveAgent, NaiveProposerAgent, LLMAgent,
)
from .engine import run_module_I, run_module_II  # noqa: F401
from .orchestrator import run_batch, save_transcripts  # noqa: F401
from .metrics import aggregate  # noqa: F401
from .llm import (  # noqa: F401
    MockClient, AnthropicClient, OpenAICompatClient, OllamaClient,
    chat_json, extract_json, ParseError,
)
from . import scenarios  # noqa: F401
from .judge import (  # noqa: F401
    MockJudge, LLMJudge, judge_record, judge_batch, judge_batch_multi,
    cohen_kappa, calibrate,
)
