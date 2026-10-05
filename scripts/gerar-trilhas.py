#!/usr/bin/env python3
"""Gera context/corpos/trilha{1..4}.html do curso ccmods-tecnico a partir da SPEC + dados abaixo."""
import re, html
from pathlib import Path

RAIZ = Path.home() / 'projetos' / 'ccmods-tecnico'
spec = (RAIZ / 'context' / 'SPEC.md').read_text(encoding='utf-8')

# --- lê mapa congelado da SPEC ---
MODS = {}   # '1-1' -> dict(emoji, titulo, sub, tipo, topicos[])
atual = None
for linha in spec.split('\n'):
    m = re.match(r'- \*\*(\d)\.(\d) \[(.+?)\] (.+?)\*\* — "(.+?)" · (\w+)', linha)
    if m:
        atual = f'{m.group(1)}-{m.group(2)}'
        MODS[atual] = dict(emoji=m.group(3), titulo=m.group(4), sub=m.group(5), tipo=m.group(6), topicos=[])
        continue
    m = re.match(r'\s+\d\. (.+)$', linha)
    if m and atual and len(MODS[atual]['topicos']) < 6:
        MODS[atual]['topicos'].append(m.group(1).strip())
assert len(MODS) == 16 and all(len(v['topicos']) == 6 for v in MODS.values()), MODS.keys()

CORES = {1: ('emerald', '#34d399', '#a7f3d0', '#0e2018'), 2: ('blue', '#60a5fa', '#bfdbfe', '#0f1b33'),
         3: ('purple', '#c084fc', '#e9d5ff', '#1e1233'), 4: ('amber', '#fbbf24', '#fde68a', '#2a1d06')}
NOMES = {1: ('🧬', 'Anatomia'), 2: ('⚡', 'Eventos e estado'), 3: ('🖥️', 'Telas e comandos'), 4: ('🛡️', 'Controlar e distribuir')}
NIVEL = {1: 'Técnico', 2: 'Técnico', 3: 'Técnico', 4: 'Avançado'}

HERO_TXT = {
 1: 'Abra um mod e veja o que tem dentro: três arquivos, uma função register e hooks com três parâmetros. Monte a pasta, carregue com --plugin-dir, instale por marketplace e termine com o seu primeiro mod funcionando, um comando que conta leituras.',
 2: 'Escolha o evento certo antes de escrever código. Entenda a cadeia ligada por next, guarde estado que sobrevive ao reload e faça trabalho fora do dispatch com relógio, arquivos e processos — sempre na forma tipada.',
 3: 'Desenhe no Claude Code: ui.render e as quatro superfícies, a faixa acima do prompt, status e avisos, painéis com botões, comandos de barra que respondem sem modelo e ferramentas que o modelo pode chamar.',
 4: 'Mods que mudam o fluxo: interceptar, negar, perguntar ao humano e trocar o modelo de um subagente. Depois, testar com claude plugin test, depurar com --debug, percorrer as pegadinhas e distribuir por marketplace.',
}

MOD_DESC = {
 '1-1': 'O que um mod é por dentro, onde ele roda e como ele se separa do hook clássico, da skill e do MCP.',
 '1-2': 'A árvore mínima: .claude-plugin/plugin.json, hooks/hooks.json e o módulo. Opções com userConfig e validação antes de carregar.',
 '1-3': 'Do --plugin-dir com hot-reload à instalação por marketplace, com escopo certo e desinstalação limpa.',
 '1-4': 'O starter-mod do kit da Prompt Advisers: o comando /readcount, o contador de leituras, validate, test e claude -p.',
 '2-1': 'Os eventos agrupados por noun, a volta completa de um turno, matchers, streams e os hooks clássicos dentro do mod.',
 '2-2': 'A cadeia de plugins: observar, reescrever com next, responder sem next, .catch e o orçamento de cada dispatch.',
 '2-3': 'Por que a variável de módulo some, como declarar o contrato de estado e quando usar $.state ou $.store.',
 '2-4': 'session.start, relógio do engine, arquivos, processos locais, acordar a sessão e decidir se o mod gasta modelo.',
 '3-1': 'O que o hook de ui.render recebe, a tabela de elementos de cada superfície e as regras de uma árvore que valida.',
 '3-2': 'A faixa AbovePrompt compartilhada, status, toast e log, com o exemplo oficial band.tsx dissecado.',
 '3-3': 'Painéis abertos por comando, dimensionados pelo bodyColumns, com botões, hotkeys, campos e modo diálogo.',
 '3-4': 'Comandos de barra que respondem sem modelo, ferramentas para o modelo, opções do /config e nomes sem colisão.',
 '4-1': 'Interceptar tool.call, negar com motivo, perguntar com $.ui.ask, trocar modelo de subagente e respeitar permissões.',
 '4-2': 'O engine de verdade sem modelo: mocks antes do $, comandos de ponta a ponta, relógio controlado e telas montadas.',
 '4-3': 'O log do --debug, módulos que não carregam, árvores recusadas, as 23 pegadinhas e o teste de fumaça.',
 '4-4': 'marketplace.json, repositório, versões, revisão antes de compartilhar, o projeto final e os próximos passos.',
}

