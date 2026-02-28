from __future__ import annotations

from typing import Any

EXTRA_ATTEMPT_FEE = 12.5


def _select_rate(shipment_row: dict[str, Any], rate_table):
    candidates = rate_table[
        (rate_table["transportadora"] == shipment_row["transportadora"])
        & (rate_table["uf_destino"] == shipment_row["uf_destino"])
        & (rate_table["km_min"] <= shipment_row["dist_km"])
        & (rate_table["km_max"] >= shipment_row["dist_km"])
    ]
    if candidates.empty:
        fallback = rate_table[
            (rate_table["transportadora"] == shipment_row["transportadora"])
            & (rate_table["uf_destino"] == shipment_row["uf_destino"])
        ]
        if fallback.empty:
            raise ValueError("Nenhuma tarifa encontrada para o embarque")
        return fallback.iloc[0], True
    return candidates.iloc[0], False


def calculate_expected_freight(shipment_row: dict[str, Any], rate_table) -> dict[str, float | bool]:
    rate, out_of_km_range = _select_rate(shipment_row, rate_table)

    cubado = shipment_row["volume_m3"] * rate["fator_cubagem"]
    peso_cobrado = max(shipment_row["peso_kg"], cubado)
    base = (rate["tarifa_base"] + (peso_cobrado * rate["tarifa_por_kg"])) * rate["fator_regiao"]
    pedagio = shipment_row["dist_km"] * rate["pedagio_por_km"]
    expected_subtotal = base + pedagio
    risco = expected_subtotal * rate["taxa_risco_pct"]
    adicionais = max(shipment_row["tentativas"] - 1, 0) * EXTRA_ATTEMPT_FEE
    expected_total = expected_subtotal + risco + adicionais

    return {
        "base": round(base, 2),
        "peso_cobrado": round(peso_cobrado, 2),
        "cubagem": round(cubado, 2),
        "pedagio": round(pedagio, 2),
        "risco": round(risco, 2),
        "adicionais": round(adicionais, 2),
        "expected_total": round(expected_total, 2),
        "out_of_km_range": out_of_km_range,
    }
