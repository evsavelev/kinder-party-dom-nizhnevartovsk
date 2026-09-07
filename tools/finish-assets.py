from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
p=Path('tools/build.mjs');s=p.read_text(encoding='utf-8')
s=s.replace('<span class="brand-symbol" aria-hidden="true">к<span>п</span>д</span>','<img class="brand-logo" src="assets/images/logo.webp" alt="" width="64" height="44">')
s=s.replace('2ГИС · отзыв родителя','2ГИС · отзыв о компании')
s=s.replace(')} ">',')}">')
p.write_text(s,encoding='utf-8')
im=Image.open('assets/images/family-party.webp');ImageOps.fit(im,(1200,630),centering=(.5,.38)).save('assets/og-image.jpg',quality=85)
im=Image.new('RGB',(180,180),'#a72b50');d=ImageDraw.Draw(im)
d.line([(56,42),(56,138)],fill='#faf7f2',width=18);d.line([(60,91),(126,42)],fill='#faf7f2',width=18);d.line([(60,91),(126,138)],fill='#faf7f2',width=18)
im.save('assets/apple-touch-icon.png');im.resize((64,64)).save('assets/favicon.png')