# (emoji, dica curta, o que é, por que aprender, conceitos-chave) — na ordem dos tópicos da SPEC
T = {
'1-1': [
 ('🔌', 'register roda, hooks entram na cadeia', 'Quando o Claude Code carrega um mod, ele importa o módulo, chama register(on, options) e passa a chamar os hooks registrados a cada evento.', 'Entender esse momento explica por que um mod pode mudar o que o Claude vê, desenha e faz sem tocar no código do Claude Code.', 'mod, plugin, function hook, register, carregamento.'),
 ('🧩', 'quatro formas de estender', 'Mod roda dentro do processo, em um ambiente próprio; hook clássico é um comando de shell do settings.json; skill é instrução para o modelo; MCP é um servidor de ferramentas.', 'Escolher a forma errada custa caro: muita coisa que parece mod se resolve com uma skill, e vice-versa.', 'mod, hook clássico, skill, MCP, settings.json.'),
 ('✍️', 'on adiciona, options lê a config', 'A função exportada recebe on, para registrar hooks, e options, com os valores dos campos que o manifesto declara em userConfig.', 'É a única porta de entrada do mod: tudo o que ele faz começa nessa função.', 'register, on(evento, matcher?, hook), options, userConfig.'),
 ('🎛️', '$, e e next', 'Todo hook tem a forma ($, e, next): $ é a interface do engine, e é a entrada do evento e next(e) passa adiante na cadeia.', 'Esses três nomes aparecem em todo exemplo do curso; dominá-los é ler qualquer mod.', '$, e, next, cadeia, resultado do evento.'),
 ('📦', 'sem DOM, sem Node', 'O módulo é um ES module que roda num ambiente próprio, sem DOM e sem Node; tudo fora dele é alcançado pelo $.', 'Evita o erro mais comum de quem chega: importar fs do Node ou usar import() dinâmico, que não carregam.', 'ES module, ambiente isolado, $ como única saída, import estático.'),
 ('🗺️', 'quatro trilhas, dois kits', 'O caminho do curso, do primeiro mod ao marketplace, e os dois kits usados: o Claude Mods Starter Kit (Prompt Advisers, MIT) e o inema-mods.', 'Você sabe de onde vem cada exemplo e em que versão foi conferido: Claude Code 2.1.289.', 'starter kit, inema-mods, versão 2.1.289, acesso antecipado.'),
],
'1-2': [
 ('🌳', 'três arquivos', 'A pasta do mod com .claude-plugin/plugin.json, hooks/hooks.json e o módulo de hooks, mais tests/ quando houver teste.', 'Com a árvore certa o Claude Code acha o mod; com um nome trocado, nada carrega e nada avisa alto.', 'pasta do plugin, .claude-plugin, hooks/, tests/.'),
 ('🪪', 'nome, versão, descrição', 'O manifesto do plugin: name, version, description e, quando houver, userConfig e types.', 'O name vira o prefixo de comandos, ferramentas e estado; mudar depois quebra quem já usa.', 'plugin.json, name, version, manifesto.'),
 ('🧭', 'modules: um caminho', 'O hooks.json lista em modules o caminho do módulo, relativo ao próprio hooks.json, como {"modules":["./starter.mjs"]}.', 'É o elo entre o manifesto e o código; o validate mostra se ele aponta para o lugar certo.', 'hooks.json, modules, caminho relativo.'),
 ('📄', '.mjs, .ts ou .tsx', 'O módulo pode ser .ts, .tsx, .jsx, .js, .mjs, .cjs, .mts ou .cts, e é sempre ES module; outro sufixo não carrega.', 'O kit começa em .mjs sem compilação; a partir da trilha 2 o curso usa .tsx tipado.', 'extensão, ES module, TypeScript, JSX com h.'),
 ('⚙️', 'opções no /config', 'Campos declarados em userConfig no plugin.json viram linhas do menu de configuração e chegam ao mod em options.', 'Deixa o usuário ajustar o mod sem editar código, e cada mudança recarrega o módulo.', 'userConfig, options, pluginConfigs, /config.'),
 ('✅', 'claude plugin validate', 'O comando lê o manifesto e o código do módulo como o engine leria e lista os hooks, as chamadas e o que seria recusado.', 'Pega o erro antes de abrir uma sessão: é o primeiro passo de todo ciclo de mudança.', 'claude plugin validate, hooks listados, calls, Validation passed.'),
],
'1-3': [
 ('📂', 'só nesta sessão', 'A flag carrega o mod de uma pasta do disco só para aquela sessão; repita a flag para carregar vários.', 'É o jeito de desenvolver: nada fica instalado, e fechar a sessão desfaz tudo.', '--plugin-dir, sessão, pasta local.'),
 ('♻️', 'salvou, recarregou', 'Numa sessão interativa a pasta é vigiada: salvar um arquivo roda o register de novo num ambiente novo, e os timers antigos caem.', 'Você ajusta e vê na hora, sem reiniciar o Claude Code.', 'hot-reload, pasta vigiada, ambiente novo, timers.'),
 ('🖥️', 'quando não dá para passar flag', 'A variável de ambiente nomeia as mesmas pastas, com caminho absoluto, para sessões abertas pelo app desktop ou por um SDK.', 'No desktop não existe linha de comando para pôr a flag; a variável resolve.', 'CLAUDE_CODE_PLUGIN_DIRS, desktop, SDK, settings env.'),
 ('🏪', 'marketplace add + install', 'Registrar uma pasta ou repositório como marketplace e instalar o plugin dele com claude plugin install.', 'É como o mod chega às sessões de todo dia sem flag nenhuma.', 'marketplace, claude plugin marketplace add, claude plugin install.'),
 ('🎚️', 'user, project, local', 'O escopo diz onde a instalação vale: para você em todo projeto, para o projeto inteiro ou só na sua cópia local.', 'Instalar no escopo errado espalha o mod onde não devia ou esconde de quem precisa.', '--scope user, project, local.'),
 ('🧹', 'disable e uninstall', 'Desligar com claude plugin disable e remover a instalação sem deixar marketplace ou config esquecidos.', 'Mod que não sai direito vira suspeito de todo comportamento estranho depois.', 'claude plugin disable, remover a instalação, claude plugin list.'),
],
'1-4': [
 ('📋', 'templates/starter-mod', 'Copiar o modelo do kit da Prompt Advisers, que já traz manifesto, hooks.json, starter.mjs e um teste.', 'Começar de um mod que passa no validate e no test tira o atrito do primeiro dia.', 'starter-mod, cópia, read-counter-example.'),
 ('🔎', 'session.start, tool.call, command.run', 'O starter.mjs registra o comando em session.start, conta leituras bem-sucedidas em tool.call com matcher Read e responde em command.run.', 'São três dos eventos mais usados, num arquivo curto que você lê inteiro.', 'session.start, tool.call, matcher, command.run, $.command.register.'),
 ('🧪', 'validate e test', 'Rodar claude plugin validate e claude plugin test na pasta copiada e ler as duas saídas.', 'Você confirma que a cópia está íntegra antes de mudar uma linha.', 'Validation passed, 1 pass, 0 fail.'),
 ('⚡', 'claude -p sem modelo', 'Chamar /readcount com claude -p e --plugin-dir: o próprio mod responde, sem turno do modelo.', 'É o teste de fumaça mais barato que existe e vale para qualquer comando de mod.', 'claude -p, comando de barra, resposta sem modelo.'),
 ('🔧', 'outra ferramenta no matcher', 'Trocar o matcher do tool.call para contar outra ferramenta, como Edit ou Write, e rodar o teste de novo.', 'É a primeira mudança real: você vê o teste quebrar e sabe consertar.', 'matcher, tool, teste que falha, ajuste.'),
 ('🏷️', 'nome, comando, estado', 'Trocar o name do manifesto, o nome do comando e as mensagens para o mod virar seu.', 'Nome repetido colide com outros mods; seu nome é o prefixo de tudo o que o mod registra.', 'name, prefixo, colisão, README.'),
],
'2-1': [
 ('🗂️', 'tool, ui, session, turn...', 'Cada evento é noun.ação; agrupar por noun mostra o que o mod pode tocar: ferramentas, tela, sessão, turno, prompt, estado.', 'Ver o mapa inteiro evita escrever em ui.render o que deveria ser um tool.call.', 'evento, noun, tool, ui, session, turn, prompt.'),
 ('🔁', 'prompt.submit a turn.complete', 'A ordem em que os eventos disparam: prompt.submit, turn.start, turn.step, tool.call, session.append e turn.complete.', 'Saber onde você está na volta diz o que já aconteceu e o que ainda dá para mudar.', 'turno, prompt.submit, turn.start, turn.step, turn.complete.'),
 ('🎯', 'o segundo argumento do on', 'O matcher filtra quais eventos chegam ao hook, como { tool: \'Read\' } ou { command: \'readcount\' }.', 'Hook sem matcher roda em tudo e gasta orçamento à toa.', 'matcher, filtro, on(evento, matcher, hook).'),
 ('🌊', 'turn.step e process.spawn', 'Dois eventos são stream: o hook é um async generator, e yield* next(e) repassa os pedaços.', 'Hook comum nesses eventos não carrega; o erro só aparece no --debug.', 'stream, async function*, yield* next(e), for await.'),
 ('🪝', 'classic.PreToolUse e cia.', 'Os hooks clássicos do settings.json aparecem para o mod como classic.<Nome>, com a mesma entrada que o hook receberia.', 'Você aproveita o que já conhece de hooks clássicos sem sair do mod.', 'classic.PreToolUse, classic.Stop, hook clássico.'),
 ('📖', 'index.d.ts manda', 'Procurar qualquer evento, entrada e resultado no arquivo de tipos da sua instalação, .claude-plugin/types/claude-code/index.d.ts.', 'A API está em acesso antecipado e muda: o arquivo da sua versão é a autoridade, não a memória.', 'declaração de tipos, index.d.ts, grep, versão.'),
],
'2-2': [
 ('⛓️', 'todos os plugins + o engine', 'Os hooks de todos os plugins e o comportamento do próprio Claude Code formam uma cadeia ligada por next.', 'Seu mod não está sozinho: o que você devolve é o que os outros e o engine recebem.', 'cadeia, ordem, engine, plugins vizinhos.'),
 ('👀', 'return next(e)', 'O hook mais simples olha o evento, registra algo e devolve next(e) sem mudar nada.', 'É o padrão seguro: medir sem interferir.', 'observar, next(e), efeito colateral.'),
 ('✏️', 'next({ ...e, ... })', 'Chamar next com um evento alterado muda o que o resto da cadeia vê, dentro do que aquele evento permite.', 'É como um mod corrige um caminho, acrescenta contexto ou troca um modelo.', 'reescrever, spread, campos permitidos.'),
 ('🛑', 'quem não chama next decide', 'Um hook que retorna sem chamar next responde pelo evento, e a cadeia abaixo dele não roda.', 'É o poder de negar uma ferramenta ou responder um comando, e também o maior risco do mod.', 'responder, deny, curto-circuito.'),
 ('🪂', 'o registro tem .catch', 'O .catch encadeado no on responde no lugar do hook que falhou; sem ele, o hook é pulado e a cadeia segue.', 'Falha silenciosa num mod de segurança deixa passar o que devia barrar.', '.catch, hook pulado, padrão seguro.'),
 ('⏳', 'tempo do dispatch', 'Cada hook tem orçamento de tempo dentro do dispatch, e next.signal aborta quando o dispatch é abandonado.', 'Trabalho longo dentro do hook é cortado; o que precisa durar vai para fora.', 'dispatch, orçamento, next.signal, abort.'),
],
'2-3': [
 ('💨', 'reload limpa o módulo', 'Cada hot-reload roda o register num ambiente novo; a variável de módulo volta ao valor inicial.', 'O contador que zera do nada é o sintoma número um de estado no lugar errado.', 'variável de módulo, hot-reload, ambiente novo.'),
 ('📜', 'PluginState no contrato', 'Declarar o formato do estado do plugin em types/index.d.ts e apontar o arquivo em "types" no plugin.json.', 'Com o contrato, o editor e o tsc conferem cada leitura e escrita de estado.', 'types/index.d.ts, PluginState, "types", contrato.'),
 ('⚛️', 'a biblioteca de estado', 'atom, read e update vêm de import { ... } from "claude-code" e leem e gravam $.state com controle de versão.', 'update não perde clique: dois toques antes do redesenho contam os dois.', 'atom, read, update, $.state.get, $.state.set, ifVersion.'),
 ('🗄️', 'para além da sessão', 'O $.store guarda valores entre sessões com get, set, delete e keys.', '$.state vale para a sessão; o que precisa voltar amanhã vai para o store.', '$.store.get, $.store.set, persistência.'),
 ('🕰️', '$.clock, não Date', 'O engine dá o relógio do mod: now para a hora e timers que o teste pode controlar.', 'Usar o relógio do engine deixa o mod testável sem esperar tempo real.', '$.clock.now, relógio controlado, teste.'),
 ('🧭', 'módulo, state ou store', 'A regra de decisão: constante no módulo, estado da sessão em $.state, o que sobrevive entre sessões em $.store.', 'Cada dado no lugar certo evita perda no reload e lixo acumulado no disco.', 'decisão, escopo do dado, sessão, persistência.'),
],
'2-4': [
 ('🌅', 'pronto antes do 1º prompt', 'O session.start dispara uma vez, quando a sessão fica pronta, e é aguardado antes do primeiro prompt.', 'É o lugar de registrar comandos e ferramentas e de acender o que roda em segundo plano.', 'session.start, inicialização, $.command.register, $.tool.register.'),
 ('⏲️', 'timers do engine', 'clock.every repete e clock.after agenda uma vez; os timers duram até serem cancelados ou o módulo recarregar.', 'Trabalho periódico fora do dispatch não tem orçamento cortando no meio.', '$.clock.every, $.clock.after, cancelamento, reload.'),
 ('📁', 'ler, escrever, listar', 'O $.fs lê texto ou bytes, escreve, lista e dá stat de caminhos, com realPath para guardas robustas.', 'Sem Node, o $.fs é a única forma de o mod tocar arquivos.', '$.fs.read, $.fs.write, $.fs.stat, realPath.'),
 ('🛠️', 'comando por argv', 'O $.process.run roda um comando do sistema por argv, e $.process.spawn entrega a saída em pedaços.', 'git status, contagem de linhas, scripts locais: tudo por argv, sem shell montado em string.', '$.process.run, $.process.spawn, argv.'),
 ('🔔', 'trabalho que vira turno', 'O $.prompt.submit põe um prompt na fila que começa um turno quando a sessão fica ociosa.', 'Deixa um mod de segundo plano chamar o modelo na hora certa, sem atropelar o turno em curso.', '$.prompt.submit, fila, sessão ociosa.'),
 ('💸', 'model.complete custa', 'O $.model.complete e o $.model.fork chamam o modelo pelo cliente da sessão e consomem uso.', 'Mod que gasta modelo escondido surpreende quem usa; a regra é avisar e deixar desligar.', '$.model.complete, $.model.fork, uso, consentimento.'),
],
'3-1': [
 ('🎨', 'component, surface, props', 'O hook de ui.render recebe uma instância de componente: e.component, e.surface, e.requestId, e.props e e.viewport.', 'Com esses campos você decide se desenha, onde desenha e do tamanho certo.', 'ui.render, component, surface, requestId, viewport.'),
 ('🧱', 'elementos por superfície', 'O $.ui.resolve(e) devolve a tabela de construtores da superfície, que você desestrutura nas tags JSX.', 'O módulo não tem elementos globais; sem resolve não há Box nem Text.', '$.ui.resolve, Box, Text, JSX com h.'),
 ('📱', 'terminal, desktop, mobile, vscode', 'Cada superfície tem sua tabela: o terminal não tem Svg, mas tem Raster e Image; o mobile não tem Input nem Select.', 'Uma árvore com elemento que a superfície não tem não é desenhada.', 'superfície, Elements, diferenças, narrowing por e.surface.'),
 ('📐', 'render só lê', 'O hook de render lê o estado com $.state.get e nunca escreve; quem escreve é um handler ou outro evento.', 'Escrever ao desenhar é negado; ler assina a instância e o redesenho vem sozinho.', 'render puro, $.state.get, handler, redesenho.'),
 ('🚫', 'o engine desenha o dele', 'Uma árvore que não valida não é desenhada: o engine desenha a própria e registra o motivo no log.', 'Saber ler essa linha poupa horas de "por que não aparece nada".', 'validação, ui.render refused, debug log.'),
 ('🖼️', 'pixels no terminal', 'Raster desenha uma grade de células coloridas; Image mostra uma figura pelo protocolo gráfico do terminal, com alt nos outros.', 'Gráficos e mapas de calor sem um Box por célula.', 'Raster, Image, $.ui.blit, alt.'),
],
'3-2': [
 ('📟', 'AbovePrompt', 'O componente AbovePrompt é a faixa acima da caixa de prompt; o hook desenha nela com o tamanho de bodyColumns.', 'É o lugar de informação contínua: contadores, avisos, estado do mod.', 'AbovePrompt, faixa, bodyColumns.'),
 ('🤝', 'uma faixa para todos', 'A faixa é uma só e compartilhada: o exemplo oficial band.tsx mostra como desenhar nela sem apagar os vizinhos.', 'Um mod que toma a faixa inteira apaga os vizinhos.', 'compartilhar, next, composição.'),
 ('🔆', 'status sem abrir nada', 'O $.ui.status mostra um estado curto sem abrir painel e sem começar turno.', 'Informação discreta não precisa de tela própria.', '$.ui.status, linha de status, sem turno.'),
 ('📣', 'toast e log', 'O $.ui.toast dá um aviso passageiro e o $.ui.log escreve uma linha no registro, sem chamar o modelo.', 'Avisos certos no lugar certo, sem poluir a conversa.', '$.ui.toast, $.ui.log, aviso, registro.'),
 ('🔬', 'band.tsx linha a linha', 'Ler o exemplo oficial da faixa que vem com o Claude Code: estado tipado, resolve, árvore e botão.', 'É o modelo mais curto e correto de faixa que existe para copiar.', 'examples/band.tsx, band-state.d.ts, referência oficial.'),
 ('🧪', 'mount nas duas superfícies', 'Montar a faixa num teste para terminal e desktop, com o mesmo corpo num laço.', 'Prova que o mod não depende de uma superfície só.', 'claude plugin test, mount, terminal, desktop.'),
],
'3-3': [
 ('🪟', 'Pane', 'O $.ui.open abre um painel, o componente Pane, que o hook de ui.render desenha.', 'Painel é a tela própria do mod: listas, detalhes, formulários.', '$.ui.open, Pane, requestId.'),
 ('📏', 'largura que muda', 'O painel desenha no bodyColumns, mais estreito que a tela quando fica ao lado da conversa.', 'Árvore dimensionada pelo viewport quebra quando o painel está encaixado.', 'bodyColumns, viewport, isFullscreen.'),
 ('🔘', 'Button e hotkey', 'Botões com label, variant e hotkey de uma letra ou dígito, que funcionam quando o painel tem o teclado.', 'Atalho de uma tecla torna o painel usável sem mouse.', 'Button, hotkey, variant, foco.'),
 ('🖱️', 'ui.press, ui.input, ui.select', 'Os handlers ficam no plugin e disparam os eventos ui.press, ui.input e ui.select com a chave do elemento.', 'É assim que um clique vira ação e um texto digitado vira dado.', 'ui.press, ui.input, ui.select, key.'),
 ('💬', 'focus, closeOnEscape, holdToasts', 'Abrir o painel com focus, closeOnEscape e holdToasts faz ele se comportar como diálogo.', 'Diálogo prende a atenção do usuário; deixar holdToasts num painel fixo trava os avisos.', 'diálogo, focus, closeOnEscape, holdToasts.'),
 ('🚪', 'fechar e liberar', 'Fechar o painel por botão de dispensa ou por Esc e limpar o estado ligado a ele.', 'Painel que não fecha ou estado que sobra confunde a próxima abertura.', 'role dismiss, Esc, limpeza de estado.'),
],
'3-4': [
 ('⌨️', '$.command.register', 'Registrar um comando de barra com nome e descrição, normalmente no session.start.', 'Comando de mod roda na hora e não precisa de modelo.', '$.command.register, session.start, /comando.'),
 ('↩️', 'command.run com matcher', 'Responder o evento command.run, filtrado pelo nome do comando, com { text } e, se quiser, context.', 'text é a linha que aparece e o modelo também lê; context só o modelo lê.', 'command.run, { text }, context.'),
 ('🖨️', 'CommandOutput', 'Desenhar a saída do comando como árvore na conversa hookando o componente CommandOutput.', 'A resposta vira tabela ou card em vez de texto cru.', 'CommandOutput, ui.render, matcher por props.'),
 ('🧰', '$.tool.register', 'Declarar uma ferramenta com nome, descrição e schema, servida por um hook de tool.call; ela aparece como mcp__<plugin>__<nome>.', 'O modelo passa a usar uma capacidade que só o seu mod oferece.', '$.tool.register, tool.call, schema, mcp__plugin__nome.'),
 ('🔧', 'options na prática', 'Ler os valores que o usuário ajustou no /config pelo options do register, com padrões do manifesto.', 'Mudar uma opção recarrega o módulo; o mod nunca lê config velha.', 'userConfig, options, picker, /config.'),
 ('🏷️', 'prefixe tudo', 'Escolher nomes de comandos, ferramentas e chaves de estado que não batam com os de outros mods.', 'Dois mods com o mesmo comando brigam, e o usuário não sabe qual respondeu.', 'colisão, prefixo, nome do plugin.'),
],
'4-1': [
 ('🛑', 'tool.call antes de rodar', 'Hookar tool.call com matcher na ferramenta e olhar a entrada antes de a chamada acontecer.', 'É o ponto em que um mod pode impedir um estrago, não apenas registrá-lo.', 'tool.call, matcher, entrada da ferramenta.'),
 ('🚫', 'deny com mensagem', 'Responder sem next com um motivo que o modelo lê e entende como recusa.', 'Recusa sem motivo faz o modelo tentar de novo do mesmo jeito.', 'deny, motivo, resposta sem next.'),
 ('🙋', '$.ui.ask', 'Perguntar ao humano com opções antes de seguir, com a opção segura primeiro e um .catch para quando não há tela.', 'Sem tela (claude -p) ou sem resposta, o mod precisa de um padrão seguro e explícito.', '$.ui.ask, opção segura, .catch, afk.'),
 ('🔀', 'agent.spawn', 'Hookar agent.spawn para escolher o modelo de um subagente antes de ele rodar, como faz o roteador-subagente.', 'Tarefas simples em modelo menor economizam uso sem mudar o fluxo.', 'agent.spawn, subagente, modelo, roteador-subagente.'),
 ('🔐', 'não passar por cima', 'Um mod não deve afrouxar o que o usuário configurou: negar é ok, liberar o que estava bloqueado não.', 'Mod que fura permissão vira risco de segurança para quem instala.', 'permissões, classic.PreToolUse, menor privilégio.'),
 ('🧯', 'freio-de-mao', 'Ler a guarda do inema-mods que mede o estrago de um comando destrutivo e pergunta antes: prosseguir, lixeira, backup ou cancelar.', 'É um mod de controle real, curto, com teste e caminho para sessão sem tela.', 'freio-de-mao, $.process.run, $.ui.ask, $.ui.toast.'),
],
'4-2': [
 ('🧪', 'o engine sem modelo', 'O claude plugin test roda os *.test.ts com o engine de verdade; os hooks do teste ficam abaixo do plugin e fazem o papel do engine.', 'Testa o mod como ele roda numa sessão, sem gastar modelo.', 'claude plugin test, claude-code/testing, test, expect, mock.'),
 ('🧩', 'o mundo antes do $', 'Responder no teste cada noun que o mod usa (session.start, fs, store, ui...) antes de chamar o código.', 'Nada responde por baixo do plugin: faltou mock, o teste diz exatamente qual.', 'mocks, mundo.ts, noun faltando.'),
 ('🔁', 'comando de ponta a ponta', 'Disparar o comando no teste e conferir o texto devolvido e o estado gravado.', 'É a prova de que o caminho todo funciona, não só uma função.', 'command.run, asserção, estado.'),
 ('⏩', 'mock.clock', 'Avançar o relógio do teste para disparar timers sem esperar tempo real.', 'Mod com clock.every testado em milissegundos, sempre igual.', 'mock.clock, timers, determinismo.'),
 ('🖥️', 'mount em terminal e desktop', 'Montar o componente pelo ui do teste numa superfície nomeada e agir por chave com press, input e find.', 'O mesmo corpo de teste em duas superfícies prova que o mod não depende de uma.', 'mount, press, input, find, superfície.'),
 ('🩻', 'pass, fail e a mensagem', 'Ler a saída do teste: quantos pass, quantos fail e a linha que diz o que faltou.', 'Uma falha bem lida aponta a correção em uma linha.', 'pass, fail, mensagem de erro, timeout de 5 s.'),
],
'4-3': [
 ('🔦', 'claude --debug', 'Rodar com --debug para ter no log uma linha para cada hook pulado e cada resultado recusado.', 'Mod que parece não fazer nada quase sempre já disse por quê no log.', 'claude --debug, debug log.'),
 ('📃', 'plugin, evento, motivo', 'A linha do hook pulado traz o plugin, o evento e o nome do erro; o texto da primeira, encurtado, aparece na transcrição.', 'Ler essa linha é metade da depuração.', 'hook pulado, motivo, transcrição.'),
 ('🧱', 'import() e sufixo', 'Módulo com import() dinâmico, arquivo com sufixo fora da lista ou caminho errado no hooks.json não carregam.', 'São as causas mais comuns de "o mod sumiu".', 'import(), sufixo, hooks.json, validate.'),
 ('🪟', 'elemento que não existe', 'Achar no log a linha da árvore que não valida e trocar o elemento ou a prop que a superfície não aceita.', 'Sem isso o engine continua desenhando o dele e você não vê o seu.', 'ui.render refused, elemento, prop.'),
 ('📋', '23 pegadinhas', 'A lista do docs/COMO-FAZER-UM-MOD.md do inema-mods: funções com $ no topo, mocks, opção segura primeiro e as outras.', 'Cada pegadinha foi um erro real; ler antes poupa o mesmo erro.', 'COMO-FAZER-UM-MOD.md, pegadinhas, checar-mod.sh.'),
 ('💨', 'o comando responde?', 'Rodar o comando do mod com claude -p e --plugin-dir e conferir a resposta sem abrir sessão interativa.', 'Fumaça rápida antes de qualquer commit.', 'claude -p, --plugin-dir, teste de fumaça.'),
],
'4-4': [
 ('📇', 'a vitrine dos plugins', 'O .claude-plugin/marketplace.json lista os plugins com name e source, como no kit: ./plugins/<nome>.', 'É o que permite instalar o seu mod com um comando.', 'marketplace.json, plugins, source.'),
 ('🌐', 'dono/repo', 'Pôr o mod num repositório público e adicioná-lo como marketplace pelo caminho dono/repo.', 'Quem usa instala direto do repositório e recebe atualizações.', 'repositório, claude plugin marketplace add, dono/repo.'),
 ('🔼', 'version e update', 'Subir a version a cada mudança e saber que quem instalou recebe por claude plugin update e /reload-plugins.', 'Mudar nome de comando ou formato de estado sem aviso quebra quem já usa.', 'version, claude plugin update, /reload-plugins, compatibilidade.'),
 ('🔍', 'checklist final', 'validate, test com 0 fail, README, botão ou comando de desligar e nada que gaste modelo sem avisar.', 'Mod compartilhado roda na máquina de outra pessoa: o cuidado é seu.', 'revisão, README, desligar, consentimento.'),
 ('🏁', 'o mod do Rafa', 'Comando /x, faixa ou painel, estado em $.state, teste com mocks, validate OK e comando de desligar.', 'Junta tudo o que o curso ensinou num mod que você mesmo usa.', 'projeto final, claude plugin test, claude -p.'),
 ('🧭', 'cchooks, MakeClaudeX e mais', 'Os cursos de hooks clássicos, de plugins de produção e o curso-agent-runtime, além dos dois kits.', 'O curso termina; os mods continuam mudando a cada versão.', 'cchooks, MakeClaudeX, curso-agent-runtime, kits.'),
],
}

