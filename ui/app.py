from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import tempfile

import streamlit as st

from ai.summarizer import generate_contestation_text
from core.audit import run_audit

st.set_page_config(page_title="FreightGuard AI", layout="wide")
st.title("FreightGuard AI - Auditor de Frete Inteligente")

embarques = st.file_uploader("Upload embarques.csv", type="csv")
faturas = st.file_uploader("Upload faturas.csv", type="csv")
tabela = st.file_uploader("Upload tabela_frete.csv", type="csv")

if st.button("Rodar Auditoria"):
    if not (embarques and faturas and tabela):
        st.error("Envie os três CSVs.")
    else:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            p1 = base / "embarques.csv"
            p2 = base / "faturas.csv"
            p3 = base / "tabela_frete.csv"
            p1.write_bytes(embarques.read())
            p2.write_bytes(faturas.read())
            p3.write_bytes(tabela.read())

            df, summary = run_audit(str(p1), str(p2), str(p3))
            st.session_state["audit_df"] = df
            st.session_state["summary"] = summary

if "audit_df" in st.session_state:
    df = st.session_state["audit_df"]
    summary = st.session_state["summary"]

    st.subheader("Resumo")
    st.json(summary)

    col1, col2, col3 = st.columns(3)
    sev = col1.selectbox("Severidade", ["todas"] + sorted(df["severidade"].unique().tolist()))
    trp = col2.selectbox("Transportadora", ["todas"] + sorted(df["transportadora"].unique().tolist()))
    uf = col3.selectbox("UF Destino", ["todas"] + sorted(df["uf_destino"].unique().tolist()))

    filt = df.copy()
    if sev != "todas":
        filt = filt[filt["severidade"] == sev]
    if trp != "todas":
        filt = filt[filt["transportadora"] == trp]
    if uf != "todas":
        filt = filt[filt["uf_destino"] == uf]

    st.dataframe(filt.head(500), use_container_width=True)
    st.download_button("Export CSV", filt.to_csv(index=False).encode("utf-8"), "auditoria_filtrada.csv", "text/csv")

    if not filt.empty:
        idx = st.number_input("Linha para contestação", min_value=0, max_value=len(filt) - 1, value=0)
        row = filt.iloc[int(idx)]
        if st.button("Gerar contestação"):
            st.text_area("Texto de contestação", generate_contestation_text(row), height=180)
