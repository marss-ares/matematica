# Generează lectii/test-capitol4.html (test mai greu: arbori, APM, Kruskal, Prim)
import json
src = open('lectii/capitol4.html', encoding='utf-8').read()
head = src[:src.find('</style>')]
head = head.replace('<title>Arbori</title>', '<title>Test arbori</title>')
head = head.replace('Lecție interactivă pentru Capitolul 4: arbori, păduri, teorema de echivalențe, arbore parțial de cost minim, algoritmii Kruskal și Prim.',
  'Test mai greu pentru capitolul 4: arbori, păduri, arbore parțial de cost minim, Kruskal și Prim.')

# (tip, text, optiuni/raspuns, explicatie, [graf?])
Q = [
 ('fill','O pădure are 15 vârfuri și 4 componente conexe. Câte muchii are?','11','m = n − k = 15 − 4 = 11. Fiecare componentă e un arbore, deci „pierde” câte o muchie față de numărul ei de vârfuri.',0),
 ('mc','Un graf are 9 vârfuri, 8 muchii și are cel puțin un ciclu. Ce știm sigur despre el?',
   [('Nu e conex',1),('E arbore',0),('E conex, dar are ciclu',0)],
   'Dacă ar fi conex, cu m = n − 1 ar fi arbore și n-ar avea ciclu. Deci nu e conex.',0),
 ('fill','Un graf conex are 10 vârfuri și 14 muchii. Câte muchii trebuie scoase, minim, ca să obții un arbore parțial?','5','Un arbore parțial are n − 1 = 9 muchii. Ai 14, deci scoți 14 − 9 = 5 (câte una din fiecare ciclu rămas).',0),
 ('mc','Scoți o muchie dintr-un arbore cu 10 vârfuri. Ce obții?',
   [('O pădure cu 2 componente și 8 muchii',1),('Un arbore cu 9 muchii',0),('O pădure cu 2 componente și 9 muchii',0)],
   'Arborele avea 9 muchii. Scoți una: 8. Se rupe în 2 arbori (m = n − k = 10 − 2 = 8).',0),
 ('mc','Care afirmație este FALSĂ?',
   [('Un graf conex are exact un singur arbore parțial',1),('Orice arbore parțial al unui graf cu n vârfuri are n − 1 muchii',0),('Un arbore parțial conține toate vârfurile grafului',0)],
   'Un graf conex cu cicluri are de obicei mai mulți arbori parțiali (poți scoate muchii diferite din cicluri).',0),
 ('mc','Un graf conex are n vârfuri și exact n muchii. Câte cicluri are?',
   [('Exact unul',1),('Niciunul',0),('Cel puțin două',0)],
   'Arbore (n − 1 muchii) + încă o muchie = exact un ciclu.',0),
 ('fill','Care e costul arborelui parțial de cost minim al grafului de mai sus?','32','Kruskal: 1 + 2 + 3 + 4 + 5 + 6 + 11 = 32 (muchiile 6–7, 2–3, 4–5, 1–2, 5–6, 3–5, 6–8).',1),
 ('mc','Kruskal pe graful de mai sus. Care e a 4-a muchie LUATĂ în arbore?',
   [('1–2 (cost 4)',1),('3–4 (cost 7)',0),('2–4 (cost 8)',0)],
   'Ordinea luată: 6–7 (1), 2–3 (2), 4–5 (3), 1–2 (4).',1),
 ('mc','Kruskal pe același graf. Care e prima muchie SĂRITĂ (pentru că face ciclu)?',
   [('3–4 (cost 7)',1),('3–5 (cost 6)',0),('5–6 (cost 5)',0)],
   'Până la costul 6 s-au luat toate. La 3–4 (7): 3 și 4 sunt deja legate prin 3–5–4, deci ar face ciclu.',1),
 ('fill','Câte muchii sare Kruskal pe acest graf, în total, până se oprește?','4','Sărite: 3–4 (7), 2–4 (8), 1–3 (9), 4–6 (10). Apoi ia 6–8 (11) și are 7 = n − 1 muchii.',1),
 ('mc','Prim pornit din vârful 1. Care e a 3-a muchie adăugată?',
   [('3–5 (cost 6)',1),('1–3 (cost 9)',0),('2–4 (cost 8)',0)],
   'Pas 1: 1–2 (4). Pas 2: 2–3 (2). Pas 3: din {1,2,3} ies 1–3? nu (ambele capete în arbore), 2–4 (8), 3–4 (7), 3–5 (6) → se ia 3–5.',1),
 ('mc','Prim pornit din vârful 6. Care e prima muchie aleasă?',
   [('6–7 (cost 1)',1),('5–6 (cost 5)',0),('6–8 (cost 11)',0)],
   'Din {6} ies 4–6 (10), 5–6 (5), 6–7 (1), 6–8 (11). Cea mai ieftină: 6–7.',1),
 ('fill','Pornești Prim din vârful 8. Care e costul final al arborelui?','32','Alt start, același cost minim: 32. Se schimbă ordinea muchiilor, nu rezultatul.',1),
 ('mc','Vârful 8 are doar muchiile 6–8 (11) și 7–8 (13). Care intră în APM?',
   [('Doar 6–8',1),('Doar 7–8',0),('Amândouă',0)],
   '6–7 (cost 1) e deja în APM. Dacă ai pune ambele muchii ale lui 8, ar apărea ciclul 6–7–8. Se ia cea mai ieftină: 6–8.',1),
 ('mc','Muchia 3–4 (cost 7) intră în APM?',
   [('Nu: 3 și 4 se leagă mai ieftin prin 3–5–4 (6 + 3)',1),('Da, 7 e un cost mic',0),('Da, pentru că 3 și 4 nu sunt vecini în arbore',0)],
   'Ciclul 3–4–5–3 are muchiile 7, 6, 3. Cea mai scumpă din ciclu (7) nu e necesară.',1),
 ('fill','Costul muchiei 2–3 crește de la 2 la 20. Care e acum costul APM?','38','Noul APM nu mai folosește 2–3 (20). Vârful 2 se leagă acum prin 2–4 (8), iar 3 prin 3–5 (6). Muchiile: 6–7, 4–5, 1–2, 5–6, 3–5, 2–4, 6–8 = 1 + 3 + 4 + 5 + 6 + 8 + 11 = 38.',1),
]
data = json.dumps([{'t':q[0],'q':q[1],'a':q[2],'e':q[3],'g':q[4]} for q in Q], ensure_ascii=False)

