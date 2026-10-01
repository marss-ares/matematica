import re, itertools
from collections import deque

def adj(E):
    A = {}
    for a,b in E: A.setdefault(a,set()).add(b); A.setdefault(b,set()).add(a)
    return A
def bfs(A,s):
    d={s:0}; q=deque([s])
    while q:
        u=q.popleft()
        for w in sorted(A[u]):
            if w not in d: d[w]=d[u]+1; q.append(w)
    return d
def comps(V,E):
    A=adj(E); [A.setdefault(v,set()) for v in V]; seen=set(); k=0
    for v in V:
        if v not in seen: k+=1; seen|=set(bfs(A,v))
    return k
def bip(V,E):
    A=adj(E); col={}
    for s in V:
        if s in col: continue
        col[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for w in A.get(u,()):
                if w not in col: col[w]=1-col[u]; q.append(w)
                elif col[w]==col[u]: return None
    return col
def graphical(seq):
    s=sorted(seq,reverse=True); n=len(s)
    if sum(s)%2: return False
    for k in range(1,n+1):
        if sum(s[:k]) > k*(k-1)+sum(min(x,k) for x in s[k:]): return False
    return True

# ---- graph H ----
PH={1:(60,125),2:(170,55),3:(170,195),4:(300,55),5:(300,195),6:(430,55),7:(430,195),8:(560,195)}
EH=[(1,2),(1,3),(2,3),(2,4),(3,5),(4,5),(4,6),(5,7),(6,7),(7,8)]
VH=sorted(PH); AH=adj(EH)
deg={v:len(AH[v]) for v in VH}; m=len(EH)
ecc={v:max(bfs(AH,v).values()) for v in VH}
D=max(ecc.values()); r=min(ecc.values()); center=[v for v in VH if ecc[v]==r]
odd=[v for v in VH if deg[v]%2]
bridges=[e for e in EH if comps(VH,[f for f in EH if f!=e])>1]
d18=bfs(AH,1)[8]
assert bip(VH,EH) is None
assert sorted(bridges)==[(7,8)], bridges

def svgH():
    o=['<div class="graphbox"><svg viewBox="0 0 620 250" width="620" height="250">']
    for a,b in EH:
        (x1,y1),(x2,y2)=PH[a],PH[b]; o.append(f'<line class="edge-line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    for n,(x,y) in PH.items():
        o.append(f'<circle class="node-circle" cx="{x}" cy="{y}" r="16"/><text class="node-label" x="{x}" y="{y+4}" text-anchor="middle">{n}</text>')
    return '\n'.join(o)+'</svg></div>'
GH=svgH()

def seqcheck(seq):
    E=set(); 
    for i in range(len(seq)-1):
        a,b=seq[i],seq[i+1]
        if b not in AH[a]: return 'nu'
        e=frozenset((a,b))
        if e in E: return 'nu'
        E.add(e)
    closed = seq[0]==seq[-1]
    inner = seq[:-1] if closed else seq
    elem = len(set(inner))==len(inner)
    return ('ciclu ' if closed else 'lanț ')+('elementar' if elem else 'neelementar')
s1=(1,2,4,5,3,1); s2=(2,4,5,3,2,1); s3=(4,5,7,6,4,5)
assert seqcheck(s1)=='ciclu elementar' and seqcheck(s2)=='lanț neelementar' and seqcheck(s3)=='nu'

# ---- matrix M ----
VM=[1,2,3,4,5,6]; EM=[(1,2),(1,4),(3,2),(3,6),(5,4),(5,6),(1,6)]
AM=adj(EM); colM=bip(VM,EM); assert colM
X1=sorted(v for v in VM if colM[v]==colM[1]); X2=sorted(v for v in VM if colM[v]!=colM[1])
eM1=max(bfs(AM,1).values())
Mrows=[[1 if w in AM[v] else 0 for w in VM] for v in VM]
MAT=('<div class="graphbox"><table style="border-collapse:collapse;font-family:\'JetBrains Mono\',monospace;"><tr><td></td>'
     + ''.join(f'<td style="padding:4px 10px;font-weight:700;text-align:center;">{c}</td>' for c in VM) + '</tr>'
     + ''.join('<tr><td style="padding:4px 10px;font-weight:700;">'+str(VM[i])+'</td>'+''.join(f'<td style="padding:4px 10px;text-align:center;">{x}</td>' for x in Mrows[i])+'</tr>' for i in range(6))
     + '</table></div>')

seqA=(3,3,1,1); seqB=(4,4,3,3,2,2)
assert sum(seqA)%2==0 and not graphical(seqA)
okB=graphical(seqB)
C2=lambda p:p*(p-1)//2

qs=[
 ('fill','Graful H: cât este suma gradelor tuturor vârfurilor?', GH, str(2*m),
  f'H are {m} muchii, deci suma gradelor = 2 · {m} = {2*m}. Gradele: ' + ', '.join(f'd({v})={deg[v]}' for v in VH) + '.'),
 ('fill','Graful H: câte vârfuri au grad impar?', GH, str(len(odd)),
  f'Vârfurile cu grad impar: {", ".join(map(str,odd))}, adică {len(odd)}. E un număr par, cum spune regula.'),
 ('mc','Graful H: există un ciclu eulerian (traseu închis care trece exact o dată pe fiecare muchie)?', GH,
  [('Da',False),('Nu, pentru că există vârfuri cu grad impar',True),('Nu, pentru că graful nu e conex',False)],
  f'Pentru ciclu eulerian toate gradele trebuie să fie pare. Aici {", ".join(map(str,odd))} au grad impar, ca la podurile din Königsberg.'),
 ('mc','Graful H este bipartit?', GH, [('Da',False),('Nu',True)],
  'Nu. Are triunghiul 1-2-3, care e ciclu impar. Ciclul 1-2-4-5-3-1 are și el 5 muchii, tot impar.'),
 ('mc',f'Graful H: secvența {s1} este:', GH,
  [('ciclu elementar',True),('lanț elementar',False),('ciclu neelementar',False),('nu e lanț',False)],
  'Muchiile: (1,2), (2,4), (4,5), (5,3), (3,1). Toate există și sunt diferite. Pleacă din 1 și se întoarce în 1, iar pe drum nu se repetă niciun vârf, deci e ciclu elementar.'),
 ('fill',f'Graful H: care e lungimea ciclului {s1}?', GH, '5', 'Lungimea = numărul de muchii = 5.'),
 ('mc',f'Graful H: secvența {s2} este:', GH,
  [('lanț elementar',False),('lanț, dar nu elementar',True),('ciclu',False),('nu e lanț',False)],
  'Muchiile: (2,4), (4,5), (5,3), (3,2), (2,1). Toate diferite, deci e lanț. Vârful 2 apare de 2 ori, deci nu e elementar. Nu se termină unde începe, deci nu e ciclu.'),
 ('mc',f'Graful H: secvența {s3} este:', GH,
  [('lanț, dar nu elementar',False),('ciclu',False),('nu e lanț',True)],
  'Muchiile: (4,5), (5,7), (7,6), (6,4), (4,5). Muchia (4,5) apare de 2 ori, deci nu e lanț deloc.'),
 ('fill','Graful H: cât este distanța d(1, 8)?', GH, str(d18),
  f'Cel mai scurt drum are {d18} muchii, de exemplu 1→3→5→7→8.'),
 ('fill','Graful H: cât este excentricitatea e(1)?', GH, str(ecc[1]),
  f'Cel mai departe de 1 e vârful 8, la distanța {ecc[1]}.'),
 ('fill','Graful H: cât este diametrul D(H)?', GH, str(D),
  'Excentricitățile: ' + ', '.join(f'e({v})={ecc[v]}' for v in VH) + f'. Cea mai mare = {D}.'),
 ('fill','Graful H: cât este raza r(H)?', GH, str(r),
  f'Cea mai mică excentricitate = {r}.'),
 ('mc','Graful H: care este centrul?', GH,
  [('{'+', '.join(map(str,center))+'}',True),('{4, 5}',False),('{2, 3, 4, 5}',False),('{1, 8}',False)],
  f'Vârfurile cu excentricitatea minimă ({r}): {", ".join(map(str,center))}.'),
 ('mc','Graful H: care muchie, dacă o ștergi, rupe graful în 2 bucăți?', GH,
  [('(2, 4)',False),('(6, 7)',False),('(7, 8)',True),('(1, 2)',False)],
  'Doar (7,8) nu face parte din niciun ciclu. (2,4) e în ciclul 2-4-5-3-2, (6,7) în 4-6-7-5-4, iar (1,2) în triunghiul 1-2-3.'),
 ('fill','Câte muchii are graful dat prin matricea de mai jos?', MAT, str(len(EM)),
  f'Numeri 1-urile de deasupra diagonalei: {len(EM)}. Sau toate 1-urile / 2 = {2*len(EM)} / 2.'),
 ('mc','Graful din matrice este bipartit? Dacă da, care sunt grupele?', MAT,
  [('Da: {'+', '.join(map(str,X1))+'} și {'+', '.join(map(str,X2))+'}',True),('Da: {1, 2, 3} și {4, 5, 6}',False),('Nu, are ciclu impar',False)],
  'Pornești cu 1 într-o culoare. Vecinii lui (' + ', '.join(map(str,sorted(AM[1]))) + ') primesc cealaltă culoare, și tot așa. Nicio muchie nu leagă două vârfuri din aceeași grupă.'),
 ('fill','Graful din matrice: cât este e(1)?', MAT, str(eM1),
  'Valuri din 1: ' + ', '.join(f'{v}→{bfs(AM,1)[v]}' for v in VM) + f'. Cel mai mare = {eM1}.'),
 ('mc',f'Poate exista un graf cu gradele {", ".join(map(str,seqA))}?', '',
  [('Da',False),('Nu, suma gradelor e impară',False),('Nu, deși suma e pară',True)],
  'Suma e 8, pară, deci testul parității trece. Dar un vârf cu grad 3 într-un graf cu 4 vârfuri e legat de toți ceilalți 3. Cu două asemenea vârfuri, fiecare dintre celelalte are cel puțin gradul 2, nu 1. Deci e imposibil. Testul parității e necesar, dar nu ajunge.'),
 ('mc',f'Poate exista un graf cu gradele {", ".join(map(str,seqB))}?', '',
  [('Da',okB),('Nu',not okB)],
  'Suma e 18, pară, iar niciun grad nu depășește n − 1 = 5. Un exemplu există: îl poți construi pe tabla de grafuri.' if okB else 'Nu există.'),
 ('fill','Un graf are 9 vârfuri și 4 componente conexe. Care e numărul MAXIM de muchii?', '', str(C2(9-4+1)),
  f'Maxim = C²ₙ₋ₖ₊₁ = C²₆ = 6 · 5 / 2 = {C2(6)}. Faci o bucată completă cu 6 vârfuri și lași 3 vârfuri izolate.'),
 ('fill','Un graf are 6 vârfuri și 9 muchii. Câte muchii are complementarul lui?', '', str(C2(6)-9),
  f'Graful complet cu 6 vârfuri are C²₆ = {C2(6)} muchii. Complementarul are exact muchiile care lipsesc: {C2(6)} − 9 = {C2(6)-9}.'),
 ('fill','În graful bipartit complet K₃,₅: ce grad are un vârf din grupa cu 3 vârfuri?', '', '5',
  'E legat de toate cele 5 vârfuri din cealaltă grupă, deci gradul e 5. Graful are în total 3 · 5 = 15 muchii.'),
 ('mc','Un graf conex are 7 vârfuri și 6 muchii. Are cicluri?', '',
  [('Da, sigur',False),('Nu, sigur nu',True),('Depinde de desen',False)],
  'Un graf conex are minim n − 1 = 6 muchii. Cu exact minimul, nicio muchie nu e în plus, deci orice muchie scoți rupe graful și nu există cicluri. Un asemenea graf se numește arbore (capitolul 4).'),
]

src = open('mktest2.py', encoding='utf-8').read()
start = src.index("P = {"); end = src.index("cards = []")
src = src[:start] + "\n" + src[end:]
src = src.replace("for i,(kind,text,show,data,expl) in enumerate(qs, 1):\n    g = graph() if show else ''",
                  "for i,(kind,text,g,data,expl) in enumerate(qs, 1):")
src = src.replace('Test: Lanțuri și cicluri', 'Test: Recapitulare avansată')
src = src.replace('Test de verificare pentru Capitolul 2: lanțuri, cicluri, conexitate, distanțe.', 'Test lung și mai greu din Capitolele 1 și 2.')
src = src.replace('<h1>Test — Lanțuri și cicluri</h1>', '<h1>Test avansat — capitolele 1 și 2</h1>')
src = src.replace('Capitolul 2 · la întrebările cu desen se folosește același graf', 'Capitolele 1 și 2 · mai greu · graful H apare la întrebările 1–14, matricea la 15–17')
src = src.replace("-capitol2').set", "-avansat12').set").replace("test: 'capitol2'", "test: 'avansat12'")
src = src.replace("score >= 9 ?", "score >= 20 ?").replace("score >= 7 ?", "score >= 15 ?")
src = src.replace("Capitolul 2 e stăpânit. Putem trece la Capitolul 3.", "Ești pregătit pentru Capitolul 3.")
src = src.replace("open('test-capitol2.html'", "open('test-avansat12.html'")
src = src.replace('maxlength="3" inputmode="numeric"', 'maxlength="3" inputmode="numeric" autocomplete="off"')
g = {'qs': qs, '__name__': '__main__'}
exec(src, g)
print('questions', len(qs), 'center', center, 'ecc', ecc, 'D', D, 'r', r, 'd18', d18, 'X', X1, X2, 'eM1', eM1, 'okB', okB)
