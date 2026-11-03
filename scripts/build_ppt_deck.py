#!/usr/bin/env python3
"""Package existing, faithfully rendered artwork into a copyable PowerPoint library.

Optional dependency: python-pptx==1.0.2. No drawing or image content is synthesized.
"""
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ROOT=Path(__file__).resolve().parents[1]
INK='173C3A';TEAL='17786B';MUTED='607D79';BG='F6F8F3';LINE='DFE8DF'

def text(slide,x,y,w,h,value,size=12,color=INK,bold=False):
    box=slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    box.text_frame.word_wrap=True
    box.text_frame.margin_left=box.text_frame.margin_right=0
    box.text_frame.margin_top=box.text_frame.margin_bottom=0
    p=box.text_frame.paragraphs[0];p.text=value
    for run in p.runs:
        run.font.name='Microsoft YaHei';run.font.size=Pt(size)
        run.font.bold=bold;run.font.color.rgb=RGBColor.from_string(color)
    return box

def picture(slide,asset,x,y,w,h):
    iw,ih=asset['ppt_png_width'],asset['ppt_png_height'];scale=min(w/iw,h/ih)
    pw,ph=iw*scale,ih*scale
    slide.shapes.add_picture(str(ROOT/asset['ppt_png_path']),Inches(x+(w-pw)/2),Inches(y+(h-ph)/2),width=Inches(pw),height=Inches(ph))

def main():
    data=json.loads((ROOT/'data/catalog.json').read_text());selection=json.loads((ROOT/'data/ppt-selection.json').read_text())
    byid={a['id']:a for a in data['assets']};allart=[byid[i] for i in selection['asset_ids'] if byid[i].get('ppt_png_path')]
    chosen=[];seen=set();budget=0
    def take(candidates,count):
        nonlocal budget
        added=0
        for a in candidates:
            if added>=count:break
            ratio=a['ppt_png_width']/a['ppt_png_height']
            if a['id'] in seen or not .4<=ratio<=2.8:continue
            if budget+a['ppt_png_bytes']>50*1024*1024:continue
            chosen.append(a);seen.add(a['id']);budget+=a['ppt_png_bytes'];added+=1
    take([byid[i] for i in selection['featured_ids']],40)
    take([a for a in allart if a['author']=='SwissBioPics'],16)
    take([a for a in allart if a['author']=='DBCLS' and a['subcategory']!='People-Other'],16)
    take(allart,72-len(chosen))
    assert len(chosen)==72,f'Expected72 artworks, found {len(chosen)}'
    prs=Presentation();prs.slide_width=Inches(13.333333);prs.slide_height=Inches(7.5)
    blank=prs.slide_layouts[6];records=[]
    def page():
        s=prs.slides.add_slide(blank);s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string(BG);return s
    cover=page();text(cover,.7,.55,11.9,.35,'OPEN RESEARCH ILLUSTRATIONS',12,TEAL,True)
    text(cover,.7,1.12,11.9,.75,'科研插画 · PowerPoint 素材板',32,INK,True)
    text(cover,.75,2.05,11.8,.8,'72 张精选科研插画，可直接选择图片并复制到你的幻灯片。\n原始 SVG 与更多高清 PNG 见 GitHub 仓库。',17,MUTED)
    for j,a in enumerate(chosen[:3]):picture(cover,a,.9+j*4.1,3.0,3.45,2.9)
    text(cover,.75,6.55,11.8,.4,'每图作者与许可列于图下及幻灯片备注。PNG 按原 SVG 忠实渲染，原图内容未补绘。',11,MUTED)
    cover.notes_slide.notes_text_frame.text='Repository: https://github.com/winderflow/example-text\n'+ '\n\n'.join(a['attribution'] for a in chosen[:3])
    cats={c['id']:c['name'] for c in data['categories']}
    for offset in range(0,len(chosen),4):
        batch=chosen[offset:offset+4];slide=page();number=len(prs.slides)
        text(slide,.55,.28,11.9,.45,'科研插画素材板',21,INK,True);text(slide,11.8,.35,1,.3,f'{number:02d}',11,MUTED)
        notes=[]
        for j,a in enumerate(batch):
            x=.65+(j%2)*6.35;y=1.0+(j//2)*3.1
            picture(slide,a,x,y,5.65,2.05)
            title=a['name'] if len(a['name'])<75 else a['name'][:72]+'…'
            text(slide,x,y+2.12,5.7,.4,title,11,INK,True)
            text(slide,x,y+2.55,5.7,.3,f"{a['author']} · {a['license']} · {cats[a['category']]}",8,MUTED)
            notes.append(a['attribution']+'\nPNG conversion: faithful rasterization; original aspect ratio retained.\nPNG: '+a['ppt_png_path'])
            records.append({'asset_id':a['id'],'slide':number,'png_path':a['ppt_png_path'],'sha256':a['ppt_png_sha256'],'attribution':a['attribution']})
        slide.notes_slide.notes_text_frame.text='\n\n'.join(notes)
    end=page();text(end,.7,.65,11.8,.8,'使用与署名',30,INK,True)
    text(end,.75,1.8,11.7,3.8,'1. 单击需要的图片，复制，再粘贴到你的研究报告或课件。\n\n2. 这些是高清 PNG；若需编辑路径或无限缩放，请下载仓库内对应 SVG。\n\n3. 每张图的作者、来源与许可证记录在该页备注中，发表或分享时保留署名。\n\n4. 各图保持原有许可；CC BY-SA 图形的改编分享还需遵守相同方式共享条款。',17,MUTED)
    text(end,.75,6.6,11.7,.4,'https://github.com/winderflow/example-text',13,TEAL)
    out=ROOT/'downloads/ppt-illustrations.pptx';out.parent.mkdir(exist_ok=True);prs.save(out)
    assert out.stat().st_size<90*1024*1024,'Deck exceeds repository file-size budget'
    manifest={'file':out.relative_to(ROOT).as_posix(),'slides':len(prs.slides),'unique_artworks':len(chosen),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'images':records}
    (ROOT/'data/ppt-deck.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    # A text-only GitHub index lets users find named artwork without a running website.
    lines=['# PPT 高清科研插画目录','',f'共 {len(allart)} 张已有原图的高清 PNG 兼容版本，长边2400像素。PNG转换不计作新增科研图形。点击下方链接打开原图后可保存；完整署名见目录清单。','', '[下载72张精选的PowerPoint素材板](../downloads/ppt-illustrations.pptx) · [使用与署名指南](PPT-GUIDE.md)','']
    for cat in data['categories']:
        rows=sorted([a for a in allart if a['category']==cat['id']],key=lambda a:(a['subcategory'],a['name']))
        if not rows:continue
        lines += ['## '+cat['name'],'','| 图名 / 专题 | 作者 | 高清 PNG | 原始 SVG | 许可 |','| --- | --- | --- | --- | --- |']
        for a in rows:
            title=(a['name']+' / '+a['subcategory']).replace('|','／').replace('\n',' ')
            png='../'+quote(a['ppt_png_path'],safe='/')+'?raw=true';svg='../'+quote(a['path'],safe='/')+'?raw=true'
            lines.append(f"| {title} | {a['author']} | [{a['ppt_png_width']}×{a['ppt_png_height']}]({png}) | [SVG]({svg}) | [{a['license']}]({a['license_url']}) |")
        lines.append('')
    (ROOT/'docs/PPT-INDEX.md').write_text('\n'.join(lines).rstrip()+'\n')
    print(f'PowerPoint: {len(chosen)} images, {len(prs.slides)} slides, {out.stat().st_size/1e6:.1f} MB')

if __name__=='__main__':main()
