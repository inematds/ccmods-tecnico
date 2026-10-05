# Estado — atualizado 2026-10-05 18:45

## Funciona
- SPEC (context/SPEC.md) com mapa congelado 4×4×6 e comandos Tier A rodados aqui.
- Gerador copiado do curso-agent-runtime (montar/lint/checar-navegador), courseId ccmt; lint com checagem anti-invenção de API.
- Modelo context/corpos/modulo-1-1.html → LINT OK.
- 16 módulos + 4 índices + landing escritos; LINT OK; checar-navegador 42/42; exemplos de código extraídos e validados (claude plugin validate) — os que falham são trechos rotulados ou o exemplo propositalmente errado da pegadinha 1.
- Capa (flux, cena temática). Repo inematds/ccmods-tecnico publicado (05a9576), Pages via Actions configurado.

## Falta
- Prompts de entrevista (inema-mods + prompts-prontos): ver ~/projetos/output/cursos-mods/CONTINUAR-PROMPTS-ENTREVISTA.md
- Pages no ar (incidente do GitHub Actions: runners não alocam; vigia em scratchpad/vigia-pages.sh redispara). Depois: portal (curso em platformsData + trilha 🖥️ Claude Code + updatesData + enrichment curso:ccmods-tecnico).
- Pendências paralelas desta sessão:
  - claude-mods-starter-kit: Pages travado no incidente do GitHub Actions; redisparado run 37368206172. Depois: registrar EN/ES em portal/src/data/translated-courses.ts.
  - curso-agent-runtime no portal: patch em /tmp/claude-1000/-home-nmaldaner-projetos-wifi/d9283068-d105-468a-b00a-a8d64c3b4f42/scratchpad/portal-agent-runtime.patch — aplicar só quando https://inematds.github.io/curso-agent-runtime/ der 200 (Pages legacy dele também travado). Outra sessão traduz esse curso (en/, i18n/ não commitados) — não mexer no repo.
  - Curso básico v6: o usuário precisa invocar /formato-curso-v6 sozinho (skill bloqueada para o modelo). Brief: ~/projetos/output/cursos-mods/BRIEF.md.

## Como retomar
```
cd ~/projetos/ccmods-tecnico
python3 scripts/montar.py && python3 scripts/lint.py
```
