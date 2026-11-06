#!/usr/bin/env python3
"""Import pinned scientific originals without modifying their bytes; standard library only."""
import argparse
import configparser
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
from collect_web_images import dimensions

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'biomedical':'生物医学','chemistry':'化学与分子','ecology':'生态与物种','earth-space':'地理、气象与空间','engineering':'工程与物理','computing':'计算与数据流程','general':'科研交流与通用'}
SUB = {'Animals':'动物','Plants_Algae':'植物与藻类','Viruses':'病毒','Microbiology':'微生物','Lab_apparatus':'实验仪器','Blood_Immunology':'血液与免疫','Human_physiology':'人体生理','Cell_types':'细胞类型','Cell_membrane':'细胞膜','Intracellular_components':'细胞内组分','Genetics':'遗传学','Genomics':'基因组学','Nucleic_acids':'核酸','Neuroscience':'神经科学','Chemistry':'化学','Amino-Acids':'氨基酸','Molecular_modelling':'分子建模','Computer_hardware':'计算机硬件','Machine_Learning':'机器学习','Scientific_graphs':'科学图表','protein':'蛋白质','compound':'化合物','cell_element':'细胞组分','receptor':'受体','cell_type':'细胞类型','transporter':'转运蛋白','human_tissue':'人体组织','therapeutic':'治疗','bacteria':'细菌','viruses':'病毒','fungi':'真菌','parasites':'寄生虫与媒介','immune-cells':'免疫细胞','molecules':'分子','organs':'器官','clinical':'临床与实验室'}
LICENSES = {'cc-0':('CC0-1.0','https://creativecommons.org/publicdomain/zero/1.0/'),'cc-by-3.0':('CC-BY-3.0','https://creativecommons.org/licenses/by/3.0/'),'cc-by-4.0':('CC-BY-4.0','https://creativecommons.org/licenses/by/4.0/'),'cc-by-sa-3.0':('CC-BY-SA-3.0','https://creativecommons.org/licenses/by-sa/3.0/'),'cc-by-sa-4.0':('CC-BY-SA-4.0','https://creativecommons.org/licenses/by-sa/4.0/'),'mit':('MIT','https://opensource.org/license/mit/'),'bsd':('BSD-3-Clause','https://opensource.org/license/bsd-3-clause/'),'apache':('Apache-2.0','https://www.apache.org/licenses/LICENSE-2.0'),'isc':('ISC','https://opensource.org/license/isc/'),'isc-mit':('ISC AND MIT','https://github.com/lucide-icons/lucide/blob/main/LICENSE')}
LICENSES['lgpl-2.1-or-later']=('LGPL-2.1-or-later','https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html')
INFO = {
 'bioicons':('Bioicons（含 Servier / Togo）','https://bioicons.com/','逐图授权','生物、医学、植物、实验器材；含经 Bioicons 分发的 Servier 与 DBCLS 素材，保留其历史逐图许可。'),
 'bioicons-id':('ID & Immunology Icons','https://github.com/apsmunro/bioicons-id','CC0-1.0','病原体、免疫细胞、器官与感染传播，含彩色和单色版本。'),
 'reactome':('Reactome Illustrations','https://reactome.org/','Apache-2.0','Reactome 官方蛋白、细胞、组织和通路组件，以及完整生物通路插画；图标保留原始 XML 元数据。'),
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
 'scienceicons':('Scienceicons 开放科学选集','https://github.com/continuous-foundation/scienceicons','MIT','开放获取及科研交流基础符号；不收录第三方品牌。'),
 'lucide':('Lucide 科研符号选集','https://lucide.dev/','ISC / MIT','科研仪器、医学、生态、计算与流程符号；继承 Feather 的图标保留 MIT 条件。'),
 'fontawesome':('Font Awesome Free 科研选集','https://fontawesome.com/','CC-BY-4.0','选择非品牌的科学、仪器、医学、工程与数据图标；排除同名别名重复文件。'),
 'bootstrap':('Bootstrap 科研符号选集','https://icons.getbootstrap.com/','MIT','实验、医疗、环境、计算设备、数据和流程符号。'),
 'iconpark':('IconPark 科研与工程选集','https://iconpark.oceanengine.com/','Apache-2.0','包含上游中文名称、作者和标签的医学、动植物、能源、工业、测量、硬件与数据符号。'),
 'carbon-pictograms':('Carbon 科研与工业插图选集','https://carbondesignsystem.com/elements/pictograms/overview/','Apache-2.0','IBM Carbon 的科学、气候、工业、设备和数据概念插图；排除品牌标识。'),
 'electrical-symbol-library':('Electrical Symbol Library','https://github.com/basverdoes/ElectricalSymbolLibrary','CC0-1.0','仅收 src/symbols 独立电气符号；其余文件的非商业许可不用于这些单图。'),
 'electricalsymbols':('Electricalsymbols 工业电气符号','https://github.com/chille/electricalsymbols','CC-BY-SA-3.0','IEC 工业电气元件、开关、保护、传感器和电机；排除空白文档模板。'),
 'geologic-patterns':('FGDC Geologic Patterns','https://github.com/davenquinn/geologic-patterns','CC0-1.0','USGS / FGDC 地质、岩性、冰川和地层剖面填充图案；可用于地学论文制图。'),
 'gissymbology':('GISsymbology 专题地图符号','https://github.com/GISsymbology/symbols','CC-BY-SA-4.0','选取地震微区划、地质图、FGDC 地质符号和水利防护四个许可明确的子库。'),
 'openstax-anatomy':('OpenStax 人体解剖与生理历史开放插画','https://github.com/openstax/osbooks-anatomy-physiology','CC-BY-4.0','固定历史 CC BY 4.0 版本中逐图核验的人体解剖与生理插画；保留真实像素尺寸和章节证据。'),
 'openstax-biology':('OpenStax 生物学历史开放插画','https://github.com/openstax/osbooks-biology-bundle','CC-BY-4.0','固定历史CC BY4版本中的生物学、细胞、分子与生态原图；保留实际尺寸和逐图章节证据。'),
 'openstax-chemistry':('OpenStax 化学历史开放插画','https://github.com/openstax/osbooks-chemistry-bundle','CC-BY-4.0','固定历史CC BY4版本中的分子、晶体、实验装置与科学曲线原图；按实际尺寸区分标准与高清。'),
 'openstax-microbiology':('OpenStax 微生物学历史开放插画','https://github.com/openstax/osbooks-microbiology','CC-BY-4.0','固定历史CC BY4版本中的微生物、免疫与实验技术原图，保留原始尺寸和逐图来源。'),
 'openstax-college-physics':('OpenStax 基础物理开放插画','https://github.com/openstax/osbooks-college-physics-bundle','CC-BY-4.0','固定CC BY4快照中的力学、光学、声学、电磁学与热学示意图；保留实际尺寸和章节证据。'),
 'openstax-university-physics':('OpenStax 大学物理开放插画','https://github.com/openstax/osbooks-university-physics-bundle','CC-BY-4.0','固定CC BY4快照中的力学、电路、电磁学、波动及现代物理原图；保留实际尺寸和章节证据。'),
 'cpm-labicons':('CPM LabIcons 实验室仪器插画','https://github.com/Center-for-Proteomics-and-Metabolomics/LabIcons','CC-BY-4.0','质谱仪、色谱设备、离心机与耗材透明PNG原图；逐图保留作者和ORCID署名。'),
 'justfig-icons':('JustFig 原创科研图形','https://github.com/BooneAndrewsLab/justfig-icons','CC0-1.0','仅收原创 house 集合中的实验室、细胞、蛋白、免疫和微生物图形，不收聚合库其他来源。')}
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
ALIASES.update({'resistor':'电阻','capacitor':'电容','diode':'二极管','transistor':'晶体管','inductor':'电感','transformer':'变压器','switch':'开关','relay':'继电器','motor':'电机','geolog':'地质','litholog':'岩性','stratigraph':'地层','seismic':'地震','hydrolog':'水文','sensor':'传感器','battery':'电池','solar':'太阳能','telescope':'望远镜','radiation':'辐射','magnet':'磁场 磁铁','flow':'流程','data':'数据'})
ALIASES.update({'embryo':'胚胎','placenta':'胎盘','pregnancy':'妊娠 怀孕','uterus':'子宫','neonatal':'新生儿','lymph':'淋巴','complement':'补体','cloning':'克隆','membrane':'细胞膜','photosynth':'光合作用','chloroplast':'叶绿体','mitosis':'有丝分裂','meiosis':'减数分裂','titration':'滴定','covalent':'共价键','ionic':'离子'})

