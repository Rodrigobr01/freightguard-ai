import pandas as pd

from core.pricing_engine import calculate_expected_freight


def test_calculate_expected_freight_basic():
    rates = pd.DataFrame(
        [
            {
                "transportadora": "T1",
                "uf_destino": "SP",
                "km_min": 0,
                "km_max": 500,
                "tarifa_base": 10,
                "tarifa_por_kg": 2,
                "fator_regiao": 1.1,
                "pedagio_por_km": 0.1,
                "taxa_risco_pct": 0.05,
                "fator_cubagem": 200,
            }
        ]
    )
    shipment = {
        "transportadora": "T1",
        "uf_destino": "SP",
        "dist_km": 100,
        "peso_kg": 20,
        "volume_m3": 0.05,
        "tentativas": 2,
    }
    result = calculate_expected_freight(shipment, rates)
    assert result["peso_cobrado"] == 20
    assert result["base"] > 0
    assert result["expected_total"] > result["base"]