# --- SVGs do hero, um por trilha (ids com prefixo t<N>a-) ---
def svg_hero(n):
    _, c1, c2, cbg = CORES[n]
    p = f't{n}a-'
    defs = (f'<defs>\n            <pattern id="{p}grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" r="1.2" fill="{c1}" opacity="0.12"/></pattern>\n'
            f'            <filter id="{p}glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="1.8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
            f'            <marker id="{p}seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#38bdf8"/></marker>\n          </defs>')
    if n == 1:
        label = 'Uma pasta de mod aberta: plugin.json aponta para hooks.json, que aponta para o módulo. Do módulo sai a função register(on, options), e dela três hooks com a forma ($, e, next).'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11">
            <rect x="20" y="20" width="150" height="200" rx="10" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/>
            <text x="34" y="42" fill="{c1}" font-weight="600">📁 meu-mod/</text>
            <rect x="34" y="56" width="124" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="96" y="73" text-anchor="middle" fill="#bae6fd">plugin.json</text>
            <rect x="34" y="104" width="124" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="96" y="121" text-anchor="middle" fill="#bae6fd">hooks.json</text>
            <g filter="url(#{p}glow)"><rect x="34" y="152" width="124" height="26" rx="6" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g><text x="96" y="169" text-anchor="middle" fill="{c2}">starter.mjs</text>
            <line x1="96" y1="82" x2="96" y2="102" stroke="#38bdf8" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <line x1="96" y1="130" x2="96" y2="150" stroke="#38bdf8" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <text x="96" y="205" text-anchor="middle" fill="{c2}" font-size="10">três arquivos</text>
            <line class="wf-flow" x1="158" y1="165" x2="206" y2="120" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <rect x="208" y="98" width="156" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="2"/><text x="286" y="120" text-anchor="middle" fill="{c1}" font-weight="600">register(on, options)</text>
            <rect class="wf-a" x="200" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="227" y="47" text-anchor="middle" fill="#bae6fd">$</text>
            <rect class="wf-a" x="260" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="287" y="47" text-anchor="middle" fill="#bae6fd">e</text>
            <rect class="wf-a" x="320" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="347" y="47" text-anchor="middle" fill="#bae6fd">next</text>
            <line x1="286" y1="98" x2="286" y2="60" stroke="{c1}" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <rect x="208" y="160" width="156" height="60" rx="8" fill="none" stroke="{c1}" stroke-width="1.4" stroke-dasharray="4 3"/>
            <text x="286" y="182" text-anchor="middle" fill="{c2}">on('tool.call', …)</text>
            <text x="286" y="202" text-anchor="middle" fill="{c2}">on('command.run', …)</text>
            <line x1="286" y1="132" x2="286" y2="158" stroke="{c1}" stroke-width="1.6" marker-end="url(#{p}seta)"/>
          </g>'''
    elif n == 2:
        label = 'Um evento entra pela esquerda e atravessa a cadeia: plugin A observa e chama next, plugin B reescreve e chama next, e o engine responde no fim. Embaixo, o estado mora em $.state durante a sessão e em $.store entre sessões.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11" text-anchor="middle">
            <g filter="url(#{p}glow)"><circle cx="40" cy="70" r="24" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g><text x="40" y="74" fill="{c1}" font-weight="600">evento</text>
            <rect class="wf-a" x="88" y="50" width="76" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.6"/><text x="126" y="68" fill="#bae6fd">plugin A</text><text x="126" y="83" fill="#7dd3fc" font-size="9">observa</text>
            <rect class="wf-a" x="188" y="50" width="76" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.6"/><text x="226" y="68" fill="#bae6fd">plugin B</text><text x="226" y="83" fill="#7dd3fc" font-size="9">reescreve</text>
            <rect x="288" y="50" width="76" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="2"/><text x="326" y="68" fill="{c1}">engine</text><text x="326" y="83" fill="{c2}" font-size="9">responde</text>
            <line class="wf-flow" x1="64" y1="70" x2="86" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line class="wf-flow" x1="164" y1="70" x2="186" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line class="wf-flow" x1="264" y1="70" x2="286" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <text x="175" y="40" fill="{c2}" font-size="10">next(e) → next(e) → resultado</text>
            <rect x="40" y="130" width="140" height="44" rx="10" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="110" y="150" fill="{c1}" font-weight="600">$.state</text><text x="110" y="165" fill="{c2}" font-size="10">vale na sessão</text>
            <rect x="200" y="130" width="140" height="44" rx="10" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="270" y="150" fill="#bae6fd" font-weight="600">$.store</text><text x="270" y="165" fill="#7dd3fc" font-size="10">volta amanhã</text>
            <rect x="40" y="190" width="300" height="34" rx="8" fill="none" stroke="#f87171" stroke-width="1.4" stroke-dasharray="4 3"/><text x="190" y="211" fill="#fca5a5">variável de módulo: some no reload</text>
          </g>'''
    elif n == 3:
        label = 'A janela do Claude Code com três lugares onde um mod desenha: a conversa no alto, um painel encaixado à direita com botões e, logo acima da caixa de prompt, a faixa compartilhada. Ao lado, as quatro superfícies: terminal, desktop, mobile e vscode.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11">
            <rect x="16" y="16" width="260" height="208" rx="10" fill="#0b1220" stroke="{c1}" stroke-width="1.8"/>
            <rect x="28" y="30" width="150" height="104" rx="6" fill="#111827" stroke="#334155" stroke-width="1"/>
            <text x="40" y="50" fill="#94a3b8">conversa</text>
            <rect x="40" y="60" width="120" height="8" rx="3" fill="#334155"/><rect x="40" y="76" width="96" height="8" rx="3" fill="#334155"/><rect x="40" y="92" width="110" height="8" rx="3" fill="#334155"/>
            <g filter="url(#{p}glow)"><rect x="186" y="30" width="78" height="104" rx="6" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g>
            <text x="225" y="50" text-anchor="middle" fill="{c1}" font-weight="600">Pane</text>
            <rect x="196" y="64" width="58" height="18" rx="4" fill="none" stroke="{c2}" stroke-width="1.2"/><text x="225" y="77" text-anchor="middle" fill="{c2}" font-size="10">[ a ] abrir</text>
            <rect x="196" y="90" width="58" height="18" rx="4" fill="none" stroke="{c2}" stroke-width="1.2"/><text x="225" y="103" text-anchor="middle" fill="{c2}" font-size="10">[ x ] fechar</text>
            <rect class="wf-a" x="28" y="144" width="236" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="146" y="161" text-anchor="middle" fill="#bae6fd">AbovePrompt · faixa de todos</text>
            <rect x="28" y="180" width="236" height="30" rx="6" fill="#111827" stroke="#475569" stroke-width="1.2"/><text x="40" y="199" fill="#94a3b8">&gt; /meu-comando</text>
            <g text-anchor="middle" font-size="10">
              <rect x="294" y="30" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="51" fill="{c2}">terminal</text>
              <rect x="294" y="76" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="97" fill="{c2}">desktop</text>
              <rect x="294" y="122" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="143" fill="{c2}">mobile</text>
              <rect x="294" y="168" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="189" fill="{c2}">vscode</text>
            </g>
          </g>'''
    else:
        label = 'Uma chamada de ferramenta perigosa chega a um escudo, que pergunta ao humano antes de deixar passar. Abaixo, a esteira de entrega: validate, test com zero falhas e marketplace.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11" text-anchor="middle">
            <rect x="16" y="40" width="110" height="40" rx="8" fill="#2a0f0f" stroke="#f87171" stroke-width="1.8"/><text x="71" y="58" fill="#fca5a5">tool.call</text><text x="71" y="72" fill="#fca5a5" font-size="10">rm -rf build</text>
            <line class="wf-flow" x1="126" y1="60" x2="160" y2="60" stroke="#f87171" stroke-width="2" marker-end="url(#{p}seta)"/>
            <g filter="url(#{p}glow)"><path d="M190 22 L230 34 L230 66 Q230 92 190 104 Q150 92 150 66 L150 34 Z" fill="{cbg}" stroke="{c1}" stroke-width="2.2"/></g>
            <text x="190" y="62" fill="{c1}" font-weight="600">mod</text><text x="190" y="78" fill="{c2}" font-size="10">guarda</text>
            <line x1="230" y1="60" x2="262" y2="60" stroke="#38bdf8" stroke-width="2" marker-end="url(#{p}seta)"/>
            <rect class="wf-a" x="264" y="36" width="104" height="48" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="316" y="56" fill="#bae6fd">$.ui.ask </text><text x="316" y="72" fill="#7dd3fc" font-size="10">prosseguir?</text>
            <rect x="20" y="150" width="104" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="72" y="168" fill="{c2}">validate</text><text x="72" y="182" fill="{c2}" font-size="10">✔ passed</text>
            <rect x="140" y="150" width="104" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="192" y="168" fill="{c2}">test</text><text x="192" y="182" fill="{c2}" font-size="10">0 fail</text>
            <rect x="260" y="150" width="104" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="312" y="168" fill="#bae6fd">marketplace</text><text x="312" y="182" fill="#7dd3fc" font-size="10">install</text>
            <line x1="124" y1="170" x2="138" y2="170" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line x1="244" y1="170" x2="258" y2="170" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <text x="190" y="220" fill="{c2}" font-size="10">controlar → testar → distribuir</text>
          </g>'''
    return (f'<svg viewBox="0 0 380 240" class="w-full h-auto" role="img" aria-label="{html.escape(label)}">\n          {defs}\n'
            f'          <rect x="0" y="0" width="380" height="240" fill="url(#{p}grid)"/>\n          {corpo}\n        </svg>')

