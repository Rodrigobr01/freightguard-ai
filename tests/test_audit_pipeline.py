from pathlib import Path

import pandas as pd

from core.audit import run_audit


def test_run_audit_small(tmp_path: Path):
    shipments = pd.DataFrame([
        {"shipment_id": "S1", "order_id": "O1", "transportadora": "T", "modal": "rod", "uf_origem": "SP", "cidade_origem": "A", "uf_destino": "RJ", "cidade_destino": "B", "data_coleta": "2024-01-01", "data_prevista": "2024-01-02", "peso_kg": 10, "volume_m3": 0.1, "dist_km": 80, "tentativas": 1, "valor_contratado": 100, "sla_dias": 2}
    ])
    invoices = pd.DataFrame([
        {"invoice_id": "I1", "shipment_id": "S1", "data_fatura": "2024-01-03", "valor_cobrado": 150, "itens_taxa": "frete;taxa indevida", "observacao": "ok"}
    ])
    rates = pd.DataFrame([
        {"transportadora": "T", "uf_destino": "RJ", "km_min": 0, "km_max": 100, "tarifa_base": 10, "tarifa_por_kg": 2, "fator_regiao": 1, "pedagio_por_km": 0.1, "taxa_risco_pct": 0.02, "fator_cubagem": 100}
    ])

    sp = tmp_path / "s.csv"
    ip = tmp_path / "i.csv"
    rp = tmp_path / "r.csv"
    shipments.to_csv(sp, index=False)
    invoices.to_csv(ip, index=False)
    rates.to_csv(rp, index=False)

    out, summary = run_audit(str(sp), str(ip), str(rp), output_path=str(tmp_path / "out.csv"))
    assert len(out) == 1
    assert summary["divergencias"] == 1
    assert out.iloc[0]["divergencia_tipo"] in {"taxa_indevida", "valor", "cubagem"}
