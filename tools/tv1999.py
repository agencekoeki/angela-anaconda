"""Filtre « télé 1999 » : l'étalonnage terne de la série, sur une image nette.

Usage : python3 tv1999.py entree.png sortie.png [--sombre 0.93] [--sat 0.88]

Par défaut, le filtre ne touche qu'aux couleurs : il assombrit un peu, désature,
baisse légèrement le contraste et resserre les noirs. L'image reste parfaitement
nette, sans flou, sans grain et sans artefacts, parce qu'un flou voulu serait pris
pour une image mal compressée.

L'option --vieux rend l'ancien effet de vieille télé : passage en basse définition,
JPEG fort, bavure des couleurs, grain et lignes. Elle reste disponible pour un plan
d'archive ou un générique, jamais pour les images du site.
"""
import argparse
import io

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--sombre', type=float, default=0.93, help='gamma < 1 assombrit')
ap.add_argument('--sat', type=float, default=0.88, help='saturation globale')
ap.add_argument('--contraste', type=float, default=0.94)
ap.add_argument('--out', type=int, default=0, help='largeur de sortie (0 = taille d\'origine)')
ap.add_argument('--vieux', action='store_true', help='ancien effet vieille télé (flou, grain, lignes)')
ap.add_argument('--sd', type=int, default=480, help='avec --vieux : largeur basse définition')
ap.add_argument('--grain', type=float, default=5.0, help='avec --vieux : force du grain')
a = ap.parse_args()

im = Image.open(a.src)
alpha = im.getchannel('A') if im.mode in ('RGBA', 'LA') else None
im = im.convert('RGB')
W, H = im.size
ow = a.out or W
oh = round(H * ow / W)

if a.vieux:
    sd = im.resize((a.sd, round(H * a.sd / W)), Image.LANCZOS)
    buf = io.BytesIO(); sd.save(buf, 'JPEG', quality=38, subsampling=2); sd = Image.open(buf).convert('RGB')
    y, cb, cr = sd.convert('YCbCr').split()
    cb = cb.filter(ImageFilter.BoxBlur(1.6)); cr = cr.filter(ImageFilter.BoxBlur(1.6))
    im = Image.merge('YCbCr', (y, cb, cr)).convert('RGB').resize((ow, oh), Image.BICUBIC)
elif ow != W:
    im = im.resize((ow, oh), Image.LANCZOS)

im = ImageEnhance.Color(im).enhance(a.sat)
im = ImageEnhance.Contrast(im).enhance(a.contraste)
arr = np.asarray(im).astype(np.float32) / 255.0
arr = np.clip(arr ** (1 / a.sombre) * 0.97 + 0.02, 0, 1)
if a.vieux:
    rng = np.random.default_rng(7)
    arr += rng.normal(0, a.grain / 255.0, arr.shape[:2])[..., None]
    arr[1::2] *= 0.965
out = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
if alpha is not None:
    out.putalpha(alpha.resize(out.size))
if a.dst.lower().endswith(('.jpg', '.jpeg')):
    out.convert('RGB').save(a.dst, quality=95, subsampling=0)
else:
    out.save(a.dst)
print(a.dst, *out.size)
