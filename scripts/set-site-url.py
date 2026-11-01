"""Set canonical and social URLs in the static output before deployment."""
from pathlib import Path
from urllib.parse import urlsplit
import re,sys
root=Path(__file__).resolve().parents[1]/'dist'
url=sys.argv[1].rstrip('/')
if urlsplit(url).scheme!='https' or not urlsplit(url).netloc:
 raise SystemExit('Provide a complete https:// website URL.')
index=root/'index.html'
text=index.read_text()
old=re.search(r'<link rel="canonical" href="([^"]+)"',text).group(1).rstrip('/')
for name in ['index.html','robots.txt','sitemap.xml']:
 p=root/name;p.write_text(p.read_text().replace(old,url))
print('Updated canonical, structured data, social and sitemap URLs.')
