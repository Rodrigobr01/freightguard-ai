# Modelo de Regras Determinísticas

## Fórmulas
- `peso_cubado = max(peso_kg, volume_m3 * fator_cubagem)`
- `base = (tarifa_base + (peso_cobrado * tarifa_por_kg)) * fator_regiao`
- `pedágio = dist_km * pedagio_por_km`
- `expected_subtotal = base + pedágio`
- `risco = expected_subtotal * taxa_risco_pct`
- `adicionais = (tentativas - 1) * taxa_fixa_tentativa_extra`
- `expected_total = expected_subtotal + risco + adicionais`

## Classificação de divergência
- Duplicidade de invoice por `shipment_id`.
- Faixa de km sem match exato na tabela.
- Taxa indevida detectada em `itens_taxa/observacao`.
- Cubagem com impacto relevante.
- Diferença simples de valor.
