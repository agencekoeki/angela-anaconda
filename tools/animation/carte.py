"""La carte-titre : une grande carte à collectionner (façon carte de jeu) qui présente l'épisode du jour, brille,
puis se retourne ; son dos est le volet bleu ondulé, qui grandit jusqu'à remplir l'écran et enchaîne sur le plan suivant.

Demande de Sébastien (30/10/2026) : « pas un jingle, plutôt une espèce de super carte Pokémon qui présente l'épisode
du jour, et hop, ça se retourne et on continue ». Aucune marque, aucun logo : seulement la mécanique d'une carte de jeu.

Dans un plan : Plan(4.2, decor, carte={...}) ; les clés sont décrites dans CARTE_EXEMPLE.
"""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import moteur as M

CARTE_EXEMPLE = {
    'debut': 0.0,
    'serie': 'LES TARASCONNADES', 'numero': 'ÉP. 1',
    'nom': 'Juste une petite idée',
    'illustration': ['assets/seb-tete-nuit-2.png'], 'flamme': 'assets/flamme-1.png',
    'espece': 'Expert SEO · Tarascon · Taille : une petite idée',
    'attaques': [('Petite idée', '∞', 'Transforme deux heures gagnées en une nuit blanche.')],
    'pied': ('Faiblesse : Kristina ×2', 'Saison 1 · 1/12 ★'),
}
OR = (240, 196, 52)
CREME = (252, 238, 200)
ENCRE = (52, 30, 12)


def _degrade(w, h, haut, bas):
    y = np.linspace(0, 1, h)[:, None, None]
    a = np.array(haut, np.float32)[None, None] * (1 - y) + np.array(bas, np.float32)[None, None] * y
    return Image.fromarray(np.repeat(a, w, 1).astype(np.uint8))


def _texte_ajuste(d, xy, texte, taille, largeur, police, fill, anchor='la', **kw):
    f = police(taille)
    while d.textlength(texte, font=f) > largeur and taille > 14:
        taille -= 2; f = police(taille)
    d.text(xy, texte, font=f, fill=fill, anchor=anchor, **kw)
    return f


def _lignes(d, texte, f, largeur):
    mots, l, out = texte.split(), '', []
    for m in mots:
        if d.textlength((l + ' ' + m).strip(), font=f) > largeur:
            out.append(l); l = m
        else:
            l = (l + ' ' + m).strip()
    return out + [l]


_REG = {}


