# Dicionário de Dados

## embarques.csv
`shipment_id, order_id, transportadora, modal, uf_origem, cidade_origem, uf_destino, cidade_destino, data_coleta, data_prevista, peso_kg, volume_m3, dist_km, tentativas, valor_contratado, sla_dias`

## faturas.csv
`invoice_id, shipment_id, data_fatura, valor_cobrado, itens_taxa, observacao`

## tabela_frete.csv
`transportadora, uf_destino, km_min, km_max, tarifa_base, tarifa_por_kg, fator_regiao, pedagio_por_km, taxa_risco_pct, fator_cubagem`

## auditoria_resultado.csv
Inclui os campos originais e derivados: `expected_total, diferenca_valor, divergencia_tipo, severidade, anomaly_score, prioridade`.
