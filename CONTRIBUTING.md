# Como trabalhamos

## Branches

- `main` é protegida e só recebe merge via PR.
- Uma branch por issue: `feat/12-producer-pubsub`, `fix/30-join-uf`, `docs/44-readme`.

## Commits

Mensagens curtas no imperativo, referenciando a issue:

```
feat: extrai tabela municipio para bronze (#9)
```

## Pull requests

- Pelo menos 1 revisão de outra pessoa do grupo antes do merge.
- CI precisa estar verde.
- Se a PR muda algo que o README descreve, atualizar o README na mesma PR.

## Project board

Fluxo das colunas: `Todo` -> `In Progress` -> `Done`.
Ao pegar uma tarefa, preencha o campo Responsável e mova para In Progress. A issue fecha quando a PR com `Closes #N` for mergeada.

## Credenciais

Nada de chave, token ou JSON de service account no repositório. Use `.env` (já está no `.gitignore`).
