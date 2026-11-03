#!/usr/bin/env python3
"""Collect license-verified HD illustrations from the official Wellcome and Commons APIs.

Python standard library only. Uses inherited TLS/proxy configuration; never bypasses
policy failures. A 403 exits immediately. API metadata license is never substituted
for the image's own license. Each imported image has its exact API evidence saved.
"""
import argparse
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA='ResearchOpenIllustrations/1.0 (open-license educational collection; https://github.com/winderflow/example-text)'
QUERIES={
 'wellcome':['anatomy engraving','botanical illustration','human skeleton','brain anatomy','microscopy','medical illustration'],
 'commons':['anatomical diagram filetype:svg','human anatomy illustration filetype:bitmap','botanical illustration filetype:bitmap','cell biology diagram filetype:svg','scientific diagram filetype:svg']}
SAFE_HOSTS={'wellcomecollection.org','api.wellcomecollection.org','iiif.wellcomecollection.org','commons.wikimedia.org','upload.wikimedia.org'}

class PolicyBlocked(RuntimeError):pass
class BudgetReached(RuntimeError):pass
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,data):self.parts.append(data)
def clean(value):
 p=Text();p.feed(str(value));return ' '.join(unescape(' '.join(p.parts)).split())
def safe_url(url):
 p=urllib.parse.urlsplit(url)
 if p.scheme!='https' or p.hostname not in SAFE_HOSTS:raise ValueError('Unexpected nonofficial URL host: '+str(p.hostname))
 return url
