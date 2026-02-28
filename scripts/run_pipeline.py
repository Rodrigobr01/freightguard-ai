from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.audit import run_audit


if __name__ == "__main__":
    df, summary = run_audit(
        "data/raw/embarques.csv",
        "data/raw/faturas.csv",
        "data/raw/tabela_frete.csv",
    )
    print(summary)
    print(f"Arquivo gerado com {len(df)} linhas em data/processed/auditoria_resultado.csv")
