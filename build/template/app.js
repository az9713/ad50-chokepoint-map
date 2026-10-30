const D = __DATA__;
const NS='http://www.w3.org/2000/svg';
const byId={}; D.choke.forEach(c=>{c.kind='choke';byId['k:'+c.id]=c}); D.comp.forEach(c=>{c.kind='comp';byId['c:'+c.id]=c}); D.companies.forEach(c=>{c.kind='co';byId['o:'+c.id]=c});
const score={}; D.scores.forEach((s,i)=>{s.rank=i+1;score[s.id]=s});
const rcol=r=>r>=5?'var(--r5)':r>=4?'var(--r4)':'var(--r3)';
const pcol=p=>p==='Systems'?'var(--sys)':p==='Factories'?'var(--fac)':'var(--inp)';
// edges
const E=[]; D.comp.forEach(m=>m.up.forEach(k=>E.push(['k:'+k,'c:'+m.id])));
D.companies.forEach(o=>o.uses.forEach(m=>E.push(['c:'+m,'o:'+o.id])));
// layout
const W=1000,TOP=40,rowH=21,gapH=18;
const order=['Systems','Factories','Inputs']; let y=TOP; const pos={};
order.forEach((p,pi)=>{ if(pi) y+=gapH; D.companies.filter(o=>o.pillar===p).sort((a,b)=>b.uses.length-a.uses.length||a.id.localeCompare(b.id)).forEach(o=>{pos['o:'+o.id]=y;y+=rowH}) });
const H=y+10;
const bary=(id,dir)=>{const ys=E.filter(e=>e[dir?0:1]===id).map(e=>pos[e[dir?1:0]]).filter(v=>v!=null);return ys.length?ys.reduce((a,b)=>a+b)/ys.length:H/2};
const spread=(ids)=>{const n=ids.length,step=(H-TOP-20)/n;ids.forEach((id,i)=>pos[id]=TOP+step*(i+.5))};
spread(D.comp.map(c=>'c:'+c.id).sort((a,b)=>bary(a,true)-bary(b,true)));
spread(D.choke.map(c=>'k:'+c.id).sort((a,b)=>bary(a,true)-bary(b,true)));
const X={k:[16,205],c:[400,610],o:[810,990]};
const svg=document.getElementById('map'); svg.setAttribute('viewBox',`0 0 ${W} ${H}`); svg.style.width='100%';svg.style.minWidth='820px';svg.style.height='auto';svg.style.display='block';
const el=(t,a,p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e};
[['Chokepoints',16],['Components',400],['The AD 50',810]].forEach(([t,x])=>{el('text',{x,y:20,class:'colhead'}).textContent=t});
const gE=el('g',{}),gN=el('g',{});
const edgeEls=E.map(([a,b])=>{const t=a[0],x1=X[t][1],x2=X[b[0]][0]-6,y1=pos[a],y2=pos[b],mx=(x1+x2)/2;
  const p=el('path',{d:`M${x1} ${y1} C${mx} ${y1} ${mx} ${y2} ${x2} ${y2}`,class:'edge'},gE);p.dataset.a=a;p.dataset.b=b;return p});
const nodeEls={};
function addNode(id,label,color,side,extra){const t=id[0],g=el('g',{class:'node',tabindex:0,role:'button','aria-label':label},gN);g.dataset.id=id;
  const [x0,x1]=X[t],yy=pos[id];
  el('rect',{class:'hit',x:x0-4,y:yy-10,width:x1-x0+8,height:20},g);
  if(t==='o'){el('circle',{cx:x0,cy:yy,r:4,fill:color},g);el('text',{x:x0+10,y:yy+4},g).textContent=label}
  else{el('rect',{x:x0,y:yy-7,width:6,height:14,rx:1,fill:color},g);const tx=el('text',{x:x0+12,y:yy+4},g);tx.textContent=label;
    if(extra){const s=el('tspan',{fill:'var(--muted)','font-family':'var(--mono)','font-size':'11'},tx);s.textContent='  '+extra}}
  nodeEls[id]=g; g.addEventListener('click',()=>select(id)); g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(id)}});
  g.addEventListener('mouseenter',()=>{if(!locked)highlight(id)}); g.addEventListener('mouseleave',()=>{if(!locked)highlight(null)})}
