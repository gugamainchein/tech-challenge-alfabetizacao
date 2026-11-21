# Pipeline Híbrido para Análise da Alfabetização no Brasil

Tech Challenge Fase 2 - POSTECH IA para Devs / Data (FIAP)

| Integrante | RM |
|---|---|
| Gustavo Mainchein | RM377234 |
| Gustavo Lopes | RM377947 |
| Gustavo Valentim | RM377956 |
| Luana Barbosa | RM377490 |

> Status: em desenvolvimento. As seções abaixo serão preenchidas conforme o que estiver de fato implementado.
> Tudo que ainda não existe no repositório deve aparecer como "planejado", nunca no presente.

Vídeo executivo: _(link)_

## 1. Contexto do problema

_TODO: Compromisso Nacional Criança Alfabetizada, ponto de corte 743 no Saeb, Indicador Criança Alfabetizada._

### Meta de 2030

_TODO: explicar a diferença entre a meta pactuada (`meta_alfabetizacao_2030`, valor 80 para a rede pública) e a leitura de universalização. Ver [docs/adr/002-meta-2030.md](docs/adr/002-meta-2030.md)._

## 2. Arquitetura

_TODO: diagrama do que foi implementado. Fonte do diagrama em [docs/arquitetura.md](docs/arquitetura.md)._

### Camadas

| Camada | Onde fica | Política de escrita |
|---|---|---|
| Bronze | _TODO_ | _TODO_ |
| Silver | _TODO_ | _TODO_ |
| Gold | _TODO_ | _TODO_ |

## 3. Fonte de dados e forma de acesso

Dataset `br_inep_avaliacao_alfabetizacao` da Base dos Dados.

- Por que escolhemos esse caminho: _TODO_
- Impacto em custo (bytes escaneados, transferência, egress): _TODO_
- O que acontece quando a fonte for atualizada: _TODO_

Decisão registrada em [docs/adr/001-nuvem-e-acesso.md](docs/adr/001-nuvem-e-acesso.md).

## 4. Tecnologias

| Ferramenta | Uso | Status |
|---|---|---|
| _TODO_ | | implementado / planejado |

## 5. Decisões arquiteturais

- Batch x streaming: _TODO_
- Data lake x data warehouse: _TODO_
- Custo x performance: _TODO_

## 6. Ingestão streaming

- Mecanismo de mensageria: _TODO_
- Processamento incremental: _TODO_
- Latência, frequência e garantias em relação ao batch: _TODO_
- Eventos inválidos e duplicados: _TODO_
- Identificação de origem (dado simulado x oficial): _TODO_

## 7. Qualidade de dados

Regras, classificação (bloqueante / informativa), limiar da taxa de correspondência dos joins e onde os resultados ficam gravados: [docs/qualidade.md](docs/qualidade.md).

Evidência do pipeline falhando: _TODO_

## 8. Monitoramento

Em produção, quem descobre que o pipeline quebrou, e em quanto tempo? _TODO_

Detalhes em [docs/monitoramento.md](docs/monitoramento.md).

## 9. FinOps

| Serviço | Unidade | Quantidade medida | Preço unitário | Custo mensal projetado |
|---|---|---|---|---|
| | | | | |

Metodologia e medições em [docs/finops.md](docs/finops.md).

## 10. Aplicação em IA

_TODO: uso da Gold para predição de alfabetização, desigualdade educacional e políticas públicas. Cuidado com vazamento de alvo na base de features._

## 11. Limitações conhecidas

_TODO_

## 12. Como executar

### Pré-requisitos

- Python 3.12+
- Conta GCP com billing ativo e `gcloud` autenticado
- Terraform 1.9+

### Passo a passo

```bash
git clone <url-do-repo>
cd tech-challenge-alfabetizacao
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencher com os dados do seu projeto
```

_TODO: comandos de infra, batch, streaming, silver, gold e checks._

### Testes

```bash
pip install -r requirements-dev.txt
pytest
```

## 13. Evidências de execução

Ver [evidencias/](evidencias/).

## Estrutura do repositório

```
config/          parâmetros da pipeline (tabelas, colunas, limiares)
src/pipeline/    código da pipeline
  ingestion/     batch e streaming
  quality/       regras de qualidade
  monitoring/    métricas de execução e alertas
sql/             transformações bronze, silver e gold
infra/terraform/ infraestrutura
orchestration/   orquestração
docs/            documentação técnica e decisões (ADRs)
evidencias/      prints, job ids, logs e contagens
notebooks/       exploração
tests/           testes automatizados
```