E = html.escape

def trilha(n):
    cor, c1, _, _ = CORES[n]
    emo, nome = NOMES[n]
    mids = [f'{n}-{k}' for k in range(1, 5)]
    out = [f'<!--TITLE: Trilha {n} · {nome} -->']
    out.append(f'''  <header class="bg-gradient-to-br from-{cor}-900/30 via-dark-800 to-dark-800 py-12 border-b border-dark-600" data-inema-track="{n}">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 lg:grid lg:grid-cols-[1fr_380px] lg:gap-10 lg:items-center">
      <div>
        <span class="inline-block px-3 py-1 bg-{cor}-500/20 text-{cor}-400 text-xs font-semibold rounded-full mb-4">TRILHA {n}</span>
        <h1 class="text-3xl sm:text-4xl font-bold mb-4">{emo} {nome}</h1>
        <p class="text-lg text-neutral-400 max-w-3xl">{E(HERO_TXT[n])}</p>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 max-w-2xl">
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">4</div><div class="text-xs text-neutral-400">Módulos</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">24</div><div class="text-xs text-neutral-400">Tópicos</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">~2h20</div><div class="text-xs text-neutral-400">Duração</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">{NIVEL[n]}</div><div class="text-xs text-neutral-400">Nível</div></div>
        </div>
        <div data-inema-meter="trilha:{n}" class="mt-6 max-w-2xl" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Progresso da trilha {n}">
          <div class="flex justify-between text-xs text-neutral-400 mb-1"><span data-inema-meter-frac>0 de 24</span><span data-inema-meter-pct>0%</span></div>
          <div class="inema-bar"><div class="inema-bar__fill" data-inema-meter-fill></div></div>
        </div>
      </div>
      <div class="mt-8 lg:mt-0 rounded-2xl border border-{cor}-500/30 bg-dark-900/40 p-3 overflow-hidden">
        {svg_hero(n)}
      </div>
    </div>
  </header>

  <main id="conteudo" class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-inema-track="{n}">

    <section class="mb-12">
      <h2 class="text-2xl font-bold mb-6">Mapa da trilha</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''        <a href="#modulo-{mid}" class="group bg-dark-800 rounded-xl border border-dark-600 hover:border-{cor}-500/30 p-5 transition-all">
          <div class="flex items-center justify-between mb-2"><span class="text-{cor}-400 font-bold text-sm">{num}</span><span class="text-xs text-neutral-500">{M['tipo']} · ~35 min</span></div>
          <h3 class="font-semibold mb-1 group-hover:text-{cor}-400 transition-colors">{M['emoji']} {E(M['titulo'])}</h3>
          <p class="text-xs text-neutral-400">{E(M['sub'])}</p>
        </a>''')
    out.append('''      </div>
    </section>

    <h2 class="text-2xl font-bold mb-6">Conteúdo detalhado</h2>
''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''    <!-- ===== MODULO {num} ===== -->
    <div id="modulo-{mid}" data-inema-module="{mid}" data-inema-track="{n}" class="bg-dark-800 rounded-xl border border-dark-600 mb-6">
      <div class="p-6 border-b border-dark-600">
        <div class="flex items-center justify-between mb-2"><span class="text-{cor}-400 font-bold">{num}</span><span class="text-xs text-neutral-500">{M['tipo']} · ~35 min</span></div>
        <h3 class="text-2xl font-bold mb-2">{M['emoji']} {E(M['titulo'])}</h3>
        <p class="text-neutral-400 text-sm">{E(MOD_DESC[mid])}</p>
        <div data-inema-meter="modulo:{mid}" class="mt-4" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Progresso do módulo {num}">
          <div class="flex justify-between text-xs text-neutral-400 mb-1"><span data-inema-meter-frac>0 de 6</span><span data-inema-meter-pct>0%</span></div>
          <div class="inema-bar"><div class="inema-bar__fill" data-inema-meter-fill></div></div>
        </div>
      </div>
      <div class="divide-y divide-dark-600">''')
        assert len(T[mid]) == 6, mid
        for i, (titulo, (em, dica, oque, porque, conc)) in enumerate(zip(M['topicos'], T[mid]), 1):
            tid = f't{i}-{mid}'
            out.append(f'''        <div class="topic-item">
          <button onclick="toggleTopic(this)" aria-expanded="false" aria-controls="{tid}" class="w-full px-6 py-4 flex items-center space-x-3 hover:bg-dark-700/50 transition-colors text-left">
            <span class="w-6 h-6 rounded-full bg-{cor}-500/20 text-{cor}-400 text-sm font-bold flex items-center justify-center flex-shrink-0">{i}</span>
            <span class="text-lg">{em}</span>
            <div><span class="font-medium">{titulo}</span><span class="text-neutral-500 text-sm ml-2">- {E(dica)}</span></div>
          </button>
          <div id="{tid}" class="topic-explanation px-6 pb-4">
            <div class="bg-dark-700/50 rounded-lg p-4 space-y-3 ml-9">
              <div><span class="text-{cor}-400 font-semibold">O que é:</span><p class="text-neutral-300 text-sm">{E(oque)}</p></div>
              <div><span class="text-{cor}-400 font-semibold">Por que aprender:</span><p class="text-neutral-300 text-sm">{E(porque)}</p></div>
              <div><span class="text-{cor}-400 font-semibold">Conceitos-chave:</span><p class="text-neutral-300 text-sm">{E(conc)}</p></div>
            </div>
          </div>
        </div>''')
        out.append(f'''      </div>
      <div class="p-4 bg-dark-700/30 flex justify-start space-x-3">
        <button onclick="openModal('modal-{mid}')" class="px-4 py-2 text-sm bg-dark-600 hover:bg-dark-500 rounded-lg transition-colors">Ver em Modal</button>
        <a href="modulo-{mid}.html" class="px-4 py-2 text-sm bg-{cor}-600 hover:bg-{cor}-500 text-white rounded-lg transition-colors">Ver Completo</a>
      </div>
    </div>
''')
    if n < 4:
        prox = f'<a href="../trilha{n+1}/index.html" class="flex-1 text-center px-6 py-3 bg-{cor}-600 text-white rounded-lg font-semibold hover:bg-{cor}-500 transition-colors">Próxima trilha: {NOMES[n+1][1]} →</a>'
    else:
        prox = f'<a href="modulo-4-4.html#topico-5" class="flex-1 text-center px-6 py-3 bg-{cor}-600 text-white rounded-lg font-semibold hover:bg-{cor}-500 transition-colors">Ir para o projeto final →</a>'
    out.append(f'''    <div class="flex flex-col sm:flex-row gap-4 mt-12">
      <a href="../../index.html" class="flex-1 text-center px-6 py-3 bg-dark-700 text-neutral-300 rounded-lg font-semibold hover:bg-dark-600 transition-colors">← Voltar ao início</a>
      {prox}
    </div>
  </main>

  <!-- MODAIS (iframe carrega a pagina do modulo) -->''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''  <div id="modal-{mid}" class="modal hidden fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/80" role="dialog" aria-modal="true" aria-labelledby="modal-{mid}-title" onclick="if(event.target === this) closeModal()">
    <div class="bg-dark-800 rounded-xl w-full max-w-6xl h-[95vh] flex flex-col border border-dark-600">
      <div class="p-4 border-b border-dark-600 flex justify-between items-center flex-shrink-0">
        <div class="flex items-center space-x-3"><span class="text-{cor}-400 font-bold">{num}</span><span id="modal-{mid}-title" class="font-semibold">{E(M['titulo'])}</span></div>
        <button onclick="closeModal()" class="text-neutral-400 hover:text-neutral-100 text-2xl leading-none" aria-label="Fechar">&times;</button>
      </div>
      <iframe src="modulo-{mid}.html" title="Módulo {num}" loading="lazy" class="flex-1 w-full rounded-b-xl"></iframe>
    </div>
  </div>''')
    return '\n'.join(out) + '\n'

for n in range(1, 5):
    p = RAIZ / 'context' / 'corpos' / f'trilha{n}.html'
    p.write_text(trilha(n), encoding='utf-8')
    print(p, p.read_text().count('\n'), 'linhas')
