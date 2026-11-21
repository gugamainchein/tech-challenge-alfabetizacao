# Evidências de execução

Organizar por data de execução: `evidencias/AAAA-MM-DD/`.

O que guardar:

- [ ] job ids do BigQuery (export bronze, silver, gold)
- [ ] prints do console (GCS com as partições, datasets, Pub/Sub)
- [ ] contagem de linhas por tabela em cada camada
- [ ] consulta em `ops.pipeline_runs` mostrando várias execuções acumuladas
- [ ] consulta em `ops.dq_results`, incluindo uma execução reprovada
- [ ] log/print do pipeline parando numa regra bloqueante
- [ ] alerta de falha recebido (e-mail ou webhook)
- [ ] latência medida no streaming
- [ ] dry runs usados na estimativa de custo
