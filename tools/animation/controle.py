"""Contrôle d'un épisode avant livraison : lisibilité, tailles, places, débordements, bande des sous-titres.

Usage : python3 controle.py short_ep01 [--pas 1.0] [--langue fr] [--plans 3,4]
(contraste.py est l'ancien nom ; il appelle ce fichier.)
Sortie : un rapport (texte) et une planche des images en défaut, dans controle/<module>-<langue>/.
Code de sortie 1 s'il reste une ERREUR : on ne livre pas.

Ce qui est mesuré, image par image (échantillonnée tous les --pas secondes) :

1. Personnage contre fond. Deux mesures, en écart de couleur Lab (ΔE 1976) :
   - le CONTOUR : en chaque point du bord extérieur de ce qui est dessiné (liseré ou halo compris),
     la couleur moyenne juste dedans (8 px) contre la couleur moyenne juste dehors (8 px). C'est ce
     qui fait qu'une silhouette se détache. On garde la médiane sur tout le contour ;
   - la SILHOUETTE : on dessine l'image avec le personnage, puis sans lui, et on compare pixel à
     pixel ce qu'il montre et ce qu'il y aurait derrière lui (le camouflage). Ce qu'un autre
     personnage cache est retiré du calcul ; plus l'écart de valeur seule (ΔL, test du noir et blanc).
     ERREUR    : contour < 13
     ATTENTION : contour < 20, silhouette < 30, ΔL < 6, ou caché à plus de 45 % derrière un autre
                 (normal en passant ; pas s'il y reste)
   Étalonnage à l'œil (30/10/2026), contour / silhouette : Tara devant un écran turquoise 12 / 28,
   à peine visible (ERREUR) ; Django assis sur le carrelage roux 16 / 28 et Olympe couchée sur la
   serviette sépia 17 / 23, lisibles grâce à leur poitrail blanc mais sans marge (ATTENTION) ;
   Kristina 29, Tara sur écran bleu nuit avec sa lueur 36, Diana 42, Sébastien 45 (OK).
2. Texte. Contraste WCAG entre la couleur des lettres et le fond qui est dessous (le fond le plus
   défavorable de la boîte, 10e et 90e centiles), le contour épais comptant comme une aide ;
   même couleur que le fond ; texte posé sur un personnage ; taille ; zones sûres des applis.
     ERREUR    : contraste effectif < 3:1 ; corps < 48 px ; texte hors de 10–75 % de la hauteur
     ATTENTION : lettres de la couleur du fond (ΔE < 25) ; carton sur un personnage (> 15 % de
                 sa boîte) ; corps < 56 px ; texte hors de 13–70 % de la hauteur, ou dans la
                 colonne des boutons à droite (x > 88 %, entre 40 et 85 % de la hauteur)
                 Les sous-titres ont leur bande, plus basse (décision du 30/10/2026 : pas en plein
                 milieu) : ATTENTION au-delà de 76,5 % de la hauteur, ERREUR au-delà de 80 %.
3. Géométrie (même échantillonnage) :
     TAILLE    : chaque image a sa proportion (PROPORTIONS : part de la hauteur d'un humain debout) ; deux
                 personnages posés sur la même ligne de sol (à 7 % de hauteur près) doivent supposer le même humain.
                 ATTENTION au-delà de ×1,2, ERREUR au-delà de ×1,35. On accuse l'animal. `Acteur.echelle_libre`
                 exempte une taille voulue (Tara dans le téléphone, le rêve).
     PLACE     : un acteur qui a une `cible` (une vitre) ne doit pas en déborder (ERREUR) et doit la couvrir
                 (ATTENTION sous 92 %) ; et la cible doit tomber sur la vitre du décor, retrouvée par calage.py
                 (ERREUR à plus de 6 px, avec le rectangle retrouvé à recopier).
     BORD      : un personnage immobile coupé par le bord gauche ou droit du cadre (ATTENTION ; couper le bas, c'est un plan moyen).
     VISAGE    : un sous-titre qui couvre un visage (la tête d'un humain, un gros plan) : ATTENTION au-delà de 10 %,
                 ERREUR au-delà de 35 %. Les plans se composent en laissant libre la bande des sous-titres.
Les seuils de personnage sont des choix d'atelier (aucune norme n'existe) ; ceux du texte partent
des WCAG 1.4.3 (3:1 pour le grand texte) et des guides de zones sûres de Meta.
"""
import argparse
import importlib
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from skimage.color import rgb2lab

