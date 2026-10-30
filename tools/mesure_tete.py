"""Mesure la grosseur de la tête d'un personnage détouré, et la compare à l'image maître.

Usage :
  python3 mesure_tete.py maitre.png pose1.png pose2.png ... [--planche controle.jpg] [--moins 0.05] [--plus 0.25]

Chaque image est une découpe (PNG transparent) ou une image sur fond vert uni,
debout et en pied. Pour chacune, l'outil :
  1. lit la silhouette (alpha, ou ce qui n'est pas vert) ;
  2. trouve la tête : le haut de la silhouette jusqu'au cou, c'est-à-dire la rangée
     la plus étroite sous la partie la plus large de la tête ;
  3. calcule le RAPPORT tête / hauteur totale, et la largeur de la tête rapportée à
     la hauteur totale ;
  4. compare au maître. La tolérance est ASYMÉTRIQUE, à la demande de Sébastien :
     une tête un peu plus grosse renforce le style (jusqu'à +25 % par défaut),
     une tête plus petite le casse (pas plus de −5 % par défaut).
Avec --planche, il dessine chaque image avec la tête encadrée (vert = conforme,
rouge = écart), les lignes du haut, du cou et des pieds, et les chiffres.

Pourquoi : la grosse tête sur un corps filiforme est la signature du personnage.
Le générateur la rétrécit sans prévenir, surtout de dos ou de profil. On la
vérifie à la mesure, pas à l'œil.

Limites : une pose où un bras passe au-dessus de la tête, ou un personnage couché,
fausse la détection du cou. L'outil le signale (« cou introuvable ») au lieu
d'inventer un chiffre.
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def silhouette(chemin):
    im = Image.open(chemin)
    if im.mode in ('RGBA', 'LA') and np.asarray(im.getchannel('A')).min() < 250:
        m = np.asarray(im.getchannel('A')) > 128
    else:
        a = np.asarray(im.convert('RGB')).astype(int)
        dom = a[..., 1] - np.maximum(a[..., 0], a[..., 2])
        m = dom < 40
    return im.convert('RGBA'), m


def mesurer(m):
    rows = np.where(m.any(1))[0]
    if len(rows) < 50:
        return None
    haut, bas = rows[0], rows[-1]
    H = bas - haut + 1
    larg = m.sum(1).astype(float)
    # lissage léger pour ignorer les poils et les oreilles isolées
    k = max(3, H // 200)
    larg = np.convolve(larg, np.ones(k) / k, mode='same')
    # Le cou d'abord : la rangée la plus étroite entre 12 % et 40 % de la hauteur.
    # (Chercher d'abord le plus large de la tête prendrait les épaules pour la tête.)
    z = larg[haut: haut + int(H * 0.40)]
    debut = int(H * 0.12)
    if len(z) <= debut + 5:
        return None
    i_cou = debut + int(np.argmin(z[debut:]))
    i_max = int(np.argmax(z[:i_cou]))                   # le plus large de la tête, au-dessus du cou
    if z[i_cou] > 0.75 * z[i_max]:                      # pas de vrai rétrécissement
        return None
    cou = haut + i_cou
    tete_h = cou - haut
    cols = np.where(m[haut:cou].any(0))[0]
    return dict(haut=int(haut), cou=int(cou), bas=int(bas), H=int(H),
                tete_h=int(tete_h), tete_l=int(z[i_max]),
                x0=int(cols.min()), x1=int(cols.max()),
                rapport=tete_h / H, largeur=z[i_max] / H)


ap = argparse.ArgumentParser()
ap.add_argument('maitre'); ap.add_argument('poses', nargs='*')
ap.add_argument('--planche')
ap.add_argument('--moins', type=float, default=0.05, help='écart toléré en plus petit')
ap.add_argument('--plus', type=float, default=0.25, help='écart toléré en plus gros')
a = ap.parse_args()

res = []
for chemin in [a.maitre] + a.poses:
    im, m = silhouette(chemin)
    res.append((chemin, im, mesurer(m)))

ref = res[0][2]
if ref is None:
    sys.exit(f'{a.maitre} : cou introuvable sur le maître, impossible de comparer')
print(f'{"image":45s} tête/hauteur  largeur/hauteur  écart  verdict')
for chemin, im, r in res:
    nom = chemin.split('/')[-1]
    if r is None:
        print(f'{nom:45s} cou introuvable (bras levé, personnage couché ?) : à juger à l\'œil'); continue
    ecart = r['rapport'] / ref['rapport'] - 1
    r['ecart'] = ecart
    r['ok'] = -a.moins <= ecart <= a.plus
    print(f'{nom:45s} {r["rapport"]:.3f}        {r["largeur"]:.3f}          {ecart:+.0%}   {"conforme" if r["ok"] else "ÉCART : tête trop " + ("petite" if ecart < 0 else "grosse")}')

if a.planche:
    Ht = 700
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    except OSError:
        f = ImageFont.load_default()
    tuiles = []
    for chemin, im, r in res:
        s = Ht / im.height
        t = Image.new('RGB', im.size, (60, 60, 66)); t.paste(im, (0, 0), im)
        d = ImageDraw.Draw(t)
        if r:
            c = (40, 220, 90) if r.get('ok', True) else (240, 50, 50)
            w = max(3, im.width // 200)
            d.rectangle([r['x0'], r['haut'], r['x1'], r['cou']], outline=c, width=w)
            for y in (r['haut'], r['cou'], r['bas']):
                d.line([0, y, im.width, y], fill=(255, 210, 0), width=max(1, w // 2))
        t = t.resize((round(im.width * s), Ht))
        d = ImageDraw.Draw(t)
        nom = chemin.split('/')[-1][:30]
        txt = nom if not r else f'{nom}\ntête {r["rapport"]:.1%} de la hauteur' + ('' if chemin == a.maitre else f'\nécart {r["ecart"]:+.0%}')
        d.multiline_text((8, 8), txt, font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        tuiles.append(t)
    W = sum(t.width for t in tuiles) + 12 * (len(tuiles) + 1)
    p = Image.new('RGB', (W, Ht + 24), (25, 25, 30)); x = 12
    for t in tuiles:
        p.paste(t, (x, 12)); x += t.width + 12
    p.save(a.planche, quality=90)
    print('planche :', a.planche)
