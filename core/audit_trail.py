from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from core.schemas import AuditTrailEntry


def hash_inputs(*paths: str) -> str:
    h = hashlib.sha256()
    for path in paths:
        h.update(Path(path).read_bytes())
    return h.hexdigest()


def append_audit_trail(
    trail_path: str,
    input_hash: str,
    pipeline_version: str,
    llm_enabled: bool,
    confidence: float,
    fallback_used: bool,
    details: str | None = None,
) -> None:
    entry = AuditTrailEntry(
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        input_hash=input_hash,
        pipeline_version=pipeline_version,
        llm_enabled=llm_enabled,
        confidence=confidence,
        fallback_used=fallback_used,
        details=details,
    )
    out = Path(trail_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry.model_dump(), ensure_ascii=False) + "\n")
