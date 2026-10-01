# Generează lectii/capitol4.html (Arbori) refolosind CSS-ul din capitol3.html
src = open('lectii/capitol3.html', encoding='utf-8').read()
css_end = src.find('</style>')
head = src[:css_end].replace('<title>Mulțimi stabile</title>', '<title>Arbori</title>')
head = head.replace('Lecție interactivă pentru Capitolul 3: mulțimi stabile interior și exterior, nucleu, acoperiri, clici și cuplaje. Alegi vârfuri sau muchii și vezi pe loc ce proprietăți are mulțimea.',
  'Lecție interactivă pentru Capitolul 4: arbori, păduri, teorema de echivalențe, arbore parțial de cost minim, algoritmii Kruskal și Prim.')
extra_css = """
.wlabel{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;fill:var(--ink);}
.wbg{fill:var(--surface);stroke:var(--line);stroke-width:1;}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0;}
@media (max-width:640px){.cmp{grid-template-columns:1fr;}}
.card{font-family:'Inter',sans-serif;background:var(--surface-2);border-radius:10px;padding:12px 14px;font-size:0.92rem;line-height:1.55;}
.quiz{background:var(--surface-2);border-radius:12px;padding:14px 16px;margin:12px 0;font-family:'Inter',sans-serif;}
.quiz .q{font-family:'Source Serif 4',Georgia,serif;font-size:1rem;margin-bottom:10px;line-height:1.5;}
.gbadge,.nobadge{font-size:0.7rem;font-weight:700;border-radius:999px;padding:2px 8px;margin-right:6px;background:var(--accent);color:var(--accent-ink);}
.nobadge{background:var(--line);color:var(--ink-dim);}
.steplog{font-size:0.82rem;line-height:1.45;max-height:210px;overflow:auto;margin-top:8px;}
.steplog div{padding:3px 0;border-top:1px dashed var(--line);}
.steplog .ok{color:var(--good);} .steplog .no{color:var(--bad);}
.swrow{font-family:'Inter',sans-serif;font-size:0.9rem;margin:10px 0;display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
"""
body = open('scripturi/capitol4_body.html', encoding='utf-8').read()
open('lectii/capitol4.html', 'w', encoding='utf-8').write(head + extra_css + body)
print('ok')