IGNORE = {'ecran'}          # les lueurs d'écran font partie du décor


def lum(rgb):
    c = np.asarray(rgb, np.float64) / 255
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def ratio(l1, l2):
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def mesurer_acteur(avec, sans, alpha, px, py, Wd, Hd):
    h, w = alpha.shape
    m = np.zeros((Hd, Wd), bool)
    x0, y0 = max(0, px), max(0, py); x1, y1 = min(Wd, px + w), min(Hd, py + h)
    if x1 <= x0 or y1 <= y0:
        return None
    m[y0:y1, x0:x1] = alpha[y0 - py:y1 - py, x0 - px:x1 - px] > 128
    if m.sum() < 400 or m.sum() < 0.6 * (alpha > 128).sum():
        return None          # trop petit, ou à moitié hors du cadre (il entre ou il sort)
    er = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(29))) > 128
    bord = m & ~er
    # le bord du cadre de l'image ne compte pas comme un bord de silhouette
    bord[:3, :] = bord[-3:, :] = False; bord[:, :3] = bord[:, -3:] = False
    if bord.sum() < 100:
        return None
    ys, xs = np.nonzero(m)
    sl = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    sl2 = (slice(sl[0].start, sl[0].stop, 2), slice(sl[1].start, sl[1].stop, 2))     # un pixel sur quatre suffit
    la, lb = rgb2lab(np.asarray(avec)[sl2]), rgb2lab(np.asarray(sans)[sl2])
    de = np.linalg.norm(la - lb, axis=-1); dl = np.abs(la[..., 0] - lb[..., 0])
    mm, bb = m[sl2], bord[sl2]
    cache = float((de[mm] < 1.5).mean())
    # ce qu'un autre personnage cache (rien n'a changé à cet endroit) n'est pas du camouflage : on le retire
    vis = de >= 1.5
    if (mm & vis).sum() > 50 and (bb & vis).sum() > 30:
        mm, bb = mm & vis, bb & vis
    # le contour se prend au bord extérieur de ce qui est dessiné (halo compris), là où le décor reprend
    m_ext = np.zeros_like(m)
    m_ext[y0:y1, x0:x1] = alpha[y0 - py:y1 - py, x0 - px:x1 - px] > 24
    fr, ff = frontiere(np.asarray(avec), m_ext)
    return dict(de=float(np.median(de[bb])), tout=float(np.median(de[mm])), faible=float((de[bb] < 15).mean()),
                cache=cache, front=fr, front_faible=ff,
                dl=float(np.median(dl[mm])), boite=(int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())),
                aire=int(m.sum()), masque=m)


def frontiere(img, m, marge=24):
    """Le contraste de part et d'autre du contour : la couleur moyenne juste dedans (8 px)
    contre la couleur moyenne juste dehors (8 px), en chaque point du contour."""
    from scipy import ndimage
    ys, xs = np.nonzero(m)
    y0, y1 = max(0, ys.min() - marge), min(m.shape[0], ys.max() + marge + 1)
    x0, x1 = max(0, xs.min() - marge), min(m.shape[1], xs.max() + marge + 1)
    mc = m[y0:y1, x0:x1]
    lab = rgb2lab(img[y0:y1, x0:x1])
    dedans = mc & ~ndimage.binary_erosion(mc, iterations=8)
    dehors = ndimage.binary_dilation(mc, iterations=8) & ~mc
    bord = mc & ~ndimage.binary_erosion(mc, iterations=1)
    bord[[0, -1], :] = False; bord[:, [0, -1]] = False
    # le contour qui touche le bord de l'image ne compte pas
    if y0 == 0: bord[:3, :] = False
    if x0 == 0: bord[:, :3] = False
    if y1 == m.shape[0]: bord[-3:, :] = False
    if x1 == m.shape[1]: bord[:, -3:] = False

    def moyenne(masque):
        w = ndimage.gaussian_filter(masque.astype(np.float32), 4)
        return np.stack([ndimage.gaussian_filter(lab[..., k] * masque, 4) for k in range(3)], -1) / np.maximum(w[..., None], 1e-6)
    if bord.sum() < 50:
        return 99.0, 0.0
    d = np.linalg.norm(moyenne(dedans) - moyenne(dehors), axis=-1)[bord]
    return float(np.median(d)), float((d < 15).mean())



