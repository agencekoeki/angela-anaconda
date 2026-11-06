"""Pour chaque plan non procédural : la hauteur à l'écran du plus grand humain (part de l'écran), et la place de sa tête."""
import importlib, os, sys
os.environ['SANS_ASSERT'] = '1'
ICI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ICI); os.chdir(ICI)
m = importlib.import_module(sys.argv[1])
from PIL import Image
HUM = {'seb', 'diana', 'kristina', 'boulanger'}
def vis(img):
    if isinstance(img, tuple):
        im = Image.open(img[1]); bb = im.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox()
        return (bb[3] - bb[1]) / im.height
    return 1.0
for i, p in enumerate(m.plans, 1):
    if p.fond or p.carte: continue
    z = (p.zoom[0] + p.zoom[1]) / 2
    best = None
    for a in p.acteurs:
        if a.gros_plan or a.nom not in HUM: continue
        img = a.poses[0][1] if a.poses else a.image
        hs = a.h * z * vis(img)
        top = (a.y - a.h * vis(img) - (p.cam_y - 0.5 / z)) * z        # haut de la tête, en part de l'écran
        if best is None or hs > best[0]: best = (hs, top, a.nom)
    if best:
        print(f'{i:2d} zoom {z:.2f} cam_y {p.cam_y:.3f}  plus grand : {best[2]:9s} {best[0]:.2f} de l\'écran, tête à {best[1]:.2f}', '  <<< PETIT' if best[0] < 0.6 else '')
