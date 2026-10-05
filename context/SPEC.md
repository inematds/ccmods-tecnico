# SPEC — Mods do Claude Code: curso técnico (formato-curso-v2)

Curso INEMA.CLUB (aberto e gratuito) para **quem programa** e quer escrever, testar e distribuir mods do Claude Code.
Título exato: **Mods do Claude Code — o curso técnico**. courseId = `ccmt`. Repo `inematds/ccmods-tecnico`.
Skill de formato: `~/.claude/skills/formato-curso-v2/` (erros críticos #1–#31 valem).

## Versão e autoridade (dizer no curso)

- Tudo foi conferido no **Claude Code 2.1.289**, em **05/10/2026**, nesta máquina (Linux ARM64).
- A API de mods está em **acesso antecipado e muda entre versões**. A autoridade é o arquivo de tipos da SUA instalação: `.claude-plugin/types/claude-code/index.d.ts`, que o Claude Code escreve dentro da pasta do mod quando ele carrega por `--plugin-dir`/pasta de mods. O curso ensina a ler esse arquivo; nunca prometer que um nome vale para sempre.

## Fontes da verdade (ler à vontade; NÃO editar nenhuma delas)

1. Referência oficial (vem com o Claude Code): `/tmp/claude-1000/bundled-skills/2.1.289/4a690ea2f793d25136db54dac3d94b2a/plugin-authoring/reference.md` (182 linhas) e `.../plugin-authoring/examples/{band.tsx,band-state.d.ts,pane.tsx,pane-state.d.ts,tool-call.ts}`.
2. Tipos (20 422 linhas — use grep): `.../plugin-authoring/types/claude-code.d.ts`.
3. Kit da Prompt Advisers (MIT, **dar crédito**): `~/projetos/claude-mods-starter-kit` — 10 plugins em `plugins/`, `templates/starter-mod/`, `scripts/{check.sh,try.sh,manage.sh}`, `prompts/`, `.claude-plugin/marketplace.json`.
4. Kit INEMA: `~/projetos/inema-mods` — 18 mods em `mods/`, `docs/COMO-FAZER-UM-MOD.md` (estrutura, verificação e **23 pegadinhas** — copiar o sentido, citar a fonte), `scripts/checar-mod.sh`, modelo `mods/recibo-sessao/`.

## Público e tom

- Programador ou quase: sabe usar terminal, já leu JavaScript/TypeScript, já usou o Claude Code. Não precisa conhecer a API de mods.
- Mesmo assim, cada termo da API é definido na 1ª vez (box "🆕 Novo aqui?"): hook, `$`, `e`, `next`, dispatch, surface, noun, matcher, atom, store...
- Tom: direto, frases curtas, parágrafos de 2–4 linhas, sem coachzinho, português correto com acentos.
- Não citar criadores, canais ou vídeos de terceiros. A Prompt Advisers aparece **só como autora do kit** (crédito, MIT).
- Personagem fixo dos exemplos: **Rafa, 34, dev** de uma agência pequena, que quer ver o que o Claude toca no repositório e não perder trabalho entre sessões.

## Forma do código (congelado)

- **Primeiro mod (T1)**: a forma do kit, `hooks/starter.mjs` com `export function register(on) {…}` — sem compilação, sem tipos.
- **A partir da T2**: a forma tipada dos exemplos oficiais e do inema-mods: `hooks/register.tsx` (ou `.ts`) com `import type { Register } from 'claude-code'` e `export const register: Register = (on, options) => {…}`; JSX com `h` como fábrica; tipos de estado em `types/index.d.ts` apontado por `"types"` no `plugin.json`.
- Toda função que recebe `$` é declarada no topo do arquivo (pegadinha 1).

## Vocabulário fixo (um nome por conceito)

- **mod** = plugin do Claude Code com *function hooks* (módulo que exporta `register`). "Plugin" é o pacote; "mod" é o apelido.
- **hook** = função `($, e, next)` registrada com `on(evento, matcher?, hook)`.
- **hook clássico** = os hooks de `settings.json` (comandos de shell, PreToolUse/PostToolUse...). No mod eles aparecem como eventos `classic.<Nome>`.
- **evento** = nome como `tool.call`; **noun** = a parte antes do ponto (`tool`, `ui`, `session`...).
- **cadeia** = os hooks de todos os plugins + o comportamento do próprio Claude Code, ligados por `next`.
- **dispatch** = uma passagem de um evento pela cadeia (tem orçamento de tempo).
- **superfície** = onde desenha: `terminal`, `desktop`, `mobile`, `vscode`.
- **faixa** = `AbovePrompt` (uma só, compartilhada); **painel** = `Pane`.

## COMANDOS PERMITIDOS (nenhum outro entra numa página)

Tier A = rodado aqui em 05/10/2026, saída real abaixo (pode mostrar como saída).
Tier B = da referência oficial ou da documentação dos kits (mostrar o comando; resultado como "esperado", sem inventar saída de terminal).

| Comando (verbatim) | Fonte | Tier | Saída / esperado |
|---|---|---|---|
| `claude --version` | — | A | `2.1.289 (Claude Code)` |
| `git clone https://github.com/inematds/claude-mods-starter-kit` · `cd claude-mods-starter-kit` | README do kit | — | — |
| `git clone https://github.com/inematds/inema-mods` · `cd inema-mods` | README inema-mods | — | — |
| `claude plugin validate templates/starter-mod` | kit | A | bloco VALIDATE |
| `claude plugin test templates/starter-mod` | kit | A | bloco TEST |
| `claude plugin validate <pasta-do-mod>` · `claude plugin test <pasta-do-mod>` | reference.md | A | `✔ Validation passed` · `N pass` / `0 fail` |
| `bash scripts/check.sh` (kit) | kit | A | ver TABELA DO KIT — aqui parou no terminal-pet (teste de desempenho estourou 5 s) |
| `bash scripts/try.sh terminal-pet` | kit START-HERE | B | abre uma sessão temporária só com o mod |
| `bash scripts/manage.sh install user all` · `bash scripts/manage.sh disable user all` | kit | B | — |
| `claude -p "/readcount" --plugin-dir templates/starter-mod` | kit | A | `read-counter-example: Successful reads observed: 0` |
| `claude -p "/recibo" --plugin-dir mods/recibo-sessao` | inema-mods | A | `recibo-sessao: Nesta sessão: nenhum arquivo criado ou alterado.` |
| `TSC=<caminho do tsc> scripts/checar-mod.sh mods/recibo-sessao` | inema-mods | A | bloco CHECAR |
| `claude --plugin-dir <pasta>` (repita a flag para vários) | reference.md | B | carrega só nesta sessão; pasta vigiada (hot-reload) |
| `CLAUDE_CODE_PLUGIN_DIRS=<caminho absoluto>` | reference.md | B | igual ao `--plugin-dir`, para desktop/SDK |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH=1` | reference.md | B | vigia também sessões headless longas |
| `claude --debug` | reference.md | B | log com cada hook pulado e o motivo |
| `/reload-plugins` (dentro da sessão) | reference.md | B | relê plugin instalado de marketplace-pasta |
| `claude plugin marketplace add <pasta-ou-dono/repo> --scope user` | kit START-HERE | B | — |
| `claude plugin install <plugin>@<marketplace> --scope user` (ou `project`, `local`) | kit START-HERE | B | — |
| `claude plugin disable <plugin>@<marketplace> --scope user` | guias do kit | B | — |
| `claude plugin update` · `claude plugin list` | reference.md | B | `list` mostra `Read from:` |
| `claude plugin init` | reference.md | B | **cria outro tipo de plugin** (command hooks), não um mod — avisar |
| `ls .claude-plugin/types/` (na pasta do mod carregado) | reference.md | B | `claude-code/`, `claude-code-tools/`, `claude-code-mcp/`, `tsconfig.json` |
| `tsc -p <pasta-do-mod>` | reference.md | B | checa tipos sem passo extra |

Prompts para colar no Claude Code podem ser criados, desde que só peçam leitura de arquivos, os comandos acima, ou o uso de um prompt de `prompts/` do kit (ex.: `Leia prompts/01-terminal-pet.txt e construa esse mod numa pasta nova chamada meu-pet. Não instale nada; teste com claude plugin validate e claude plugin test.`).

### Saídas reais (Tier A)

VALIDATE (`claude plugin validate templates/starter-mod`):
```
Validating plugin manifest: .../templates/starter-mod/.claude-plugin/plugin.json

Validating hooks: .../templates/starter-mod/hooks/hooks.json

  ❯ ./starter.mjs hooks: session.start, tool.call{tool=Read}, command.run{command=readcount}
  ❯ ./starter.mjs calls: $.command.register

✔ Validation passed
```
TEST (`claude plugin test templates/starter-mod`):
```
tests/starter.test.ts:
(pass) counts successful reads and excludes failed ones [20.64ms]

 1 pass
 0 fail
Ran 1 test across 1 file. [0.13s]
```
CHECAR (`scripts/checar-mod.sh mods/recibo-sessao`):
```
== recibo-sessao
  validate: ok
  tsc: ok
  test: ok (6 linhas de aprovação)
```
TABELA DO KIT (validate + test por plugin, 2.1.289): auto-handoff 15/0 · changes-receipt 18/0 · context-meter 2/0 · coral-skin 9/0 · flight-recorder 7/0 · model-router 7/0 · output-tray 18/0 · repo-heatmap 19/0 · session-bookmarks 15/0 · terminal-pet 12/1 (o teste "whole sprite set stays far under the terminal's color-pair table" estourou o limite de 5 s com a máquina carregada) · starter-mod 1/0. Total 123 de 124. Todos `validate=ok`.

### Arquivos reais que podem ser mostrados (copiar, não reescrever)

- `templates/starter-mod/hooks/hooks.json` = `{"modules":["./starter.mjs"]}`
- `templates/starter-mod/hooks/starter.mjs` e `tests/starter.test.ts` (inteiros — são curtos).
- `templates/starter-mod/.claude-plugin/plugin.json` (`name: read-counter-example`).
- `.claude-plugin/marketplace.json` do kit (`name: claude-mods-kit`, `plugins[].source: ./plugins/<nome>`).
- `examples/band.tsx` e `examples/pane.tsx` da referência oficial (trechos).
- `inema-mods/mods/recibo-sessao/` (register.tsx, types, tests/mundo.ts) e `mods/freio-de-mao`, `mods/vigia-api`, `mods/guarda-colisao`, `mods/roteador-subagente` para os exemplos de controle (trechos curtos, sempre com o caminho).

### Nomes de API

Todo `$.<noun>.<método>` e todo `on('<evento>'` citado precisa existir no `claude-code.d.ts` 2.1.289 (o `lint.py` confere). Eventos mais usados: `session.start`, `session.end`, `prompt.submit`, `turn.start`, `turn.step` (stream), `turn.complete`, `tool.call`, `tool.describe`, `command.run`, `ui.render`, `ui.press`, `ui.input`, `ui.select`, `session.append`, `state.set`, `process.spawn` (stream), `classic.<Nome>` (ex.: `classic.PreToolUse`, `classic.Stop`).

## Mapa do curso (CONGELADO — títulos h2 dos tópicos = títulos no índice da trilha)

Cada módulo: 6 tópicos, `~35 min`. Emoji do card entre colchetes.

### T1 · 🧬 Anatomia (emerald) — nav "Anatomia"
- **1.1 [🧬] O que é um mod por dentro** — "Três arquivos e uma função" · Fundamento
  1. Entenda o que muda quando um mod carrega
  2. Separe mod, hook clássico, skill e MCP
  3. Leia a assinatura register(on, options)
  4. Conheça os três parâmetros de todo hook
  5. Saiba onde o mod roda e o que ele não tem
  6. Veja o mapa do curso e os dois kits
- **1.2 [🗂️] Estrutura de arquivos e manifesto** — "plugin.json manda" · Prático
  1. Monte a árvore mínima de pastas
  2. Escreva o plugin.json
  3. Aponte o módulo no hooks.json
  4. Escolha a extensão do arquivo
  5. Declare opções com userConfig
  6. Valide antes de carregar
- **1.3 [🔄] Carregar, recarregar e instalar** — "Pasta vigiada, mod vivo" · Prático
  1. Carregue com --plugin-dir
  2. Veja o hot-reload acontecer
  3. Use CLAUDE_CODE_PLUGIN_DIRS no desktop
  4. Instale por marketplace
  5. Escolha o escopo certo
  6. Desligue e desinstale sem sobras
- **1.4 [🚀] Seu primeiro mod: comando e contador** — "readcount funcionando" · Prático
  1. Copie o starter-mod
  2. Leia o código linha por linha
  3. Valide e teste
  4. Rode o comando sem gastar modelo
  5. Mude o contador para outra ferramenta
  6. Renomeie para virar seu

### T2 · ⚡ Eventos e estado (blue) — nav "Eventos e estado"
- **2.1 [🗺️] O mapa de eventos** — "Escolha o evento antes do código" · Fundamento
  1. Agrupe os eventos por noun
  2. Siga uma volta completa do turno
  3. Use matchers para filtrar
  4. Trate os eventos que são stream
  5. Pendure-se nos hooks clássicos
  6. Ache qualquer evento nos tipos
- **2.2 [⛓️] A cadeia: next, reescrever e responder** — "Quem chama next decide" · Fundamento
  1. Entenda a cadeia de plugins
  2. Observe e passe adiante
  3. Reescreva o que vem depois
  4. Responda sem chamar next
  5. Use .catch para falhar com segurança
  6. Respeite o orçamento e o next.signal
- **2.3 [💾] Estado que sobrevive** — "Variável some no reload" · Prático
  1. Veja a variável de módulo sumir
  2. Declare o contrato em types/index.d.ts
  3. Use atom, read e update
  4. Guarde entre sessões com $.store
  5. Use o relógio do engine
  6. Escolha onde cada dado mora
- **2.4 [⏱️] Trabalho fora do dispatch** — "session.start acende, clock mantém" · Prático
  1. Comece no session.start
  2. Agende com clock.every e clock.after
  3. Leia e escreva arquivos com $.fs
  4. Rode processos locais com $.process
  5. Acorde a sessão com prompt.submit
  6. Decida se o mod pode gastar modelo

### T3 · 🖥️ Telas e comandos (purple) — nav "Telas e comandos"
- **3.1 [🎨] ui.render e as superfícies** — "Uma árvore por superfície" · Fundamento
  1. Entenda o que o ui.render recebe
  2. Pegue os elementos com ui.resolve
  3. Respeite as diferenças entre superfícies
  4. Desenhe do estado, nunca escreva ao desenhar
  5. Saiba o que acontece quando a árvore não valida
  6. Use Raster e Image no terminal
- **3.2 [📟] Faixa, status e avisos** — "Uma faixa para todos" · Prático
  1. Desenhe na faixa acima do prompt
  2. Conviva com os outros mods
  3. Mostre status sem abrir nada
  4. Avise com toast e log
  5. Disseque o exemplo oficial da faixa
  6. Teste a faixa no terminal e no desktop
- **3.3 [🪟] Painéis e botões** — "Abra por comando" · Prático
  1. Abra um painel com ui.open
  2. Dimensione pelo bodyColumns
  3. Ponha botões com hotkey
  4. Trate press, input e select
  5. Faça um painel virar diálogo
  6. Feche e libere o painel
- **3.4 [⌨️] Comandos, ferramentas e configuração** — "/comando sem modelo" · Prático
  1. Registre um comando de barra
  2. Responda o command.run
  3. Desenhe a saída do comando
  4. Dê uma ferramenta ao modelo
  5. Leia as opções do /config
  6. Evite colisão de nomes

### T4 · 🛡️ Controlar, testar e distribuir (amber) — nav "Controlar e distribuir"
- **4.1 [🛡️] Mods que mudam o fluxo** — "Pergunte antes de apagar" · Prático
  1. Intercepte uma chamada de ferramenta
  2. Negue com motivo claro
  3. Pergunte ao humano com ui.ask
  4. Troque o modelo de um subagente
  5. Preserve as permissões do usuário
  6. Estude a guarda do freio-de-mão
- **4.2 [🧪] Testar com claude plugin test** — "O engine de verdade, sem modelo" · Prático
  1. Entenda o que o teste simula
  2. Escreva os mocks antes do $
  3. Teste um comando de ponta a ponta
  4. Controle o relógio
  5. Monte a tela em terminal e desktop
  6. Leia uma falha de teste
- **4.3 [🔍] Depurar e as pegadinhas** — "O log diz por quê" · Prático
  1. Ligue o --debug
  2. Leia a linha de hook pulado
  3. Corrija um módulo que não carrega
  4. Corrija uma árvore recusada
  5. Percorra as pegadinhas do kit INEMA
  6. Faça um teste de fumaça com claude -p
- **4.4 [📦] Distribuir e projeto final** — "Seu mod no marketplace" · Prático
  1. Monte o marketplace.json
  2. Publique num repositório
  3. Atualize sem quebrar quem usa
  4. Revise antes de compartilhar
  5. Faça o projeto final
  6. Siga para os próximos passos

## Projeto final (4.4)

Um mod próprio do Rafa: comando `/x` + faixa ou painel + estado em `$.state` + teste com `claude plugin test` (mocks antes do `$`) + `claude plugin validate` OK + botão/comando de desligar + README. Prova: `claude plugin test <pasta>` com `0 fail` e `claude -p "/<comando>" --plugin-dir <pasta>` respondendo sem modelo.

## Próximos passos (4.4 tópico 6, e landing)

- Curso básico de mods (v6) — "em breve" (sem link até existir).
- `https://inematds.github.io/cchooks/` (hooks clássicos), `https://inematds.github.io/makeclaudex/` (plugins de produção), `https://inematds.github.io/curso-agent-runtime/` (trilha 4: guarda e painel), repos `https://github.com/inematds/inema-mods` e `https://github.com/inematds/claude-mods-starter-kit`.