# ---------------------------------------------------------------- 3. tailles, places, débordements, bande des sous-titres
# La hauteur VISIBLE de chaque image, en part de la hauteur d'un humain debout (1,80 m). Le préfixe le plus long
# du nom de fichier qui correspond l'emporte. Sébastien, 30/10/2026 : « attention à la taille ; le chien, parfois, il
# est minuscule ». À compléter quand une nouvelle pose ou un nouveau personnage arrive.
PROPORTIONS = {
    'seb-': 1.0, 'diana-pyjama': 0.52, 'diana-': 0.96, 'kristina-nuit': 0.95, 'kristina-': 0.95,
    'django-assis': 0.42, 'django-saut': 0.36, 'django-': 0.40,
    'olympe-bonjour-2': 0.28, 'olympe-bonjour-3': 0.28, 'olympe-bonjour': 0.38,
    'olympe-aboie-1': 0.17, 'olympe-aboie': 0.24, 'olympe-o1': 0.25, 'olympe-': 0.30,
    'patchy-': 0.18, 'tara-': 0.25, 'boulanger-': 0.95,
}
HUMAINS = {'seb', 'diana', 'kristina', 'boulanger'}
SANS_TAILLE = {'ecran', 'flamme'}
_CALAGE = {}


def proportion(src):
    best = None
    for k, v in PROPORTIONS.items():
        if src.startswith(k) and (best is None or len(k) > len(best[0])):
            best = (k, v)
    return best[1] if best else None


