# Brief para os agentes que escrevem páginas (curso ccmods-tecnico)

Você escreve CORPOS em `~/projetos/ccmods-tecnico/context/corpos/`. Nunca edite `curso/**` nem `index.html` (são gerados), nem o modelo `context/corpos/modulo-1-1.html`, nem a SPEC, nem os scripts.

## Leia antes de escrever
1. `context/SPEC.md` — público, tom, vocabulário, **mapa congelado** (títulos dos 6 tópicos de cada módulo = os h2, verbatim), COMANDOS PERMITIDOS e saídas reais.
2. `context/corpos/modulo-1-1.html` — o MODELO. Copie a estrutura por marcador de texto (header, `<main>`, cada `<section id="topico-N">`, boxes, resumo, `<aside>` com TOC, `<!--CHECKS-->`), nunca por número de linha.
3. As fontes técnicas da SPEC (reference.md, claude-code.d.ts, kits). Use `grep` no d.ts (20 mil linhas) para confirmar cada nome de evento, noun, método e campo ANTES de escrever. Não invente API: o lint rejeita `$.x.y` e `on('evento'` que não existam no d.ts.

## Regras de cada módulo (o lint confere)
- Primeira linha: `<!--TITLE: <título do módulo> -->`.
- Cor da trilha: T1 emerald, T2 blue, T3 purple, T4 amber (troque todas as classes `emerald` do modelo; ciano `#38bdf8` continua secundário nos SVG). Cores SVG da trilha: emerald #34d399/#a7f3d0/#0e2018 · blue #60a5fa/#bfdbfe/#0f1b33 · purple #c084fc/#e9d5ff/#1e1233 · amber #fbbf24/#fde68a/#2a1d06.
- Exatamente 6 `<section id="topico-N" data-inema-topic="modulo-X-Y#topico-N">`, com `<h2 class="text-2xl font-bold flex-1">` = título da SPEC, verbatim.
- `data-inema-module="X-Y"` e `data-inema-track="X"` no header e no main; `data-inema-block="mX-Y-tN-pM"` únicos nos parágrafos; botão "Tenho dúvida" e "Marcar como lido" em cada tópico (copiar do modelo).
- **≥2 SVG** `role="img"` com `aria-label` que ensina, cada um seguido de "Como ler o desenho". IDs de `pattern/filter/marker/gradient` únicos na página: prefixo `m<XY><letra>-` (ex.: `m23a-grid`, `m23b-glow`).
- Cada módulo **Prático** tem ≥1 bloco copia-e-cola no formato do modelo 1.2 do agent-runtime: cabeçalho "🎯 Objetivo: …", `<pre>` com o código/comando, rodapé `<strong>Como verificar:</strong> …`. Só comandos da tabela COMANDOS PERMITIDOS; saída mostrada só se for Tier A (verbatim da SPEC); senão "resultado esperado".
- Código de mod mostrado: copie de arquivos reais (com o caminho no cabeçalho do bloco) ou escreva exemplos curtos que usem SÓ nomes confirmados no d.ts. A partir da T2, forma tipada (`import type { Register } from 'claude-code'`, `export const register: Register = (on, options) => {…}`), funções que recebem `$` declaradas no topo do arquivo.
- Escape HTML dentro de `<pre>`: `&lt;` `&gt;` `&amp;`.
- Box "🆕 Novo aqui?" para cada termo novo da API na primeira aparição.
- Variedade: ≥2 grids ✓/✗, ≥1 sequência numerada (timeline), ≥2 boxes (💡 dica, ⚠️ alerta), tabelas quando comparar.
- 1 teste rápido (`data-inema-check="modulo-X-Y#q1"`, 3 opções, feedback no bloco `<!--CHECKS-->` com `INEMA.registerCheck`).
- Resumo com 5 ✓, "Próximo módulo" e botões ← trilha / Módulo seguinte → (no último módulo da trilha, aponte para `../trilhaN+1/index.html`; no 4.4, para `../../index.html`).
- `<aside>` com TOC de 6 itens curtos.
- Tamanho do corpo: 420–560 linhas (a página montada fica entre 500 e 850).
- Português correto com acentos, frases curtas, sem emoji em excesso no texto corrido. Exemplos com o Rafa quando couber.
- Crédito: o Claude Mods Starter Kit é da Prompt Advisers (MIT).

## Verificação (obrigatória antes de terminar)
```
cd ~/projetos/ccmods-tecnico && python3 scripts/montar.py && LINT_SEM_LINKS=1 python3 scripts/lint.py curso/trilhaX/modulo-X-Y.html
```
Precisa terminar em `LINT OK` para cada arquivo seu. Corrija até passar. Responda só com as linhas de resultado do lint dos seus arquivos e, se houver, o que você não conseguiu confirmar no d.ts.
