import sys, film
from moteur import dessiner_plan
from PIL import Image
plans = film.plans
sel = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else range(len(plans))
ks = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [0.15, 0.5, 0.85]
ims = []
for i in sel:
    p = plans[i]
    for k in ks:
        ims.append((f'p{i:02d}-{int(k*100)}', dessiner_plan(p, p.duree * k)))
w, h = 640, 360; cols = min(3, len(ks))
c = Image.new('RGB', (w * cols, (h + 20) * ((len(ims) + cols - 1) // cols)))
from PIL import ImageDraw
d = ImageDraw.Draw(c)
for j, (n, im) in enumerate(ims):
    x, y = (j % cols) * w, (j // cols) * (h + 20)
    c.paste(im.resize((w, h)), (x, y + 20)); d.text((x + 4, y + 4), n, fill=(255, 255, 0))
c.save(sys.argv[3] if len(sys.argv) > 3 else '/tmp/claude-0/-home-claude/99710d10-c167-57a1-903a-3129e7324f27/scratchpad/cles.jpg', quality=85)
print('ok')