def controles_geometrie(p, t, tr, W, H, decor_source):
    """Renvoie [(verdict, clé, message, boîte)] pour l'image au temps t."""
    out = []
    cam = next((r for r in tr if r[0] == 'camera'), None)
    dw, Hd, ox, oy, procedural = cam[1:] if cam else (W, H, 0, 0, True)
    sous_titres = [r[3] for r in tr if r[0] == 'texte' and r[1] == 'lettres']
    infos = []
    for rec in [r for r in tr if r[0] == 'acteur']:
        _, i_a, nom, px, py, alpha, *src = rec
        a = p.acteurs[i_a]
        src = src[0] if src else ''
        ys, xs = np.nonzero(alpha > 128)
        if len(ys) == 0:
            continue
        bx0, by0, bx1, by1 = px + xs.min(), py + ys.min(), px + xs.max() + 1, py + ys.max() + 1
        dans = max(0, min(W, bx1) - max(0, bx0)) * max(0, min(H, by1) - max(0, by0)) / max(1, (bx1 - bx0) * (by1 - by0))
        dans_x = max(0, min(W, bx1) - max(0, bx0)) / max(1, bx1 - bx0)     # coupé à gauche ou à droite (couper le bas, c'est un plan moyen)
        bouge = a.bouge(t) if a.trajet else False
        cadre_actif = a.cadre and (len(a.cadre) < 5 or t < a.cadre[4])
        infos.append((a, nom, src, (bx0, by0, bx1, by1), dans, bouge, cadre_actif))
        # la place exacte (une vitre) : ni débordement, ni vide
        if a.cible and not procedural:
            c = a.cible
            cx0, cy0, cx1, cy1 = c[0] * dw - ox, c[1] * Hd - oy, c[2] * dw - ox, c[3] * Hd - oy
            tol = max(3, 0.03 * (cx1 - cx0))
            deb = max(cx0 - bx0, cy0 - by0, bx1 - cx1, by1 - cy1)
            if deb > tol:
                out.append(('ERREUR', ('place', nom, c), f'{nom} ({src}) déborde de sa place de {deb:.0f} px', (bx0, by0, bx1, by1)))
            couv = max(0, min(bx1, cx1) - max(bx0, cx0)) * max(0, min(by1, cy1) - max(by0, cy0)) / max(1, (cx1 - cx0) * (cy1 - cy0))
            if couv < 0.92:
                out.append(('ATTENTION', ('place', nom, c), f'{nom} ne couvre que {couv:.0%} de sa place', (int(cx0), int(cy0), int(cx1), int(cy1))))
            # la place déclarée tombe-t-elle sur la vitre du décor ?
            cle = (p.decor, tuple(c))
            if cle not in _CALAGE:
                from calage import detecter_zone, ecart
                z, conf = detecter_zone(decor_source(p.decor), c)
                _CALAGE[cle] = (z, conf, ecart(c, z, decor_source(p.decor).size) if z else None)
            z, conf, ec = _CALAGE[cle]
            if z and conf > 0.85 and ec > 6:
                out.append(('ERREUR', ('calage', nom, c), f'la place de {nom} est à {ec:.0f} px de la vitre du décor ; retrouvée : '
                            + ', '.join(f'{v:.3f}' for v in z), (int(cx0), int(cy0), int(cx1), int(cy1))))
        # coupé par le bord du cadre, sans bouger
        if not a.gros_plan and not bouge and 0.05 < dans_x < 0.85 and nom not in SANS_TAILLE:
            out.append(('ATTENTION', ('bord', nom, src), f'{nom} coupé par le bord gauche ou droit du cadre ({dans_x:.0%} visible)', (bx0, by0, bx1, by1)))
        # un visage sous les sous-titres
        if sous_titres and (nom in HUMAINS or a.gros_plan):
            hb = (bx0, by0, bx1, by0 + (by1 - by0) * (0.85 if a.gros_plan else 0.28))
            aire = max(1, (hb[2] - hb[0]) * (hb[3] - hb[1]))
            rec_max = 0
            for sb in sous_titres:
                rec_max = max(rec_max, max(0, min(hb[2], sb[2]) - max(hb[0], sb[0])) * max(0, min(hb[3], sb[3]) - max(hb[1], sb[1])) / aire)
            if rec_max > 0.10:
                out.append(('ERREUR' if rec_max > 0.35 else 'ATTENTION', ('visage', nom),
                            f'le sous-titre cache le visage de {nom} ({rec_max:.0%})', tuple(int(v) for v in hb)))
    # les proportions entre personnages posés sur la même ligne de sol
    if not procedural:
        pris = [(a, nom, src, b, proportion(src)) for (a, nom, src, b, dans, bouge, cadre_actif) in infos
                if not a.gros_plan and not a.echelle_libre and not cadre_actif and nom not in SANS_TAILLE and dans > 0.9 and proportion(src)]
        for k1 in range(len(pris)):
            for k2 in range(k1 + 1, len(pris)):
                a1, n1, s1, b1, r1 = pris[k1]; a2, n2, s2, b2, r2 = pris[k2]
                if abs(b1[3] - b2[3]) > 0.07 * H or n1 == n2:
                    continue
                h1, h2 = (b1[3] - b1[1]) / r1, (b2[3] - b2[1]) / r2       # la taille d'humain que chacun suppose
                q = h1 / h2
                if max(q, 1 / q) > 1.2:
                    # on accuse l'animal (ou le plus petit écart à la norme si ce sont deux humains)
                    fautif, autre, qq = (n2, n1, 1 / q) if (n1 in HUMAINS and n2 not in HUMAINS) else (n1, n2, q) if (n2 in HUMAINS and n1 not in HUMAINS) else (n2, n1, 1 / q)
                    sens = 'trop grand' if qq > 1 else 'trop petit'
                    out.append(('ERREUR' if max(q, 1 / q) > 1.35 else 'ATTENTION', ('taille', fautif, autre),
                                f'{fautif} {sens} à côté de {autre} (×{qq:.2f} de la bonne proportion)',
                                tuple(int(v) for v in (b2 if fautif == n2 else b1))))
    return out


