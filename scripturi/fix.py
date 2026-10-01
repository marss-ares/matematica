import re
src = open('capitol2.html', encoding='utf-8').read()

def svg(pos, edges, hl_edges=(), hl_nodes=(), w=280, h=210, r=15):
    hl_e = {frozenset(e) for e in hl_edges}
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        cls = 'edge-line hl' if frozenset((a, b)) in hl_e else 'edge-line'
        out.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    for n, (x, y) in pos.items():
        cls = 'node-circle hl' if n in hl_nodes else 'node-circle'
        out.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}"/><text class="node-label" x="{x}" y="{y+4}" text-anchor="middle">{n}</text>')
    out.append('</svg>')
    return '\n'.join(out)

def path_edges(p):
    return [(p[i], p[i+1]) for i in range(len(p)-1)]

# --- lanț vs lanț elementar: same layout as the main section-1 graph ---
P1 = {'1':(40,110),'2':(110,50),'4':(180,110),'3':(110,170),'7':(250,50),'8':(250,170)}
E1 = [('1','2'),('2','4'),('4','3'),('4','7'),('4','8'),('7','8')]
ne = ['2','4','7','8','4','3']
el = ['1','2','4','8']
block1 = f'''<div class="graphbox" style="gap:30px; flex-wrap:wrap;">
      <div>
        {svg(P1, E1, path_edges(ne), set(ne), w=290, h=220)}
        <p style="text-align:center; font-family:'Inter',sans-serif; font-size:0.85rem;"><b>l = (2, 4, 7, 8, 4, 3)</b><br><span style="color:var(--bad);">Lanț, dar NU elementar</span><br>Muchii folosite: (2,4), (4,7), (7,8), (8,4), (4,3) — toate diferite.<br>Vârful 4 apare de 2 ori.</p>
      </div>
      <div>
        {svg(P1, E1, path_edges(el), set(el), w=290, h=220)}
        <p style="text-align:center; font-family:'Inter',sans-serif; font-size:0.85rem;"><b>l = (1, 2, 4, 8)</b><br><span style="color:var(--good);">Lanț elementar</span><br>Muchii folosite: (1,2), (2,4), (4,8).<br>Fiecare vârf apare o singură dată.</p>
      </div>
    </div>'''
src, n1 = re.subn(r'<div class="graphbox" style="gap:30px; flex-wrap:wrap;">\s*<div>\s*<svg viewBox="0 0 220 220".*?</div>\s*</div>\s*</div>', block1, src, count=1, flags=re.S)

# --- conex example: no crossing lines ---
PC = {'a':(30,30),'b':(110,30),'d':(110,90),'e':(30,90)}
EC = [('a','b'),('b','d'),('d','e'),('e','a')]
conex_svg = svg(PC, EC, w=140, h=120, r=13)
src, n2 = re.subn(r'<svg viewBox="0 0 140 120" width="140" height="120">.*?</svg>', conex_svg, src, count=1, flags=re.S)

# --- excentricity diagrams: same layout as main section-5 graph ---
P5 = {'1':(50,60),'2':(130,30),'3':(130,150),'5':(200,120),'6':(250,180)}
E5 = [('1','2'),('1','3'),('2','3'),('3','5'),('5','6')]
rows = [
  ('1', ['1','3','5','6'], 'd(1,2)=1, d(1,3)=1, d(1,5)=2, d(1,6)=3', 3),
  ('2', ['2','3','5','6'], 'd(2,1)=1, d(2,3)=1, d(2,5)=2, d(2,6)=3', 3),
  ('3', ['3','5','6'],     'd(3,1)=1, d(3,2)=1, d(3,5)=1, d(3,6)=2', 2),
  ('5', ['5','3','1'],     'd(5,1)=2, d(5,2)=2, d(5,3)=1, d(5,6)=1', 2),
  ('6', ['6','5','3','1'], 'd(6,1)=3, d(6,2)=3, d(6,3)=2, d(6,5)=1', 3),
]
cards = []
for v, p, dists, e in rows:
    arrow = '→'.join(p)
    cards.append(f'''      <div style="max-width:280px;">
        {svg(P5, E5, path_edges(p), set(p), w=280, h=210)}
        <p style="text-align:center; font-family:'Inter',sans-serif; font-size:0.82rem;"><b>e({v}) = {e}</b><br>{dists}<br>cea mai mare = {e}, drumul: {arrow}</p>
      </div>''')
block5 = '''<h3 style="font-family:'Inter',sans-serif; font-size:0.95rem; margin-top:22px; margin-bottom:10px;">Drumul exact folosit pentru fiecare e(x)</h3>
    <p style="font-size:0.88rem;">Pentru fiecare vârf: scrii distanța (cel mai scurt drum) până la fiecare alt vârf, apoi alegi cea mai mare. Cu roșu e drumul spre vârful cel mai îndepărtat.</p>
    <div class="graphbox" style="gap:20px; flex-wrap:wrap;">
''' + '\n'.join(cards) + '''
    </div>
    <p style="font-size:0.82rem; color:var(--ink-dim);">Graful: muchii (1,2), (1,3), (2,3), (3,5), (5,6) — un triunghi 1-2-3 cu o „coadă" 3-5-6.</p>'''
src, n3 = re.subn(r'<h3 style="font-family:\'Inter\',sans-serif; font-size:0.95rem; margin-top:22px; margin-bottom:10px;">Drumul exact.*?cu o "coadă" 3-5-6\.</p>', block5, src, count=1, flags=re.S)

open('capitol2.html','w',encoding='utf-8').write(src)
print(n1, n2, n3)
