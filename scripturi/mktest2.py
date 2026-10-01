import re
base = open('test-capitol1.html', encoding='utf-8').read()
head = base[:base.index('<div class="wrap">')]
head = head.replace('<title>Test: Noțiuni de bază</title>', '<title>Test: Lanțuri și cicluri</title>')
head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Test de verificare pentru Capitolul 2: lanțuri, cicluri, conexitate, distanțe.">', head)
head = head.replace('</style>', '.fb-explain{color:var(--ink); margin-top:6px; line-height:1.5;}\n</style>')

P = {'1':(40,100),'2':(120,100),'3':(200,40),'4':(280,100),'5':(200,160),'6':(290,200)}
E = [('1','2'),('2','3'),('3','4'),('4','5'),('5','2'),('5','6')]
def graph():
    o = ['<div class="graphbox"><svg viewBox="0 0 330 230" width="330" height="230">']
    for a,b in E:
        (x1,y1),(x2,y2) = P[a],P[b]
        o.append(f'<line class="edge-line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    for n,(x,y) in P.items():
        o.append(f'<circle class="node-circle" cx="{x}" cy="{y}" r="15"/><text class="node-label" x="{x}" y="{y+4}" text-anchor="middle">{n}</text>')
    o.append('</svg></div>')
    return '\n'.join(o)

qs = [
 ('mc', 'Secvența (1, 2, 3, 4, 5, 2) este:', True,
  [('lanț elementar',False),('lanț, dar nu elementar',True),('nu e lanț',False)],
  'Muchiile: (1,2), (2,3), (3,4), (4,5), (5,2). Toate sunt diferite, deci e lanț. Vârful 2 apare de 2 ori, deci nu e elementar.'),
 ('mc', 'Secvența (2, 3, 4, 5, 2) este:', True,
  [('ciclu elementar',True),('lanț elementar',False),('nu e ciclu, pentru că 2 se repetă',False)],
  'Pleacă din 2 și se întoarce în 2, deci e ciclu. În afară de capete, vârfurile 3, 4, 5 apar o singură dată, deci e elementar.'),
 ('fill', 'Care e lungimea ciclului (2, 3, 4, 5, 2)?', True, '4',
  'Lungimea = numărul de muchii: (2,3), (3,4), (4,5), (5,2) = 4.'),
 ('fill', 'Cât este distanța d(1, 6)?', True, '3',
  'Cel mai scurt drum: 1→2→5→6 = 3 muchii. Drumul 1→2→3→4→5→6 are 5 muchii, dar e un ocol, nu contează.'),
 ('fill', 'Cât este excentricitatea e(2)?', True, '2',
  'd(2,1)=1, d(2,3)=1, d(2,5)=1, d(2,4)=2, d(2,6)=2. Cea mai mare = 2.'),
 ('mc', 'Care este centrul grafului?', True,
  [('{2, 5}',True),('{1, 6}',False),('{3, 4}',False)],
  'Excentricitățile: e(1)=3, e(2)=2, e(3)=3, e(4)=3, e(5)=2, e(6)=3. Cea mai mică e 2 (raza), o au vârfurile 2 și 5.'),
 ('mc', 'Dacă ștergi muchia (5, 6), graful:', True,
  [('rămâne conex',False),('devine neconex: vârful 6 rămâne separat',True)],
  'Muchia (5,6) nu face parte din niciun ciclu. 6 era legat doar de 5, deci după ștergere rămâne singur: 2 componente.'),
 ('mc', 'Dacă ștergi muchia (3, 4), graful:', True,
  [('rămâne conex',True),('devine neconex',False)],
  'Muchia (3,4) face parte din ciclul 2-3-4-5-2. Poți ocoli: din 3 în 4 mergi 3→2→5→4.'),
 ('fill', 'Un graf conex are 8 vârfuri. Care e numărul minim de muchii?', False, '7',
  'Minimul pentru un graf conex: n − 1 = 8 − 1 = 7.'),
 ('fill', 'Care e numărul maxim de muchii într-un graf cu 5 vârfuri?', False, '10',
  'Maximul e graful complet: C²₅ = 5 · 4 / 2 = 10.'),
]

cards = []
for i,(kind,text,show,data,expl) in enumerate(qs, 1):
    g = graph() if show else ''
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
  <h1>Test — Lanțuri și cicluri</h1>
  <div class="subtitle">{n} întrebări · Capitolul 2 · la întrebările cu desen se folosește același graf</div>

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
      await db.doc('tests/' + slugify(name) + '-capitol2').set({{
        name: name || '(anonim)', test: 'capitol2', results: results,
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
        score >= 9 ? 'Excelent! Capitolul 2 e stăpânit. Putem trece la Capitolul 3.' :
        score >= 7 ? 'Bine! Mai clarificăm întrebările greșite și mergem mai departe.' :
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
open('test-capitol2.html','w',encoding='utf-8').write(head + body)
print('ok')
