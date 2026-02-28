# Segurança de IA

- `LLM_ENABLED=false` por padrão.
- IA nunca altera valores financeiros; apenas extrai e resume.
- Extração estruturada exige JSON validado por schema.
- Em caso de falha do LLM, aplica fallback determinístico.
- `anti_prompt_injection`: remove instruções embutidas maliciosas do texto não confiável.
- `redact_pii`: mascara e-mail, telefone, CPF e CNPJ.
- Audit trail: hash de inputs, timestamp, versão, modo LLM, confiança e fallback.
