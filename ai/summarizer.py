from __future__ import annotations

import pandas as pd


def generate_divergence_explanation(row: pd.Series) -> str:
    return (
        f"Embarque {row['shipment_id']} apresentou divergência '{row['divergencia_tipo']}'. "
        f"Valor esperado: R$ {row['expected_total']:.2f}; cobrado: R$ {row['valor_cobrado']:.2f}; "
        f"diferença: R$ {row['diferenca_valor']:.2f}."
    )


def generate_contestation_text(row: pd.Series) -> str:
    return (
        f"Prezados, identificamos inconsistência na fatura {row['invoice_id']} vinculada ao shipment "
        f"{row['shipment_id']}. O valor cobrado (R$ {row['valor_cobrado']:.2f}) diverge do cálculo "
        f"contratual (R$ {row['expected_total']:.2f}), diferença de R$ {row['diferenca_valor']:.2f}. "
        "Solicitamos revisão e emissão de crédito conforme contrato."
    )


def summarize_results(df: pd.DataFrame) -> dict:
    return {
        "total_registros": int(len(df)),
        "divergencias": int((df["diferenca_valor"].abs() > 0.01).sum()),
        "severidade_alta": int((df["severidade"] == "alta").sum()),
        "valor_total_diferenca": float(df["diferenca_valor"].sum()),
    }
