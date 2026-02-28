# FreightGuard AI

[![CI](https://github.com/Rodrigobr01/freightguard-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Rodrigobr01/freightguard-ai/actions/workflows/ci.yml) ![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Auditor de frete inteligente com regras determinísticas, ML de anomalias e camada de IA segura opcional.

## Principais entregas
- Motor determinístico de cálculo de frete esperado.
- Pipeline de auditoria ponta a ponta (cruzamento, divergências, severidade, export).
- Ranking de prioridade por anomalia com IsolationForest.
- API FastAPI (`POST /audit`) e UI Streamlit.
- Camada de IA segura com fallback determinístico (LLM desabilitado por padrão).
- Testes automatizados com `pytest`.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Execução
```bash
python scripts/generate_synthetic_data.py
python scripts/run_pipeline.py
uvicorn api.main:app --reload
streamlit run ui/app.py
```


## Desenvolvimento
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Segurança de IA
- `LLM_ENABLED=false` por padrão.
- IA apenas explica e formata; não altera cálculos financeiros.
- Extração por LLM só é aceita em JSON validado por schema.
- Falha de LLM ativa fallback determinístico.
- Anti prompt injection e redaction de PII habilitados.
- Trilha de auditoria em `data/processed/audit_trail.jsonl`.

## Roadmap
1. Suporte a OCR nativo para PDFs de fatura.
2. Regras versionadas por contrato com effective date.
3. Explainability avançada no ranking de anomalia.
4. Integração com workflow de disputa (tickets/ERP).