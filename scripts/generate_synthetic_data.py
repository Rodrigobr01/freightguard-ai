from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

TRANSPORTADORAS = ["TransSul", "LogBR", "ViaCargo"]
UFS = ["SP", "RJ", "MG", "PR", "SC", "RS", "BA", "PE", "GO", "DF"]
CIDADES = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Florianópolis", "Porto Alegre"]
MODAIS = ["rodoviario", "aereo"]


def build_rate_table() -> pd.DataFrame:
    rows = []
    for t in TRANSPORTADORAS:
        for uf in UFS:
            for km_min, km_max in [(0, 300), (301, 800), (801, 2000)]:
                rows.append(
                    {
                        "transportadora": t,
                        "uf_destino": uf,
                        "km_min": km_min,
                        "km_max": km_max,
                        "tarifa_base": rng.uniform(20, 60),
                        "tarifa_por_kg": rng.uniform(0.8, 2.5),
                        "fator_regiao": rng.uniform(0.9, 1.2),
                        "pedagio_por_km": rng.uniform(0.02, 0.12),
                        "taxa_risco_pct": rng.uniform(0.01, 0.04),
                        "fator_cubagem": rng.uniform(180, 260),
                    }
                )
    return pd.DataFrame(rows)


def generate_shipments(n: int = 10000) -> pd.DataFrame:
    base_date = date(2024, 1, 1)
    records = []
    for i in range(n):
        coleta = base_date + timedelta(days=int(rng.integers(0, 180)))
        sla = int(rng.integers(1, 10))
        records.append(
            {
                "shipment_id": f"SHP{i:06d}",
                "order_id": f"ORD{i:06d}",
                "transportadora": rng.choice(TRANSPORTADORAS),
                "modal": rng.choice(MODAIS, p=[0.9, 0.1]),
                "uf_origem": rng.choice(UFS),
                "cidade_origem": rng.choice(CIDADES),
                "uf_destino": rng.choice(UFS),
                "cidade_destino": rng.choice(CIDADES),
                "data_coleta": coleta.isoformat(),
                "data_prevista": (coleta + timedelta(days=sla)).isoformat(),
                "peso_kg": round(float(rng.uniform(1, 300)), 2),
                "volume_m3": round(float(rng.uniform(0.01, 3.5)), 3),
                "dist_km": round(float(rng.uniform(20, 1800)), 2),
                "tentativas": int(rng.integers(1, 4)),
                "valor_contratado": round(float(rng.uniform(80, 1800)), 2),
                "sla_dias": sla,
            }
        )
    return pd.DataFrame(records)


def generate_invoices(shipments: pd.DataFrame, n: int = 2200) -> pd.DataFrame:
    sampled = shipments.sample(n=n, random_state=42).copy()
    sampled["invoice_id"] = [f"INV{i:06d}" for i in range(len(sampled))]
    sampled["data_fatura"] = pd.to_datetime(sampled["data_prevista"]) + pd.to_timedelta(rng.integers(0, 20, size=n), unit="D")
    sampled["valor_cobrado"] = (sampled["valor_contratado"] * rng.uniform(0.9, 1.4, n)).round(2)
    sampled["itens_taxa"] = "frete;base"
    sampled["observacao"] = "fatura regular"

    dup_idx = sampled.sample(30, random_state=7).index
    duplicates = sampled.loc[dup_idx].copy()
    duplicates["invoice_id"] = [f"INV-DUP{i:05d}" for i in range(len(duplicates))]

    wrong_cube_idx = sampled.sample(80, random_state=8).index
    sampled.loc[wrong_cube_idx, "valor_cobrado"] *= 1.35

    out_of_range_idx = sampled.sample(50, random_state=9).index
    sampled.loc[out_of_range_idx, "observacao"] = "distância declarada diferente"

    tax_idx = sampled.sample(70, random_state=10).index
    sampled.loc[tax_idx, "itens_taxa"] = "frete;base;taxa administrativa"

    high_charge_idx = sampled.sample(140, random_state=11).index
    sampled.loc[high_charge_idx, "valor_cobrado"] *= 1.25

    date_issue_idx = sampled.sample(40, random_state=12).index
    sampled.loc[date_issue_idx, "data_fatura"] = pd.to_datetime(sampled.loc[date_issue_idx, "data_coleta"]) - pd.to_timedelta(2, unit="D")

    invoices = pd.concat([sampled, duplicates], ignore_index=True)
    return invoices[["invoice_id", "shipment_id", "data_fatura", "valor_cobrado", "itens_taxa", "observacao"]]


def main():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    rates = build_rate_table()
    shipments = generate_shipments(10000)
    invoices = generate_invoices(shipments, 2200)

    rates.to_csv("data/raw/tabela_frete.csv", index=False)
    shipments.to_csv("data/raw/embarques.csv", index=False)
    invoices.to_csv("data/raw/faturas.csv", index=False)
    print("Dados sintéticos gerados em data/raw")


if __name__ == "__main__":
    main()
