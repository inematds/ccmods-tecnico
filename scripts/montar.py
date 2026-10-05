#!/usr/bin/env python3
"""Monta as páginas PT do curso a partir de context/partes (cabeça, nav, scripts) e context/corpos.

Uso: python3 scripts/montar.py            # monta tudo que tiver corpo
Não chama rede nem modelo. A landing (index.html da raiz) é escrita à mão e só recebe o manifesto.
"""
import json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PARTES = RAIZ / 'context' / 'partes'
CORPOS = RAIZ / 'context' / 'corpos'
NOME = 'Mods do Claude Code — técnico'

TRILHAS = [
    ('1', 'Anatomia', 'emerald', [
        ('1-1', 'O que é um mod por dentro'), ('1-2', 'Estrutura de arquivos e manifesto'),
        ('1-3', 'Carregar, recarregar e instalar'), ('1-4', 'Seu primeiro mod: comando e contador')]),
    ('2', 'Eventos e estado', 'blue', [
        ('2-1', 'O mapa de eventos'), ('2-2', 'A cadeia: next, reescrever e responder'),
        ('2-3', 'Estado que sobrevive'), ('2-4', 'Trabalho fora do dispatch')]),
    ('3', 'Telas e comandos', 'purple', [
        ('3-1', 'ui.render e as superfícies'), ('3-2', 'Faixa, status e avisos'),
        ('3-3', 'Painéis e botões'), ('3-4', 'Comandos, ferramentas e configuração')]),
    ('4', 'Controlar e distribuir', 'amber', [
        ('4-1', 'Mods que mudam o fluxo'), ('4-2', 'Testar com claude plugin test'),
        ('4-3', 'Depurar e as pegadinhas'), ('4-4', 'Distribuir e projeto final')]),
]

DESC = ('Curso técnico gratuito do INEMA.CLUB: escreva, teste e distribua mods do Claude Code — '
        'register, eventos, cadeia com next, estado, faixa, painéis, comandos, guardas e claude plugin test.')


BACKLINKS = ('<!-- inema-backlink:v1 -->\n      <p style="display:block;width:100%;text-align:center;font-size:.85rem;margin:.75rem 0 0;opacity:.85">'
             '<a href="https://www.inema.club/cursos/314-mods-do-claude-code-o-curso-tecnico/" style="color:inherit;text-decoration:underline">Ficha completa deste curso no INEMA.CLUB</a>'
             ' · <a href="https://www.inema.club/aprender-inteligencia-artificial/" style="color:inherit;text-decoration:underline">Guia: como aprender inteligência artificial</a></p>\n'
             '      <!-- /inema-backlink:v1 -->\n      ')

CONTINUAR = '''  <script>
    // "Continuar de onde parei": lê o último módulo visitado (gravado pelo learn.js)
    (function () {
      try {
        var meta = JSON.parse(localStorage.getItem('inema.ccmt.meta') || '{}');
        var href = meta && meta.lastModuleHref;
        var m = href && String(href).match(/curso\\/trilha\\d+\\/modulo-\\d+-\\d+\\.html/);
        if (!m) return;
        var anchor = meta.lastTopicAnchor && String(meta.lastTopicAnchor).split('#')[1];
        var a = document.getElementById('continuar');
        a.href = m[0] + (anchor ? '#' + anchor : '');
        a.classList.remove('hidden'); a.classList.add('inline-flex');
      } catch (e) {}
    })();
  </script>
'''


def manifesto():
    return json.dumps({'course': 'ccmt', 'tracks': [
        {'n': n, 'title': t, 'modules': [
            {'id': mid, 'title': mt, 'topics': 6, 'href': f'curso/trilha{n}/modulo-{mid}.html'} for mid, mt in mods]}
        for n, t, _, mods in TRILHAS]}, ensure_ascii=False, separators=(',', ':'))


def head(titulo, root):
    h = (PARTES / 'head.html').read_text(encoding='utf-8')
    return (h.replace('{{TITLE}}', titulo).replace('{{DESC}}', DESC)
             .replace('{{ROOT}}', root).replace('{{MANIFEST}}', manifesto()))


