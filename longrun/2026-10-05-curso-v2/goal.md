# Goal — curso-v2 (ccmods-tecnico)

- **Início:** 2026-10-05 17:09 · **Agente:** Claude (sessão interativa) + 5 subagentes
- **Tetos:** tempo 4 h · sem API paga · Codex só pela assinatura (tradução, se fizer)

## Resultado
Curso v2 "Mods do Claude Code — o curso técnico" publicado em inematds.github.io/ccmods-tecnico/ e cadastrado no portal (trilha 🖥️ Claude Code).

## Critérios de pronto
**Função**
- [ ] `python3 scripts/montar.py && python3 scripts/lint.py` → `LINT OK` (16 módulos × 6 tópicos, 4 índices com 24 tópicos, landing; checagem de API contra o d.ts 2.1.289)
- [ ] `node scripts/checar-navegador.cjs http://127.0.0.1:<porta> pt` (NODE_PATH=~/projetos/agent-browser/node_modules) → 0 erros de página, 0 overflow em 360 px
- [ ] `curl -s -o /dev/null -w '%{http_code}' https://inematds.github.io/ccmods-tecnico/` → `200`
**Regressão**
- [ ] `context/corpos/modulo-1-1.html` sem mudança depois do lote (modelo congelado): `git diff --stat <commit-modelo> -- context/corpos/modulo-1-1.html` → vazio
**Limite**
- [ ] nada editado em ~/projetos/inema-mods nem ~/projetos/claude-mods-starter-kit (`git -C … status --short` igual ao início)
- [ ] portal: só as linhas do curso (courses.ts, Portal.tsx trilha Claude Code, courses.data.json)

**Teste rápido por ciclo**: `LINT_SEM_LINKS=1 python3 scripts/lint.py <arquivo>`
**Teste completo no final**: lint completo + checar-navegador
