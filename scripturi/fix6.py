import re, math
src = open('capitol2.html', encoding='utf-8').read()

def svg(pos, edges, w, h, r=14, colors=None):
    colors = colors or {}
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line class="edge-line" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"/>')
    for n, (x, y) in pos.items():
        st = f' style="fill:var({colors[n]})"' if n in colors else ''
        out.append(f'<circle class="node-circle" cx="{x:.0f}" cy="{y:.0f}" r="{r}"{st}/><text class="node-label" x="{x:.0f}" y="{y+4:.0f}" text-anchor="middle">{n}</text>')
    out.append('</svg>')
    return '\n'.join(out)

def circle(names, cx, cy, R):
    k = len(names)
    return {n: (cx + R*math.cos(-math.pi/2 + 2*math.pi*i/k), cy + R*math.sin(-math.pi/2 + 2*math.pi*i/k)) for i, n in enumerate(names)}

def card(svgtxt, caption):
    return f'''<div style="max-width:330px;">
        {svgtxt}
        <p style="text-align:center; font-family:'Inter',sans-serif; font-size:0.84rem;">{caption}</p>
      </div>'''

V = ['1','2','3','4','5','6']
line_pos = {v: (30 + 52*i, 50) for i, v in enumerate(V)}
chain = [('1','2'),('2','3'),('3','4'),('4','5'),('5','6')]
broken = [('1','2'),('2','3'),('3','4'),('5','6')]
star_pos = {'1': (110, 90)}; star_pos.update(circle(['2','3','4','5','6'], 110, 90, 65))
star = [('1', v) for v in ['2','3','4','5','6']]
k6_pos = circle(V, 110, 105, 80)
k6 = [(a, b) for i, a in enumerate(V) for b in V[i+1:]]
two_chains = [('1','2'),('2','3'),('4','5'),('5','6')]
k5_pos = circle(['1','2','3','4','5'], 100, 100, 75); k5_pos['6'] = (230, 100)
k5 = [(a, b) for i, a in enumerate(['1','2','3','4','5']) for b in ['1','2','3','4','5'][i+1:]]
two_col = {'1':'--node-2','2':'--node-2','3':'--node-2','4':'--node-3','5':'--node-3','6':'--node-3'}

