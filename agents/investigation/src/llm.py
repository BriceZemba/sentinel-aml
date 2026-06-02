"""LLM helper with a deterministic offline fallback.

If ANTHROPIC_API_KEY is set, the synthesis node uses Claude to write the analyst
rationale. If it is not (CI, offline judging, no key), the agent still runs
end-to-end using a templated rationale, so the graph never hard-fails on a
missing key. This keeps the repo testable without credentials.
"""
from __future__ import annotations

import os

_DEFAULT_MODEL = os.getenv("SENTINEL_LLM_MODEL", "claude-opus-4-8")


def llm_available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def get_llm(temperature: float = 0.0):
    """Return a LangChain chat model, or None if no key is configured."""
    if not llm_available():
        return None
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(model=_DEFAULT_MODEL, temperature=temperature, max_tokens=1024)