extra_css = """
.wlabel{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;fill:var(--ink);}
.wbg{fill:var(--surface);stroke:var(--line);stroke-width:1;}
.gbadge{font-size:0.7rem;font-weight:700;border-radius:999px;padding:2px 8px;margin-left:6px;background:var(--accent);color:var(--accent-ink);}
"""
body = """</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Source+Serif+4:wght@400;500&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap">
<div class="wrap" style="max-width:720px">
  <h1>Test: arbori și APM (mai greu)</h1>
  <div class="subtitle">Capitolul 4 · 16 întrebări · grafurile cu costuri sunt desenate sub întrebare</div>
  <div class="identity-box"><span style="font-size:0.85rem;">Numele tău:</span><input type="text" id="studentName" placeholder="ex: Victor" autocomplete="off"></div>
  <div class="progressbar"><div class="pbar-track"><div class="pbar-fill" id="pf"></div></div><div class="pbar-label" id="pl">0 din 16</div></div>
  <div id="qs"></div>
  <div class="resultbox" id="res"><div class="score" id="sc"></div><div class="msg" id="ms"></div></div>
</div>
<script>
(function(){
  const NS='http://www.w3.org/2000/svg';
  function mk(t,a){ const e=document.createElementNS(NS,t); for(const k in a) e.setAttribute(k,a[k]); return e; }
  const G={W:640,H:490,pos:{1:[80,70],2:[230,70],3:[380,70],4:[230,200],5:[380,200],6:[300,330],7:[480,330],8:[300,440]},
    E:[[1,2,4],[1,3,9],[2,3,2],[2,4,8],[3,4,7],[3,5,6],[4,5,3],[4,6,10],[5,6,5],[5,7,12],[6,7,1],[6,8,11],[7,8,13]]};
  function graph(){
    const svg=mk('svg',{viewBox:`0 0 ${G.W} ${G.H}`,role:'img','aria-label':'graf cu costuri'});
    G.E.forEach(([a,b,w])=>{ const [x1,y1]=G.pos[a],[x2,y2]=G.pos[b];
      svg.appendChild(mk('line',{class:'edge-line',x1,y1,x2,y2,style:'stroke-width:3'})); });
    G.E.forEach(([a,b,w])=>{ const [x1,y1]=G.pos[a],[x2,y2]=G.pos[b],mx=(x1+x2)/2,my=(y1+y2)/2;
      svg.appendChild(mk('rect',{class:'wbg',x:mx-14,y:my-11,width:28,height:22,rx:6}));
      const t=mk('text',{class:'wlabel',x:mx,y:my+5,'text-anchor':'middle'}); t.textContent=w; svg.appendChild(t); });
    Object.entries(G.pos).forEach(([id,[x,y]])=>{ const g=mk('g',{}); g.appendChild(mk('circle',{class:'node-circle',cx:x,cy:y,r:19}));
      const t=mk('text',{class:'node-label',x,y:y+5,'text-anchor':'middle',style:'font-size:15px'}); t.textContent=id; g.appendChild(t); svg.appendChild(g); });
    const box=document.createElement('div'); box.className='graphbox'; box.appendChild(svg); return box;
  }
  const Q=__DATA__;
  const N=Q.length, results={}; let done=0, right=0;
  const root=document.getElementById('qs');
  function upd(){ document.getElementById('pf').style.width=(done/N*100)+'%'; document.getElementById('pl').textContent=done+' din '+N;
    if(done===N){ const r=document.getElementById('res'); r.classList.add('show');
      document.getElementById('sc').textContent=right+' / '+N;
      document.getElementById('ms').textContent = right>=14?'Excelent! Ești gata pentru capitolul 5.':right>=10?'Bine! Mai citește explicațiile la întrebările greșite.':'Mai repetă lecția (capitol4.html) și încearcă din nou.';
      r.scrollIntoView({behavior:'smooth',block:'center'}); } }
  let db=null;
  function slug(s){ return (s||'anonim').trim().toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'')||'anonim'; }
  async function save(){ const name=document.getElementById('studentName').value.trim(); try{ localStorage.setItem('graf_student_name', name); }catch(e){}
    if(!db) return; try{ await db.doc('lessons/' + slug(name) + '-test-capitol4').set({name:name||'(anonim)', results, updatedAt:new Date().toISOString()}); }catch(e){} }
  function finish(card,i,ok,fb,msg){ results['q'+(i+1)]=ok; done++; if(ok) right++;
    fb.innerHTML=(ok?'✓ Corect! ':'✗ ')+'<span style="color:var(--ink-dim)">'+Q[i].e+'</span>'; fb.style.color=ok?'var(--good)':'var(--bad)'; fb.classList.add('show'); save(); upd(); }
  Q.forEach((q,i)=>{
    const card=document.createElement('div'); card.className='qcard';
    card.innerHTML=`<div class="qnum">Întrebarea ${i+1} din ${N}${q.g?'<span class="gbadge">graf cu costuri</span>':''}</div><div class="qtext">${q.q}</div>`;
    if(q.g) card.appendChild(graph());
    const fb=document.createElement('div'); fb.className='feedback';
    if(q.t==='mc'){
      const o=document.createElement('div'); o.className='opts';
      const order=q.a.map((x,k)=>k); for(let j=order.length-1;j>0;j--){ const r=Math.floor(Math.random()*(j+1)); [order[j],order[r]]=[order[r],order[j]]; }
      order.forEach(k=>{ const b=document.createElement('button'); b.className='opt'; b.textContent=q.a[k][0]; o.appendChild(b);
        b.onclick=()=>{ if(b.disabled) return; const bs=[...o.children]; bs.forEach(x=>x.disabled=true); const ok=q.a[k][1]===1;
          b.classList.add(ok?'correct':'wrong'); if(!ok) bs[order.findIndex(kk=>q.a[kk][1]===1)].classList.add('correct'); finish(card,i,ok,fb); }; });
      card.appendChild(o);
    } else {
      const r=document.createElement('div'); r.className='fillrow'; r.innerHTML='<input class="fillbox" type="text" inputmode="numeric" autocomplete="off"><button class="check">Verifică</button>';
      const inp=r.querySelector('input'), btn=r.querySelector('button');
      btn.onclick=()=>{ if(btn.disabled||!inp.value.trim()) return; btn.disabled=true; inp.disabled=true; finish(card,i,inp.value.trim()===q.a,fb); };
      inp.addEventListener('keydown',e=>{ if(e.key==='Enter') btn.click(); });
      card.appendChild(r);
    }
    card.appendChild(fb); root.appendChild(card);
  });
  try{ const s=localStorage.getItem('graf_student_name'); if(s) document.getElementById('studentName').value=s; }catch(e){}
  document.getElementById('studentName').addEventListener('change', save);
  (async function(){ try{ if(window.claude && window.claude.use) db = await window.claude.use('db'); }catch(e){} })();
  upd();
})();
</script>
""".replace('__DATA__', data)
open('lectii/test-capitol4.html','w',encoding='utf-8').write(head + extra_css + body)
print(len(Q))