def nav(root, ativa):
    """root = prefixo até a raiz ('' na landing, '../../' nas páginas de curso). ativa = '1'..'4' ou None."""
    links = []
    for n, t, cor, _ in TRILHAS:
        if ativa is None:
            href = f'curso/trilha{n}/index.html'
        elif n == ativa:
            href = 'index.html'
        else:
            href = f'../trilha{n}/index.html'
        cls = (f'text-{cor}-400 bg-{cor}-500/10' if n == ativa
               else f'text-neutral-400 hover:text-{cor}-400 hover:bg-{cor}-500/10 transition-colors')
        links.append(f'''          <a href="{href}" class="px-1.5 sm:px-2.5 py-1.5 rounded-lg text-sm font-semibold {cls}">
            <span class="xl:hidden">T{n}</span><span class="hidden xl:inline">{t}</span>
          </a>''')
    return f'''<body class="bg-dark-900 text-neutral-100 min-h-screen">
  <a href="#conteudo" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[60] focus:px-4 focus:py-2 focus:bg-primary focus:text-black focus:rounded-lg">Pular para o conteúdo</a>

  <nav class="sticky top-0 z-50 bg-dark-900/95 backdrop-blur-sm border-b border-dark-600">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-14">
        <div class="flex items-center space-x-1.5 sm:space-x-3">
          <a href="{root}index.html" class="flex items-center space-x-2 text-yellow-400 hover:text-yellow-300">
            <span class="text-2xl">🧩</span>
            <span class="font-bold text-lg hidden lg:inline">Mods técnico</span>
          </a>
          <span class="text-neutral-600 hidden sm:inline">|</span>
          <a href="https://inema.club" target="_blank" class="text-sky-400 hover:text-sky-300 text-sm font-medium">INEMA.CLUB</a>
          <span class="text-neutral-600">-</span>
          <a href="https://inema.pro" target="_blank" class="text-amber-700 hover:text-amber-600 dark:text-slate-300 dark:hover:text-slate-200 text-sm font-medium">PRO</a>
        </div>
        <div class="flex items-center sm:space-x-1">
''' + '\n'.join(links) + '\n' + (PARTES / 'nav-direita.html').read_text(encoding='utf-8')


def cauda(root, checks='', landing=False):
    footer = f'''
  <footer class="border-t border-dark-600 py-8 mt-16">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-neutral-500 text-sm">
      <p>{NOME} · 2026 | <a href="https://inema.club" target="_blank" class="text-sky-400 hover:text-sky-300">INEMA.CLUB</a> - <a href="https://inema.pro" target="_blank" class="text-amber-700 hover:text-amber-600 dark:text-slate-300 dark:hover:text-slate-200">PRO</a></p>
      {BACKLINKS if landing else ''}<p class="mt-2 text-xs">Kits usados no curso: <a href="https://github.com/inematds/inema-mods" target="_blank" class="text-sky-400 hover:text-sky-300">inematds/inema-mods</a> · <a href="https://github.com/promptadvisers/claude-mods-starter-kit" target="_blank" class="text-sky-400 hover:text-sky-300">Claude Mods Starter Kit</a> (Prompt Advisers, MIT)</p>
    </div>
  </footer>

'''
    s = footer + (PARTES / 'scripts-nucleo.html').read_text(encoding='utf-8')
    if landing:
        s += CONTINUAR
    s += f'''  <script src="{root}assets/learn.js"></script>
  <script>
    if (window.INEMA && typeof window.INEMA.init === 'function') {{ window.INEMA.init(); }}
  </script>
'''
    if checks.strip():
        s += f'''  <script>
    window.addEventListener('DOMContentLoaded', function () {{
      if (window.INEMA && INEMA.registerCheck) {{
{checks.rstrip()}
      }}
    }});
  </script>
'''
    return s + '</body>\n</html>\n'


def ler_corpo(p):
    txt = p.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--TITLE:\s*(.*?)\s*-->\s*\n', txt)
    if not m:
        sys.exit(f'{p}: primeira linha precisa ser <!--TITLE: ... -->')
    txt = txt[m.end():]
    corpo, _, checks = txt.partition('<!--CHECKS-->')
    return m.group(1), corpo.rstrip() + '\n', checks


def montar():
    feitos = 0
    for n, t, _, mods in TRILHAS:
        pasta = RAIZ / 'curso' / f'trilha{n}'
        pasta.mkdir(parents=True, exist_ok=True)
        alvos = [(CORPOS / f'trilha{n}.html', pasta / 'index.html')]
        alvos += [(CORPOS / f'modulo-{mid}.html', pasta / f'modulo-{mid}.html') for mid, _ in mods]
        for corpo_p, saida in alvos:
            if not corpo_p.exists():
                continue
            titulo, corpo, checks = ler_corpo(corpo_p)
            html = head(f'{titulo} | {NOME}', '../../') + nav('../../', n) + '\n' + corpo + cauda('../../', checks)
            saida.write_text(html, encoding='utf-8')
            feitos += 1
    land = CORPOS / 'landing.html'
    if land.exists():
        titulo, corpo, _ = ler_corpo(land)
        html = head(titulo, '') + nav('', None) + '\n' + corpo + cauda('', '', landing=True)
        (RAIZ / 'index.html').write_text(html, encoding='utf-8')
        feitos += 1
    print(f'montadas: {feitos} páginas')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'partes-landing':
        # imprime cabeça e nav da landing para colar ao escrever a landing à mão
        print(head(f'{NOME} — o curso técnico | INEMA.CLUB', '') + nav('', None))
    else:
        montar()
