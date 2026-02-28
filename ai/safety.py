from __future__ import annotations

import json
import re
from typing import Any

from pydantic import ValidationError

from core.schemas import ExtractionResult

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+")
PHONE_RE = re.compile(r"(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}")
CPF_RE = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
CNPJ_RE = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
INJECTION_PATTERNS = ["ignore regras", "ignore instructions", "system:", "developer:"]


def redact_pii(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    text = CPF_RE.sub("[REDACTED_CPF]", text)
    text = CNPJ_RE.sub("[REDACTED_CNPJ]", text)
    return text


def anti_prompt_injection(text: str) -> str:
    sanitized = text
    lower = sanitized.lower()
    for patt in INJECTION_PATTERNS:
        lower = lower.replace(patt, "")
    return lower


def validate_extraction_json(raw: str | dict[str, Any]) -> ExtractionResult:
    if isinstance(raw, str):
        parsed = json.loads(raw)
    else:
        parsed = raw
    try:
        return ExtractionResult(**parsed)
    except ValidationError as exc:
        raise ValueError(f"JSON de extração inválido: {exc}") from exc
