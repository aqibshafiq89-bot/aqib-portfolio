from pathlib import Path
from html.parser import HTMLParser
import json,fitz
class Page(HTMLParser):
 def __init__(self):super().__init__();self.elements=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs);attrs['tag']=tag;self.elements.append(attrs)
  if tag=='h1':self.h1+=1
root=Path(__file__).resolve().parents[1];dist=root/'dist'
raw=(dist/'index.html').read_text();page=Page();page.feed(raw);errors=[]
ids=[e['id'] for e in page.elements if 'id' in e]
if len(ids)!=len(set(ids)):errors.append('Duplicate HTML ids')
if page.h1!=1:errors.append('Expected one H1')
linkcount=0
for el in page.elements:
 value=el.get('href') or el.get('src')
 if value:linkcount+=1
 if not value or value.startswith(('http','mailto:','tel:','data:')):continue
 if value.startswith('#'):
  if value[1:] not in ids:errors.append('Missing anchor: '+value)
 elif not (dist/value.split('#')[0].split('?')[0]).exists():errors.append('Missing asset: '+value)
for el in page.elements:
 if el['tag']=='img' and 'alt' not in el:errors.append('Image missing alt')
 for source in el.get('srcset','').split(','):
  if source.strip() and not (dist/source.strip().split()[0]).is_file():errors.append('Missing responsive image: '+source)
import re
if re.search(r'\{\{\w+\}\}',raw):errors.append('Unresolved template token')
for project in json.loads((root/'content/projects.json').read_text()):
 if not (dist/project['image']).is_file():errors.append('Missing project modal image: '+project['image'])
for font in re.findall(r'url\((assets/fonts/[^)]+)\)',(dist/'styles.css').read_text()):
 if not (dist/font).is_file():errors.append('Missing font: '+font)
for j in re.findall(r'<script[^>]*type="application/(?:ld\+)?json"[^>]*>(.*?)</script>',raw,re.S):json.loads(j)
cv=fitz.open(dist/'assets/Aqib-Shafiq-Academic-CV.pdf');cv_text=''.join(p.get_text() for p in cv)
if 'Passport No' in cv_text or 'References' in cv_text:errors.append('Non-public CV sections remain')
if set(re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',cv_text))!={'aqib.shafiq89@gmail.com'}:errors.append('Unexpected email in public CV')
if 'aqib.shafiq89@gmail.com' not in cv_text or '+971 56 786 3596' not in cv_text:errors.append('Public CV contact missing')
for p in cv:
 for link in p.get_links():
  uri=link.get('uri','')
  if uri.startswith('mailto:') and uri!='mailto:aqib.shafiq89@gmail.com':errors.append('Unexpected email link retained')
papers=json.loads((root/'content/publications.json').read_text())
project_count=sum('project-card' in e.get('class','').split() for e in page.elements)
assert len(papers)==12
assert sum(x['type']=='Journal' for x in papers)==8
assert sum(x['type']=='Conference' for x in papers)==4
assert project_count==6
assert 'href="tel:+971567863596"' in raw
print(json.dumps({'status':'failed' if errors else 'passed','errors':errors,'publication_count':len(papers),'project_count':project_count,'local_links_checked':linkcount,'public_cv_pages':len(cv)},indent=2))
raise SystemExit(bool(errors))
