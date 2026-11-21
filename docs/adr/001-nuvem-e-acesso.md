# ADR 001 - Nuvem e forma de acesso à fonte

Status: proposta (validar com o grupo)

## Contexto

A Base dos Dados disponibiliza o dataset nativamente no BigQuery e também para download direto. As duas formas são aceitas; o que conta é a justificativa (arquitetura, custo, atualização da fonte).

## Proposta

GCP, lendo direto do BigQuery público e exportando para Parquet no GCS (bronze).

Motivos:

- A fonte já está no BigQuery, então não há transferência entre nuvens nem egress.
- Custo de leitura medido por dry run antes de cada extração.
- Silver e Gold no BigQuery, que é onde a fase 3 vai consumir.

## Pontos a medir e registrar

- Bytes escaneados por tabela (com `SELECT *` e com as colunas que de fato usamos)
- Tamanho dos Parquet no GCS
- O que muda quando a fonte publicar um novo ano: _TODO_

## Alternativas consideradas

- Download dos arquivos + AWS (S3/Glue/Athena): _TODO prós e contras_
- Multi cloud: _TODO, se for o caso discutir egress, billing duplo, IAM duplo_
