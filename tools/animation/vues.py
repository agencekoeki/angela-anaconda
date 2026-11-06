"""python3 vues.py module 'plan:k,plan:k' sortie.jpg — images choisies, côte à côte, à la demi-taille."""
import importlib, sys, os
ICI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ICI); os.chdir(ICI)
os.environ.setdefault('SANS_ASSERT', '1')
m = importlib.import_module(sys.argv[1])
from PIL import Image
vs = [(int(a), float(b)) for a, b in (x.split(':') for x in sys.argv[2].split(','))]
ims = [m.dessiner_plan(m.plans[i - 1], m.plans[i - 1].duree * k).convert('RGB').resize((432, 768)) for i, k in vs]
c = Image.new('RGB', (432 * min(5, len(ims)), 768 * ((len(ims) + 4) // 5)))
for j, im in enumerate(ims):
    c.paste(im, ((j % 5) * 432, (j // 5) * 768))
c.save(sys.argv[3], quality=85)
