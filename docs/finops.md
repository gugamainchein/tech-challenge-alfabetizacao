# FinOps

## Práticas aplicadas

- [ ] Parquet com Snappy na bronze
- [ ] Particionamento / clustering nas tabelas silver e gold
- [ ] Seleção de colunas na extração (sem `SELECT *`)
- [ ] Filtro na origem
- [ ] Evitar releitura da fonte
- [ ] Budget alert e labels de custo

## Medições

| Medição | Ferramenta | Valor | Data |
|---|---|---|---|
| Bytes escaneados por extração | dry run BigQuery | | |
| Tamanho da bronze | `gsutil du -s` | | |
| Duração dos jobs | ops.pipeline_runs | | |
| Mensagens Pub/Sub | console | | |

## Estimativa

| Serviço | Unidade | Quantidade medida | Preço unitário | Custo mensal projetado |
|---|---|---|---|---|
| BigQuery (consultas) | TiB escaneado | | | |
| BigQuery (storage) | GiB/mês | | | |
| Cloud Storage | GiB/mês | | | |
| Pub/Sub | TiB | | | |
| Cloud Run Jobs | vCPU-s | | | |

Cadência considerada em produção: _TODO_. Se usarmos free tier, informar e projetar o mesmo desenho sem ele.
