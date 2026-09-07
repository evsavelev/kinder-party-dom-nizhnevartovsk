from pathlib import Path
from PIL import Image
import requests,json
url='https://pp.userapi.com/c855736/v855736668/570b/SP-1IO_8s9w.jpg'
r=requests.get(url,timeout=20);r.raise_for_status();Path('.research/teen-party.jpg').write_bytes(r.content);im=Image.open('.research/teen-party.jpg').convert('RGB');im.thumbnail((1400,1600));size=im.size;im.save('assets/images/teen-party.webp','WEBP',quality=82)
if im.width>640:im.thumbnail((640,960));im.save('assets/images/teen-party-640.webp','WEBP',quality=78)
p=Path('assets/media-manifest.json');data=json.loads(p.read_text(encoding='utf-8'));data=[x for x in data if x['file']!='assets/images/teen-party.webp'];data.append({'file':'assets/images/teen-party.webp','width':size[0],'height':size[1],'source':'https://kinderparty-nv.orgs.biz/#galley','cdn':url,'note':'Групповой кадр подросткового праздника из фотоальбома компании; не документирует конкретную программу «Сможешь Пати».'});p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
p=Path('tools/build.mjs');s=p.read_text(encoding='utf-8')
s=s.replace("image:'party-audience',alt:'Гости одного из праздников Киндер Пати Дом'","image:'teen-party',alt:'Компания подростков на празднике из фотоальбома Киндер Пати Дом'")
s=s.replace("alt:'Сквиш-лапка на ладони участника мастер-класса'","alt:'Блестящая татуировка в виде лапки — дополнение к празднику'")
s=s.replace('${p.kind}</span></div><div class="program-info">','${p.kind}</span>${p.id===\'taba\'?\'<span class="photo-note">На фото — блестящая татуировка</span>\':\'\'}</div><div class="program-info">')
s=s.replace("${gallery('venue-celebration','Место встречи с любимыми героями')}","${gallery('venue-celebration','Встреча с героями')}${gallery('birthday-table','Гости за праздничным столом')}")
s=s.replace("img('outdoor-party','Артисты Киндер Пати Дом проводят праздник на улице')","img('outdoor-party','Артисты Киндер Пати Дом в образах скомороха и Марфуши')")
p.write_text(s,encoding='utf-8')
print('Teen image:',size)
