import pandas as pd
import pytest

from core.validation import DataValidationError, validate_datasets


def test_validate_datasets_invalid():
    shipments = pd.DataFrame(
        [
            {
                "shipment_id": "S1",
                "order_id": "O1",
                "transportadora": "T",
                "modal": "rod",
                "uf_origem": "SP",
                "cidade_origem": "A",
                "uf_destino": "RJ",
                "cidade_destino": "B",
                "data_coleta": "2024-01-01",
                "data_prevista": "2024-01-02",
                "peso_kg": -1,
                "volume_m3": 1,
                "dist_km": 10,
                "tentativas": 1,
                "valor_contratado": 100,
                "sla_dias": 2,
            }
        ]
    )
    invoices = pd.DataFrame(
        [
            {
                "invoice_id": "I1",
                "shipment_id": "S1",
                "data_fatura": "2024-01-03",
                "valor_cobrado": 100,
                "itens_taxa": "",
                "observacao": "",
            }
        ]
    )
    rates = pd.DataFrame(
        [
            {
                "transportadora": "T",
                "uf_destino": "RJ",
                "km_min": 0,
                "km_max": 100,
                "tarifa_base": 10,
                "tarifa_por_kg": 1,
                "fator_regiao": 1,
                "pedagio_por_km": 0.1,
                "taxa_risco_pct": 0.01,
                "fator_cubagem": 200,
            }
        ]
    )
    with pytest.raises(DataValidationError):
        validate_datasets(shipments, invoices, rates)
