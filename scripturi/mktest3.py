import re
base = open('test-capitol1.html', encoding='utf-8').read()
head = base[:base.index('<div class="wrap">')]
head = head.replace('<title>Test: Noțiuni de bază</title>', '<title>Test: Recapitulare 1–2</title>')
head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Test mixt din Capitolele 1 și 2.">', head)
head = head.replace('</style>', '.fb-explain{color:var(--ink); margin-top:6px; line-height:1.5;}\n</style>')


PA = {'1':(50,50),'2':(50,150),'3':(140,100),'4':(230,100),'5':(310,100)}
EA = [('1','2'),('1','3'),('2','3'),('3','4'),('4','5')]
def gsvg(P, E):
    o = ['<div class="graphbox"><svg viewBox="0 0 350 200" width="350" height="200">']
    for a,b in E:
        (x1,y1),(x2,y2) = P[a],P[b]
        o.append(f'<line class="edge-line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    for n,(x,y) in P.items():
        o.append(f'<circle class="node-circle" cx="{x}" cy="{y}" r="15"/><text class="node-label" x="{x}" y="{y+4}" text-anchor="middle">{n}</text>')
    o.append('</svg></div>')
    return '\n'.join(o)
GA = gsvg(PA, EA)
M = [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]]
L = 'abcd'
rows = ''.join('<tr><td style="padding:4px 10px;font-weight:700;">'+L[i]+'</td>' + ''.join(f'<td style="padding:4px 10px;text-align:center;">{v}</td>' for v in M[i]) + '</tr>' for i in range(4))
MAT = ('<div class="graphbox"><table style="border-collapse:collapse;font-family:\'JetBrains Mono\',monospace;">'
       '<tr><td></td>' + ''.join(f'<td style="padding:4px 10px;font-weight:700;text-align:center;">{c}</td>' for c in L) + '</tr>' + rows + '</table></div>')
def graph(): return GA
qs = [
 ('fill','Graful A: care e gradul vârfului 3, adică d(3)?', GA, '3',
  'Din 3 pleacă 3 muchii: spre 1, spre 2 și spre 4.'),
 ('fill','Graful A: cât este suma gradelor tuturor vârfurilor?', GA, '10',
  'Graful are 5 muchii, deci suma gradelor = 2 · 5 = 10. Verificare: 2 + 2 + 3 + 2 + 1 = 10.'),
 ('mc','Poate exista un graf cu gradele 2, 2, 3, 3, 3, 1?', '',
  [('Da, trece testul',True),('Nu, e imposibil',False)],
  'Gradele impare: 3, 3, 3, 1, adică 4 vârfuri. 4 e număr par, deci trece testul. Verificare: suma = 14, pară.'),
 ('mc','Poate exista un graf cu gradele 4, 3, 3, 2, 1, 1, 1?', '',
  [('Da, trece testul',False),('Nu, e imposibil',True)],
  'Gradele impare: 3, 3, 1, 1, 1, adică 5 vârfuri. 5 e impar, deci e imposibil. Verificare: suma = 15, impară, nu poate fi 2 · m.'),
 ('mc','Graful A este bipartit?', GA,
  [('Da',False),('Nu',True)],
  'Vârfurile 1, 2, 3 formează un triunghi. Un triunghi nu se poate colora cu 2 culori fără ca 2 vârfuri legate să aibă aceeași culoare.'),
 ('fill','Câte muchii are graful dat prin această matrice de adiacență?', MAT, '4',
  'Matricea are 8 de 1. Fiecare muchie apare de 2 ori (simetric), deci m = 8 / 2 = 4. Muchiile: a–b, a–d, b–c, c–d, adică un pătrat.'),
 ('fill','Pentru graful din aceeași matrice: cât este excentricitatea e(a)?', MAT, '2',
  'Graful e pătratul a–b–c–d–a. d(a,b)=1, d(a,d)=1, d(a,c)=2. Cea mai mare = 2.'),
 ('fill','Graful A: cât este distanța d(1, 5)?', GA, '3',
  'Cel mai scurt drum: 1→3→4→5, adică 3 muchii.'),
 ('fill','Graful A: câte componente conexe rămân dacă ștergi muchia (3, 4)?', GA, '2',
  'Muchia (3,4) nu e în niciun ciclu. Rămân bucățile {1, 2, 3} și {4, 5}.'),
 ('mc','Graful A: dacă ștergi muchia (1, 2), graful:', GA,
  [('rămâne conex',True),('devine neconex',False)],
  'Muchia (1,2) face parte din triunghiul 1-2-3. Poți ocoli: 1→3→2.'),
 ('mc','Graful A: care este centrul grafului?', GA,
  [('{3}',False),('{3, 4}',True),('{1, 2, 5}',False)],
  'e(1)=3, e(2)=3, e(3)=2, e(4)=2, e(5)=3. Cea mai mică excentricitate e 2 și o au vârfurile 3 și 4.'),
 ('fill','Câte muchii are graful bipartit complet K₃,₄?', '', '12',
  'm = |X₁| · |X₂| = 3 · 4 = 12.'),
]
cards = []
for i,(kind,text,g,data,expl) in enumerate(qs, 1):
    if kind == 'mc':
        opts = '\n'.join(f'<button class="opt" data-correct="{str(c).lower()}">{t}</button>' for t,c in data)
        body = f'<div class="opts">{opts}</div>'
    else:
        body = f'''<div class="fillrow"><span>Răspuns:</span><input class="fillbox" id="in-t{i}" data-ans="{data}" maxlength="3" inputmode="numeric"></div>
    <button class="check">Verifică</button>'''
    cards.append(f'''  <div class="qcard" data-qid="t{i}" data-explain="{expl}">
    <div class="qnum">Întrebarea {i}</div>
    <div class="qtext">{text}</div>
    {g}
    {body}
    <div class="feedback"></div>
  </div>''')

