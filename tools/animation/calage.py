"""Calage d'une cible dans un décor : retrouver le rectangle exact d'une vitre d'écran, d'une fenêtre, d'un cadre…

Le moteur pose des choses DANS le décor (la lueur d'un écran allumé, Tara derrière la vitre). Si le rectangle
déclaré dans le script est approximatif, la lueur déborde sur le plastique de l'écran, ou laisse un liseré de
vitre éteinte. Ce module retrouve le vrai rectangle à partir d'une estimation :

    from calage import detecter_zone
    detecter_zone(chemin_decor, (x0, y0, x1, y1))   -> (x0, y0, x1, y1) en fraction du décor, et un indice de confiance

Méthode : autour de l'estimation (élargie de 60 %), on prend la luminance, on sépare le sombre du clair par la
méthode d'Otsu, on garde la tache sombre qui contient le centre de l'estimation, et on en prend la boîte. Ça marche
pour une zone nettement plus sombre (ou plus claire, `sombre=False`) que son cadre : vitre d'écran, fenêtre de nuit,
tableau noir, porte ouverte.

En ligne de commande :
    python3 calage.py decor.png x0,y0,x1,y1 [x0,y0,x1,y1 …] [--vue sortie.jpg]
écrit les rectangles retrouvés, et une vue où l'estimation est en orange et le rectangle retrouvé en vert.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


def _otsu(v):
    h, b = np.histogram(v, bins=64, range=(0, 255))
    c = (b[:-1] + b[1:]) / 2
    w = np.cumsum(h); m = np.cumsum(h * c)
    tot, mt = w[-1], m[-1]
    w1 = tot - w
    var = np.where((w > 0) & (w1 > 0), (mt * w - m * tot) ** 2 / np.maximum(w * w1, 1), 0)
    return c[int(np.argmax(var))]


def detecter_zone(decor, rect, marge=0.6, sombre=True):
    im = Image.open(decor).convert('L') if isinstance(decor, str) else decor.convert('L')
    W, H = im.size
    x0, y0, x1, y1 = rect
    w, h = x1 - x0, y1 - y0
    bx0, by0 = max(0, x0 - w * marge), max(0, y0 - h * marge)
    bx1, by1 = min(1, x1 + w * marge), min(1, y1 + h * marge)
    px0, py0, px1, py1 = int(bx0 * W), int(by0 * H), int(bx1 * W), int(by1 * H)
    a = np.asarray(im)[py0:py1, px0:px1].astype(np.float32)
    a = ndimage.gaussian_filter(a, 1.5)
    seuil = _otsu(a)
    m = a < seuil if sombre else a > seuil
    m = ndimage.binary_opening(m, iterations=2)
    lab, n = ndimage.label(m)
    cy, cx = int(((y0 + y1) / 2) * H) - py0, int(((x0 + x1) / 2) * W) - px0
    k = lab[min(max(cy, 0), lab.shape[0] - 1), min(max(cx, 0), lab.shape[1] - 1)]
    if k == 0:
        return None, 0.0
    ys, xs = np.nonzero(lab == k)
    r = ((xs.min() + px0) / W, (ys.min() + py0) / H, (xs.max() + 1 + px0) / W, (ys.max() + 1 + py0) / H)
    # confiance : la tache remplit-elle bien sa boîte (un rectangle), et ne touche-t-elle pas le bord de la recherche ?
    remplissage = (lab == k).sum() / max(1, (xs.max() - xs.min() + 1) * (ys.max() - ys.min() + 1))
    touche = xs.min() == 0 or ys.min() == 0 or xs.max() == lab.shape[1] - 1 or ys.max() == lab.shape[0] - 1
    return r, float(remplissage) * (0.5 if touche else 1.0)


def ecart(a, b, decor_taille):
    """Le plus grand écart entre deux rectangles, en pixels du décor."""
    W, H = decor_taille
    return max(abs(a[0] - b[0]) * W, abs(a[2] - b[2]) * W, abs(a[1] - b[1]) * H, abs(a[3] - b[3]) * H)


if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    vue = sys.argv[sys.argv.index('--vue') + 1] if '--vue' in sys.argv else None
    decor = args[0]
    rects = [tuple(float(v) for v in s.split(',')) for s in args[1:] if s != vue]
    im = Image.open(decor).convert('RGB'); d = ImageDraw.Draw(im); W, H = im.size
    for r in rects:
        t, conf = detecter_zone(decor, r)
        print('estimé', tuple(round(v, 3) for v in r), '-> retrouvé', tuple(round(v, 3) for v in t) if t else None,
              f'confiance {conf:.2f}', f'écart {ecart(r, t, (W, H)):.0f} px' if t else '')
        d.rectangle([r[0] * W, r[1] * H, r[2] * W, r[3] * H], outline=(255, 150, 0), width=2)
        if t:
            d.rectangle([t[0] * W, t[1] * H, t[2] * W, t[3] * H], outline=(0, 255, 0), width=2)
    if vue:
        im.save(vue, quality=90)