class Redirects(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  safe_url(newurl)
  return super().redirect_request(req,fp,code,msg,headers,newurl)
OPENER=urllib.request.build_opener(Redirects())
def fetch(url,max_bytes=20*1024*1024):
 req=urllib.request.Request(safe_url(url),headers={'User-Agent':UA,'Accept':'application/json,image/*;q=0.9,*/*;q=0.8'})
 try:
  with OPENER.open(req,timeout=45) as r:
   data=r.read(max_bytes+1)
   if len(data)>max_bytes:raise ValueError('File exceeds size budget')
   return data,r.headers.get('Content-Type',''),r.geturl()
 except urllib.error.HTTPError as e:
  if e.code==403:raise PolicyBlocked('HTTP 403 from '+urllib.parse.urlsplit(url).hostname) from e
  raise
 except urllib.error.URLError as e:
  if '403' in str(e):raise PolicyBlocked('Proxy CONNECT 403 for '+urllib.parse.urlsplit(url).hostname) from e
  raise

def get_json(url):return json.loads(fetch(url,25*1024*1024)[0])
def cc_license(url):
 p=urllib.parse.urlsplit(url)
 if p.scheme not in {'http','https'}:return None
 if p.hostname not in {'creativecommons.org','www.creativecommons.org'}:return None
 path=p.path.lower().rstrip('/')+'/'
 m=re.fullmatch(r'/licenses/(by|by-sa)/(2\.0|2\.5|3\.0|4\.0)/',path)
 if m:return 'CC-'+m[1].upper()+'-'+m[2], 'https://creativecommons.org'+path
 if path=='/publicdomain/zero/1.0/':return 'CC0-1.0','https://creativecommons.org'+path
 if path=='/publicdomain/mark/1.0/':return 'Public-Domain-Mark-1.0','https://creativecommons.org'+path
 return None

def dimensions(data):
 if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>=24:return struct.unpack('>II',data[16:24])
 if data[:2]==b'\xff\xd8':
  i=2
  while i+4<=len(data):
   if data[i]!=255:i+=1;continue
   while i<len(data) and data[i]==255:i+=1
   marker=data[i];i+=1
   if marker in [0x01,*range(0xd0,0xda)]:continue
   if i+2>len(data):break
   n=int.from_bytes(data[i:i+2],'big')
   if n<2:break
   if marker in {0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf}:
    h,w=struct.unpack('>HH',data[i+3:i+7]);return w,h
   i+=n
 raise ValueError('Unsupported or malformed raster image')

def wellcome_candidate(image,info,max_edge=3200):
 source=image.get('source',{});locations=image.get('locations',[])
 chosen=next((x for x in locations if cc_license(x.get('license',{}).get('url',''))),None)
 if not chosen:raise ValueError('Missing open image license on its own location')
 lic,url=cc_license(chosen['license']['url']);w=int(info['width']);h=int(info['height'])
 root=info.get('id') or info.get('@id')
 if not root:root=image['thumbnail']['url'].removesuffix('/info.json')
 safe_url(root)
 if not root.startswith('https://iiif.wellcomecollection.org/'):raise ValueError('Unexpected image service')
 edge=min(max(w,h),max_edge);size=str(edge)+',' if w>=h else ','+str(edge)
 authors=[clean(c.get('agent',{}).get('label','')) for c in source.get('contributors',[])];authors=[a for a in authors if a]
 credit=clean(chosen.get('credit',''))
 if not authors and not credit and lic.startswith('CC-BY'):raise ValueError('No image author/credit supplied for attribution license')
 ident=str(image['id']);title=clean(source.get('title','')) or ident
 return dict(id=ident,name=title,author='; '.join(authors) or credit or 'Creator not supplied by source',credit=credit,license=lic,license_url=url,source_url='https://wellcomecollection.org/images/'+urllib.parse.quote(ident),download_url=root.rstrip('/')+'/full/'+size+'/0/default.jpg',original_width=w,original_height=h,format='jpg',image_api_url='https://api.wellcomecollection.org/catalogue/v2/images/'+urllib.parse.quote(ident),tags=[clean(s.get('label','')) for s in source.get('subjects',[])],transformations='Official IIIF full-frame JPEG derivative; longest edge capped at '+str(max_edge)+'px without upscaling')

def commons_candidate(page):
 info=page.get('imageinfo',[{}])[0];meta=info.get('extmetadata',{})
 def value(k):return clean(meta.get(k,{}).get('value',''))
 license_pair=cc_license(value('LicenseUrl'))
 if license_pair is None and value('LicenseShortName').lower()=='public domain' and value('Copyrighted').lower()=='false':license_pair=('Public-Domain','https://commons.wikimedia.org/wiki/Commons:Licensing#Material_in_the_public_domain')
 if license_pair is None:raise ValueError('No unambiguous redistributable image license')
 # Do not silently choose among a multi-license string whose parsed URL is incomplete.
 if value('Restrictions'):raise ValueError('Per-image restrictions need manual review: '+value('Restrictions'))
 lic,license_url=license_pair;url=info.get('url','');safe_url(url)
 ext=Path(urllib.parse.urlsplit(url).path).suffix.lower()
 if ext not in ['.svg','.jpg','.jpeg','.png']:raise ValueError('Unsupported original image format')
 author=value('Artist') or value('Attribution')
 if not author and lic.startswith('CC-BY'):raise ValueError('Missing author for attribution license')
 source_url=info.get('descriptionurl') or 'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(page['title'].replace(' ','_'))
 safe_url(source_url)
 ident=str(page['pageid']);return dict(id=ident,name=value('ObjectName') or page['title'].removeprefix('File:'),description=value('ImageDescription'),author=author or 'Creator not supplied by source',credit=value('Credit'),license=lic,license_url=license_url,source_url=source_url,download_url=url,original_width=int(info.get('width',0)),original_height=int(info.get('height',0)),format='jpg' if ext=='.jpeg' else ext[1:],tags=[],transformations='Original file, no modification',commons_title=page['title'])

def emit_candidate(record,evidence,out,source,args,budget):
 ext=record['format']
 if not re.fullmatch(r'[A-Za-z0-9_-]{1,128}',record['id']):raise ValueError('Invalid source image identifier')
 path=out/'images'/(record['id']+'.'+ext)
 if max(record['original_width'],record['original_height'])<args.min_edge and ext!='svg':raise ValueError('Source image smaller than minimum')
 if path.exists():raw=path.read_bytes()
 else:raw,_,_=fetch(record['download_url'],args.max_file_mb*1024*1024)
 if len(raw)+budget>args.max_mb*1024*1024:raise BudgetReached('Total source download budget reached')
 if ext=='svg':
  from xml.etree import ElementTree as ET
  root=ET.fromstring(raw)
  if root.tag.split('}')[-1]!='svg':raise ValueError('Not an SVG')
  for e in root.iter():
   if e.tag.split('}')[-1] in {'script','foreignObject'}:raise ValueError('Active SVG content')
   for k,v in e.attrib.items():
    if k.lower().startswith('on'):raise ValueError('SVG event handler')
    if k.split('}')[-1]=='href' and v and not v.startswith(('#','data:image/')):raise ValueError('External SVG resource')
  w,h=record['original_width'],record['original_height']
 else:
  w,h=dimensions(raw)
  if max(w,h)<args.min_edge:raise ValueError('Downloaded image smaller than minimum')
 path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
 evidence_path=out/'evidence'/(record['id']+'.json');evidence_path.parent.mkdir(exist_ok=True);evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
 record.update(source=source,path=str(path.resolve()),relative_path=str(path.relative_to(out)),width=w,height=h,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),evidence=str(evidence_path.resolve()))
 record['attribution']=f"{record['name']} — {record['author']}. {record['credit']} Source: {record['source_url']}. License: {record['license']} ({record['license_url']}). {record['transformations']}."
 return len(raw)

