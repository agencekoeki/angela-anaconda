"""Détourage sur fond vert uni : PNG transparent recadré, peau ramenée au gris.

Usage : python3 detourage.py entree.png sortie.png [--marge 12]

Le vert (# 00B140 environ) est repéré par la dominance du canal vert sur le
rouge et le bleu. L'alpha suit cette dominance, avec un fondu de deux seuils
pour garder des bords doux. Le vert qui « bave » sur les bords est neutralisé
(despill). L'image est ensuite recadrée au personnage, avec une petite marge.
"""
import argparse
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--bas', type=float, default=40)    # dominance sous laquelle on garde tout
ap.add_argument('--haut', type=float, default=90)   # dominance au-delà de laquelle tout est fond
ap.add_argument('--marge', type=int, default=12)
ap.add_argument('--frange', type=int, default=6, help='largeur (px) de la bande de bord nettoyée du vert ; 30 pour des cheveux longs')
ap.add_argument('--frange-haut', type=float, default=1.0, help='ne nettoyer que le haut de l\'image (ex. 0.8 : épargne une bretelle verte en bas)')
ap.add_argument('--gris', type=float, default=0.45,
                help='désature les tons moins saturés que ce seuil (peau grise), 0 pour désactiver')
ap.add_argument('--flashy', default='',
                help="teinte de la pièce flashy à pousser, en degrés 'debut-fin' (ex. 0-35 pour des cheveux roux, 300-345 pour un rose) : saturation et lumière poussées, comme le t-shirt rose de Sébastien")
ap.add_argument('--flashy-epais', type=int, default=0,
                help="ne pousser que les zones épaisses de la teinte (ouverture de N px) : épargne une monture de lunettes ou des lèvres de la même teinte que les cheveux")
ap.add_argument('--force', type=float, default=1.0, help='intensité du --flashy (1 = normal, 1.5 = très fort)')
a = ap.parse_args()

im = np.asarray(Image.open(a.src).convert('RGB')).astype(np.float32)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
dom = g - np.maximum(r, b)
alpha = 1 - np.clip((dom - a.bas) / (a.haut - a.bas), 0, 1)
# despill : le vert ne dépasse jamais le plus fort des deux autres canaux
# les pixels de bord, et toute la bande de 6 px autour de la découpe (mèches de
# cheveux, poils) : le vert du fond y bave ; l'intérieur (une robe verte) est épargné
from scipy import ndimage as _nd
_plein = alpha > 0.5
_bande = _plein & ~_nd.binary_erosion(_plein, iterations=a.frange)
_bande[int(_bande.shape[0] * a.frange_haut):] = False
# « verdâtre » : plus de vert que la moyenne rouge/bleu (un roux mêlé de vert donne de l'olive, sans que le vert domine)
bord = (g > (r + b) / 2 + 6) & ((alpha < 0.98) | _bande)
# vert ramené à la moyenne rouge/bleu : un gris reste gris, un roux reste roux
# (ramener au plus fort des deux rendait les mèches rousses jaunes)
g2 = np.where(bord, np.minimum(g, (r + b) / 2), g)
# les pixels de la bande encore nettement verts sont surtout du fond : on les estompe
alpha = np.where(_bande & (dom > 25), alpha * 0.35, alpha)
if a.gris > 0:
    # la peau doit rester grise : on retire la teinte des tons peu saturés,
    # sans toucher aux couleurs franches (t-shirt, yeux, passepoil)
    mx = np.maximum(np.maximum(r, g2), b); mn = np.minimum(np.minimum(r, g2), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    k = np.clip(1 - sat / a.gris, 0, 1)[..., None]          # 1 = tout gris, 0 = intact
    lum = (0.299 * r + 0.587 * g2 + 0.114 * b)[..., None]
    # gris argenté froid, comme la peau d'Angela : un soupçon de bleu
    froid = np.dstack([lum[..., 0] * 0.97, lum[..., 0] * 0.99, lum[..., 0] * 1.04])
    rgb = np.dstack([r, g2, b]) * (1 - k) + froid * k
    r, g2, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
if a.flashy:
    # une seule pièce flashy par personnage : on pousse sa teinte, rien d'autre
    import colorsys
    h1, h2 = [float(x) / 360 for x in a.flashy.split('-')]
    rgb = np.dstack([r, g2, b]) / 255.0
    mx = rgb.max(-1); mn = rgb.min(-1); dlt = mx - mn
    hue = np.zeros_like(mx)
    nz = dlt > 1e-6
    rr, gg, bb = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    c1 = nz & (mx == rr); c2 = nz & (mx == gg) & ~c1; c3 = nz & ~c1 & ~c2
    hue[c1] = ((gg - bb)[c1] / dlt[c1]) % 6
    hue[c2] = ((bb - rr)[c2] / dlt[c2]) + 2
    hue[c3] = ((rr - gg)[c3] / dlt[c3]) + 4
    hue = hue / 6.0
    sat = np.where(mx > 0, dlt / np.maximum(mx, 1e-6), 0)
    dans = (hue >= h1) & (hue <= h2) if h1 <= h2 else ((hue >= h1) | (hue <= h2))
    cible = dans & (sat > 0.22) & (mx > 0.08)
    if a.flashy_epais:
        # une monture fine disparaît à l'ouverture ; on regagne le bord des mèches par une petite dilatation
        coeur = _nd.binary_opening(cible, iterations=a.flashy_epais)
        cible = cible & _nd.binary_dilation(coeur, iterations=a.flashy_epais + 1)
    s_new = np.clip(sat * (1.6 * a.force) + 0.18 * a.force, 0, 1)
    v_new = np.clip(mx * (1.0 + 0.25 * a.force) + 0.05, 0, 1)
    # reconstruire la couleur avec la même teinte, plus saturée et plus lumineuse
    hh = (hue * 6.0); i = np.floor(hh).astype(int) % 6; f = hh - np.floor(hh)
    p_ = v_new * (1 - s_new); q_ = v_new * (1 - s_new * f); t_ = v_new * (1 - s_new * (1 - f))
    choix = [(v_new, t_, p_), (q_, v_new, p_), (p_, v_new, t_), (p_, q_, v_new), (t_, p_, v_new), (v_new, p_, q_)]
    R = np.zeros_like(mx); G = np.zeros_like(mx); B = np.zeros_like(mx)
    for k, (cr, cg, cb) in enumerate(choix):
        sel = cible & (i == k); R[sel] = cr[sel]; G[sel] = cg[sel]; B[sel] = cb[sel]
    r = np.where(cible, R * 255, r); g2 = np.where(cible, G * 255, g2); b = np.where(cible, B * 255, b)
out = np.dstack([r, g2, b, alpha * 255]).clip(0, 255).astype(np.uint8)
ys, xs = np.where(alpha > 0.05)
y0, y1 = max(ys.min() - a.marge, 0), min(ys.max() + a.marge, im.shape[0])
x0, x1 = max(xs.min() - a.marge, 0), min(xs.max() + a.marge, im.shape[1])
Image.fromarray(out[y0:y1, x0:x1], 'RGBA').save(a.dst)
print(a.dst, x1 - x0, y1 - y0)