D.choke.forEach(c=>addNode('k:'+c.id,c.label,rcol(c.R),0,String(score[c.id].score100)));
D.comp.forEach(c=>addNode('c:'+c.id,c.label,c.sup.length?'var(--fix)':'var(--edge)',0,c.sup.length?'':'no AD 50 supplier'));
D.companies.forEach(o=>addNode('o:'+o.id,o.id,pcol(o.pillar)));
// graph walk
const down=id=>E.filter(e=>e[0]===id).map(e=>e[1]), up=id=>E.filter(e=>e[1]===id).map(e=>e[0]);
function related(id){const on=new Set([id]),fix=new Set();const t=id[0];
  if(t==='k'){down(id).forEach(c=>{on.add(c);down(c).forEach(o=>on.add(o))});(byId[id].fix||[]).forEach(f=>fix.add('o:'+f.co))}
  if(t==='c'){up(id).forEach(k=>on.add(k));down(id).forEach(o=>on.add(o));byId[id].sup.forEach(s=>fix.add('o:'+s.co))}
  if(t==='o'){up(id).forEach(c=>{on.add(c);up(c).forEach(k=>on.add(k))})}
  return {on,fix}}
let locked=null;
function highlight(id){svg.classList.toggle('dimmed',!!id);Object.values(nodeEls).forEach(g=>g.classList.remove('on','fixer','sel'));edgeEls.forEach(p=>p.classList.remove('on'));
  if(!id)return;const {on,fix}=related(id);on.forEach(n=>nodeEls[n].classList.add('on'));fix.forEach(n=>nodeEls[n].classList.add('fixer'));nodeEls[id].classList.add('sel');
  edgeEls.forEach(p=>{if(on.has(p.dataset.a)&&on.has(p.dataset.b))p.classList.add('on')})}
