"""Pantin à têtes de rechange : pose une tête (expression ou bouche) sur un corps.

C'est la technique de la série : un corps en papier découpé, et des têtes
photographiques qu'on échange. Ici, le corps est une découpe en pied (PNG
transparent) et la tête vient d'un gros plan tête-et-cou, détouré lui aussi.

geom_corps(img)  -> la boîte de la tête dans le corps (haut du crâne, cou, x0, x1)
geom_tete(img)   -> la même chose dans un gros plan (le cou est la rangée la plus
                    étroite dans le bas de l'image)
poser(corps, tete) -> le corps avec la nouvelle tête, à la même taille et au même
                    endroit que l'ancienne, l'ancienne tête effacée
"""
from functools import lru_cache

import numpy as np
from PIL import Image


def _profil(img):
    m = np.asarray(img.getchannel('A')) > 128
    rows = np.where(m.any(1))[0]
    larg = m.sum(1).astype(float)
    k = max(3, (rows[-1] - rows[0]) // 200)
    return m, rows, np.convolve(larg, np.ones(k) / k, mode='same')


def geom_corps(img):
    m, rows, larg = _profil(img)
    haut, bas = rows[0], rows[-1]; H = bas - haut
    z = larg[haut: haut + int(H * 0.40)]
    d = int(H * 0.12)
    i_cou = d + int(np.argmin(z[d:]))
    cou = haut + i_cou
    cols = np.where(m[haut:cou].any(0))[0]
    # le centre de la tête : le milieu de la rangée la plus large du crâne
    i_max = int(np.argmax(z[:i_cou])); r = np.where(m[haut + i_max])[0]
    return dict(haut=int(haut), cou=int(cou), x0=int(cols.min()), x1=int(cols.max()),
                cx=float((r.min() + r.max()) / 2), larg=float(z[i_max]))


def geom_tete(img):
    m, rows, larg = _profil(img)
    haut, bas = rows[0], rows[-1]; H = bas - haut
    a, b = haut + int(H * 0.55), haut + int(H * 0.95)
    cou = a + int(np.argmin(larg[a:b]))
    i_max = haut + int(np.argmax(larg[haut:cou]))
    r = np.where(m[i_max])[0]
    return dict(haut=int(haut), cou=int(cou), cx=float((r.min() + r.max()) / 2), larg=float(larg[i_max]))


@lru_cache(maxsize=64)
def charger(chemin):
    return Image.open(chemin).convert('RGBA')


@lru_cache(maxsize=48)
def poser(chemin_corps, chemin_tete, echelle=1.0, sans_bras=False):
    corps = charger(chemin_corps).copy()
    tete = charger(chemin_tete)
    gc, gt = geom_corps(corps), geom_tete(tete)
    s = gc['larg'] / gt['larg'] * echelle
    # 1. la nouvelle tête : du crâne jusque bien sous le cou du gros plan (le col
    #    du corps passera par-dessus), sans le vêtement du gros plan
    hc = gt['cou'] - gt['haut']
    crop = tete.crop((0, gt['haut'], tete.width, min(tete.height, gt['cou'] + int(hc * 0.22))))
    c = np.asarray(crop).copy(); hh = c.shape[0]
    rgb = c[..., :3].astype(int); mx = rgb.max(-1); mn = rgb.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1)
    bas = np.zeros_like(sat, dtype=bool); bas[int(hh * 0.70):] = True
    c[bas & (sat > 0.30) & (mx > 90), 3] = 0
    f0 = int(hh * 0.94)
    c[f0:, :, 3] = (c[f0:, :, 3] * np.linspace(1, 0, hh - f0)[:, None]).astype(np.uint8)
    crop = Image.fromarray(c, 'RGBA')
    crop = crop.resize((max(1, round(crop.width * s)), max(1, round(crop.height * s))), Image.LANCZOS)
    # 2. le vêtement du corps = seulement ses couleurs franches ET claires (le rose
    #    du t-shirt), jamais les pixels sombres de l'ancienne barbe
    a = np.asarray(corps).copy()
    a[a[..., 3] < 40, 3] = 0                      # poussières de détourage
    rgb = a[..., :3].astype(int); mx = rgb.max(-1); mn = rgb.min(-1)
    satc = (mx - mn) / np.maximum(mx, 1)
    opaque = a[..., 3] > 30
    vet = (satc >= 0.45) & (mx >= 120) & opaque
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    # le haut du col : première rangée sous le cou où le vêtement passe au centre
    cxi = int(gc['cx']); bande = slice(max(0, cxi - 6), cxi + 6)
    y_col = gc['cou']
    for y in range(gc['cou'], min(a.shape[0], gc['cou'] + (gc['cou'] - gc['haut']))):
        if vet[y, bande].mean() > 0.5:
            y_col = y; break
    # 3. effacer TOUTE l'ancienne tête et l'ancien cou (tout ce qui n'est pas vêtement)
    #    jusqu'au col ; sur un corps qui a encore ses bras, on épargne ce qui est
    #    loin du crâne (une main levée près du visage)
    zone = (yy < y_col + 3) & ~vet
    if not sans_bras:
        ry = (gc['cou'] - gc['haut']) / 2 + 30; cy = (gc['cou'] + gc['haut']) / 2
        rx = gc['larg'] / 2 + 45
        ell = ((xx - gc['cx']) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0
        cou_bande = (yy >= gc['cou'] - 10) & (np.abs(xx - gc['cx']) < gc['larg'] * 0.30)
        zone &= (ell | cou_bande)
    a[zone, 3] = 0
    corps = Image.fromarray(a, 'RGBA')
    dessus = np.zeros_like(a)
    col = vet & (yy >= gc['cou'] - (gc['cou'] - gc['haut']) * 0.15)
    from scipy import ndimage
    col = ndimage.binary_opening(col, iterations=2)   # pas de points isolés au bord du col
    dessus[col] = a[col]
    dessus = Image.fromarray(dessus, 'RGBA')
    # 4. poser la tête, puis remettre le col PAR-DESSUS le cou
    dx = round(gc['cx'] - gt['cx'] * s); dy = round(gc['haut'])
    pad_t = max(0, -dy); pad_l = max(0, -dx); pad_r = max(0, dx + crop.width - corps.width)
    pad_b = max(0, dy + crop.height - corps.height)
    if pad_t or pad_l or pad_r or pad_b:
        def agrandir(im):
            n = Image.new('RGBA', (im.width + pad_l + pad_r, im.height + pad_t + pad_b)); n.paste(im, (pad_l, pad_t)); return n
        corps = agrandir(corps); dessus = agrandir(dessus); dx += pad_l; dy += pad_t
    corps.alpha_composite(crop, (dx, dy))
    corps.alpha_composite(dessus)
    return corps
