"""Verify exact published assets, status codes and custom 404 without sending messages."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,hashlib,json,datetime
base='https://evsavelev.github.io/kinder-party-dom-nizhnevartovsk/'
files=['index.html','robots.txt','sitemap.xml','404.html','assets/styles.css','assets/app.js','assets/favicon.svg','assets/favicon.png','assets/apple-touch-icon.png','assets/og-image.jpg','assets/fonts/manrope.woff2']
files += [str(p).replace('\\','/') for p in Path('assets/images').glob('*.webp')]
def check(name):
    url=base+('' if name=='index.html' else name)
    r=requests.get(url,timeout=30)
    normalized=lambda b:b.replace(b'\r\n',b'\n') if name.endswith(('.html','.css','.js','.txt','.xml','.svg')) else b
    match=hashlib.sha256(normalized(r.content)).hexdigest()==hashlib.sha256(normalized(Path(name).read_bytes())).hexdigest()
    return {'file':name,'status':r.status_code,'matchesLocal':match}
results=list(ThreadPoolExecutor(max_workers=6).map(check,files))
notfound=requests.get(base+'missing-page-qa',timeout=30)
report={'url':base,'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':results,'custom404':notfound.status_code==404 and 'Эта страница не нашлась.'.encode() in notfound.content}
Path('.research/public-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
failed=[r for r in results if r['status']!=200 or not r['matchesLocal']]
print(json.dumps({'checked':len(results),'failed':failed,'custom404':report['custom404']},ensure_ascii=False))
if failed or not report['custom404']:raise SystemExit(1)
