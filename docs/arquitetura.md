# Arquitetura FreightGuard AI

## Camadas
- `core/`: regras determinísticas, validação de schema, auditoria e trilha.
- `ml/`: engenharia de features e detecção de anomalias via IsolationForest.
- `ai/`: segurança, extração estruturada opcional e sumarização sem impacto financeiro.
- `api/`: FastAPI com endpoint de auditoria.
- `ui/`: Streamlit para uso operacional.
- `scripts/`: geração de dados e execução em lote.

## Fluxo
1. Carregar CSVs.
2. Validar schemas/ranges com Pydantic.
3. Cruzar faturas x embarques.
4. Calcular frete esperado de forma determinística.
5. Classificar divergências e severidade.
6. Rodar ranking por anomalia.
7. Persistir resultados + audit trail.
