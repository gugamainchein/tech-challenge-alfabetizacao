# Arquitetura

> Proposta inicial. Atualizar o diagrama para refletir apenas o que foi implementado antes da entrega.

```mermaid
flowchart LR
    subgraph Fonte
        BD[(Base dos Dados<br/>BigQuery público)]
    end

    subgraph Batch
        EX[EXPORT DATA<br/>Parquet + Snappy]
    end

    subgraph Streaming
        PR[Produtor simulado] --> PS[[Pub/Sub]]
        PS --> CO[Consumidor<br/>micro-lote]
        PS -.-> DLQ[[DLQ]]
    end

    BD --> EX --> BR[(Bronze<br/>GCS, append por run_id)]
    CO --> BRS[(Bronze stream<br/>BigQuery)]
    BR --> SI[(Silver<br/>BigQuery)]
    BRS --> SI
    SI --> GO[(Gold<br/>BigQuery)]
    GO --> F3[Base de features<br/>Fase 3]

    SI -. checks .-> DQ[(ops.dq_results)]
    GO -. checks .-> DQ
    EX -. métricas .-> RUNS[(ops.pipeline_runs)]
    RUNS --> AL[Alerta<br/>Cloud Monitoring / webhook]
```

## Entidades

| Entidade | Tabela fonte | Usada em |
|---|---|---|
| Dados de alunos | `alunos` | _TODO_ |
| Município | `municipio` | _TODO_ |
| UF | `uf` | _TODO_ |
| Meta Brasil | `meta_alfabetizacao_brasil` | _TODO_ |
| Meta UF | `meta_alfabetizacao_uf` | _TODO_ |
| Meta município | `meta_alfabetizacao_municipio` | _TODO_ |
| Dicionário | `dicionario` | _TODO_ |

Todas as seis entidades precisam aparecer na Gold de alguma forma. Tabela ingerida e não usada conta contra.
