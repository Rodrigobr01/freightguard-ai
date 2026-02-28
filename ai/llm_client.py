from __future__ import annotations

import os


class LLMUnavailableWarning(RuntimeError):
    pass


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "")

    def extract_json(self, prompt: str, text: str) -> str:
        if not self.api_key:
            raise LLMUnavailableWarning("LLM_API_KEY ausente. Usando fallback determinístico.")
        raise LLMUnavailableWarning(
            "Stub local sem integração real. Usando fallback determinístico."
        )
