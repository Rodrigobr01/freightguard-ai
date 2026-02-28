from __future__ import annotations

import pandas as pd
from pydantic import ValidationError

from core.schemas import InvoiceSchema, RateTableSchema, ShipmentSchema


class DataValidationError(Exception):
    pass


def _validate_rows(df: pd.DataFrame, schema_cls, max_errors: int = 20):
    errors = []
    for idx, row in df.iterrows():
        try:
            schema_cls(**row.to_dict())
        except ValidationError as exc:
            errors.append((idx, str(exc)))
            if len(errors) >= max_errors:
                break
    if errors:
        msg = "; ".join([f"linha {idx}: {err}" for idx, err in errors])
        raise DataValidationError(msg)


def validate_datasets(shipments: pd.DataFrame, invoices: pd.DataFrame, rates: pd.DataFrame) -> None:
    _validate_rows(shipments, ShipmentSchema)
    _validate_rows(invoices, InvoiceSchema)
    _validate_rows(rates, RateTableSchema)
