#!/usr/bin/env python3
"""Import pinned upstream SVGs without modifying their bytes; standard library only."""
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'biomedical':'生物医学','chemistry':'化学与分子','ecology':'生态与物种','earth-space':'地理、气象与空间','engineering':'工程与物理','computing':'计算与数据流程','general':'科研交流与通用'}
SUB = {'Animals':'动物','Plants_Algae':'植物与藻类','Viruses':'病毒','Microbiology':'微生物','Lab_apparatus':'实验仪器','Blood_Immunology':'血液与免疫','Human_physiology':'人体生理','Cell_types':'细胞类型','Cell_membrane':'细胞膜','Intracellular_components':'细胞内组分','Genetics':'遗传学','Genomics':'基因组学','Nucleic_acids':'核酸','Neuroscience':'神经科学','Chemistry':'化学','Amino-Acids':'氨基酸','Molecular_modelling':'分子建模','Computer_hardware':'计算机硬件','Machine_Learning':'机器学习','Scientific_graphs':'科学图表','protein':'蛋白质','compound':'化合物','cell_element':'细胞组分','receptor':'受体','cell_type':'细胞类型','transporter':'转运蛋白','human_tissue':'人体组织','therapeutic':'治疗','bacteria':'细菌','viruses':'病毒','fungi':'真菌','parasites':'寄生虫与媒介','immune-cells':'免疫细胞','molecules':'分子','organs':'器官','clinical':'临床与实验室'}
LICENSES = {'cc-0':('CC0-1.0','https://creativecommons.org/publicdomain/zero/1.0/'),'cc-by-3.0':('CC-BY-3.0','https://creativecommons.org/licenses/by/3.0/'),'cc-by-4.0':('CC-BY-4.0','https://creativecommons.org/licenses/by/4.0/'),'cc-by-sa-3.0':('CC-BY-SA-3.0','https://creativecommons.org/licenses/by-sa/3.0/'),'cc-by-sa-4.0':('CC-BY-SA-4.0','https://creativecommons.org/licenses/by-sa/4.0/'),'mit':('MIT','https://opensource.org/license/mit/'),'bsd':('BSD-3-Clause','https://opensource.org/license/bsd-3-clause/'),'apache':('Apache-2.0','https://www.apache.org/licenses/LICENSE-2.0')}
INFO = {
 'bioicons':('Bioicons（含 Servier / Togo）','https://bioicons.com/','逐图授权','生物、医学、植物、实验器材；含经 Bioicons 分发的 Servier 与 DBCLS 素材，保留其历史逐图许可。'),
 'bioicons-id':('ID & Immunology Icons','https://github.com/apsmunro/bioicons-id','CC0-1.0','病原体、免疫细胞、器官与感染传播，含彩色和单色版本。'),
 'reactome':('Reactome Illustrations','https://reactome.org/','Apache-2.0','Reactome 官方蛋白、化合物、细胞、组织和通路组件；保留原始 XML 元数据。'),
 'ebi-icons':('EMBL-EBI Science Icons','https://www.ebi.ac.uk/','CC-BY-SA-4.0','仅选 chemistry、conceptual、species 科学符号，不含第三方品牌和通用字库。'),
 'healthicons':('Health Icons','https://healthicons.org/','CC0-1.0','公共卫生、症状、医疗设备、人体与医疗服务图标，保留上游样式。'),
 'openmoji':('OpenMoji 科研选集','https://openmoji.org/','CC-BY-SA-4.0','动物、植物、地理天气、科学与技术主题彩色符号；逐图作者信息。'),
 'maki':('Maki','https://labs.mapbox.com/maki-icons/','CC0-1.0','地图兴趣点、自然环境、基础设施图标。'),
 'temaki':('Temaki','https://ideditor.github.io/temaki/','CC0-1.0','地理生态、交通、基础设施、土地利用地图符号。'),
 'weather-icons-v2':('Meteocons / Weather Icons','https://bas.dev/work/meteocons','MIT','天气、风力、降水与天体符号，静态 fill / line / monochrome 三款。'),
 'game-icons':('Game Icons 科研选集','https://game-icons.net/','逐图授权','从作者目录按公开关键词选取自然、生物、化学、物理和工程图标。'),
 'tabler':('Tabler 科研与流程图选集','https://tabler.io/icons','MIT','科学、设备、网络、数据处理与流程图符号，outline / filled 样式。'),
 'engineering-symbols':('Equinor Engineering Symbols','https://github.com/equinor/engineering-symbols','MIT','工业过程与工程设备的标准化 SVG 符号，保留原始编号。'),
 'circuit-symbols':('Inkscape Circuit Symbols','https://github.com/keikawa/InkscapeCircuitSymbols','MIT','整张电路符号 SVG 图板；在 Inkscape 内打开后选取所需元件。'),
 'scienceicons':('Scienceicons 开放科学选集','https://github.com/continuous-foundation/scienceicons','MIT','开放获取及科研交流基础符号；不收录第三方品牌。')}
