# Mods do Claude Code — o curso técnico

Curso gratuito do [INEMA.CLUB](https://inema.club) para quem programa e quer **escrever, testar e distribuir mods do Claude Code**: `register(on, options)`, eventos, a cadeia com `next`, estado em `$.state` e `$.store`, faixa acima do prompt, painéis, comandos, ferramentas, guardas que perguntam antes de apagar, `claude plugin test` e marketplace.

**Abrir o curso:** https://inematds.github.io/ccmods-tecnico/

| Trilha | Módulos |
|---|---|
| 1 · Anatomia | O que é um mod por dentro · Estrutura de arquivos e manifesto · Carregar, recarregar e instalar · Seu primeiro mod: comando e contador |
| 2 · Eventos e estado | O mapa de eventos · A cadeia: next, reescrever e responder · Estado que sobrevive · Trabalho fora do dispatch |
| 3 · Telas e comandos | ui.render e as superfícies · Faixa, status e avisos · Painéis e botões · Comandos, ferramentas e configuração |
| 4 · Controlar e distribuir | Mods que mudam o fluxo · Testar com claude plugin test · Depurar e as pegadinhas · Distribuir e projeto final |

Projeto final: um mod seu com comando, tela, estado, teste (`claude plugin test` com `0 fail`) e publicação num marketplace.

## Versão conferida

Tudo foi rodado no **Claude Code 2.1.289**, em 05/10/2026. A API de mods está em acesso antecipado e muda entre versões: a autoridade é o arquivo de tipos da sua instalação (`.claude-plugin/types/claude-code/index.d.ts`, escrito na pasta do mod quando ele carrega).

## Material usado

- [Claude Mods Starter Kit](https://github.com/promptadvisers/claude-mods-starter-kit) — da Prompt Advisers, licença MIT (espelho: [inematds/claude-mods-starter-kit](https://github.com/inematds/claude-mods-starter-kit)).
- [inematds/inema-mods](https://github.com/inematds/inema-mods) — 18 mods em português com testes e o guia das pegadinhas.
- A referência `plugin-authoring` que vem com o Claude Code.

## Manutenção

Formato `formato-curso-v2` (HTML + Tailwind CDN + JS, sem build). Progresso, dúvidas e notas ficam só no navegador.
Edite `context/corpos/`, rode `python3 scripts/montar.py` e `python3 scripts/lint.py` (precisa `LINT OK`; o lint confere cada nome de API contra os tipos 2.1.289). Os índices de trilha saem de `scripts/gerar-trilhas.py`.

## Mais no INEMA.CLUB

- [Ficha completa deste curso](https://www.inema.club/cursos/314-mods-do-claude-code-o-curso-tecnico/)
- [Guia: como aprender inteligência artificial](https://www.inema.club/aprender-inteligencia-artificial/)
- [Todos os cursos](https://www.inema.club/cursos/)
