# CLAUDE.md — ccmods-tecnico

Curso "Mods do Claude Code — o curso técnico" no formato `formato-curso-v2` (4 trilhas × 4 módulos × 6 tópicos). courseId `ccmt`.

- Regras, mapa congelado e comandos permitidos: `context/SPEC.md`. Todo comando e todo nome de API do curso tem de existir (Tier A rodado em 05/10/2026 no Claude Code 2.1.289, ou na referência oficial / docs dos kits).
- As páginas são **montadas**: edite `context/corpos/*.html` e rode `python3 scripts/montar.py` e `python3 scripts/lint.py` (precisa `LINT OK`; o lint confere `$.noun.método`, `on('evento'` e subcomandos `claude` contra o `claude-code.d.ts` 2.1.289). Não edite `curso/**/*.html` nem `index.html` à mão.
- Fontes: referência `plugin-authoring` do Claude Code, `~/projetos/claude-mods-starter-kit` (Prompt Advisers, MIT — dar crédito) e `~/projetos/inema-mods`. Não editar os kits.
- Sem API externa sem autorização explícita.
- Conta git: `inematds <inematds@gmail.com>`. Publicar = push; GitHub Pages via Actions (raiz).

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule under ## Lessons, so it never happens again.

## Lessons

- Agentes paralelos copiam do modelo congelado (`context/corpos/modulo-1-1.html`) por marcador de texto, nunca por número de linha; ninguém edita o modelo durante o lote.