sec = f'''<!-- SECTION 6: inegalitatea muchiilor -->
  <div class="section">
    <span class="tag">Teoremă</span>
    <h2><span class="num">6</span>Câte muchii poate avea un graf</h2>
    <p>Întrebarea e simplă: ai <b>n</b> vârfuri și vrei ca graful să aibă exact <b>k</b> bucăți (componente). Care e numărul <b>cel mai mic</b> și <b>cel mai mare</b> de muchii posibil? Teorema dă răspunsul:</p>
    <div class="def" style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:1.05rem;">
      n − k ≤ m ≤ C²<sub>n−k+1</sub>
    </div>
    <p>Luăm pe rând partea stângă (minimul) și partea dreaptă (maximul), cu <b>n = 6</b> vârfuri.</p>

    <h3 style="font-family:'Inter',sans-serif; font-size:1rem; margin:22px 0 6px;">Partea 1: minimul, pentru un graf conex (k = 1)</h3>
    <p>Vrei ca toate cele 6 vârfuri să fie legate într-o singură bucată, folosind cât mai puține muchii. Fiecare muchie nouă poate lipi <b>cel mult un vârf nou</b> la bucata ta. Primul vârf e deja acolo, deci mai ai de lipit 5 vârfuri, adică ai nevoie de <b>5 muchii</b>.</p>
    <div class="graphbox" style="gap:24px; flex-wrap:wrap;">
      {card(svg(line_pos, chain, 320, 100), '<b>5 muchii: conex</b><br>1–2–3–4–5–6, totul e o singură bucată.')}
      {card(svg(line_pos, broken, 320, 100, colors={'5':'--node-2','6':'--node-2'}), '<b>4 muchii: nu ajung</b><br>Oricum le-ai pune, rămâne ceva nelipit. Aici {{5,6}} e separat.')}
    </div>
    <div class="graphbox">
      {card(svg(star_pos, star, 220, 180), '<b>Tot 5 muchii, altă formă</b><br>Steaua: 1 legat de toți ceilalți. Și aici sunt exact 5 muchii.')}
    </div>
    <div class="def">
      <b>Minimul pentru k = 1:</b> m ≥ n − 1 = 6 − 1 = <b>5</b>. Un graf conex cu exact n − 1 muchii nu are cicluri (e un <i>arbore</i>, capitolul 4).
    </div>

    <h3 style="font-family:'Inter',sans-serif; font-size:1rem; margin:22px 0 6px;">Partea 2: maximul, pentru un graf conex (k = 1)</h3>
    <p>Acum pui <b>cât mai multe</b> muchii. Maximul e când fiecare vârf e legat de fiecare alt vârf (graful complet K₆). Numărul de muchii e numărul de <b>perechi</b> de vârfuri:</p>
    <div class="def" style="text-align:center;">
      C²<sub>p</sub> = p · (p − 1) / 2 &nbsp;&nbsp;→&nbsp;&nbsp; C²<sub>6</sub> = 6 · 5 / 2 = <b>15</b>
    </div>
    <p style="font-size:0.9rem;">De ce p·(p−1)/2: fiecare din cele 6 vârfuri se leagă de celelalte 5 (6·5 = 30), dar așa numeri fiecare muchie de 2 ori (o dată de la fiecare capăt), deci împarți la 2.</p>
    <div class="graphbox">
      {card(svg(k6_pos, k6, 220, 210), '<b>K₆: 15 muchii</b><br>Mai mult nu se poate: toate perechile sunt deja legate.')}
    </div>
    <div class="def">
      <b>Pentru n = 6, k = 1:</b> 5 ≤ m ≤ 15. Orice graf conex cu 6 vârfuri are între 5 și 15 muchii.
    </div>

    <h3 style="font-family:'Inter',sans-serif; font-size:1rem; margin:22px 0 6px;">Partea 3: același lucru cu 2 bucăți (k = 2)</h3>
    <p><b>Minim:</b> fiecare bucată are nevoie de (vârfurile ei − 1) muchii. Oricum ai împărți cele 6 vârfuri în 2 bucăți, totalul iese n − k = 6 − 2 = <b>4</b>.</p>
    <p><b>Maxim:</b> faci o bucată cât mai mare și complet legată, iar cealaltă bucată rămâne un singur vârf. Bucata mare are n − k + 1 = 6 − 2 + 1 = <b>5</b> vârfuri, deci C²<sub>5</sub> = 5·4/2 = <b>10</b> muchii. De aici vine n − k + 1 din formulă.</p>
    <div class="graphbox" style="gap:24px; flex-wrap:wrap;">
      {card(svg(line_pos, two_chains, 320, 100, colors=two_col), '<b>Minim, k = 2: 4 muchii</b><br>Bucata {{1,2,3}} cu 2 muchii + bucata {{4,5,6}} cu 2 muchii.')}
      {card(svg(k5_pos, k5, 260, 190, colors={'6':'--node-2'}), '<b>Maxim, k = 2: 10 muchii</b><br>K₅ pe {{1,2,3,4,5}} + vârful 6 singur.')}
    </div>

    <table class="metrictable">
      <tr><td><b>n = 6</b></td><td><b>minim (n − k)</b></td><td><b>maxim (C²<sub>n−k+1</sub>)</b></td></tr>
      <tr><td>k = 1</td><td>6 − 1 = 5</td><td>C²<sub>6</sub> = 15</td></tr>
      <tr><td>k = 2</td><td>6 − 2 = 4</td><td>C²<sub>5</sub> = 10</td></tr>
      <tr><td>k = 3</td><td>6 − 3 = 3</td><td>C²<sub>4</sub> = 6</td></tr>
    </table>

    <div class="quiz" data-qid="c6">
      <div class="q">Un graf conex (k=1) cu 6 vârfuri are minim câte muchii?</div>
      <div class="opts">
        <button class="opt" data-correct="false">6</button>
        <button class="opt" data-correct="true">5</button>
        <button class="opt" data-correct="false">15</button>
      </div>
      <div class="feedback"></div>
      <p style="font-size:0.8rem; color:var(--ink-dim); margin-top:8px;">Indiciu: uită-te la primul desen din secțiune. 15 e maximul, nu minimul.</p>
    </div>
  </div>

  '''
src, n = re.subn(r'<!-- SECTION 6.*?(?=<div class="footer-note">)', sec, src, count=1, flags=re.S)
open('capitol2.html','w',encoding='utf-8').write(src)
print(n, src.count('<div'), src.count('</div>'))
