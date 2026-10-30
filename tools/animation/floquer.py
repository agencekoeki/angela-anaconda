"""Poser un flocage (un imprimé de la boutique SEO Addict) sur le t-shirt rose de Sébastien, dans une pose de face.

Le t-shirt reste rose (règle de l'univers) : seul l'imprimé s'ajoute, et il prend les plis du tissu.
    from floquer import floquer
    sprite_floque = floquer(sprite_rgba, chemin_png_du_flocage)       # None si la pose ne montre pas le devant
La place se trouve toute seule : la plus grande tache rose fuchsia, les rangées où elle est large (le buste),
l'imprimé centré en haut du buste, à 55 % de sa largeur.
"""
from functools import lru_cache

import numpy as np
from PIL import Image
from scipy import ndimage

# poses où l'on voit le devant du t-shirt (préfixes de nom de fichier)
POSES_DE_FACE = ('seb-discours', 'seb-cles', 'seb-m0', 'seb-s2', 'seb-k00')


def masque_tshirt(a):
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mx = a[..., :3].max(-1); mn = a[..., :3].min(-1)
    s = (mx - mn) / np.maximum(mx, 1e-6)
    rose = (al > 0.5) & (r > 0.55) & (b > 0.25) & (g < 0.45) & (s > 0.45) & (r > b)
    lab, n = ndimage.label(ndimage.binary_closing(rose, iterations=2))
    if n == 0:
        return None
    k = 1 + int(np.argmax(ndimage.sum(rose, lab, range(1, n + 1))))
    return lab == k


@lru_cache(maxsize=8)
def _flocage(chemin):
    im = Image.open(chemin).convert('RGBA')
    return im.crop(im.getchannel('A').getbbox())


def place(m):
    """(cx, haut, largeur_buste, hauteur_buste) en pixels, ou None."""
    larg = m.sum(1)
    if larg.max() < 10:
        return None
    rangs = np.nonzero(larg >= 0.6 * larg.max())[0]
    y0, y1 = rangs.min(), rangs.max()
    xs = np.nonzero(m[y0:y1 + 1].any(0))[0]
    lt = float(np.median(larg[rangs]))
    cx = float(np.median(np.nonzero(m[(y0 + y1) // 2])[0]))
    return cx, y0, lt, y1 - y0


def floquer(spr, chemin, part=0.55):
    a = np.asarray(spr).astype(np.float32) / 255
    m = masque_tshirt(a)
    if m is None or m.sum() < 400:
        return None
    pl = place(m)
    if not pl:
        return None
    cx, y0, lt, ht = pl
    fl = _flocage(chemin)
    w = max(4, int(lt * part)); h = max(4, int(fl.height * w / fl.width))
    if h > ht * 0.75:                                   # un imprimé haut ne descend pas sous la ceinture
        h = int(ht * 0.75); w = int(fl.width * h / fl.height)
    f = np.asarray(fl.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
    x0 = int(cx - w / 2); yy0 = int(y0 + ht * 0.16)
    out = a.copy()
    H, W = m.shape
    sx0, sy0 = max(0, x0), max(0, yy0); sx1, sy1 = min(W, x0 + w), min(H, yy0 + h)
    if sx1 <= sx0 or sy1 <= sy0:
        return None
    fz = f[sy0 - yy0:sy1 - yy0, sx0 - x0:sx1 - x0]
    zone = out[sy0:sy1, sx0:sx1]
    # les plis : la lumière du tissu sous l'imprimé, rapportée à sa moyenne
    lum = zone[..., :3].mean(-1)
    pli = np.clip((lum / max(1e-3, float(lum[m[sy0:sy1, sx0:sx1]].mean() if m[sy0:sy1, sx0:sx1].any() else 1))) ** 0.7, 0.6, 1.25)
    al = fz[..., 3] * m[sy0:sy1, sx0:sx1]                # l'imprimé ne sort pas du t-shirt
    for c in range(3):
        zone[..., c] = zone[..., c] * (1 - al) + np.clip(fz[..., c] * pli, 0, 1) * al
    out[sy0:sy1, sx0:sx1] = zone
    return Image.fromarray((out * 255).astype(np.uint8), 'RGBA')
