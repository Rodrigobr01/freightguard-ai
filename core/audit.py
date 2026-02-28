from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from ai.extraction import extract_invoice_text
from ai.summarizer import summarize_results
from core.audit_trail import append_audit_trail, hash_inputs
from core.pricing_engine import calculate_expected_freight
from core.validation import validate_datasets
from ml.anomaly import score_anomalies


def _classify_divergence(row: pd.Series) -> str:
    if row["duplicate_invoice"]:
        return "duplicidade"
    if row["out_of_km_range"]:
        return "faixa_km"
    if row["possui_taxa_suspeita"]:
        return "taxa_indevida"
    if row["cubagem"] > row["peso_kg"] * 1.5 and row["diferenca_valor"] > 0:
        return "cubagem"
    if abs(row["diferenca_valor"]) > 0.01:
        return "valor"
    return "ok"


def _severity(row: pd.Series) -> str:
    abs_diff = abs(row["diferenca_valor"])
    if row["divergencia_tipo"] in {"duplicidade", "taxa_indevida"} or abs_diff >= 150:
        return "alta"
    if abs_diff >= 50 or row["divergencia_tipo"] in {"cubagem", "faixa_km"}:
        return "media"
    return "baixa"


def run_audit(
    shipments_path: str,
    invoices_path: str,
    rates_path: str,
    output_path: str = "data/processed/auditoria_resultado.csv",
):
    shipments = pd.read_csv(shipments_path)
    invoices = pd.read_csv(invoices_path)
    rates = pd.read_csv(rates_path)

    validate_datasets(shipments, invoices, rates)

    merged = invoices.merge(shipments, on="shipment_id", how="left", suffixes=("_invoice", "_shipment"))
    merged["duplicate_invoice"] = merged.duplicated(subset=["shipment_id"], keep=False)

    breakdowns = merged.apply(lambda r: calculate_expected_freight(r.to_dict(), rates), axis=1, result_type="expand")
    audited = pd.concat([merged, breakdowns], axis=1)

    extracted = audited.apply(lambda r: extract_invoice_text(str(r["itens_taxa"]), str(r["observacao"])), axis=1)
    extracted_df = pd.DataFrame([e.model_dump() for e in extracted])
    audited = pd.concat([audited, extracted_df], axis=1)

    audited["diferenca_valor"] = (audited["valor_cobrado"] - audited["expected_total"]).round(2)
    audited["divergencia_tipo"] = audited.apply(_classify_divergence, axis=1)
    audited["severidade"] = audited.apply(_severity, axis=1)

    audited = score_anomalies(audited)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    audited.to_csv(output_path, index=False)

    llm_enabled = os.getenv("LLM_ENABLED", "false").lower() == "true"
    confidence = float(audited["confidence"].mean()) if "confidence" in audited.columns else 0.0
    fallback_used = bool(audited["fallback_used"].any()) if "fallback_used" in audited.columns else True
    append_audit_trail(
        "data/processed/audit_trail.jsonl",
        hash_inputs(shipments_path, invoices_path, rates_path),
        os.getenv("PIPELINE_VERSION", "1.0.0"),
        llm_enabled,
        confidence,
        fallback_used,
        details=f"rows={len(audited)}",
    )

    return audited, summarize_results(audited)
