from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest

from ml.features import build_feature_matrix


def score_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    if df.empty:
        df = df.copy()
        df["anomaly_score"] = []
        df["anomaly_flag"] = []
        df["prioridade"] = []
        return df

    X = build_feature_matrix(df)
    model = IsolationForest(random_state=42, contamination=contamination)
    model.fit(X)
    raw_score = model.decision_function(X)
    pred = model.predict(X)

    out = df.copy()
    out["anomaly_score"] = -raw_score
    out["anomaly_flag"] = pred == -1
    out["prioridade"] = out["anomaly_score"].rank(method="dense", ascending=False).astype(int)
    return out.sort_values("prioridade")
