import json, csv
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
co = json.load(open(os.path.join(ROOT,'data','companies.json')))
short = {c['name']: c['name'].replace(' Industries','').replace(' Technologies','').replace(' Space','').replace(' Energy','').replace(' Automation','').replace(' Materials','').replace(' Systems','').replace(' Robotics','').replace(' Atomics','').replace(' Power','').replace(' Minerals','').replace(' Defense','').replace(' Autonomy','') for c in co}
short['Base Power']='Base Power'; short['Peak Energy']='Peak Energy'; short['Heron Power']='Heron Power'; short['General Matter']='General Matter'; short['Mind Robotics']='Mind Robotics'; short['Foundry Robotics']='Foundry'; short['Endurance Energy']='Endurance'; short['Ambrosia Energy']='Ambrosia'
short['Impulse Space']='Impulse'; short['K2 Space']='K2 Space'; short['Stoke Space']='Stoke'; short['Relativity Space']='Relativity'; short['Shield AI']='Shield AI'
ids = {c['name']: short[c['name']] for c in co}

CHOKE = {
 'ree':  dict(label='Rare earth magnets', R=5, conf='verified', fact='China made 94% of the world’s permanent magnets and did 91% of rare earth refining in 2024.', src=[('Oxford Economics, Aug 2026','https://www.oxfordeconomics.com/resource/policy-and-concentrated-supply-set-to-drive-rare-earth-magnet-prices/')]),
 'ga':   dict(label='Gallium', R=5, conf='verified', fact='China produced 99% of the world’s gallium in 2024. China banned exports to the US in Dec 2024, then paused the ban until Nov 27, 2026.', src=[('USGS Mineral Commodity Summaries 2025','https://pubs.usgs.gov/periodicals/mcs2025/mcs2025.pdf'),('Mining.com, Dec 2024','https://www.mining.com/china-bans-export-of-gallium-germanium-and-antimony-to-the-us/'),('Mining.com, Nov 2025','https://www.mining.com/china-lifts-export-ban-on-gallium-germanium-and-antimony-to-us/')]),
 'ge':   dict(label='Germanium', R=4, conf='verified', fact='China produced 59% of refined germanium in 2023 and put it under the same export ban as gallium.', src=[('Mining.com citing Project Blue','https://www.mining.com/china-bans-export-of-gallium-germanium-and-antimony-to-the-us/')]),
 'sb':   dict(label='Antimony', R=4, conf='verified', fact='China mined about 60% of the world’s antimony in 2024 (USGS estimate) and included it in the 2024 export ban. Antimony goes into primers and munitions.', src=[('USGS Mineral Commodity Summaries 2025','https://pubs.usgs.gov/periodicals/mcs2025/mcs2025.pdf')]),
 'w':    dict(label='Tungsten', R=5, conf='verified', fact='China mined about 83% of the world’s tungsten in 2024. Tungsten is used for penetrators, fragmentation and the carbide cutting tools every machine shop runs on.', src=[('USGS Mineral Commodity Summaries 2025','https://pubs.usgs.gov/periodicals/mcs2025/mcs2025.pdf')]),
 'ti':   dict(label='Titanium sponge', R=4, conf='verified', fact='The US produced no titanium sponge in 2025. The last domestic plant closed in 2024, and about 44,000 tonnes were imported.', src=[('USGS Mineral Commodity Summaries 2026, Titanium','https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-titanium.pdf')]),
 'cast': dict(label='Superalloy castings', R=3, conf='qualitative', fact='Turbine-grade nickel superalloy castings come from a small number of suppliers. Concentration is widely reported but not verified with a figure here.', src=[]),
 'batt': dict(label='Battery materials', R=5, conf='verified', fact='China produced 97% of the world’s battery anode materials in 2023.', src=[('Yicai Global, Jan 2024','https://yicaiglobal.com/news/china-produced-97-of-worlds-battery-anode-materials-last-year')]),
 'cu':   dict(label='Copper smelting', R=3, conf='verified', fact='The US had only 2 operating primary copper smelters in 2025.', src=[('USGS Mineral Commodity Summaries 2026, Copper','https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-copper.pdf')]),
 'ener': dict(label='Energetics', R=4, conf='verified', fact='Ammonium perchlorate, the oxidizer in solid rocket motors, has one qualified US producer (AMPAC, Utah). Solid rocket motor makers shrank from six to two between 1995 and 2017. The US has not made TNT since 1986; the Army awarded $435M for a Repkon USA plant in Kentucky.', src=[('TechCrunch, Aug 2025','https://techcrunch.com/2025/08/12/anduril-opens-solid-rocket-motor-factory-amidst-ongoing-chemical-chokepoint/'),('Breaking Defense, Jan 2026','https://breakingdefense.com/2026/01/with-the-boom-for-solid-rocket-motors-for-missiles-a-perilous-crunch-in-the-supply-chain/'),('AP via ABC17, Nov 2024','https://abc17news.com/news/2024/11/08/army-says-the-us-will-restart-domestic-tnt-production-at-plant-to-be-built-in-kentucky/')]),
 'haleu':dict(label='HALEU fuel', R=5, conf='verified', fact='The US government has long worried that Russia has a monopoly on HALEU. Centrus, the only US producer, is at demonstration scale: 20 kg delivered in Phase I, with a 900 kg target in Phase II.', src=[('NucNet, Jun 2025','https://www.nucnet.org/news/us-doe-extends-centrus-contract-to-produce-crucial-haleu-for-advanced-reactors-6-5-2025')]),
 'xfmr': dict(label='Power transformers', R=4, conf='verified', fact='Imports were an estimated 80% of US power transformer supply in 2025. Utilities wait 2 to 4 years, and up to 5.', src=[('Renewable Energy World citing Wood Mackenzie, Aug 2025','https://www.renewableenergyworld.com/power-grid/can-the-us-catch-up-to-transformer-demand/')]),
 'chip': dict(label='Leading-edge chips', R=4, conf='qualitative', fact='Leading-edge logic chips are made mostly in Taiwan. The exact share is not verified here.', src=[]),
 'pcb':  dict(label='Circuit board fabs', R=4, conf='verified', fact='The US share of global circuit board production fell from over 30% in 2000 to 4%. China makes roughly 50% to 56% (2020).', src=[('IPC, Jan 2022','https://www.electronics.org/news-release/flaws-us-approach-electronics-manufacturing-require-urgent-changes-or-nation-will-grow'),('ITIF, Jul 2022','https://itif.org/publications/2022/07/11/fact-of-the-week-us-share-of-the-pcb-market')]),
 'labor':dict(label='Skilled factory labor', R=3, conf='verified', fact='US manufacturing could need up to 3.8 million new workers from 2024 to 2033, and 1.9 million of those jobs could go unfilled.', src=[('Manufacturing Institute / Deloitte, Apr 2024','https://themanufacturinginstitute.org/manufacturers-need-as-many-as-3-8-million-new-employees-by-2033/')]),
 'poly': dict(label='Solar polysilicon', R=4, conf='qualitative', fact='Solar polysilicon and wafers are made overwhelmingly in China. The exact share is not verified here.', src=[]),
 'hyp':  dict(label='Hypersonic test range', R=3, conf='qualitative', fact='US hypersonic flight tests are scarce and expensive, which slows each design iteration. This is a qualitative judgment.', src=[]),
}
COMP = {
 'motor':   dict(label='Electric motors & actuators', up=['ree','cu']),
 'battery': dict(label='Battery cells & packs', up=['batt']),
 'rf':      dict(label='RF / radar electronics', up=['ga','chip']),
 'compute': dict(label='AI & edge compute', up=['chip']),
 'pcb':     dict(label='Circuit boards', up=['pcb','cu']),
 'harness': dict(label='Wire harnesses', up=['cu']),
 'machined':dict(label='Precision machined parts', up=['ti','w','labor']),
 'molded':  dict(label='Molded plastic parts', up=['labor']),
 'energetics':dict(label='Warheads & solid motors', up=['ener','sb','w']),
 'turbine': dict(label='Jet engines', up=['cast','ti']),
 'optics':  dict(label='IR & EO sensors', up=['ge']),
 'launch':  dict(label='Launch to orbit', up=['cast','labor']),
 'hyptest': dict(label='Hypersonic flight data', up=['hyp']),
 'metal':   dict(label='Metal stock & tooling', up=['ti','w','cast']),
 'power':   dict(label='Grid & site power', up=['xfmr','poly','batt']),
 'fuel':    dict(label='Reactor fuel', up=['haleu']),
 'work':    dict(label='Production engineering & labor', up=['labor']),
}
# suppliers: (company, weight, basis) basis s=stated in a16z profile, x=external reporting, i=inferred
SUP = {
 'motor':[('Westmag',1,'s')],
 'battery':[('Redwood',1,'s'),('Mariana',0.5,'s'),('Peak Energy',0.5,'s'),('Base Power',0.5,'s'),('Foundry',0.5,'s')],
 'pcb':[('Diode',0.5,'s'),('Podium',0.5,'s')],
 'harness':[('Senra',1,'s'),('Mariana',0.5,'s')],
 'machined':[('Hadrian',1,'s'),('Amca',1,'s'),('SendCutSend',1,'s')],
 'molded':[('Atomic',1,'s')],
 'energetics':[('Anduril',0.5,'x'),('Mach',0.5,'s')],
 'turbine':[('Hermeus',0.5,'s')],
 'launch':[('Stoke',1,'s'),('Relativity',1,'s'),('Impulse',0.5,'s')],
 'hyptest':[('Varda',1,'s')],
 'metal':[('Amca',0.5,'s')],
 'power':[('Heron Power',1,'s'),('Unlimited',0.5,'s'),('Ambrosia',0.5,'s'),('Base Power',0.5,'s'),('Peak Energy',0.5,'s'),('Radiant',0.5,'s'),('Valar',0.5,'s'),('Endurance',0.5,'s'),('Chariot',0.5,'s')],
 'fuel':[('General Matter',1,'s')],
 'work':[('Arda',0.5,'s'),('Nominal',0.5,'s'),('Prometheus',0.5,'s'),('Generalist',0.5,'s'),('Mind Robotics',0.5,'s'),('Foundry',0.5,'s'),('Hadrian',0.5,'s')],
 'rf':[],'compute':[('Specter',0.25,'s')],'optics':[],
}
# chokepoint-level fixers (who attacks the raw chokepoint directly)
FIX = {
 'ree':[('Westmag',0.5,'Says it is working to control upstream parts and materials for motors.')],
 'batt':[('Redwood',1,'Recovers battery materials from used cells and scrap.'),('Mariana',1,'Developing Lithium One in East Texas.'),('Peak Energy',0.5,'Sodium-ion chemistry sidesteps lithium.')],
 'cu':[('Mariana',1,'Owns and is automating the Copper One mine and refinery in Utah.')],
 'ener':[('Anduril',0.5,'Opened a solid rocket motor factory in 2025 (TechCrunch); not in the a16z profile.'),('Mach',0.5,'Develops propulsion in-house.')],
 'haleu':[('General Matter',1,'$900M DOE award to build HALEU enrichment at Paducah, KY.')],
 'xfmr':[('Heron Power',1,'Solid-state Heron Link replaces functions of transformers.'),('Unlimited',0.5,'Speeds design and construction of power infrastructure.')],
 'pcb':[('Diode',0.5,'Cuts supplier handoffs for boards; it does not fabricate them.')],
 'labor':[('Arda',0.5,'Turns designs into assembly plans.'),('Nominal',0.5,'Test data platform.'),('Prometheus',0.5,'AI for engineering design.'),('Generalist',0.5,'Robots learning from demonstration.'),('Mind Robotics',0.5,'Robots for jobs fixed equipment cannot do.'),('Foundry',0.5,'Flexible robotic assembly cells.'),('Hadrian',0.5,'Opus software trains technicians faster.')],
 'cast':[('Amca',0.5,'Re-engineers parts facing limited supply.'),('Hermeus',0.5,'Licensed to build F100 engines.')],
 'hyp':[('Varda',1,'Reentry capsules collect hypersonic flight data for the government.')],
}
USE = {
 'Anduril':['motor','battery','rf','compute','pcb','harness','machined','energetics','turbine','optics'],
 'Apex':['battery','rf','compute','pcb','harness','machined','launch','motor'],
 'Astranis':['battery','rf','pcb','harness','launch','motor'],
 'Castelion':['energetics','machined','harness','pcb','compute','hyptest'],
 'CHAOS':['rf','compute','pcb','harness','power'],
 'Covenant':['energetics','machined','harness','pcb','compute'],
 'CX2':['rf','compute','pcb','motor','battery'],
 'Forterra':['battery','compute','pcb','harness','rf','optics'],
 'Helsing':['motor','battery','compute','pcb','energetics','molded','optics'],
 'Hermeus':['turbine','machined','harness','pcb','hyptest'],
 'Impulse':['machined','launch','pcb','harness','battery'],
 'K2 Space':['battery','rf','pcb','harness','launch','motor'],
 'Mach':['energetics','machined','pcb','harness','compute'],
 'Neros':['motor','battery','pcb','molded','optics','energetics','compute','rf'],
 'Northwood':['rf','motor','pcb','machined'],
 'Perennial':['motor','battery','pcb','optics','energetics','compute'],
 'Relativity':['machined','harness','pcb','work'],
 'Saronic':['compute','pcb','harness','machined','battery','rf','optics'],
 'Shield AI':['compute','pcb','harness','optics','battery'],
 'Skydio':['motor','battery','compute','pcb','molded','optics'],
 'Specter':['compute','optics','pcb','battery'],
 'Stoke':['machined','harness','pcb','work'],
 'Ulysses':['motor','battery','pcb','compute','machined'],
 'Amca':['metal','work','power'],'Arda':['compute'],'Atomic':['metal','work','power'],'Diode':['pcb'],
 'Foundry':['motor','compute','power'],'Generalist':['compute','motor'],'Hadrian':['metal','work','power'],
 'Mind Robotics':['compute','motor'],'Nominal':['compute'],'Podium':['harness','power'],'Prometheus':['compute'],
 'SendCutSend':['metal','power'],'Senra':['work','power'],'Unlimited':['compute'],'Varda':['launch','machined'],'Westmag':['work','power'],
 'Ambrosia':['battery'],'Base Power':['battery','pcb'],'Chariot':['battery','pcb'],'Endurance':['machined'],
 'General Matter':['power','work'],'Heron Power':['pcb'],'Mariana':['power','compute'],'Peak Energy':['power'],
 'Radiant':['fuel','machined'],'Redwood':['power'],'Valar':['fuel','machined'],
}
names=set(ids.values())
for k in list(USE)+[s for v in SUP.values() for s,_,_ in v]+[s for v in FIX.values() for s,_,_ in v]:
    assert k in names, k