KEYWORDS = {
 'chemistry':'atom molecule molecular chemistry chemical flask beaker test-tube test_pipe vial dna acid nucleic peptides compound amino nanotechnology',
 'ecology':'animal plant algae tree leaf flower forest fish bird insect butterfly bee bacteria mushroom ecology seed crop sprout paw bug cat dog turtle rabbit whale dolphin fossil deer biohazard',
 'earth-space':'world globe earth map mountain terrain volcano compass satellite planet solar moon sun star cloud rain snow weather wind water river sea ocean tide waves hurricane tornado temperature thermometer snowflake meteor rocket orbit galaxy',
 'engineering':'engineering circuit resistor capacitor transistor diode motor pump valve battery bolt electric power energy radiation radioactive magnet nuclear turbine gear tool microscope telescope laser prism lens antenna radar robot drone truck train plane ship crane engine factory building ruler scale triangle geometry polygon vector cube dimension',
 'computing':'computer laptop device server database cloud network neural brain ai algorithm chart graph plot diagram flow arrow git code terminal cpu gpu chip binary math function matrix sum infinity abacus calculator logic topology hierarchy nodes file storage microscope analysis data',
 'biomedical':'medical health medicine hospital heart lung lungs kidney liver cell cells virus viruses antibody blood syringe vaccine pill capsule dna protein receptor membrane tissue therapeutic stethoscope anatomy bone skull skeleton infection disease patient bacterium ambulance bandage tooth ear eye nose organ mask wheelchair',
 'general':'book school education certificate research science open-access email website clipboard presentation report zoom search checklist notes writing microscope'}
RX = {k:re.compile(r'(?<![a-z])(?:'+ '|'.join(map(re.escape,v.split())) +r')(?:s)?(?![a-z])', re.I) for k,v in KEYWORDS.items()}
ALIASES={'dna':'DNA 脱氧核糖核酸','rna':'RNA 核糖核酸','protein':'蛋白质','virus':'病毒','bacter':'细菌','cell':'细胞','heart':'心脏','lung':'肺','brain':'大脑 神经','antibod':'抗体','blood':'血液','immun':'免疫','microscope':'显微镜','flask':'烧瓶','test-tube':'试管','atom':'原子','molecul':'分子','gene':'基因','tree':'树木','plant':'植物','fish':'鱼','bird':'鸟','cloud':'云','rain':'降雨','sun':'太阳','moon':'月亮','wind':'风','water':'水','earth':'地球','map':'地图','server':'服务器','database':'数据库','chart':'图表','network':'网络','circuit':'电路','pump':'泵','valve':'阀门','receptor':'受体','mitochond':'线粒体','neuron':'神经元','cancer':'癌症 肿瘤','tissue':'组织','lab':'实验室'}

