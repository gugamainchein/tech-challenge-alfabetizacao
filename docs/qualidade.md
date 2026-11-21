# Qualidade de dados

As regras ficam em `src/pipeline/quality/checks.py`. Cada regra retorna um valor numérico e tem limite mínimo e/ou máximo.

- Bloqueante: se falhar, a camada seguinte não é publicada e o processo termina com código diferente de zero.
- Informativa: só registra.

Resultados vão para `ops.dq_results` em toda execução (append), antes do gate ser aplicado.

## Catálogo de regras

| Regra | Camada | Tabela | Tipo | Limite |
|---|---|---|---|---|
| Duplicidade de chave | silver | _TODO_ | bloqueante | 0 |
| Nulos em colunas-chave | silver | _TODO_ | bloqueante | 0 |
| Nulos em proficiência | silver | alunos | informativa | _TODO_ |
| Código sem tradução no dicionário | silver | _TODO_ | bloqueante | 0 |
| Taxa de correspondência dos joins | silver/gold | _TODO_ | bloqueante | `join_match_min` |
| Consistência entre tabelas | gold | _TODO_ | _TODO_ | _TODO_ |

## Limiar da taxa de correspondência

Valor atual em `config/pipeline.yaml`: `join_match_min: 0.98`. Justificativa: _TODO depois de medir as taxas reais._

## Execução reprovada

_TODO: registrar aqui (e em evidencias/) uma execução que parou numa regra bloqueante._