def verdict_acteur(r):
    if r['cache'] > 0.45:
        return 'ATTENTION'          # caché derrière un autre (en passant, c'est normal ; s'il y reste, non)
    if r['front'] < 13:
        return 'ERREUR'
    if r['front'] < 20 or r['tout'] < 30 or r['dl'] < 6:
        return 'ATTENTION'
    return 'OK'


def mesurer_texte(rec, fond, masques, W, H):
    _, genre, texte, bb, fill, taille, bandeau, *cont = rec
    x0, y0, x1, y1 = [int(v) for v in bb]
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, x1), min(H, y1)
    notes = []; niveau = 'OK'

    def monte(n, msg):
        nonlocal niveau
        notes.append(msg)
        if n == 'ERREUR' or (n == 'ATTENTION' and niveau == 'OK'):
            niveau = n
    if x1 <= x0 or y1 <= y0:
        return 'OK', ['hors champ']
    if not bandeau:
        zone = np.asarray(fond)[y0:y1, x0:x1].reshape(-1, 3)
        lz = lum(zone); lf = float(lum(fill))
        pires = [float(np.percentile(lz, 10)), float(np.percentile(lz, 90))]
        # pour chaque fond, la lettre se lit si elle tranche sur lui, ou si son contour épais
        # tranche sur lui ET qu'elle tranche sur son contour ; on garde le pire des fonds
        lc = float(lum(cont[0])) if cont and cont[1] >= 4 else None
        eff = min(max(ratio(lf, l), min(ratio(lf, lc), ratio(lc, l)) if lc is not None else 0) for l in pires)
        if eff < 3:
            monte('ERREUR', f'contraste {eff:.1f}:1 (< 3:1)')
        med = np.median(zone, axis=0)
        de = float(np.linalg.norm(rgb2lab(np.array([[fill]], np.uint8)) - rgb2lab(med.reshape(1, 1, 3).astype(np.uint8))))
        if de < 25:
            monte('ATTENTION', f'lettres de la couleur du fond (ΔE {de:.0f})')
        notes.append(f'contraste {eff:.1f}:1')
    if genre in ('carton', 'carton-sous', 'bandeau') and masques:
        boite = np.zeros((H, W), bool); boite[y0:y1, x0:x1] = True
        cover = max((boite & m).sum() / max(1, boite.sum()) for m in masques)
        if cover > 0.15:
            monte('ATTENTION', f'posé sur un personnage ({cover:.0%} de la boîte)')
    if genre != 'horloge':
        if taille < 48:
            monte('ERREUR', f'corps {taille} px (< 48)')
        elif taille < 56:
            monte('ATTENTION', f'corps {taille} px (< 56)')
    yc0, yc1 = y0 / H, y1 / H
    # les sous-titres ont leur bande (0,66–0,76) : plus bas, c'est la légende et les boutons de TikTok, Reels, Shorts
    bas_err, bas_att = (0.80, 0.765) if genre == 'lettres' else (0.75, 0.70)
    if yc0 < 0.10 or yc1 > bas_err:
        monte('ERREUR', f'hors zone sûre ({yc0:.0%}–{yc1:.0%} de la hauteur)')
    elif yc0 < 0.13 or yc1 > bas_att:
        monte('ATTENTION', f'au bord de la zone sûre ({yc0:.0%}–{yc1:.0%})')
    if x1 / W > 0.88 and yc1 > 0.40 and yc0 < 0.85:
        monte('ATTENTION', 'dans la colonne des boutons à droite')
    return niveau, notes


