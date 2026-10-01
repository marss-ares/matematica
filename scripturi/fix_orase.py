import math
src = open('capitol2.html', encoding='utf-8').read()

def svg(pos, edges, w, h, r=16, colors=None, dashed=()):
    colors = colors or {}
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line class="edge-line" style="stroke-width:3" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"/>')
    for n, (x, y) in pos.items():
        st = f' style="fill:var({colors[n]})"' if n in colors else ''
        out.append(f'<circle class="node-circle" cx="{x:.0f}" cy="{y:.0f}" r="{r}"{st}/><text class="node-label" x="{x:.0f}" y="{y+4:.0f}" text-anchor="middle">{n}</text>')
    out.append('</svg>')
    return '\n'.join(out)

def card(s, cap):
    return f'''<div style="max-width:320px;">
        {s}
        <p style="text-align:center; font-family:'Inter',sans-serif; font-size:0.85rem;">{cap}</p>
      </div>'''

# "map" layout of 6 cities
M = {'A':(40,60),'B':(130,30),'C':(230,55),'D':(270,150),'E':(160,170),'F':(60,160)}
tree5 = [('A','B'),('B','C'),('C','D'),('B','E'),('E','F')]
four = [('A','B'),('B','C'),('C','D'),('B','E')]
names = list(M)
k6 = [(a,b) for i,a in enumerate(names) for b in names[i+1:]]
three = [('A','B'),('C','D'),('E','F')]
col3 = {'A':'--node-2','B':'--node-2','C':'--node-3','D':'--node-3'}

block = f'''
    <div class="def" style="border-left-color:var(--node-2);">
      <b>Pe înțelesul tuturor:</b> punctele sunt <b>orașe</b> (A, B, C, D, E, F), liniile sunt <b>drumuri</b>. Avem n = 6 orașe.
    </div>

    <h3 style="font-family:'Inter',sans-serif; font-size:1rem; margin:22px 0 6px;">Întrebarea 1 (minimul)</h3>
    <p><i>„Care e cel mai mic număr de drumuri pe care trebuie să le construiesc ca să pot ajunge din orice oraș în orice alt oraș?”</i></p>
    <div class="graphbox" style="gap:24px; flex-wrap:wrap;">
      {card(svg(M, tree5, 310, 200), '<b>5 drumuri: ajungi peste tot</b><br>De exemplu, din F în D: F→E→B→C→D.')}
      {card(svg(M, four, 310, 200, colors={'F':'--bad'}), '<b>4 drumuri: nu ajung</b><br>Orașul F a rămas fără drum. Oricum ai pune 4 drumuri, un oraș rămâne tăiat.')}
    </div>
    <div class="def">
      <b>Răspuns:</b> n − k = 6 − 1 = <b>5 drumuri</b>. Aici k = 1, pentru că vrei o singură „bucată” în care ajungi peste tot. E calculul celui care vrea să cheltuie cât mai puțin.
    </div>

    <h3 style="font-family:'Inter',sans-serif; font-size:1rem; margin:22px 0 6px;">Întrebarea 2 (maximul)</h3>
    <p><i>„Care e cel mai mare număr de drumuri pe care le pot construi, dacă fac cel mult un drum direct între fiecare 2 orașe?”</i></p>
    <div class="graphbox">
      {card(svg(M, k6, 310, 200), '<b>15 drumuri</b><br>Fiecare oraș are drum direct spre fiecare alt oraș. Nu mai încape niciun drum nou.')}
    </div>
    <div class="def">
      <b>Răspuns:</b> C²<sub>6</sub> = 6 · 5 / 2 = <b>15 drumuri</b>. Fiecare oraș are 5 drumuri (spre ceilalți 5), deci 6 · 5 = 30. Dar fiecare drum l-ai numărat de 2 ori (o dată de la fiecare capăt), așa că împarți la 2.
    </div>

    <h3 style="font-family:'Inter',sans-serif; font-size:1rem; margin:22px 0 6px;">Întrebarea 3 (verificarea)</h3>
    <p><i>„Cineva zice că a legat 6 orașe cu 3 drumuri și că poți ajunge peste tot. Minte?”</i></p>
    <div class="graphbox">
      {card(svg(M, three, 310, 200, colors=col3), '<b>3 drumuri: minte</b><br>Cu 3 drumuri obții cel puțin 3 bucăți separate. Aici: {A,B}, {C,D}, {E,F}. Din A nu ajungi niciodată în D.')}
    </div>
    <div class="def">
      <b>Verificare cu formula:</b> ar trebui 5 ≤ m ≤ 15.<br>
      • m = 3: 3 &lt; 5 → <b>imposibil</b>, prea puține drumuri ca să ajungi peste tot.<br>
      • m = 20: 20 &gt; 15 → <b>imposibil</b>, între 6 orașe nu încap 20 de drumuri directe diferite.<br>
      • m = 8: 5 ≤ 8 ≤ 15 → <b>posibil</b>.
    </div>

    <p style="margin-top:22px;">Mai jos e aceeași idee cu cifre în loc de litere, plus cazul cu 2 bucăți.</p>
'''
marker = 'cu <b>n = 6</b> vârfuri.</p>'
assert src.count(marker) == 1
src = src.replace(marker, marker + block, 1)
open('capitol2.html','w',encoding='utf-8').write(src)
print('ok', src.count('<div'), src.count('</div>'))