@lru_cache(maxsize=4)
def face(cle):
    c = _REG[cle]
    W = int(M.W * 0.86); H = int(W * 1.40)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=40, fill=OR + (255,), outline=(120, 90, 20, 255), width=6)
    corps = _degrade(W - 56, H - 56, (255, 196, 110), (236, 120, 60)).convert('RGBA')
    m = Image.new('L', corps.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, corps.width - 1, corps.height - 1], radius=24, fill=255)
    im.paste(corps, (28, 28), m)
    f_st = lambda t: M.police_st(t, 'Bold')
    # l'en-tête : la série, le nom, le numéro
    d.text((56, 44), M.en_langue(c['serie']), font=f_st(26), fill=ENCRE)
    _texte_ajuste(d, (52, 76), M.en_langue(c['nom']), 62, W - 230, M.police_carte, ENCRE)
    d.rounded_rectangle([W - 170, 64, W - 52, 132], radius=16, fill=(200, 40, 40), outline=ENCRE, width=4)
    d.text((W - 111, 98), M.en_langue(c['numero']), font=f_st(34), fill=(255, 255, 255), anchor='mm')
    # l'illustration : un soleil orange, la tête, la flamme
    ix0, iy0, ix1, iy1 = 52, 160, W - 52, int(H * 0.52)
    iw, ih = ix1 - ix0, iy1 - iy0
    ill = Image.new('RGBA', (iw, ih), (255, 150, 40, 255))
    di = ImageDraw.Draw(ill)
    cx, cy = iw / 2, ih * 0.62
    for k in range(18):
        a0 = 2 * math.pi * k / 18; a1 = a0 + math.pi / 18
        di.polygon([(cx, cy), (cx + 1500 * math.cos(a0), cy + 1500 * math.sin(a0)), (cx + 1500 * math.cos(a1), cy + 1500 * math.sin(a1))],
                   fill=(255, 196, 70, 255))
    tete = Image.open(c['illustration'][0]).convert('RGBA'); tete = tete.crop(tete.getchannel('A').getbbox())
    th = int(ih * 0.80); tete = tete.resize((int(tete.width * th / tete.height), th), Image.LANCZOS)
    ill.alpha_composite(tete, (int(cx - tete.width / 2), ih - th + int(ih * 0.06)))
    if c.get('flamme'):
        fl = Image.open(c['flamme']).convert('RGBA'); fl = fl.crop(fl.getchannel('A').getbbox())
        fh = int(ih * 0.30); fl = fl.resize((int(fl.width * fh / fl.height), fh), Image.LANCZOS)
        ill.alpha_composite(fl, (int(cx - fl.width / 2), max(0, ih - th - int(fh * 0.55))))
    im.alpha_composite(ill, (ix0, iy0))
    d.rectangle([ix0, iy0, ix1, iy1], outline=(150, 150, 160, 255), width=8)
    d.rectangle([ix0 - 4, iy0 - 4, ix1 + 4, iy1 + 4], outline=(90, 70, 20, 255), width=3)
    # la ligne d'espèce, en italique de carte
    d.rounded_rectangle([90, iy1 + 14, W - 90, iy1 + 58], radius=14, fill=(230, 200, 120, 255))
    _texte_ajuste(d, (W / 2, iy1 + 36), M.en_langue(c['espece']), 26, W - 200, f_st, ENCRE, anchor='mm')
    # les attaques
    y = iy1 + 92
    fl_ico = Image.open(c['flamme']).convert('RGBA') if c.get('flamme') else None
    for (nom, degats, desc) in c['attaques']:
        d.ellipse([60, y, 116, y + 56], fill=(220, 60, 30, 255), outline=ENCRE, width=3)
        if fl_ico:
            ic = fl_ico.crop(fl_ico.getchannel('A').getbbox()); ic = ic.resize((int(ic.width * 40 / ic.height), 40))
            im.alpha_composite(ic, (88 - ic.width // 2, y + 8))
        _texte_ajuste(d, (134, y + 28), M.en_langue(nom), 46, W - 330, M.police_carte, ENCRE, anchor='lm')
        d.text((W - 64, y + 28), degats, font=M.ImageFont.truetype(M.POLICE, 50), fill=ENCRE, anchor='rm')   # ∞ et × : Fredoka ne les a pas
        fd = f_st(30)
        yy = y + 70
        for l in _lignes(d, M.en_langue(desc), fd, W - 140):
            d.text((70, yy), l, font=fd, fill=ENCRE); yy += 36
        y = yy + 18
        d.line([60, y - 8, W - 60, y - 8], fill=(150, 80, 30, 255), width=2)
    # le pied de carte
    g, dr = c['pied']
    d.text((60, H - 96), M.en_langue(g), font=f_st(26), fill=ENCRE)
    d.text((W - 60, H - 96), M.en_langue(dr), font=f_st(26), fill=ENCRE, anchor='ra')
    return im


def dos(t, W, H):
    """Le dos : le volet bleu ondulé, un cadre, et le nom de la série au milieu."""
    b = M.fond_bleu(t, W, H).convert('RGBA')
    d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=40, outline=(10, 22, 70, 255), width=26)
    return b


def embleme(W, H, serie):
    e = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(e)
    d.ellipse([W * 0.12, H * 0.36, W * 0.88, H * 0.64], fill=(255, 140, 30, 255), outline=(14, 5, 0, 255), width=8)
    mots = M.en_langue(serie).split()
    f = M.police_carte(int(W * 0.10))
    for k, m in enumerate(mots):
        d.text((W / 2, H * 0.5 + (k - (len(mots) - 1) / 2) * f.size * 1.05), m, font=f, fill=(255, 245, 220), anchor='mm',
               stroke_width=5, stroke_fill=(14, 5, 0))
    return e


def _ease_back(u):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2


def dessiner_carte(im, t, c):
    t0 = c.get('debut', 0.0); u = t - t0
    if u < 0:
        return im
    W, H = M.W, M.H
    # le fond : le décor assombri, des rayons qui tournent
    a = np.asarray(im).astype(np.float32) * 0.45
    fond = Image.fromarray(a.astype(np.uint8)).convert('RGBA')
    ray = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ray)
    cx, cy = W / 2, H * 0.46
    for k in range(16):
        a0 = 2 * math.pi * k / 16 + u * 0.35; a1 = a0 + math.pi / 16
        dr.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))],
                   fill=(255, 190, 60, 46))
    fond.alpha_composite(ray)
    cle = _figer(c)
    _REG[cle] = c
    F = face(cle)
    fw, fh = F.size
    # la chronologie
    if u < 0.45:                                   # elle arrive
        k = _ease_back(u / 0.45); s = 0.15 + 0.85 * k; rot = -25 * (1 - k) - 3 * k; flip = 0.0; grand = 1.0
    elif u < 2.7:                                  # elle flotte et brille
        s = 1.0; rot = -3 * math.cos((u - 0.45) * 2.2); flip = 0.0; grand = 1.0
    elif u < 3.25:                                 # elle se retourne
        s = 1.0; rot = 0.0; flip = (u - 2.7) / 0.55; grand = 1.0
    else:                                          # son dos grandit et devient l'écran bleu
        s = 1.0; rot = 0.0; flip = 1.0; grand = 1.0 + 2.6 * min(1.0, (u - 3.25) / 0.6) ** 2
    angle = math.pi * flip
    larg = abs(math.cos(angle))
    if flip < 0.5:
        carte = F.copy()
        # le reflet holographique : une bande claire qui traverse la carte en diagonale
        if 0.45 <= u < 2.7:
            p = ((u - 0.45) / 1.1) % 1.0
            g = np.zeros((fh, fw), np.float32)
            xx = np.arange(fw)[None, :] + np.arange(fh)[:, None] * 0.6
            pos = -fh * 0.6 + p * (fw + fh * 1.2)
            g = np.clip(1 - np.abs(xx - pos) / 90, 0, 1) * 0.55
            arc = np.stack([np.full_like(g, 255), np.full_like(g, 250), np.full_like(g, 230), g * 255 * np.asarray(carte.getchannel('A')) / 255], -1)
            carte.alpha_composite(Image.fromarray(arc.astype(np.uint8), 'RGBA'))
    else:
        carte = dos(t, fw, fh)
        if grand < 1.6:
            e = embleme(fw, fh, c['serie'])
            if grand > 1.0:
                e.putalpha(e.getchannel('A').point(lambda v: int(v * max(0.0, 1 - (grand - 1) / 0.6))))
            carte.alpha_composite(e)
    tw = max(2, int(fw * s * grand * max(larg, 0.02))); th = max(2, int(fh * s * grand))
    carte = carte.resize((tw, th), Image.BILINEAR)
    if rot:
        carte = carte.rotate(rot, resample=Image.BICUBIC, expand=True)
    # l'ombre portée
    ombre = Image.new('RGBA', carte.size, (0, 0, 0, 0)); ombre.putalpha(carte.getchannel('A').point(lambda v: int(v * 0.5)))
    ombre = ombre.filter(ImageFilter.GaussianBlur(14))
    yc = cy + (0 if u >= 0.45 else 0) + (8 * math.sin(u * 2.4) if 0.45 <= u < 2.7 else 0)
    yc = yc * (1 - min(1, grand - 1)) + (H / 2) * min(1, grand - 1)
    x, y = int(cx - carte.width / 2), int(yc - carte.height / 2)
    fond.alpha_composite(ombre, (x + 14, y + 22))
    fond.alpha_composite(carte, (x, y))
    out = fond.convert('RGB')
    if grand >= 3.5:                               # l'écran est bleu : on enchaîne
        out = M.fond_bleu(t, W, H)
    if M.TRACE is not None and flip < 0.5 and u >= 0.45:
        M.TRACE.append(('texte', 'bandeau', M.en_langue(c['nom']), (x + 52, y + 76, x + fw - 230, y + 140), ENCRE, 62, True))
    return out


def _figer(c):
    """Une clé de cache stable (et dépendante de la langue) pour la face de la carte."""
    out = [('langue', M.LANGUE)]
    for k in sorted(c):
        if k == 'debut':
            continue
        v = c[k]
        out.append((k, repr(v)))
    return tuple(out)