_EP = None


def _plan(args):
    """Contrôle d'un plan (tourne dans un processus à part)."""
    i, pas = args
    import moteur
    W, H = moteur.W, moteur.H
    p = _EP.plans[i]
    defauts = []; compte = {'OK': 0, 'ATTENTION': 0, 'ERREUR': 0}
    ts = list(np.arange(min(0.25, p.duree / 2), p.duree, pas))
    vus = {}
    for t in ts:
        moteur.TRACE = []
        moteur.dessiner_plan(p, t)
        tr = moteur.TRACE
        avant = next(r[1] for r in tr if r[0] == 'avant-texte')
        masques = []
        # pendant un flash, un fondu au noir ou un volet, l'image est voulue illisible
        trouble = any(tf <= t < tf + df for (tf, df) in p.flash) or (p.noir and t >= p.noir[0]) \
            or any(v0 <= t for (v0, v1, sens) in p.volet if sens == 'couvre') \
            or any(t < v1 for (v0, v1, sens) in p.volet if sens == 'decouvre') \
            or (p.lumiere and t < p.lumiere[1]) or (p.vague and p.vague[0] <= t < p.vague[1])
        for rec in [r for r in tr if r[0] == 'acteur' and not trouble]:
            _, i_a, nom, px, py, alpha, *_src = rec
            if nom in IGNORE:
                continue
            moteur.TRACE = []
            moteur.dessiner_plan(p, t, sans=i_a)
            sans = next(r[1] for r in moteur.TRACE if r[0] == 'avant-texte')
            m = mesurer_acteur(avant, sans, alpha, px, py, W, H)
            if not m:
                continue
            masques.append(m.pop('masque'))
            v = verdict_acteur(m)
            compte[v] += 1
            cle = ('acteur', nom)
            pire = vus.get(cle)
            if pire is None or (m['cache'] <= 0.45 and (pire[1]['cache'] > 0.45 or m['front'] < pire[1]['front'])):
                vus[cle] = (v, m, t)
            if v != 'OK' and sum(1 for d_ in defauts if d_[4].startswith(nom)) < 2:
                defauts.append((i, t, vignette(avant), m['boite'], f"{nom} contour {m['front']:.0f}, silhouette {m['tout']:.0f}", v))
        if not trouble:
            for (v, cle, msg, boite) in controles_geometrie(p, t, tr, W, H, moteur.decor_source):
                compte[v] += 1
                if cle not in vus or ['OK', 'ATTENTION', 'ERREUR'].index(v) > ['OK', 'ATTENTION', 'ERREUR'].index(vus[cle][0]):
                    vus[cle] = (v, [msg], t)
                if not any(d_[4] == msg for d_ in defauts) and sum(1 for d_ in defauts if d_[5] == v) < 6:
                    moteur.TRACE = None
                    defauts.append((i, t, vignette(moteur.dessiner_plan(p, t)), boite, msg, v))
        for rec in [r for r in tr if r[0] == 'texte']:
            v, notes = mesurer_texte(rec, avant, masques, W, H)
            compte[v] += 1
            cle = ('texte', rec[1], rec[2])
            if cle not in vus or ['OK', 'ATTENTION', 'ERREUR'].index(v) > ['OK', 'ATTENTION', 'ERREUR'].index(vus[cle][0]):
                vus[cle] = (v, notes, t)
            if v != 'OK' and not any(rec[2][:28] in d_[4] for d_ in defauts):
                moteur.TRACE = None
                fin = vignette(moteur.dessiner_plan(p, t))
                defauts.append((i, t, fin, rec[3], f"« {rec[2][:28]} » : {'; '.join(n for n in notes if not n.startswith('contraste ') or v == 'ERREUR')}", v))
    moteur.TRACE = None
    lignes = []
    for cle, (v, info, t) in vus.items():
        if cle[0] == 'acteur':
            cache = f"  caché à {info['cache']:.0%} derrière un autre" if info['cache'] > 0.45 else ''
            lignes.append(f"  {v:9s} {cle[1]:10s} contour {info['front']:5.1f} (faible {info['front_faible']:3.0%})  silhouette {info['tout']:5.1f}  ΔL {info['dl']:4.1f}   (pire à {t:.2f} s){cache}")
        else:
            if cle[0] == 'texte':
                lignes.append(f"  {v:9s} {cle[1]:10s} « {cle[2][:40]} » {'; '.join(info)}")
            elif v != 'OK':
                lignes.append(f"  {v:9s} {cle[0]:10s} {'; '.join(info)}   (à {t:.2f} s)")
    return lignes, defauts, compte