def classify(text, default='general'):
    for c in KEYWORDS:
        if RX[c].search(text.replace('_',' ').replace('-',' ')): return c
    return default

def read_lucide_metadata(directory, stem, stack=()):
    """Resolve the upstream per-field $extends references without installing JS."""
    if stem in stack:raise ValueError('Cyclic Lucide metadata inheritance')
    file=directory/(stem+'.json')
    if not file.exists():return {}
    result={}
    for key, values in json.loads(file.read_text()).items():
        if not isinstance(values,list):continue
        result[key]=[]
        for value in values:
            if isinstance(value,str) and value.startswith('$extends:'):
                result[key].extend(read_lucide_metadata(directory,value.split(':',1)[1],stack+(stem,)).get(key,[]))
            else:result[key].append(value)
    return result

def check_svg(raw, allow_static_html=False):
    """Keep passive SVG/metadata links; reject executable or missing external content."""
    root=ET.fromstring(raw)
    if root.tag.split('}')[-1]!='svg':raise ValueError('not SVG root')
    for node in root.iter():
        tag=node.tag.split('}')[-1].lower()
        if tag in {'script','iframe','object','embed'}:raise ValueError('active SVG content')
        if tag=='foreignobject' and not allow_static_html:raise ValueError('unreviewed foreignObject content')
        for key,value in node.attrib.items():
            key=key.split('}')[-1].lower()
            # Inkscape's `only_selected` is an export preference, not an event handler.
            if re.fullmatch(r'on[a-z]+',key):raise ValueError('event handler')
            if key in {'href','src'} and value:
                passive=value.startswith(('#','data:image/'))
                passive|=tag=='a' and value.startswith(('https://','http://'))
                passive|=tag=='color-profile' and value.startswith('data:application/vnd.iccprofile')
                if not passive:raise ValueError('external resource reference')
    return root

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--sources',type=Path,required=True);parser.add_argument('--only',nargs='+',help='Reimport selected source IDs and preserve other verified inventory'); args=parser.parse_args()
    lock=json.loads((ROOT/'data/sources.lock.json').read_text()); assets=[]; sources=[]; excluded=[]
    previous_catalog=json.loads((ROOT/'data/catalog.json').read_text()) if (ROOT/'data/catalog.json').exists() else {}
    previous=previous_catalog.get('assets',[])
    if args.only:
        if not previous_catalog:raise SystemExit('--only requires an existing verified catalog')
        if set(args.only)-{s['id'] for s in lock['sources']}:raise SystemExit('Unknown source ID in --only')
        for a in previous:
            if a['source'] not in args.only:
                file=ROOT/a['path']
                if hashlib.sha256(file.read_bytes()).hexdigest()!=a['sha256']:raise SystemExit(f'Preserved original has changed: {file}')
                assets.append(a)
        sources=[s for s in previous_catalog['sources'] if s['id'] not in args.only]
        if (ROOT/'data/excluded.json').exists():excluded=[x for x in json.loads((ROOT/'data/excluded.json').read_text()) if x['source'] not in args.only]
    static=json.loads((ROOT/'data/bioicons-static-allowlist.json').read_text()) if (ROOT/'data/bioicons-static-allowlist.json').exists() else {}
    static_hashes={a['path']:a['sha256'] for a in static.get('assets',[])}
    if static:
        assert hashlib.sha256((ROOT/static['audit_file']).read_bytes()).hexdigest()==static['audit_sha256'],'Static SVG audit mismatch'
        assert next(s['commit'] for s in lock['sources'] if s['id']=='bioicons')==static['commit'],'Static allowlist requires re-audit for new upstream commit'
    renders=json.loads((ROOT/'data/ppt-renders.json').read_text()).get('renders',{}) if (ROOT/'data/ppt-renders.json').exists() else {}
    for s in lock['sources']:
        if args.only and s['id'] not in args.only:continue
        sid=s['id']; p=(args.sources/sid).resolve()
        actual=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
        if actual!=s['commit']: raise SystemExit(f'Commit mismatch: {sid}')
        if subprocess.check_output(['git','-C',str(p),'status','--porcelain'],text=True).strip():raise SystemExit(f'Upstream checkout is dirty: {sid}')
        if sid in INFO:
            name,homepage,summary,desc=INFO[sid]
        else:
            info=s.get('catalog')
            if not isinstance(info,dict) or not all(info.get(k) for k in ['name','license','description']):
                raise SystemExit(f'Source {sid} requires catalog metadata: name, license and description')
            if not (ROOT/'data/source-selections'/(sid+'.json')).is_file():
                raise SystemExit(f'Source {sid} requires data/source-selections/{sid}.json')
            name,homepage,summary,desc=info['name'],info.get('homepage',s['repository']),info['license'],info['description']
        licdir=ROOT/'licenses'/sid;licdir.mkdir(parents=True,exist_ok=True)
        for notice in s.get('supplemental_license_files',[]):
            filename=notice['filename']
            assert Path(filename).name==filename,'Invalid supplemental license filename'
            original=ROOT/'licenses/common'/filename
            assert hashlib.sha256(original.read_bytes()).hexdigest()==notice['sha256'],'Supplemental license checksum mismatch'
            shutil.copyfile(original,licdir/filename)
        for f in p.iterdir():
            if sid=='electrical-symbol-library' and f.name=='README.md':continue
            if f.is_file() and (f.name.lower().startswith(('license','licence','notice','readme','copying','authors'))): shutil.copyfile(f,licdir/f.name)
        entries=[]
        def add(f,cat,sub='',lic='mit',author=None,title=None,tags=None,author_url='',metadata=None,details=None):
            entries.append((f,cat,sub,lic,author or name,title or f.stem.replace('_',' ').replace('-',' '),tags or [],author_url,metadata,details or {}))
        def selected_figures(selection_file):
            selection=json.loads(selection_file.read_text())
            assert selection['commit']==s['commit'],'Selection and source commit mismatch'
            lookup={v[0]:k for k,v in LICENSES.items()}
            for x in selection['assets']:
                f=(p/x['path']).resolve();assert f.is_relative_to(p.resolve()),'Selection escapes checkout'
                assert hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256'],'Selected original checksum mismatch'
                if sid=='wikipathways':
                    metadata=f.with_suffix('.json');metadata_raw=metadata.read_bytes()
                    expected=s['repository']+'/blob/'+s['commit']+'/'+quote(metadata.relative_to(p).as_posix(),safe='/')
                    assert x['metadata_url']==expected and hashlib.sha256(metadata_raw).hexdigest()==x['metadata_sha256'],'Pathway metadata provenance mismatch'
                    pathway=json.loads(metadata_raw)['pathway'];pid=x['pathway_id']
                    assert pathway['id'] in {pid,'http://identifiers.org/wikipathways/'+pid,'https://identifiers.org/wikipathways/'+pid},'Pathway identity mismatch'
                    assert pathway['organism']==x['organism'] and pathway['dataSourceVersion']==x['pathway_revision'],'Pathway organism or revision mismatch'
                key=x['license'] if x['license'] in LICENSES else lookup[x['license']]
                details={k:x[k] for k in ['caption','figure_id','credit','reference_url','metadata_url','metadata_sha256','pathway_revision','pathway_id','organism','cited_source_urls','original_license_declaration','original_license_references','unicode'] if x.get(k)}
                if f.suffix.lower() in {'.png','.jpg','.jpeg'}:
                    details['minimum_long_edge']=int(x.get('minimum_long_edge',selection.get('minimum_long_edge',1600)))
                    details['minimum_short_edge']=int(x.get('minimum_short_edge',selection.get('minimum_short_edge',1)))
                    assert details['minimum_long_edge']>=600 and details['minimum_short_edge']>=1,'Invalid original resolution policy'
                    assert details['minimum_long_edge']>=1600 or details['minimum_short_edge']>=200,'Standard-resolution selection requires a 200px short edge'
                if x.get('evidence_path'):details['evidence_url']=s['repository']+'/blob/'+s['commit']+'/'+quote(x['evidence_path'],safe='/')
                add(f,x.get('category','biomedical'),x.get('subcategory','科研插画'),key,x['author'],x.get('title',x.get('name')),x.get('tags',[]),author_url=x.get('author_url',''),details=details)
            evidence=set(x['evidence_path'] for x in selection['assets'] if x.get('evidence_path'))
            license_paths=selection.get('license_evidence',[])
            for path in license_paths if isinstance(license_paths,list) else []:
                if isinstance(path,str) and (p/path).is_file():evidence.add(path)
            for path in evidence:
                original=(p/path).resolve();assert original.is_relative_to(p.resolve())
                target=licdir/'evidence'/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target)
            shutil.copyfile(selection_file,licdir/'selected-figures.json')
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
            selection=ROOT/'data/source-selections/reactome-pathways.json'
            if selection.exists():selected_figures(selection)
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
        elif sid=='lucide':
            text=(p/'LICENSE').read_text();feather=set(x.strip() for x in text.split('project:',1)[1].split('The MIT License',1)[0].strip().split(','))
            for f in sorted((p/'icons').glob('*.svg')):
                meta=read_lucide_metadata(p/'icons',f.stem);cats=meta.get('categories',[]);tags=meta.get('tags',[])
                named=f.stem.replace('-',' ')
                if not any(r.search(named) for r in RX.values()) and not set(cats)&{'science','medical','nature','weather','math'}:continue
                aliases={a.get('name','') if isinstance(a,dict) else a for a in meta.get('aliases',[])}
                inherited=f.stem in feather or bool(aliases&feather)
                license_key='isc-mit' if inherited else 'isc'
                authors=['Lucide contributors']+meta.get('contributors',[])+(['Cole Bemis / Feather'] if inherited else [])
                add(f,classify(named+' '+' '.join(tags)),' / '.join(cats),license_key,'; '.join(authors),tags=tags+cats)
                shutil.copyfile(f.with_suffix('.json'),licdir/f.with_suffix('.json').name)
        elif sid=='fontawesome':
            meta=json.loads((p/'metadata/icons.json').read_text())
            for style in ['solid','regular']:
                for f in sorted((p/'svgs'/style).glob('*.svg')):
                    if f.stem not in meta:continue
                    x=meta[f.stem];text=f.stem.replace('-',' ')
                    if not any(r.search(text) for r in RX.values()):continue
                    add(f,classify(text),'科研符号 · '+style,'cc-by-4.0','Fonticons, Inc.',x['label']+' · '+style,x.get('search',{}).get('terms',[]))
        elif sid=='bootstrap':
            for f in sorted((p/'icons').glob('*.svg')):
                text=f.stem.replace('-',' ')
                if not any(r.search(text) for r in RX.values()):continue
                add(f,classify(text),'科研与流程符号','mit','The Bootstrap Authors')
        elif sid=='iconpark':
            mapping={'Health':'biomedical','Animals':'ecology','Energy':'engineering','Industry':'engineering','Measurement':'engineering','Weather':'earth-space','Hardware':'computing','Charts':'computing','Datas':'computing','Connect':'computing','Components':'engineering','Graphics':'computing','Arrows':'computing','Build':'engineering','Abstract':'general','Travel':'earth-space'}
            for x in json.loads((p/'source/icons.json').read_text()):
                cat=x['category']
                if cat not in mapping:continue
                f=p/'source'/cat/(x['name']+'.svg')
                if not f.exists():raise FileNotFoundError(f)
                add(f,mapping[cat],x.get('categoryCN',cat),'apache',x.get('author') or 'IconPark contributors',x.get('title',x['name']),x.get('tag',[])+[x['name'],cat])
        elif sid=='carbon-pictograms':
            package=p/'packages/pictograms';shutil.copyfile(package/'README.md',licdir/'PICTOGRAMS-README.md')
            for extra in ['pictograms.yml','categories.yml']:shutil.copyfile(package/extra,licdir/extra)
            for f in sorted((package/'src/svg').glob('*.svg')):
                text=f.stem.replace('-',' ')
                if f.stem.startswith(('ibm','logo','brand')) or not any(r.search(text) for r in RX.values()):continue
                add(f,classify(text),'科研与工业概念插图','apache','IBM / Carbon Design System contributors')
        elif sid=='electrical-symbol-library':
            # The repository's other files are NC-licensed; import only the explicitly CC0 symbols.
            (licdir/'SCOPE.txt').write_text('Imported only src/symbols/**/*.svg. Upstream README license statement: "The individual symbols, which are found in the `src/symbols/` directory, are licensed under the CC0 1.0 Universal license." Every imported SVG retains its embedded CC0 license and creator metadata. Other repository files are not imported.\nEvidence: '+s['repository']+'/blob/'+s['commit']+'/README.md#license\n')
            for f in sorted((p/'src/symbols').rglob('*.svg')):
                root=ET.parse(f).getroot();ns={'dc':'http://purl.org/dc/elements/1.1/','cc':'http://creativecommons.org/ns#','rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}
                creators=root.findall('.//dc:creator',ns);creator='; '.join(' '.join(e.itertext()).strip() for e in creators)
                licenses=root.findall('.//cc:license',ns)
                assert any('creativecommons.org/publicdomain/zero/1.0' in e.get('{'+ns['rdf']+'}resource','') for e in licenses),f
                add(f,'engineering','模拟与数字电路 · '+f.parent.name,'cc-0',creator or 'Filip Dominec and contributors')
        elif sid=='electricalsymbols':
            for f in sorted((p/'Symbols').glob('*.svg')):
                if f.stem=='A4_landscape':
                    excluded.append({'source':sid,'path':str(f.relative_to(p)),'reason':'blank A4 document template'});continue
                add(f,'engineering','工业电气与传感器','cc-by-sa-3.0','Christian Antila')
        elif sid=='geologic-patterns':
            shutil.copyfile(p/'docs/data.yaml',licdir/'pattern-series.yaml')
            series={'1':'地表沉积图案','2':'沉积岩图案','3':'火成岩图案','4':'变质岩与其他图案','5':'冰川与冰缘图案','6':'沉积岩性与地层剖面','7':'变质岩、火成岩与脉体岩性'}
            for f in sorted((p/'assets/svg').glob('*.svg')):
                sub=series.get(f.stem[:1],'地质填充图案')
                add(f,'earth-space',sub,'cc-0','Daven Quinn; underlying USGS / FGDC symbology',f'FGDC {f.stem} · {sub}',['geology','lithology','stratigraphy','pattern','地质','岩性','地层','剖面','填充'])
        elif sid=='gissymbology':
            meta=configparser.ConfigParser();meta.read(p/'metadata.ini');shutil.copyfile(p/'metadata.ini',licdir/'metadata.ini')
            titles={'microzonazione':'地震微区划','carg':'CARG 地质图','fdgc':'FGDC 地质符号','sicod':'水文与水利防护'}
            for collection,sub in titles.items():
                folder=p/'collections'/collection;notice=licdir/collection;notice.mkdir(exist_ok=True);shutil.copyfile(folder/'license',notice/'license')
                assert 'https://creativecommons.org/licenses/by-sa/4.0/' in (folder/'license').read_text()
                for f in sorted((folder/'svg').rglob('*.svg')):add(f,'earth-space',sub,'cc-by-sa-4.0',meta[collection]['author'],f'{f.stem} · {sub}',[meta[collection].get('tags',''),meta[collection].get('description',''),sub,'地质','GIS'])
        elif sid.startswith('openstax-') or (ROOT/'data/source-selections'/(sid+'.json')).is_file():
            selected_figures(ROOT/'data/source-selections'/(sid+'.json'))
            if sid.startswith('openstax-'):
                assert (p/'LICENSE').read_text().lstrip('\ufeff').strip().splitlines()[0].strip()=='Attribution 4.0 International', 'Historical CC BY license evidence required'
            elif sid=='justfig-icons':
                for path in ['house/meta.yaml','house/STYLE.md','sources/house/source.yaml']:
                    target=licdir/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p/path,target)
        before=len(assets)
        for f,cat,sub,lic,author,title,tags,author_url,metadata,details in entries:
            raw=f.read_bytes()
            raw_hash=hashlib.sha256(raw).hexdigest()
            static_approved=sid=='bioicons' and static_hashes.get(f.relative_to(p).as_posix())==raw_hash
            fmt=f.suffix.lower().lstrip('.');pixel_size=None
            try:
                if fmt=='svg':root=check_svg(raw,allow_static_html=static_approved)
                elif fmt in {'png','jpg','jpeg'}:
                    pixel_size=dimensions(raw)
                    if max(pixel_size)<details.get('minimum_long_edge',1600):raise ValueError('Native bitmap below declared long-edge threshold')
                    if min(pixel_size)<details.get('minimum_short_edge',1):raise ValueError('Native bitmap below declared short-edge threshold')
                else:raise ValueError('Unsupported original image format')
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
            asset=dict(id=aid,name=title,category=cat,subcategory=sub,source=sid,path=dest.as_posix(),license=license_name,license_url=license_url,author=author,author_url=author_url,source_url=src,attribution=attribution,tags=tags,sha256=raw_hash,bytes=len(raw),original_path=rel.as_posix(),commit=s['commit'],format=fmt,**details)
            if pixel_size:asset.update(pixel_width=pixel_size[0],pixel_height=pixel_size[1],quality_tier='native-highres' if max(pixel_size)>=1600 else 'native-standard')
            if static_approved:asset['requires_png_fallback']=True
            if aid in renders:
                r=renders[aid];png=(ROOT/r['png_path']).resolve()
                assert png.is_relative_to(ROOT/'assets/ppt-png')
                assert r['source_sha256']==raw_hash,'Regenerate stale PPT render'
                assert hashlib.sha256(png.read_bytes()).hexdigest()==r['sha256'],'PPT PNG checksum mismatch'
                asset.update(ppt_png_path=r['png_path'],ppt_png_width=r['width'],ppt_png_height=r['height'],ppt_png_sha256=r['sha256'],ppt_png_bytes=r['bytes'])
                if static_approved:asset['preview_path']=r['png_path']
            assets.append(asset)
        supporting={'lucide','fontawesome','bootstrap','iconpark','tabler','game-icons','openmoji','scienceicons','carbon-pictograms'}
        sources.append(dict(id=sid,name=name,homepage=homepage,repository=s['repository'],license=summary,license_url=s['repository']+'/tree/'+s['commit'],count=len(assets)-before,description=desc,commit=s['commit'],kind=s.get('catalog',{}).get('kind','supporting' if sid in supporting else 'specialist'),retrieved_at=s.get('retrieved_at','2026-11-02')))
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
    rank={s['id']:i for i,s in enumerate(lock['sources'])};sources.sort(key=lambda s:rank[s['id']]);assets.sort(key=lambda a:(rank[a['source']],a['original_path']))
    for a in assets:a.setdefault('format',Path(a['path']).suffix.lower().lstrip('.'))
    catalog=dict(generated_at=lock['retrieved_at'],sources=sources,categories=[dict(id=k,name=v,count=counts[k]) for k,v in CATEGORIES.items()],format_counts=dict(Counter(a['format'] for a in assets)),assets=assets)
    (ROOT/'data/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'data/excluded.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'data/manifest.csv').open('w',newline='',encoding='utf-8-sig') as fp:
        fields=['id','name','category','subcategory','source','path','format','pixel_width','pixel_height','quality_tier','minimum_long_edge','minimum_short_edge','license','license_url','author','author_url','source_url','sha256','bytes','commit','attribution','ppt_png_path','ppt_png_width','ppt_png_height','ppt_png_sha256','requires_png_fallback','evidence_url','reference_url','metadata_url','metadata_sha256','pathway_id','pathway_revision','organism','original_license_declaration','unicode'];w=csv.DictWriter(fp,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(assets)
    print(f'Total: {len(assets)} original images, {sum(x["bytes"] for x in assets)/1e6:.1f} MB; excluded {len(excluded)}')

if __name__=='__main__': main()
