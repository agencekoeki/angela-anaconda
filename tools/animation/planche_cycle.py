"""Découpe une planche de cycle (marche, trot) en images séparées, alignées sur une même ligne de sol.

Usage : python3 planche_cycle.py planche.png sortie_prefixe [--n 4] [--vert]

La planche est une rangée de N poses côte à côte, sur fond vert uni ou transparent.
Chaque pose est isolée par ses composantes connexes, puis recadrée à la même
hauteur de toile, pieds sur la même ligne, et centrée sur son centre de masse :
ainsi l'image ne « saute » pas d'une pose à l'autre quand on les enchaîne.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('prefixe'); ap.add_argument('--n', type=int, default=4)
a = ap.parse_args()

im = Image.open(a.src).convert('RGBA')
al = np.asarray(im)[..., 3]
if al.min() > 250:      # fond vert : on détoure d'abord
    tmp = Path(a.prefixe + '-detoure.png')
    subprocess.run([sys.executable, str(Path(__file__).parent.parent / 'detourage.py'), a.src, str(tmp)], check=True)
    im = Image.open(tmp).convert('RGBA'); al = np.asarray(im)[..., 3]
m = al > 60
# regrouper les composantes en N colonnes : la projection verticale sépare les poses
col = m.any(0).astype(int)
lab, n = ndimage.label(col)
spans = [(np.where(lab == k)[0].min(), np.where(lab == k)[0].max()) for k in range(1, n + 1)]
spans = [s for s in spans if s[1] - s[0] > im.width * 0.03]
if len(spans) != a.n:
    # des poses se touchent : on coupe en N parts égales entre le premier et le dernier pixel
    xs = np.where(col)[0]; x0, x1 = xs.min(), xs.max(); w = (x1 - x0) / a.n
    spans = [(int(x0 + i * w), int(x0 + (i + 1) * w)) for i in range(a.n)]
poses = []
for (x0, x1) in spans:
    sub = im.crop((max(0, x0 - 60), 0, min(im.width, x1 + 61), im.height))
    sa = np.asarray(sub).copy(); mm = sa[..., 3] > 60
    lab2, n2 = ndimage.label(mm, structure=np.ones((3, 3)))
    if n2 > 1:
        # garder la pose : la plus grande forme, et ce qui la touche presque (poils, moustaches)
        tailles = ndimage.sum(mm, lab2, range(1, n2 + 1)); k = int(np.argmax(tailles)) + 1
        proche = ndimage.binary_dilation(lab2 == k, iterations=6)
        garder = np.isin(lab2, np.unique(lab2[proche & mm]))
        sa[~garder, 3] = 0
    sub = Image.fromarray(sa, 'RGBA')
    bb = sub.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox()
    poses.append(sub.crop(bb))
H = max(p.height for p in poses)
# la toile doit contenir le bras le plus tendu une fois la pose centrée sur son centre de masse
cxs = [np.where(np.asarray(p)[..., 3] > 60)[1].mean() for p in poses]
W = int(max(2 * max(c, p.width - c) for c, p in zip(cxs, poses))) + 40
for i, p in enumerate(poses):
    t = Image.new('RGBA', (W, H))
    cx = cxs[i]
    t.paste(p, (int(W / 2 - cx), H - p.height), p)
    t.save(f'{a.prefixe}-{i + 1}.png')
print(len(poses), 'poses', W, H)
