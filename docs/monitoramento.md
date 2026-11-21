# Monitoramento

## Métricas persistidas

`ops.pipeline_runs`, uma linha por etapa por execução (append):

| Coluna | Descrição |
|---|---|
| run_id | id da execução |
| pipeline | batch, silver, gold, consume |
| step | etapa |
| started_at | início |
| duration_s | duração |
| rows_in / rows_out | linhas de entrada e saída |
| bytes_processed | bytes processados no BigQuery |
| status | success / failed |
| error | mensagem de erro |

## Latência

- Batch: _TODO_
- Streaming: `ingested_at - produced_at`. Os dois campos são gravados por processos diferentes (produtor e consumidor), senão a diferença seria sempre zero.

## Alertas

_TODO: alert policy do Cloud Monitoring + webhook. Quem recebe e em quanto tempo._