def classify(text, default='general'):
    for c in KEYWORDS:
        if RX[c].search(text.replace('_',' ').replace('-',' ')): return c
    return default

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--sources',type=Path,required=True); args=parser.parse_args()
    lock=json.loads((ROOT/'data/sources.lock.json').read_text()); assets=[]; sources=[]; excluded=[]
    previous=json.loads((ROOT/'data/catalog.json').read_text())['assets'] if (ROOT/'data/catalog.json').exists() else []
    for s in lock['sources']:
        sid=s['id']; p=args.sources/sid
        actual=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
        if actual!=s['commit']: raise SystemExit(f'Commit mismatch: {sid}')
        if subprocess.check_output(['git','-C',str(p),'status','--porcelain'],text=True).strip():raise SystemExit(f'Upstream checkout is dirty: {sid}')
        name,homepage,summary,desc=INFO[sid]
        licdir=ROOT/'licenses'/sid;licdir.mkdir(parents=True,exist_ok=True)
        for f in p.iterdir():
            if f.is_file() and (f.name.lower().startswith(('license','licence','notice','readme','copying','authors'))): shutil.copyfile(f,licdir/f.name)
        entries=[]
        def add(f,cat,sub='',lic='mit',author=None,title=None,tags=None,author_url='',metadata=None):
            entries.append((f,cat,sub,lic,author or name,title or f.stem.replace('_',' ').replace('-',' '),tags or [],author_url,metadata))
        if sid=='bioicons':
            authors=json.loads((p/'static/icons/authors.json').read_text())
            for folder in (p/'static/icons').iterdir():
                if (folder/'LICENSE').exists():
                    d=licdir/folder.name;d.mkdir(exist_ok=True);shutil.copyfile(folder/'LICENSE',d/'LICENSE')
            for f in sorted((p/'static/icons').rglob('*.svg')):
                lic,sub,author=f.relative_to(p/'static/icons').parts[:3]
                if lic=='bsd':
                    excluded.append({'source':sid,'path':str(f.relative_to(p)),'reason':'third-party software brand excluded'});continue
                cat= 'ecology' if sub in ['Animals','Plants_Algae'] else 'chemistry' if sub in ['Chemistry','Amino-Acids','Molecular_modelling','Nanotechnology','Peptides'] else 'computing' if sub in ['Computer_hardware','Machine_Learning','Scientific_graphs','Chemo-_and_Bioinformatics'] else 'biomedical'
                add(f,cat,SUB.get(sub,sub),lic,author,tags=[sub],author_url=authors.get(author,''))
            for f in ['authors.json','icons.json','categories.json']: shutil.copyfile(p/'static/icons'/f,licdir/f)
        elif sid=='bioicons-id':
            data=json.loads((p/'catalogue.json').read_text());shutil.copyfile(p/'catalogue.json',licdir/'catalogue.json')
            imported=set()
            for x in data['icons']:
                for key in ['file','monoFile']:
                    if x.get(key) and (p/x[key]).is_file():
                        f=p/x[key];imported.add(f)
                        add(f,'biomedical',SUB.get(x['category'],x['category']),'cc-0','Alasdair Munro',x['name']+(' · 单色' if key=='monoFile' else ''),x.get('tags',[])+[x.get('description','')])
            for f in sorted((p/'icons').rglob('*.svg')):
                if f not in imported:add(f,'biomedical',SUB.get(f.parent.name,f.parent.name),'cc-0','Alasdair Munro',tags=['variant 变体'])
        elif sid=='reactome':
            for f in sorted((p/'icons').glob('*.svg')):
                xml=f.with_suffix('.xml');meta=ET.parse(xml).getroot();cats=[x.text for x in meta.findall('categories/category') if x.text]
                if meta.findtext('skip')=='true':
                    excluded.append({'source':sid,'path':str(f.relative_to(p)),'reason':'upstream skip=true'});continue
                designers=meta.findall("person[@role='designer']");author='; '.join(x.text or '' for x in designers) or 'Reactome contributors'
                add(f,'chemistry' if 'compound' in cats else 'biomedical',' / '.join(SUB.get(c,c) for c in cats),'apache',author,meta.findtext('name') or f.stem,cats+[meta.findtext('description') or ''],designers[0].get('url','') if designers else '',xml)
        elif sid=='ebi-icons':
            for sub in ['chemistry','conceptual','species']:
                for f in sorted((p/'source'/sub).glob('*.svg')):add(f,'chemistry' if sub=='chemistry' else 'ecology' if sub=='species' else 'biomedical',sub,'cc-by-sa-4.0','EMBL-EBI')
        elif sid=='healthicons':
            meta={x['id']:x for x in json.loads((p/'public/icons/meta-data.json').read_text())};shutil.copyfile(p/'public/icons/meta-data.json',licdir/'meta-data.json')
            for f in sorted((p/'public/icons/svg').rglob('*.svg')):
                x=meta.get(f.stem,{});add(f,'biomedical',x.get('category',f.parent.name),'cc-0','Health Icons contributors',x.get('title',f.stem)+' · '+f.relative_to(p/'public/icons/svg').parts[0],x.get('tags',[]))
        elif sid=='openmoji':
            shutil.copyfile(p/'data/openmoji.json',licdir/'openmoji.json')
            for x in json.loads((p/'data/openmoji.json').read_text()):
                text=' '.join(str(x.get(k,'')) for k in ['annotation','tags','openmoji_tags']); group=x['group'];sub=x['subgroups'];cat=classify(text)
                if group=='animals-nature':cat='ecology'
                elif group=='travel-places' and sub in ['sky-weather','place-geographic','place-map']:cat='earth-space'
                elif not any(r.search(text.replace('-',' ')) for r in RX.values()):continue
                allowed=(group=='animals-nature' or group=='travel-places' and sub in ['sky-weather','place-geographic','place-map','transport-air','transport-ground','transport-water'] or group=='objects' and sub in ['science','medical','tool','computer','book-paper','writing','office','light-video'] or group=='people-body' and sub=='body-parts' or group=='extras-openmoji' and sub in ['healthcare','technology','climate-environment','animals-nature','gardening'])
                if not allowed or x.get('skintone'):continue
                f=p/'color/svg'/(x['hexcode']+'.svg')
                if f.exists():add(f,cat,sub,'cc-by-sa-4.0',x.get('openmoji_author') or 'OpenMoji contributors',x['annotation'],[text])
        elif sid in ['maki','temaki']:
            meta=json.loads((p/'data/icons.json').read_text()) if sid=='temaki' else {}
            for f in sorted((p/'icons').glob('*.svg')):add(f,'earth-space','地图与地理符号','cc-0',sid+' contributors',tags=meta.get(f.stem,{}).get('groups',[]))
        elif sid=='weather-icons-v2':
            for style in ['fill','line','monochrome']:
                for f in sorted((p/'production'/style/'svg-static').glob('*.svg')):add(f,'earth-space','气象 · '+style,'mit','Bas Milius',f.stem+' · '+style)
        elif sid in ['game-icons','tabler']:
            files=(p/'icons').rglob('*.svg') if sid=='tabler' else p.glob('*/*.svg')
            for f in sorted(files):
                if sid=='game-icons' and (f.parent.name=='badges' or f.stem.startswith('card-')):continue
                if not any(r.search(f.stem.replace('-',' ').replace('_',' ')) for r in RX.values()):continue
                author=f.parent.name if sid=='game-icons' else 'Paweł Kuna and Tabler contributors'
                lic='cc-0' if author in ['viscious-speed','zeromancer'] else 'cc-by-3.0' if sid=='game-icons' else 'mit'
                add(f,classify(f.stem), '科研选集 · '+f.parent.name,lic,author)
        elif sid=='engineering-symbols':
            for f in sorted((p/'package/src/svg').glob('*.svg')):add(f,'engineering','工业工程符号','mit','Equinor ASA')
        elif sid=='circuit-symbols':add(p/'symbol.svg','engineering','电路符号整图','mit','Keisuke','电路符号整图 · Circuit symbols sheet')
        elif sid=='scienceicons':
            for f in sorted((p/'src').rglob('*.svg')):
                if f.stem in ['open-access','email','website']:add(f,'general','开放科学与交流','mit','Continuous Science Foundation',f.stem+' · '+' / '.join(f.relative_to(p/'src').parts[:-1]))
        before=len(assets)
        for f,cat,sub,lic,author,title,tags,author_url,metadata in entries:
            raw=f.read_bytes()
            try:
                root=ET.fromstring(raw)
                if root.tag.split('}')[-1]!='svg':raise ValueError('not SVG root')
                for node in root.iter():
                    if node.tag.split('}')[-1] in ['script','foreignObject']:raise ValueError('active SVG content')
                    for k,v in node.attrib.items():
                        if k.lower().startswith('on'):raise ValueError('event handler')
                        if k.split('}')[-1]=='href' and v and not v.startswith(('#','data:image/')):raise ValueError('external reference')
            except (ET.ParseError,ValueError) as e:
                excluded.append({'source':sid,'path':str(f.relative_to(p)),'reason':str(e)});continue
            rel=f.relative_to(p); dest=Path('assets')/cat/sid/rel
            out=ROOT/dest;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,out)
            if metadata:shutil.copyfile(metadata,out.with_suffix('.xml'))
            license_name,license_url=LICENSES[lic]
            src=s['repository']+'/blob/'+s['commit']+'/'+quote(rel.as_posix(),safe='/')
            aid=hashlib.sha256((sid+'/'+str(rel)).encode()).hexdigest()[:20]
            keywords=' '.join([title,sub]+tags).lower();tags=list(tags)+[SUB.get(sub,sub)]+[zh for term,zh in ALIASES.items() if term in keywords]
            attribution=f'{title} — {author}. Source: {src}. License: {license_name} ({license_url}). Original file redistributed without modification; see licenses/{sid}/ for upstream notices.'
            assets.append(dict(id=aid,name=title,category=cat,subcategory=sub,source=sid,path=dest.as_posix(),license=license_name,license_url=license_url,author=author,author_url=author_url,source_url=src,attribution=attribution,tags=tags,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),original_path=rel.as_posix(),commit=s['commit']))
        sources.append(dict(id=sid,name=name,homepage=homepage,repository=s['repository'],license=summary,license_url=s['repository']+'/tree/'+s['commit'],count=len(assets)-before,description=desc,commit=s['commit']))
        print(sid,len(assets)-before,flush=True)
    retained={a['path'] for a in assets}
    for old in previous:
        if old['path'] not in retained:
            oldpath=(ROOT/old['path']).resolve()
            if not oldpath.is_relative_to(ROOT/'assets'):raise SystemExit('Invalid old managed path')
            if oldpath.exists() and hashlib.sha256(oldpath.read_bytes()).hexdigest()!=old['sha256']:raise SystemExit(f'Refusing to remove modified file: {oldpath}')
            oldpath.unlink(missing_ok=True)
            oldpath.with_suffix('.xml').unlink(missing_ok=True)
    counts=Counter(x['category'] for x in assets)
    catalog=dict(generated_at=lock['retrieved_at'],sources=sources,categories=[dict(id=k,name=v,count=counts[k]) for k,v in CATEGORIES.items()],assets=assets)
    (ROOT/'data/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'data/excluded.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'data/manifest.csv').open('w',newline='',encoding='utf-8-sig') as fp:
        fields=['id','name','category','subcategory','source','path','license','license_url','author','author_url','source_url','sha256','bytes','commit','attribution'];w=csv.DictWriter(fp,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(assets)
    print(f'Total: {len(assets)} SVGs, {sum(x["bytes"] for x in assets)/1e6:.1f} MB; excluded {len(excluded)}')

if __name__=='__main__': main()