def controler(nom_module, pas=1.0, plans_choisis=None, processus=None):
    global _EP
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    _EP = importlib.import_module(nom_module)
    import multiprocessing as mp
    idx = [i for i in range(len(_EP.plans)) if not plans_choisis or i in plans_choisis]
    with mp.get_context('fork').Pool(processus or os.cpu_count()) as pool:
        res = pool.map(_plan, [(i, pas) for i in idx], chunksize=1)
    lignes = []; defauts = []; compte = {'OK': 0, 'ATTENTION': 0, 'ERREUR': 0}
    t_abs = 0.0; debut = {}
    for i, p in enumerate(_EP.plans):
        debut[i] = t_abs; t_abs += p.duree
    for i, (lp, dp, cp) in zip(idx, res):
        lignes.append(f'\nPlan {i:02d} ({debut[i]:6.1f} s, {_EP.plans[i].duree:.1f} s)')
        lignes += lp; defauts += dp
        for k in compte:
            compte[k] += cp[k]
    return lignes, defauts, compte, t_abs


def vignette(im):
    return im.resize((270, 480))


def planche(defauts, chemin):
    if not defauts:
        return
    w, h = 270, 480
    cols = 6; rows = (min(len(defauts), 36) + cols - 1) // cols
    pl = Image.new('RGB', (w * cols, (h + 40) * rows), (30, 30, 30))
    d = ImageDraw.Draw(pl)
    for j, (i, t, im, bb, msg, v) in enumerate(defauts[:36]):
        im = im.copy(); di = ImageDraw.Draw(im)
        di.rectangle([v_ / 4 for v_ in bb], outline=(255, 0, 0) if v == 'ERREUR' else (255, 170, 0), width=3)
        x, y = (j % cols) * w, (j // cols) * (h + 40)
        pl.paste(im.resize((w, h)), (x, y))
        d.text((x + 4, y + h + 2), f'{v} plan {i} @ {t:.1f}s', fill=(255, 255, 255))
        d.text((x + 4, y + h + 18), msg[:44], fill=(255, 200, 120))
    pl.save(chemin, quality=85)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('module'); ap.add_argument('--pas', type=float, default=1.0)
    ap.add_argument('--langue', default=os.environ.get('LANGUE', 'fr')); ap.add_argument('--plans', default='')
    a = ap.parse_args()
    os.environ['LANGUE'] = a.langue
    choix = [int(x) for x in a.plans.split(',') if x] or None
    lignes, defauts, compte, total = controler(a.module, a.pas, choix)
    dossier = os.path.join('controle', f'{a.module}-{a.langue}'); os.makedirs(dossier, exist_ok=True)
    entete = [f'Contrôle : {a.module} ({a.langue}), {total:.1f} s, une mesure toutes les {a.pas} s',
              f"Mesures : {compte['OK']} OK, {compte['ATTENTION']} ATTENTION, {compte['ERREUR']} ERREUR"]
    texte = '\n'.join(entete + lignes)
    open(os.path.join(dossier, 'rapport.txt'), 'w', encoding='utf-8').write(texte + '\n')
    planche(sorted(defauts, key=lambda d: d[5] != 'ERREUR'), os.path.join(dossier, 'defauts.jpg'))
    print(texte)
    sys.exit(1 if compte['ERREUR'] else 0)