n = len(qs)
body = f'''<div class="wrap">
  <h1>Test — Recapitulare capitolele 1 și 2</h1>
  <div class="subtitle">{n} întrebări · Capitolele 1 și 2 · „graful A” e desenat la fiecare întrebare care îl folosește</div>

  <div class="progressbar">
    <div class="pbar-track"><div class="pbar-fill" id="pbarFill"></div></div>
    <div class="pbar-label" id="pbarLabel">0 / {n} răspunsuri date</div>
  </div>

  <div class="identity-box">
    <span style="font-size:0.85rem;">Numele tău:</span>
    <input type="text" id="studentName" placeholder="ex: Victor" autocomplete="off">
  </div>

{chr(10).join(cards)}

  <div class="resultbox" id="resultBox">
    <div class="score" id="scoreText">0 / {n}</div>
    <div class="msg" id="scoreMsg"></div>
  </div>
</div>

<script>
(function(){{
  let db = null;
  const results = {{}};
  const total = {n};
  function slugify(s){{ return (s||'anonim').trim().toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'') || 'anonim'; }}
  async function saveProgress(){{
    const name = document.getElementById('studentName').value.trim();
    try{{ localStorage.setItem('graf_student_name', name); }}catch(e){{}}
    if(!db) return;
    try{{
      await db.doc('tests/' + slugify(name) + '-recap12').set({{
        name: name || '(anonim)', test: 'recap12', results: results,
        score: Object.values(results).filter(r=>r===true).length, total: total,
        updatedAt: new Date().toISOString()
      }});
    }}catch(e){{}}
  }}
  function showFeedback(card, ok){{
    const fb = card.querySelector('.feedback');
    fb.innerHTML = '';
    const head = document.createElement('div');
    head.textContent = ok ? '✓ Corect!' : '✗ Nu chiar.';
    head.style.color = ok ? 'var(--good)' : 'var(--bad)';
    head.style.fontWeight = '600';
    const ex = document.createElement('div');
    ex.className = 'fb-explain';
    ex.textContent = card.dataset.explain;
    fb.appendChild(head); fb.appendChild(ex);
    fb.classList.add('show');
  }}
  function record(qid, ok){{
    if(results[qid] !== undefined) return;
    results[qid] = ok;
    const answered = Object.keys(results).length;
    document.getElementById('pbarFill').style.width = (answered/total*100)+'%';
    document.getElementById('pbarLabel').textContent = answered + ' / ' + total + ' răspunsuri date';
    saveProgress();
    if(answered === total){{
      const score = Object.values(results).filter(r=>r===true).length;
      document.getElementById('scoreText').textContent = score + ' / ' + total;
      document.getElementById('scoreMsg').textContent =
        score >= 11 ? 'Excelent! Capitolele 1 și 2 sunt stăpânite. Putem trece la Capitolul 3.' :
        score >= 9 ? 'Bine! Mai clarificăm întrebările greșite și mergem mai departe.' :
        'Hai să reluăm împreună întrebările greșite, pas cu pas.';
      const box = document.getElementById('resultBox');
      box.classList.add('show');
      box.scrollIntoView({{behavior:'smooth', block:'center'}});
    }}
  }}
  document.querySelectorAll('.qcard').forEach(function(card){{
    const qid = card.dataset.qid;
    const opts = card.querySelectorAll('.opt');
    opts.forEach(function(btn){{
      btn.addEventListener('click', function(){{
        if(results[qid] !== undefined) return;
        const ok = btn.dataset.correct === 'true';
        opts.forEach(o=>o.disabled=true);
        btn.classList.add(ok ? 'correct' : 'wrong');
        if(!ok) card.querySelector('.opt[data-correct="true"]').classList.add('correct');
        showFeedback(card, ok); record(qid, ok);
      }});
    }});
    const chk = card.querySelector('button.check');
    if(chk){{
      const box = card.querySelector('input.fillbox');
      chk.addEventListener('click', function(){{
        if(results[qid] !== undefined || box.value.trim()==='') return;
        const ok = box.value.trim() === box.dataset.ans;
        box.style.borderColor = ok ? 'var(--good)' : 'var(--bad)';
        box.disabled = true; chk.disabled = true;
        showFeedback(card, ok); record(qid, ok);
      }});
    }}
  }});
  try{{ const s = localStorage.getItem('graf_student_name'); if(s) document.getElementById('studentName').value = s; }}catch(e){{}}
  document.getElementById('studentName').addEventListener('change', saveProgress);
  (async function(){{ try{{ if(window.claude && window.claude.use) db = await window.claude.use('db'); }}catch(e){{ db = null; }} }})();
}})();
</script>
'''
open('test-recap12.html','w',encoding='utf-8').write(head + body)
print('ok')
