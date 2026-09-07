from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import requests,json,re
d=json.loads(Path('.research/media-index.json').read_text(encoding='utf-8'))
selected=[2,4,8,9,10,11,12,13,16,19,20,75,92,93,94,95,96,102,103,104,105,106,107,108,109,110,111,115,116,132,133,134,150,151,152,153,154,163]
Path('.research/full').mkdir(exist_ok=True)
def run(i):
 item=d[i]; url=re.sub(r'([?&])cs=[^&]+',r'\1',item['url']).rstrip('&')
 if 'market_thumb' in url:
  s=BeautifulSoup(Path('.research/mirror.html').read_text(encoding='utf-8'),'html.parser');el=s.find('img',src=item['url']); card=el.find_parent(class_='product-item')
  if not card:card=el.parent.parent
  link=card.select_one('a[href^="/product/"]')
  if link:
   item['source']='https://kinderparty-nv.orgs.biz'+link['href']
   html=requests.get(item['source'],timeout=20).text;Path(f'.research/product-{i}.html').write_text(html,encoding='utf-8');ps=BeautifulSoup(html,'html.parser');imgs=ps.select('img');url=next((im['src'] for im in imgs if item['url'].split('?')[0] in im.get('src','')),url)
   url=re.sub(r'([?&])cs=[^&]+',r'\1',url).rstrip('&')
 try:
  r=requests.get(url,timeout=20);r.raise_for_status();p=Path(f'.research/full/{i:03d}.jpg');p.write_bytes(r.content);im=Image.open(p);item['fullUrl']=url;item['fullSize']=im.size;print(i,im.size)
 except Exception as e:print(i,str(e)[:60])
 return item
out=list(ThreadPoolExecutor(max_workers=6).map(run,selected));Path('.research/full-index.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