const P=document.getElementById('panel');
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const chip=(id,label,cls='')=>`<button class="chip ${cls}" data-go="${id}">${esc(label)}</button>`;
function panel(id){if(!id){P.innerHTML=`<div class="k">Start here</div><h3>Pick a node</h3><p class="muted">Click any chokepoint, component or company on the map. Tungsten, the top-ranked chokepoint, is selected by default.</p>`;return}
  const n=byId[id],t=id[0];let h='';
  if(t==='k'){const s=score[n.id],{on}=related(id);const cos=[...on].filter(x=>x[0]==='o').map(x=>byId[x]);const sys=cos.filter(o=>o.pillar==='Systems');
    h+=`<div class="k">Chokepoint · rank ${s.rank} of ${D.scores.length}</div><h3>${esc(n.label)}</h3>
    <div><span class="pill" style="background:${rcol(n.R)}">concentration ${n.R}/5</span> <span class="pill" style="background:var(--muted)">score ${s.score100}</span> <span class="pill" style="background:${n.conf==='verified'?'var(--fix)':'var(--muted)'}">${n.conf}</span></div>
    <p>${esc(n.fact)}</p>
    <div><div class="k">If cut off, ${sys.length} of 23 Systems companies are exposed (${cos.length} of 50 overall)</div><div class="chips">${cos.map(o=>chip('o:'+o.id,o.id)).join('')}</div></div>
    <div><div class="k">Through these components</div><div class="chips">${D.comp.filter(c=>c.up.includes(n.id)).map(c=>chip('c:'+c.id,c.label)).join('')}</div></div>
    <div><div class="k">AD 50 companies working on it</div>${n.fix.length?'<div class="chips">'+n.fix.map(f=>chip('o:'+f.co,f.co+(f.w<1?' (partial)':''),'fix')).join('')+'</div><ul class="src">'+n.fix.map(f=>`<li>${esc(f.co)}: ${esc(f.note)}</li>`).join('')+'</ul>':'<p class="muted">None. This is an open gap.</p>'}</div>
    ${n.src.length?`<div><div class="k">Sources</div><ul class="src">${n.src.map(([l,u])=>`<li><a href="${u}" target="_blank" rel="noopener">${esc(l)}</a></li>`).join('')}</ul></div>`:''}`}
  if(t==='c'){const users=down(id).map(x=>byId[x]);
    h+=`<div class="k">Component</div><h3>${esc(n.label)}</h3>
    <div><div class="k">Depends on</div><div class="chips">${n.up.map(k=>chip('k:'+k,byId['k:'+k].label)).join('')}</div></div>
    <div><div class="k">AD 50 suppliers</div>${n.sup.length?'<div class="chips">'+n.sup.map(s=>chip('o:'+s.co,s.co+(s.w<1?' (partial)':'')+(s.basis==='x'?' *':''),'fix')).join('')+'</div>':'<p class="muted">None on the list.</p>'}</div>
    <div><div class="k">Used by ${users.length} companies</div><div class="chips">${users.map(o=>chip('o:'+o.id,o.id)).join('')}</div></div>`}
  if(t==='o'){const {on}=related(id);const ks=[...on].filter(x=>x[0]==='k').map(x=>byId[x]).sort((a,b)=>score[a.id].rank-score[b.id].rank);
    const supplies=D.comp.filter(c=>c.sup.some(s=>s.co===n.id));const fixes=D.choke.filter(c=>c.fix.some(f=>f.co===n.id));
    h+=`<div class="k" style="color:${pcol(n.pillar)}">${n.pillar} · ${esc(n.loc)} · founded ${n.founded}</div><h3>${esc(n.name)}</h3><p>${esc(n.desc)}</p>
    <div><div class="k">Needs (inferred)</div><div class="chips">${n.uses.map(c=>chip('c:'+c,byId['c:'+c].label)).join('')}</div></div>
    <div><div class="k">Upstream chokepoints, worst first</div><div class="chips">${ks.map(k=>chip('k:'+k.id,k.label)).join('')}</div></div>
    ${supplies.length?`<div><div class="k">Supplies</div><div class="chips">${supplies.map(c=>chip('c:'+c.id,c.label,'fix')).join('')}</div></div>`:''}
    ${fixes.length?`<div><div class="k">Works on chokepoint</div><div class="chips">${fixes.map(c=>chip('k:'+c.id,c.label,'fix')).join('')}</div></div>`:''}`}
  P.innerHTML=h}
P.addEventListener('click',e=>{const b=e.target.closest('[data-go]');if(b)select(b.dataset.go)});
function select(id){locked=(locked===id)?null:id;highlight(locked);panel(locked)}
// ranking
const R=document.getElementById('rank');
R.innerHTML=D.scores.map(s=>{const c=byId['k:'+s.id];return `<button class="rrow" data-go="k:${s.id}"><span class="n">${s.rank}</span><span class="lbl">${esc(s.label)}${c.conf!=='verified'?' <span class="muted" style="font-weight:400">· qualitative</span>':''}</span><span class="bar"><div style="width:${s.score100}%;background:${rcol(s.R)}"></div></span><span class="v">${s.score100}</span>
  <span class="rmeta">concentration ${s.R}/5 · ${s.sys} Systems / ${s.all} total exposed · coverage ${s.cov}</span></button>`}).join('');
R.addEventListener('click',e=>{const b=e.target.closest('[data-go]');if(!b)return;locked=null;select(b.dataset.go);svg.closest('section').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})});
// gaps
document.getElementById('gaps').innerHTML=D.scores.filter(s=>s.cov===0).map(s=>{const c=byId['k:'+s.id];return `<div class="gap" style="border-color:${rcol(c.R)}"><b>${esc(c.label)}</b><p>${esc(c.fact)}</p><p class="muted">${s.sys} Systems companies exposed · rank ${s.rank}</p></div>`}).join('');
select('k:'+D.scores[0].id);
