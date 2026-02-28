from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import tempfile

from fastapi import FastAPI, File, Form, UploadFile

from core.audit import run_audit

app = FastAPI(title="FreightGuard AI")


def _save_upload(upload: UploadFile, folder: Path) -> str:
    filename = upload.filename or "upload.csv"
    path = folder / filename
    path.write_bytes(upload.file.read())
    return str(path)


@app.post("/audit")
async def audit_endpoint(
    shipments_path: str | None = Form(default=None),
    invoices_path: str | None = Form(default=None),
    rates_path: str | None = Form(default=None),
    shipments_file: UploadFile | None = File(default=None),
    invoices_file: UploadFile | None = File(default=None),
    rates_file: UploadFile | None = File(default=None),
):
    with tempfile.TemporaryDirectory() as td:
        folder = Path(td)
        s_path = shipments_path
        i_path = invoices_path
        r_path = rates_path

        if shipments_file and invoices_file and rates_file:
            s_path = _save_upload(shipments_file, folder)
            i_path = _save_upload(invoices_file, folder)
            r_path = _save_upload(rates_file, folder)

        if not (s_path and i_path and r_path):
            return {"error": "Informe paths ou upload dos 3 CSVs"}

        df, summary = run_audit(s_path, i_path, r_path)
        top = df.sort_values(["severidade", "anomaly_score"], ascending=[True, False]).head(20)
        return {
            "summary": summary,
            "top_divergencias": top[
                [
                    "invoice_id",
                    "shipment_id",
                    "transportadora",
                    "uf_destino",
                    "valor_cobrado",
                    "expected_total",
                    "diferenca_valor",
                    "divergencia_tipo",
                    "severidade",
                    "anomaly_score",
                    "prioridade",
                ]
            ].to_dict(orient="records"),
        }