def collect(source,args):
 out=args.output/source;out.mkdir(parents=True,exist_ok=True);records=[];rejected=[];seen=set();budget=0
 def save():
  (out/'manifest.json').write_text(json.dumps(dict(source_id=source,source=source,assets=records,rejected=rejected,downloaded_bytes=budget),ensure_ascii=False,indent=2)+'\n')
 try:
  for query in args.query or QUERIES[source]:
   if len(records)>=args.limit:break
   if source=='wellcome':
    url='https://api.wellcomecollection.org/catalogue/v2/images?'+urllib.parse.urlencode({'query':query,'pageSize':100,'locations.license':'cc-by,cc-by-sa,cc-0,pdm'})
   else:
    params={'action':'query','format':'json','generator':'search','gsrsearch':query,'gsrnamespace':6,'gsrlimit':50,'prop':'imageinfo','iiprop':'url|size|mime|extmetadata','iiextmetadatalanguage':'en','iiextmetadatamultilang':'0'}
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
   pages=0
   while url and len(records)<args.limit and pages<args.pages_per_query:
    data=get_json(url);pages+=1
    items=data.get('results',[]) if source=='wellcome' else list(data.get('query',{}).get('pages',{}).values())
    for item in items:
     key=str(item.get('id') if source=='wellcome' else item.get('pageid'))
     if key in seen:continue
     seen.add(key)
     try:
      if source=='wellcome':
       # Re-fetch the single image so evidence includes that exact image's own license.
       detail=get_json('https://api.wellcomecollection.org/catalogue/v2/images/'+urllib.parse.quote(key))
       iiif=get_json(detail['thumbnail']['url']);record=wellcome_candidate(detail,iiif,args.max_edge);evidence={'image':detail,'iiif':iiif,'query':query}
      else:record=commons_candidate(item);evidence={'page':item,'query':query,'api_url':url}
      record['tags'].append(query);budget+=emit_candidate(record,evidence,out,source,args,budget);records.append(record);save();print(source,len(records),record['name'],flush=True)
     except PolicyBlocked:raise
     except (ValueError,KeyError,urllib.error.HTTPError) as e:rejected.append({'id':key,'reason':str(e)})
     if len(records)>=args.limit:break
     time.sleep(args.delay)
    if source=='wellcome':url=data.get('nextPage')
    elif data.get('continue'):
     params.update(data['continue']);url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    else:url=None
    time.sleep(args.delay)
 except BudgetReached as e:
  rejected.append({'reason':str(e)});save();return records
 except PolicyBlocked as e:
  rejected.append({'reason':'NETWORK_POLICY_BLOCKED: '+str(e)});save();raise
 save();return records

def self_test():
 info={'width':4000,'height':3000,'@id':'https://iiif.wellcomecollection.org/image/TEST'}
 image={'id':'fixture','source':{'title':'Anatomical plate','contributors':[{'agent':{'label':'Example Artist'}}]},'locations':[{'license':{'url':'https://creativecommons.org/licenses/by/4.0/'},'credit':'Example Credit'}],'thumbnail':{'url':info['@id']+'/info.json'}}
 r=wellcome_candidate(image,info);assert r['license']=='CC-BY-4.0' and '/full/3200,/0/default.jpg' in r['download_url']
 image['locations'][0]['license']['url']='https://creativecommons.org/licenses/by-nc/4.0/'
 try:wellcome_candidate(image,info);raise AssertionError('NC image accepted')
 except ValueError:pass
 page={'pageid':10,'title':'File:Example.svg','imageinfo':[{'width':2000,'height':2000,'url':'https://upload.wikimedia.org/wikipedia/commons/a/ab/Example.svg','extmetadata':{'LicenseUrl':{'value':'https://creativecommons.org/licenses/by-sa/4.0/'},'Artist':{'value':'<a href="https://example.org">Creator</a>'},'ObjectName':{'value':'Example'}}}]}
 assert commons_candidate(page)['author']=='Creator'
 page['imageinfo'][0]['extmetadata']['Restrictions']={'value':'personality rights'}
 try:commons_candidate(page);raise AssertionError('Restrictions accepted')
 except ValueError:pass
 png=b'\x89PNG\r\n\x1a\n'+b'\x00'*8+struct.pack('>II',3000,2000)
 assert dimensions(png)==(3000,2000)
 assert cc_license('https://creativecommons.org/licenses/by-nd/4.0/') is None
 assert cc_license('https://creativecommons.org/licenses/by-nc-sa/4.0/') is None
 assert cc_license('https://evil.invalid/licenses/by/4.0/') is None
 print('PASS: image-license scope, NC/ND exclusion, Commons author HTML, restriction review, HD dimensions and IIIF resize behavior. Fixture tests only; no remote download claim.')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',choices=['wellcome','commons','both'],default='both');p.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'.cache/web-images');p.add_argument('--limit',type=int,default=150);p.add_argument('--query',action='append');p.add_argument('--min-edge',type=int,default=1600);p.add_argument('--max-edge',type=int,default=3200);p.add_argument('--max-mb',type=int,default=120);p.add_argument('--max-file-mb',type=int,default=15);p.add_argument('--pages-per-query',type=int,default=3);p.add_argument('--delay',type=float,default=0.3);p.add_argument('--self-test',action='store_true');args=p.parse_args()
 if args.self_test:self_test();return
 for source in ['wellcome','commons'] if args.source=='both' else [args.source]:
  try:collect(source,args)
  except PolicyBlocked as e:print(str(e),file=sys.stderr);sys.exit(3)
if __name__=='__main__':main()
