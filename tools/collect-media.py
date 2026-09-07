from pathlib import Path
from bs4 import BeautifulSoup
import requests, json, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps, ImageDraw

root=Path('.research'); (root/'media').mkdir(exist_ok=True)
soup=BeautifulSoup((root/'mirror.html').read_text(encoding='utf-8'),'html.parser')
items=[]; seen=set()
for img in soup.select('img'):
    url=img.get('src',''); alt=img.get('alt','')
    if 'userapi' not in url or url in seen: continue
    seen.add(url)
    parent=img.find_parent('a'); href=parent.get('href','') if parent else ''
    items.append(dict(url=url,alt=alt,source='https://kinderparty-nv.orgs.biz'+href if href.startswith('/') else 'https://kinderparty-nv.orgs.biz/'))
soup=BeautifulSoup((root/'vk-browser.html').read_text(encoding='utf-8'),'html.parser')
for post in soup.select('[data-post-id][id^="post-"]'):
    for el in post.select('[style]'):
        for url in re.findall(r'url\((https[^)]+)\)',el.get('style','')):
            if url in seen or 'video_thumb' not in url: continue
            seen.add(url); items.append(dict(url=url,alt='Кадр публикации '+post['data-post-id'],source='https://vk.ru/wall'+post['data-post-id']))
def download(pair):
    i,item=pair; item['id']=i; p=root/'media'/f'{i:03d}.jpg'
    try:
        if not p.exists():
            r=requests.get(item['url'],timeout=20);r.raise_for_status();p.write_bytes(r.content)
        im=Image.open(p);item['size']=im.size;return item
    except Exception as e:item['error']=str(e);return item
items=list(ThreadPoolExecutor(max_workers=8).map(download,enumerate(items)))
(root/'media-index.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
valid=[i for i in items if 'error' not in i]
for start in range(0,len(valid),40):
    batch=valid[start:start+40]; sheet=Image.new('RGB',(1000,((len(batch)+4)//5)*190),'#faf7f2');draw=ImageDraw.Draw(sheet)
    for n,item in enumerate(batch):
        im=Image.open(root/'media'/f"{item['id']:03d}.jpg"); im.thumbnail((190,156));x=(n%5)*200;y=(n//5)*190;sheet.paste(im,(x+(190-im.width)//2,y));draw.text((x+5,y+158),str(item['id']),fill='black')
    sheet.save(root/f'contact-{start//40}.jpg')
print(json.dumps([{'id':i['id'],'alt':i['alt'],'size':i.get('size'),'error':i.get('error')} for i in items],ensure_ascii=False))
