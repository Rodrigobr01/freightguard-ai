from __future__ import annotations

import os

from ai.llm_client import LLMClient, LLMUnavailableWarning
from ai.prompt_templates import EXTRACTION_PROMPT
from ai.safety import anti_prompt_injection, redact_pii, validate_extraction_json
from core.schemas import ExtractionResult

SUSPICIOUS_KEYWORDS = {"taxa administrativa", "taxa extra", "taxa indevida", "avaria"}


def _fallback_extract(text: str) -> ExtractionResult:
    cleaned = anti_prompt_injection(redact_pii(text))
    taxas = [t.strip() for t in cleaned.split(";") if "taxa" in t]
    suspicious = any(k in cleaned for k in SUSPICIOUS_KEYWORDS)
    return ExtractionResult(
        taxas=taxas,
        possui_taxa_suspeita=suspicious,
        observacao_limpa=cleaned[:500],
        confidence=0.75,
        fallback_used=True,
        source="deterministic",
    )


def extract_invoice_text(itens_taxa: str, observacao: str) -> ExtractionResult:
    text = f"itens_taxa={itens_taxa}; observacao={observacao}"
    llm_enabled = os.getenv("LLM_ENABLED", "false").lower() == "true"
    if not llm_enabled:
        return _fallback_extract(text)

    client = LLMClient()
    try:
        raw = client.extract_json(EXTRACTION_PROMPT, text)
        result = validate_extraction_json(raw)
        return result
    except (LLMUnavailableWarning, ValueError):
        return _fallback_extract(text)
