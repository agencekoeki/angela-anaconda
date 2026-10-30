"""Découpe une planche dont les poses se chevauchent en x mais ne se touchent pas :
une pose = une composante connexe (plus son halo doux). Chaque pose garde sa
hauteur d'origine dans la planche (un saut garde sa courbe), centrée en x sur
son centre de masse, sur une toile commune.

Usage : python3 planche_composantes.py planche.png prefixe [--n 4]
"""
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('prefixe'); ap.add_argument('--n', type=int, default=4)
ap.add_argument('--ancre', default='centre', help="'centre' (centre de masse) ou 'arriere' : les pattes arrière restent en place (un étirement, une révérence)")
a = ap.parse_args()
im = np.asarray(Image.open(a.src).convert('RGBA'))
m = im[..., 3] > 60
lab, n = ndimage.label(m, structure=np.ones((3, 3)))
s = ndimage.sum(m, lab, range(1, n + 1))
ks = [int(k) + 1 for k in np.argsort(-s)[:a.n]]
ks.sort(key=lambda k: np.where(lab == k)[1].mean())
W = max(np.ptp(np.where(lab == k)[1]) for k in ks) * (2 if a.ancre == 'arriere' else 1) + 80
for i, k in enumerate(ks):
    zone = ndimage.binary_dilation(lab == k, iterations=4) & (im[..., 3] > 0)
    # le halo ne doit pas mordre sur une autre pose
    zone &= ~np.isin(lab, [j for j in ks if j != k])
    p = im.copy(); p[~zone, 3] = 0
    ys_k, xs_k = np.where(lab == k)
    if a.ancre == 'arriere':
        # les pieds arrière : le point le plus à gauche des dernières rangées de la pose (elle regarde à droite)
        bas = ys_k >= ys_k.max() - (ys_k.max() - ys_k.min()) * 0.08
        cx = xs_k[bas].min() + W * 0.25
    else:
        cx = xs_k.mean()
    t = np.zeros((im.shape[0], W, 4), np.uint8)
    x0 = int(cx - W / 2)
    src_x0, src_x1 = max(0, x0), min(im.shape[1], x0 + W)
    t[:, src_x0 - x0: src_x1 - x0] = p[:, src_x0:src_x1]
    Image.fromarray(t, 'RGBA').save(f'{a.prefixe}-{i + 1}.png')
print(len(ks), 'poses', W, im.shape[0])