assert set(USE)==names, names-set(USE)
pillar={ids[c['name']]:c['pillar'] for c in co}
# scores
rows=[]
for k,c in CHOKE.items():
    comps=[m for m,d in COMP.items() if k in d['up']]
    users=sorted({u for u,cs in USE.items() if any(x in comps for x in cs)})
    sysu=[u for u in users if pillar[u]=='Systems']
    cov=sum(w for _,w,_ in FIX.get(k,[]))
    score=c['R']*len(sysu+[u for u in users if pillar[u]!='Systems'])/(1+cov)
    rows.append(dict(id=k,label=c['label'],R=c['R'],sys=len(sysu),all=len(users),cov=cov,score=score))
mx=max(r['score'] for r in rows)
for r in rows: r['score100']=round(100*r['score']/mx)
rows.sort(key=lambda r:-r['score'])
for r in rows: print(f"{r['label']:24} R{r['R']} sys{r['sys']:3} all{r['all']:3} cov{r['cov']:4} -> {r['score100']}")
data=dict(companies=[dict(id=ids[c['name']],name=c['name'],loc=c['location'],founded=c['founded'],pillar=c['pillar'],desc=c['summary'],uses=USE[ids[c['name']]]) for c in co],
  choke=[dict(id=k,**v,fix=[dict(co=a,w=b,note=n) for a,b,n in FIX.get(k,[])]) for k,v in CHOKE.items()],
  comp=[dict(id=k,**v,sup=[dict(co=a,w=b,basis=s) for a,b,s in SUP.get(k,[])]) for k,v in COMP.items()],
  scores=rows)
