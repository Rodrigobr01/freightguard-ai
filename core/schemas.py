from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ShipmentSchema(BaseModel):
    shipment_id: str
    order_id: str
    transportadora: str
    modal: str
    uf_origem: str = Field(min_length=2, max_length=2)
    cidade_origem: str
    uf_destino: str = Field(min_length=2, max_length=2)
    cidade_destino: str
    data_coleta: date
    data_prevista: date
    peso_kg: float = Field(ge=0)
    volume_m3: float = Field(ge=0)
    dist_km: float = Field(ge=0)
    tentativas: int = Field(ge=1)
    valor_contratado: float = Field(ge=0)
    sla_dias: int = Field(ge=0)


class InvoiceSchema(BaseModel):
    invoice_id: str
    shipment_id: str
    data_fatura: date
    valor_cobrado: float = Field(ge=0)
    itens_taxa: str
    observacao: str


class RateTableSchema(BaseModel):
    transportadora: str
    uf_destino: str = Field(min_length=2, max_length=2)
    km_min: float = Field(ge=0)
    km_max: float = Field(gt=0)
    tarifa_base: float = Field(ge=0)
    tarifa_por_kg: float = Field(ge=0)
    fator_regiao: float = Field(gt=0)
    pedagio_por_km: float = Field(ge=0)
    taxa_risco_pct: float = Field(ge=0)
    fator_cubagem: float = Field(gt=0)

    @field_validator("km_max")
    @classmethod
    def km_range_must_be_valid(cls, v: float, info):
        km_min = info.data.get("km_min", 0)
        if v <= km_min:
            raise ValueError("km_max deve ser maior que km_min")
        return v


class ExtractionResult(BaseModel):
    taxas: list[str]
    possui_taxa_suspeita: bool
    observacao_limpa: str
    confidence: float = Field(ge=0, le=1)
    fallback_used: bool
    source: str


class AuditTrailEntry(BaseModel):
    timestamp: str
    input_hash: str
    pipeline_version: str
    llm_enabled: bool
    confidence: float = Field(ge=0, le=1)
    fallback_used: bool
    details: Optional[str] = None
