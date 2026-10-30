"""Découpe une planche de N poses qui se touchent (cheveux, queues) : chaque frontière passe
au creux de densité le plus proche du découpage régulier, sans marge qui mordrait sur la voisine.
Poses calées sur la même ligne de sol, centrées sur une toile commune.

Usage : python3 planche_creux.py planche_detouree.png prefixe [--n 4]
"""
import argparse
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('prefixe'); ap.add_argument('--n', type=int, default=4)
a = ap.parse_args()
im = Image.open(a.src).convert('RGBA'); al = np.asarray(im)[..., 3]
col = (al > 60).sum(0).astype(float); xs = np.where(col > 0)[0]; x0, x1 = xs.min(), xs.max(); w = (x1 - x0) / a.n
cuts = [x0]
for k in range(1, a.n):
    c = int(x0 + k * w); lo, hi = c - int(w * 0.25), c + int(w * 0.25)
    cuts.append(lo + int(np.argmin(col[lo:hi])))
cuts.append(x1 + 1)
poses = []
for i in range(a.n):
    sub = im.crop((cuts[i], 0, cuts[i + 1], im.height))
    bb = sub.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox(); poses.append(sub.crop(bb))
H = max(p.height for p in poses); W = max(p.width for p in poses) + 40
for i, p in enumerate(poses):
    t = Image.new('RGBA', (W, H)); t.paste(p, ((W - p.width) // 2, H - p.height), p); t.save(f'{a.prefixe}-{i + 1}.png')
print(a.n, 'poses', W, H, 'coupes', cuts)