json.dump(data,open(os.path.join(ROOT,'data','graph.json'),'w'),indent=1,ensure_ascii=False)

od=os.path.join(ROOT,'data')+'/'
with open(od+'companies.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['company','pillar','location','founded','components_used','supplies_components','summary'])
    for c in data['companies']:
        sup=[m for m,v in SUP.items() if any(s==c['id'] for s,_,_ in v)]
        w.writerow([c['name'],c['pillar'],c['loc'],c['founded'],'; '.join(COMP[u]['label'] for u in c['uses']),'; '.join(COMP[u]['label'] for u in sup),c['desc']])
with open(od+'bottlenecks.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['rank','chokepoint','concentration_1to5','systems_exposed','all_companies_exposed','ad50_coverage','score_0to100','confidence','fact','sources'])
    for i,r in enumerate(rows,1):
        c=CHOKE[r['id']]; w.writerow([i,r['label'],r['R'],r['sys'],r['all'],r['cov'],r['score100'],c['conf'],c['fact'],' | '.join(u for _,u in c['src'])])
# assemble the static page
T=os.path.join(ROOT,'build','template')
js=open(os.path.join(T,'app.js')).read().replace('__DATA__',json.dumps(data,ensure_ascii=False))
html='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+open(os.path.join(T,'head.html')).read()+'</head>\n<body>\n'+open(os.path.join(T,'body.html')).read()+'<script>\n'+js+'\n</script>\n</body>\n</html>\n'
open(os.path.join(ROOT,'index.html'),'w').write(html)
print('wrote index.html')
