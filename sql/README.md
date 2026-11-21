# SQL

Os arquivos de cada pasta rodam em ordem alfabética (`01_...sql`, `02_...sql`) pelo `pipeline.run`.
Use `{project}` para o id do projeto, ele é substituído na execução.

- `bronze/`: tabelas externas sobre os Parquet do GCS e a bronze do streaming
- `silver/`: limpeza, tipos, decodificação via dicionário, chaves normalizadas, integração
- `gold/`: indicadores, meta x resultado, evolução temporal, base de features da fase 3

Lembretes:

- Nulo não vira zero. Proficiência zero não existe.
- Sem meta cadastrada é um terceiro estado, não "não atingiu".
- Indicador agregado é ponderado por alunos, não média simples entre municípios.
- Comparar meta e resultado só no mesmo recorte de rede e série.
- Dado simulado carrega `origem = 'simulado'` em todas as camadas.
