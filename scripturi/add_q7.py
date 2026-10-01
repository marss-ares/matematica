src = open('test-recap12.html', encoding='utf-8').read()
P = {'a':(60,50),'b':(200,50),'c':(200,170),'d':(60,170)}
E = [('a','b'),('b','c'),('c','d'),('d','a')]
COL = {0:'--accent',1:'--node-2',2:'--good'}

def g(dist, hl=()):
    o = ['<div class="graphbox"><svg viewBox="0 0 260 220" width="260" height="220">']
    hs = {frozenset(e) for e in hl}
    for a,b in E:
        (x1,y1),(x2,y2) = P[a],P[b]
        st = ' style="stroke:var(--accent);stroke-width:4"' if frozenset((a,b)) in hs else ''
        o.append(f'<line class="edge-line"{st} x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    for n,(x,y) in P.items():
        st = f' style="fill:var({COL[dist[n]]})"' if n in dist else ''
        o.append(f'<circle class="node-circle" cx="{x}" cy="{y}" r="17"{st}/><text class="node-label" x="{x}" y="{y+5}" text-anchor="middle">{n}</text>')
        if n in dist:
            ly = y-28 if y < 100 else y+38
            o.append(f'<text x="{x}" y="{ly}" text-anchor="middle" style="font-family:Inter,sans-serif;font-size:14px;font-weight:700;fill:var({COL[dist[n]]})">{dist[n]}</text>')
    o.append('</svg></div>')
    return '\n'.join(o)

def mat(hl_row=None, hl_cols=()):
    M = {'a':[0,1,0,1],'b':[1,0,1,0],'c':[0,1,0,1],'d':[1,0,1,0]}
    L = 'abcd'
    h = '<div class="graphbox"><table style="border-collapse:collapse;font-family:\'JetBrains Mono\',monospace;"><tr><td></td>' + ''.join(f'<td style="padding:4px 10px;font-weight:700;text-align:center;">{c}</td>' for c in L) + '</tr>'
    for r in L:
        h += f'<tr><td style="padding:4px 10px;font-weight:700;">{r}</td>'
        for j,v in enumerate(M[r]):
            on = (r == hl_row and L[j] in hl_cols)
            st = 'background:color-mix(in srgb, var(--node-2) 35%, transparent);font-weight:700;' if on else ''
            h += f'<td style="padding:4px 10px;text-align:center;{st}">{v}</td>'
        h += '</tr>'
    return h + '</table></div>'

def step(n, title, body):
    return f'''<div style="border-top:1px solid var(--line); padding-top:14px; margin-top:14px;">
      <div style="font-weight:700; margin-bottom:6px;"><span style="display:inline-flex;width:24px;height:24px;border-radius:999px;background:var(--accent);color:var(--accent-ink);align-items:center;justify-content:center;font-size:0.8rem;margin-right:8px;">{n}</span>{title}</div>
      {body}
    </div>'''

block = f'''
  <details class="qcard" style="font-family:'Inter',sans-serif;">
    <summary style="cursor:pointer; font-weight:600;">Cum găsești excentricitatea, pas cu pas (metoda valurilor)</summary>
    <p style="margin-top:14px;"><b>e(a)</b> = cel mai scurt drum de la <b>a</b> până la vârful <b>cel mai îndepărtat</b> de a. Ca să nu te încurci cu ocolurile, numerotezi vârfurile în „valuri”, ca cercurile pe apă când arunci o piatră.</p>

    {step(1, 'Citești muchiile din matrice și desenezi graful',
      mat() + '<p>Muchiile (1-urile de deasupra diagonalei): a–b, a–d, b–c, c–d. Iese un pătrat.</p>' + g({}))}

    {step(2, 'Valul 0: pui 0 pe vârful de pornire',
      g({'a':0}) + '<p>Pornești din <b>a</b>. Distanța de la a la a e 0.</p>')}

    {step(3, 'Valul 1: vecinii lui a primesc 1',
      mat('a', ('b','d')) + '<p>Pe rândul lui <b>a</b> din matrice, 1-urile sunt la <b>b</b> și <b>d</b>. Ei sunt la 1 pas.</p>' + g({'a':0,'b':1,'d':1}, [('a','b'),('a','d')]))}

    {step(4, 'Valul 2: vecinii NEnumerotați ai lui b și d primesc 2',
      '<p>Vecinii lui b: a (are deja număr, îl sari) și <b>c</b>. Vecinii lui d: a (sari) și c (tocmai l-ai numerotat). Deci doar <b>c</b> primește 2.</p>' + g({'a':0,'b':1,'d':1,'c':2}, [('a','b'),('b','c')]))}

    {step(5, 'Te oprești când toate vârfurile au număr. Cel mai mare număr = excentricitatea',
      '<p>Numerele: a = 0, b = 1, d = 1, c = 2. Cel mai mare e <b>2</b>, deci <b>e(a) = 2</b>, iar vârful cel mai îndepărtat de a e <b>c</b>.</p>')}

    <div class="resultbox show" style="text-align:left; border-width:1px; padding:16px 18px;">
      <b>Rețeta de ținut minte:</b><br>
      1. Pui <b>0</b> pe vârful tău.<br>
      2. Vecinii lui primesc <b>1</b>.<br>
      3. Vecinii fără număr ai celor cu 1 primesc <b>2</b>, apoi 3, și tot așa.<br>
      4. Un vârf care are deja număr nu-l mai schimbi. Primul număr primit e mereu cel mai scurt drum, așa că ocolurile nu mai contează.<br>
      5. <b>Ultimul număr pus = excentricitatea.</b>
    </div>
  </details>
'''
marker = '<div class="qcard" data-qid="t8"'
assert src.count(marker) == 1
src = src.replace(marker, block + '\n  ' + marker, 1)
open('test-recap12.html','w',encoding='utf-8').write(src)
print('ok')
