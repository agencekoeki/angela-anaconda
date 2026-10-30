"""Pantin articulé : un corps sans bras, et deux bras qui pivotent à l'épaule.

Comme les marionnettes de papier de la série : chaque bras est une pièce raide
(sans coude, comme un cure-pipe), épinglée dans la manche et tournée autour de
l'épaule. Les angles se donnent « vers l'extérieur » : 0 = bras le long du
corps, 90 = bras tendu à l'horizontale vers l'extérieur, 170 = bras levé.
Un angle négatif ramène le bras devant le corps (vers l'intérieur).
"""
from functools import lru_cache

import numpy as np
from PIL import Image

import pantin


@lru_cache(maxsize=8)
def kit(corps, bras_g, bras_d):
    c = pantin.charger(corps)
    a = np.asarray(c)
    rgb = a[..., :3].astype(int); mx = rgb.max(-1); mn = rgb.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1)
    rose = (sat > 0.5) & (a[..., 3] > 128) & (rgb[..., 0] > 150) & (rgb[..., 1] < 120)
    ys, xs = np.where(rose)
    y0, y1 = ys.min(), ys.max()
    # la rangée la plus large du haut du t-shirt = le bas des manches
    larg = [(np.where(rose[y])[0].max() - np.where(rose[y])[0].min()) if rose[y].any() else 0 for y in range(y0, y0 + (y1 - y0) // 2)]
    y_manche = y0 + int(np.argmax(larg))
    r = np.where(rose[y_manche])[0]
    # le torse sous les manches
    yt = y_manche + int((y1 - y0) * 0.06)
    t = np.where(rose[yt])[0]
    g = ((r.min() + t.min()) / 2, y_manche - (y_manche - y0) * 0.25)
    d = ((r.max() + t.max()) / 2, y_manche - (y_manche - y0) * 0.25)
    # longueur du bras : la main arrive à mi-cuisse, comme sur l'image maître
    H = c.height
    longueur = H * 0.66 - g[1]
    pieces = []
    for chemin in (bras_g, bras_d):
        b = pantin.charger(chemin)
        s = longueur / (b.height * 0.93)
        b = b.resize((max(1, round(b.width * s)), max(1, round(b.height * s))), Image.LANCZOS)
        pieces.append((b, (b.width / 2, b.height * 0.07)))     # le pivot, dans la manche
    return c, g, d, pieces


def _tourner(piece, pivot, angle):
    """Tourne la pièce autour de son pivot ; renvoie l'image et le décalage du pivot."""
    b, (px, py) = piece, pivot
    R = int(np.hypot(max(px, b.width - px), max(py, b.height - py))) + 2
    toile = Image.new('RGBA', (2 * R, 2 * R))
    toile.paste(b, (int(R - px), int(R - py)))
    return toile.rotate(angle, resample=Image.BICUBIC), R


@lru_cache(maxsize=512)
def poser(corps, bras_g, bras_d, ang_g=0.0, ang_d=0.0, tete=None, devant=True):
    c, g, d, pieces = kit(corps, bras_g, bras_d)
    base = pantin.poser(corps, tete, 1.0, True) if tete else c
    # pantin.poser peut avoir agrandi la toile vers le haut ou les côtés :
    # on retrouve le décalage en comparant les tailles (agrandissement en haut et à gauche)
    dx = base.width - c.width if base.width != c.width else 0
    dy = base.height - c.height if base.height != c.height else 0
    pad = 200
    toile = Image.new('RGBA', (base.width + 2 * pad, base.height + 2 * pad))
    bras = []
    for (piece, pivot), (ex, ey), ang, signe in ((pieces[0], g, ang_g, -1), (pieces[1], d, ang_d, 1)):
        img, R = _tourner(piece, pivot, signe * ang)
        bras.append((img, (int(ex + dx // 2 + pad - R), int(ey + dy + pad - R))))
    if not devant:
        for img, pos in bras:
            toile.alpha_composite(img, pos)
    toile.alpha_composite(base, (pad, pad))
    if devant:
        for img, pos in bras:
            toile.alpha_composite(img, pos)
    bb = toile.getchannel('A').getbbox()
    return toile.crop(bb)
