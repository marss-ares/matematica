import math
src = open('test-recap12.html', encoding='utf-8').read()
PA = {'1':(60,70),'2':(60,190),'3':(160,130),'4':(260,130),'5':(350,130)}

def draw(edges, deg, extra='', w=410, h=240, ends=True):
    o = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    for a,b,*st in edges:
        (x1,y1),(x2,y2) = PA[a],PA[b]
        if st:
            cx, cy = 230, 0
            o.append(f'<path d="M {x1} {y1} Q {cx} {cy} {x2} {y2}" fill="none" style="stroke:var(--node-2);stroke-width:3"/>')
            for t in (0.09, 0.91):
                bx = (1-t)**2*x1 + 2*(1-t)*t*cx + t*t*x2; by = (1-t)**2*y1 + 2*(1-t)*t*cy + t*t*y2
                o.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="4" style="fill:var(--accent)"/>')
            continue
        o.append(f'<line class="edge-line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        if ends:
            L = math.hypot(x2-x1, y2-y1); ux, uy = (x2-x1)/L, (y2-y1)/L
            for (x,y,s) in ((x1,y1,1),(x2,y2,-1)):
                o.append(f'<circle cx="{x+s*ux*24:.0f}" cy="{y+s*uy*24:.0f}" r="4" style="fill:var(--accent)"/>')
    o.append(extra)
    for n,(x,y) in PA.items():
        o.append(f'<circle class="node-circle" cx="{x}" cy="{y}" r="15"/><text class="node-label" x="{x}" y="{y+4}" text-anchor="middle">{n}</text>')
        ly = y+34 if n == '2' else y-24
        o.append(f'<text x="{x}" y="{ly}" text-anchor="middle" style="font-family:Inter,sans-serif;font-size:13px;font-weight:700;fill:var(--accent)">d={deg[n]}</text>')
    o.append('</svg>')
    return '<div class="graphbox">' + '\n'.join(o) + '</div>'

EA = [('1','2'),('1','3'),('2','3'),('3','4'),('4','5')]
g1 = draw(EA, {'1':2,'2':2,'3':3,'4':2,'5':1})
g2 = draw(EA + [('5','1','new')], {'1':3,'2':2,'3':3,'4':2,'5':2})
half = ('<line x1="350" y1="130" x2="395" y2="200" style="stroke:var(--bad);stroke-width:3;stroke-dasharray:6 5"/>'
        '<text x="395" y="222" text-anchor="middle" style="font-family:Inter,sans-serif;font-size:22px;font-weight:700;fill:var(--bad)">✗</text>')
g3 = draw(EA, {'1':2,'2':2,'3':3,'4':2,'5':'2?'}, extra=half)

block = f'''
  <details class="qcard" style="font-family:'Inter',sans-serif;">
    <summary style="cursor:pointer; font-weight:600;">De ce suma gradelor nu poate fi 11 (deschide după ce răspunzi la întrebarea 2)</summary>
    <p style="margin-top:14px;">Fiecare muchie are <b>2 capete</b>, desenate mai jos ca punctele roșii mici. Gradul unui vârf = câte capete îl ating. Deci suma gradelor = numărul total de capete.</p>
    {g1}
    <p style="text-align:center;">5 muchii × 2 capete = <b>10 capete</b> = 2 + 2 + 3 + 2 + 1 = <b>10</b></p>

    <p><b>Încercare 1:</b> vreau suma 11, așa că îi dau vârfului 5 încă o muchie, spre 1. Dar muchia nouă (portocaliu) are și ea 2 capete: crește gradul lui 5 <b>și</b> gradul lui 1.</p>
    {g2}
    <p style="text-align:center;">Suma sare de la 10 direct la <b>12</b>, nu la 11. Orice muchie adaugi, suma crește cu 2.</p>

    <p><b>Încercare 2:</b> ca să ajung la 11, ar trebui să cresc doar gradul lui 5, cu o muchie care nu merge nicăieri (linia punctată).</p>
    {g3}
    <p style="text-align:center;">O muchie cu un singur capăt <b>nu există</b>. Pentru 11 ți-ar trebui 5 muchii și jumătate, adică 11 / 2 = 5,5.</p>

    <div class="resultbox show" style="text-align:left; border-width:1px; padding:16px 18px;">
      <b>Concluzie:</b> suma gradelor e mereu 2 · m, deci mereu <b>pară</b>. Dacă cineva îți dă grade care adunate fac un număr impar (11, 15, ...), un asemenea graf <b>nu poate exista</b>. Exact asta verifici la întrebările 3 și 4.
    </div>
  </details>
'''
marker = '<div class="qcard" data-qid="t3"'
assert src.count(marker) == 1
src = src.replace(marker, block + '\n  ' + marker, 1)
open('test-recap12.html','w',encoding='utf-8').write(src)
print('ok')
