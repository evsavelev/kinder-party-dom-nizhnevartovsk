from pathlib import Path
from PIL import Image,ImageOps
from bs4 import BeautifulSoup
import json,re,requests
out=Path('assets/images');out.mkdir(parents=True,exist_ok=True)
d=json.loads(Path('.research/media-index.json').read_text(encoding='utf-8'))
full={i['id']:i for i in json.loads(Path('.research/full-index.json').read_text(encoding='utf-8'))}
selection={115:'hero-paper',102:'family-party',110:'party-games',92:'bubble-show',93:'bubble-ring',94:'bubble-interactive',151:'robots',4:'challenge-party',133:'taba-workshop',2:'play-zone',19:'party-table',107:'venue-celebration',111:'venue-games',8:'labubu',12:'kuromi',9:'magic-heroes',10:'harry',11:'panda',20:'bunny',13:'dragon',16:'elsa',75:'graduation',103:'birthday-friends',104:'birthday-table',105:'birthday-girls',108:'characters-party',109:'cat-party',116:'paper-show',132:'glitter',134:'paper-dance',150:'new-year',152:'outdoor-party',153:'friends',154:'party-audience',163:'city-archive',136:'logo'}
manifest=[]
for i,name in selection.items():
 item=full.get(i,d[i]);p=Path(f'.research/full/{i:03d}.jpg');p=p if p.exists() else Path(f'.research/media/{i:03d}.jpg');im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
 if name=='logo':
  url=re.sub(r'([?&])cs=[^&]+',r'\1',item['url']).rstrip('&')
  try:r=requests.get(url,timeout=15);r.raise_for_status();p=Path('.research/logo.jpg');p.write_bytes(r.content);im=Image.open(p).convert('RGB')
  except Exception:pass
 im.thumbnail((1400,1600));im.save(out/f'{name}.webp','WEBP',quality=82,method=6)
 large=im.size
 if im.width>640:
  im.thumbnail((640,960));im.save(out/f'{name}-640.webp','WEBP',quality=78,method=6)
 source=item['source']
 if '/news/' in source:source='https://vk.ru/wall-106473815_'+source.rsplit('/',1)[1]
 if i in [103,104,105,106,107,108,109,110,111]:source='https://vk.ru/wall-106473815_2224'
 manifest.append({'file':f'assets/images/{name}.webp','width':large[0],'height':large[1],'source':source,'discoveredVia':item['source'],'cdn':item.get('fullUrl',item['url']),'note':item['alt']})
# Real preview frame from the company's VR post; preserve content, no synthetic scene.
soup=BeautifulSoup(Path('.research/post-2386.html').read_text(encoding='utf-8'),'html.parser')
url=next(re.search(r'url\(([^)]+)\)',el['style']).group(1) for el in soup.select('[style]') if 'M7sv4msjxN8' in el['style'])
r=requests.get(url,timeout=20);r.raise_for_status();Path('.research/vr.jpg').write_bytes(r.content);im=Image.open('.research/vr.jpg').convert('RGB');im.save(out/'vr-party.webp','WEBP',quality=84)
manifest.append({'file':'assets/images/vr-party.webp','width':im.width,'height':im.height,'source':'https://vk.ru/wall-106473815_2386','cdn':url,'note':'Кадр VR-публикации компании'})
Path('assets/media-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
# Self-host licensed Manrope; keep original OFL license.
fonts=Path('assets/fonts');fonts.mkdir(exist_ok=True)
url='https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf'
r=requests.get(url,timeout=25);r.raise_for_status();(fonts/'Manrope.ttf').write_bytes(r.content)
from fontTools.ttLib import TTFont
f=TTFont(fonts/'Manrope.ttf');f.flavor='woff2';f.save(fonts/'manrope.woff2');(fonts/'Manrope.ttf').unlink()
r=requests.get('https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/OFL.txt',timeout=20);r.raise_for_status();(fonts/'OFL.txt').write_text(r.text,encoding='utf-8')
print('Prepared',len(manifest),'real assets;',sum(p.stat().st_size for p in out.glob('*.webp')),'bytes')
