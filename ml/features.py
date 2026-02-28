from __future__ import annotations

import pandas as pd


def build_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    feat = pd.DataFrame()
    feat["diferenca_abs"] = df["diferenca_valor"].abs()
    feat["dist_km"] = df["dist_km"]
    feat["peso_cobrado"] = df["peso_cobrado"]
    feat["tentativas"] = df["tentativas"]
    feat["valor_cobrado"] = df["valor_cobrado"]
    feat["expected_total"] = df["expected_total"]
    return feat.fillna(0)
