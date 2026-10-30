"""Moteur d'animation « à la Angela Anaconda » : décors, pantins, têtes de rechange,
synchro labiale tirée du texte, sous-titres, cartons, son de synthèse.

Un film est une liste de PLANS. Chaque plan dit son décor, sa caméra, ses acteurs,
ses répliques et ses bruitages. Le moteur dessine chaque image et la pousse dans
ffmpeg, plan par plan, puis assemble et ajoute le son.

Les règles de la série, appliquées ici :
- les personnages bougent « sur deux images » (12 poses par seconde) : raides,
  par à-coups, comme des pantins de papier ;
- la caméra, elle, glisse en continu (travellings et zooms) ;
- coupes sèches, cartons orange, gros plans de face qui parlent à la caméra ;
- l'imaginaire bascule dans des couleurs saturées, la réalité reste terne.
"""
import math
import os
import random
import subprocess
import wave
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import pantin
import articule

W, H, FPS, PAS = 1280, 720, 24, 2          # PAS = 2 : les pantins changent toutes les 2 images
SR = 44100
POLICE = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
POLICE_CARTON = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'


# ---------------------------------------------------------------- images
@lru_cache(maxsize=512)
def img(chemin):
    return Image.open(chemin).convert('RGBA')


def a_taille(cle, haut_px, miroir=False):
    return _a_taille(cle, int(round(haut_px / 2) * 2), miroir)


@lru_cache(maxsize=160)
def _a_taille(cle, haut_px, miroir=False):
    """cle = chemin d'image, ou ('pantin', corps, tete)."""
    if isinstance(cle, tuple) and cle[0] == 'brut':
        # pose d'une planche : toile commune, pas de recadrage (les poses gardent
        # leur place relative : pieds sur la même ligne, saut dans sa courbe)
        base = img(cle[1])
        s = haut_px / base.height
        out = base.resize((max(1, round(base.width * s)), max(1, round(haut_px))), Image.LANCZOS)
        return out.transpose(Image.FLIP_LEFT_RIGHT) if miroir else out
    if isinstance(cle, tuple) and cle[0] == 'articule':
        base = articule.poser(*cle[1:])
    elif isinstance(cle, tuple):
        base = pantin.poser(cle[1], cle[2])
    else:
        base = img(cle)
    bb = base.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    base = base.crop(bb)
    s = haut_px / base.height
    out = base.resize((max(1, round(base.width * s)), max(1, round(haut_px))), Image.LANCZOS)
    return out.transpose(Image.FLIP_LEFT_RIGHT) if miroir else out


@lru_cache(maxsize=8)
def decor_source(chemin, etalon=True):
    im = Image.open(chemin).convert('RGB')
    return etalonner(im) if etalon else im


def decor(chemin, haut_px, etalon=True):
    im = decor_source(chemin, etalon)
    s = haut_px / im.height
    return im.resize((round(im.width * s), haut_px), Image.BILINEAR)


def etalonner(im, sombre=0.93, sat=0.88, contraste=0.94):
    from PIL import ImageEnhance
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(contraste)
    a = np.asarray(im).astype(np.float32) / 255
    a = np.clip(a ** (1 / sombre) * 0.97 + 0.02, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8))


# ---------------------------------------------------------------- synchro labiale
FORMES = ['A', 'O', 'OU', 'IE', 'MBP', 'FV', 'L', 'repos']


def formes_du_texte(texte):
    """Découpe un texte français en formes de bouche, dans l'ordre."""
    t = texte.lower()
    for a, b in [('eau', 'o'), ('au', 'o'), ('ou', 'ü'), ('oi', 'wa'), ('ch', 'l'), ('qu', 'k'),
                 ('é', 'e'), ('è', 'e'), ('ê', 'e'), ('à', 'a'), ('â', 'a'), ('ô', 'o'), ('ù', 'ü'), ('û', 'ü'), ('î', 'i'), ('ï', 'i')]:
        t = t.replace(a, b)
    out = []
    for c in t:
        if c in 'a': out.append('A')
        elif c in 'o': out.append('O')
        elif c in 'üuw': out.append('OU')
        elif c in 'eiy': out.append('IE')
        elif c in 'mbp': out.append('MBP')
        elif c in 'fv': out.append('FV')
        elif c in 'ltdnszcjkgrx': out.append('L')
        elif c in ' ,;:': out.append('repos')
        elif c in '.!?…': out.extend(['repos', 'repos'])
    # deux consonnes de suite se fondent : on garde la seconde
    res = []
    for f in out:
        if res and res[-1] == f and f != 'repos':
            continue
        res.append(f)
    return res


def duree_replique(texte):
    return 0.35 + 0.068 * len(texte)


# ---------------------------------------------------------------- acteurs
@dataclass
class Acteur:
    nom: str                     # 'seb', 'diana', 'kristina', ou un nom libre
    image: object                # chemin, ou ('pantin', corps, tete) ; pour un parleur : son corps
    x: float = 0.5               # position des pieds, en fraction de la largeur du DÉCOR
    y: float = 0.95              # en fraction de la hauteur
    h: float = 0.7               # hauteur en fraction de l'écran
    miroir: bool = False
    debut: float = 0.0
    fin: float = 1e9
    trajet: list = field(default_factory=list)     # [(t, x, y), ...] dans le plan
    saut: float = 0.0            # amplitude de petits bonds (fraction de l'écran) en déplacement
    tetes: dict = None           # pour un parleur : {'repos': chemin, 'A': chemin, ...}
    expression: object = None    # [(t, chemin_tete), ...] : la tête au repos selon le moment
    gros_plan: bool = False      # True : on affiche la tête seule (pas de corps)
    rot: float = 0.0             # rotation en degrés (apesanteur, rêve)
    tourne: float = 0.0          # vitesse de rotation (degrés par seconde)
    ombre: bool = True
    bras: list = None            # pantin articulé : [(t, angle_gauche, angle_droit), ...]
    kit: tuple = None            # (corps sans bras, bras gauche, bras droit)
    marche: list = None          # cycle de marche : [image1, image2, ...], joué pendant les déplacements
    poses: list = None           # animation de remplacement : [(t, image), ...], l'image entière change
    parle: list = None           # poses de parole : [image, ...], enchaînées tant qu'il parle
    tempo_parle: float = 0.42    # durée d'une pose de parole (secondes)
    brut: bool = False           # images d'une même planche : toile commune, pas de recadrage
    coupe_x: float = None        # fraction du décor au-delà de laquelle l'acteur disparaît (entrée de tunnel)
    marche_pas: int = 2          # images du cycle : une toutes les marche_pas*PAS images

    def angles(self, t):
        pts = self.bras
        if t <= pts[0][0]:
            return pts[0][1], pts[0][2]
        for (t0, g0, d0), (t1, g1, d1) in zip(pts, pts[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / max(1e-6, t1 - t0)
                k = k * k * (3 - 2 * k)
                return g0 + (g1 - g0) * k, d0 + (d1 - d0) * k
        return pts[-1][1], pts[-1][2]

    def pos(self, t):
        if not self.trajet:
            return self.x, self.y
        pts = self.trajet
        if t <= pts[0][0]:
            return pts[0][1], pts[0][2]
        for (t0, x0, y0, *_), (t1, x1, y1, *_) in zip(pts, pts[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / max(1e-6, t1 - t0)
                return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
        return pts[-1][1], pts[-1][2]

    def taille(self, t):
        """Un trajet peut porter une 4e valeur : la taille relative (perspective, l'acteur s'éloigne)."""
        pts = self.trajet
        if not pts or len(pts[0]) < 4:
            return 1.0
        if t <= pts[0][0]:
            return pts[0][3]
        for p0, p1 in zip(pts, pts[1:]):
            if p0[0] <= t <= p1[0]:
                k = (t - p0[0]) / max(1e-6, p1[0] - p0[0])
                return p0[3] + (p1[3] - p0[3]) * k
        return pts[-1][3]

    def bouge(self, t, dt=0.1):
        (xa, ya), (xb, yb) = self.pos(max(0, t - dt)), self.pos(t)
        return abs(xb - xa) + abs(yb - ya) > 1e-4


@dataclass
class Replique:
    qui: str
    debut: float
    texte: str
    sous_titre: bool = True
    off: bool = False            # voix off : pas de bouche qui bouge

    @property
    def fin(self):
        return self.debut + duree_replique(self.texte)


@dataclass
class Plan:
    duree: float
    decor: str = None            # chemin, ou None pour un fond procédural
    fond: str = None             # 'reve' : fond imaginaire saturé
    cam: tuple = (0.5, 0.5)      # centre de la caméra au début et à la fin (fraction de la largeur du décor)
    zoom: tuple = (1.0, 1.0)
    cam_y: float = 0.5
    acteurs: list = field(default_factory=list)
    repliques: list = field(default_factory=list)
    cartons: list = field(default_factory=list)   # [(debut, fin, texte, sous_texte)]
    bruits: list = field(default_factory=list)    # [(t, 'nom')]
    etalonner: bool = True
    flash: list = field(default_factory=list)     # [(t, durée)] flash blanc
    vague: tuple = None                            # (debut, fin) : ondulation d'entrée dans le rêve


# ---------------------------------------------------------------- dessin
def fond_reve(t, w, h):
    im = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(im)
    # dégradé saturé violet → bleu nuit
    for y in range(0, h, 4):
        k = y / h
        d.rectangle([0, y, w, y + 4], fill=(int(70 + 60 * (1 - k)), int(20 + 10 * k), int(120 + 80 * k)))
    rnd = random.Random(7)
    for i in range(140):
        x = rnd.random() * w; y = rnd.random() * h; r = rnd.choice([1, 2, 2, 3])
        tw = 0.5 + 0.5 * math.sin(t * 6 + i)
        c = (255, 255, int(160 + 90 * tw))
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
    # planètes découpées
    for (px, py, pr, col, ring) in [(0.15, 0.25, 70, (255, 120, 40), True), (0.82, 0.2, 45, (80, 220, 160), False), (0.7, 0.8, 90, (230, 70, 160), True)]:
        cx = px * w + 20 * math.sin(t * 0.7 + pr); cy = py * h + 10 * math.cos(t * 0.5 + pr)
        d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=col, outline=(30, 10, 40), width=4)
        if ring:
            d.ellipse([cx - pr * 1.7, cy - pr * 0.35, cx + pr * 1.7, cy + pr * 0.35], outline=(255, 240, 120), width=5)
    return im


def confettis(im, t, densite=90):
    d = ImageDraw.Draw(im)
    rnd = random.Random(3)
    for i in range(densite):
        x0 = rnd.random() * W; v = 60 + rnd.random() * 120; ph = rnd.random() * 10
        y = (rnd.random() * H + v * t) % (H + 40) - 20
        x = x0 + 30 * math.sin(t * 2 + ph)
        c = rnd.choice([(255, 60, 160), (255, 220, 40), (60, 220, 255), (120, 255, 90), (255, 140, 30)])
        s = 5 + rnd.random() * 6
        ang = t * 4 + ph
        pts = [(x + s * math.cos(ang + k * math.pi / 2), y + s * 0.5 * math.sin(ang + k * math.pi / 2)) for k in range(4)]
        d.polygon(pts, fill=c)


def feux(im, t, centres):
    d = ImageDraw.Draw(im)
    for i, (cx, cy, t0) in enumerate(centres):
        u = (t - t0) % 1.6
        if u > 1.2:
            continue
        r = 20 + 220 * u
        a = max(0, 1 - u / 1.2)
        col = [(255, 80, 200), (255, 230, 60), (90, 230, 255)][i % 3]
        col = tuple(int(c * a + 30 * (1 - a)) for c in col)
        for k in range(16):
            ang = k * math.pi / 8 + i
            x = cx * W + r * math.cos(ang); y = cy * H + r * math.sin(ang)
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=col)


def texte_contour(d, xy, texte, police, fill, contour=(0, 0, 0), ep=3, anchor='mm'):
    d.text(xy, texte, font=police, fill=fill, stroke_width=ep, stroke_fill=contour, anchor=anchor)


def dessiner_carton(im, texte, sous, k, yk=0.70):
    """Carton orange, lettres découpées un peu de travers, comme les cartons-titres de la série."""
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(POLICE_CARTON, 64); f2 = ImageFont.truetype(POLICE_CARTON, 26)
    rnd = random.Random(len(texte))
    x = W * 0.5; y = H * yk
    larg = d.textlength(texte, font=f)
    cx = x - larg / 2
    for ch in texte:
        lw = d.textlength(ch, font=f)
        dy = rnd.uniform(-6, 6)
        texte_contour(d, (cx + lw / 2, y + dy), ch, f, (255, 140, 30), (60, 20, 0), 4)
        cx += lw
    if sous:
        texte_contour(d, (x, y + 58), sous, f2, (255, 170, 70), (60, 20, 0), 3)


def dessiner_sous_titre(im, texte, qui):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(POLICE, 30)
    couleur = {'seb': (255, 255, 255), 'diana': (255, 210, 190), 'kristina': (255, 230, 170)}.get(qui, (235, 235, 235))
    # coupe en deux lignes si trop long
    mots = texte.split(); lignes = [''];
    for m in mots:
        if d.textlength(lignes[-1] + ' ' + m, font=f) > W * 0.8:
            lignes.append(m)
        else:
            lignes[-1] = (lignes[-1] + ' ' + m).strip()
    y = H - 40 - 38 * (len(lignes) - 1)
    for l in lignes:
        texte_contour(d, (W / 2, y), l, f, couleur, (0, 0, 0), 4)
        y += 38


def tete_du_moment(a, t, repliques):
    """Le chemin de la tête à afficher : la bouche si l'acteur parle, sinon son expression."""
    repos = a.tetes.get('repos') if a.tetes else None
    if a.expression:
        for (te, chemin) in a.expression:
            if t >= te:
                repos = chemin
    for r in repliques:
        if r.qui == a.nom and not r.off and r.debut <= t < r.fin:
            formes = formes_du_texte(r.texte)
            k = (t - r.debut) / duree_replique(r.texte)
            f = formes[min(len(formes) - 1, int(k * len(formes)))] if formes else 'repos'
            if f == 'repos':
                return repos or a.tetes.get('repos')
            return a.tetes.get(f) or a.tetes.get('A') or repos
    return repos


def dessiner_plan(p, t, monde_cache={}):
    ta = math.floor(t * FPS / PAS) * PAS / FPS          # temps « sur deux images »
    k = t / max(1e-6, p.duree)
    k_cam = k * k * (3 - 2 * k)                          # caméra adoucie
    zoom = p.zoom[0] + (p.zoom[1] - p.zoom[0]) * k_cam
    # --- fond
    if p.fond == 'reve':
        base = fond_reve(t, W, H)
        Hd = H; dw = W; off_x = 0; off_y = 0; echelle = 1.0
        cadre = base
    else:
        Hd = round(H * zoom)
        dec = decor(p.decor, Hd, p.etalonner)
        dw = dec.width
        cx = (p.cam[0] + (p.cam[1] - p.cam[0]) * k_cam) * dw
        off_x = int(min(max(0, cx - W / 2), max(0, dw - W)))
        off_y = int(min(max(0, p.cam_y * Hd - H / 2), Hd - H))
        cadre = dec.crop((off_x, off_y, off_x + W, off_y + H))
        echelle = zoom
    im = cadre.convert('RGBA')
    # --- acteurs (dans l'ordre : les premiers derrière)
    for a in p.acteurs:
        if not (a.debut <= t < a.fin):
            continue
        ax, ay = a.pos(ta)
        hp = a.h * H * (1 if a.gros_plan else echelle) * a.taille(ta)
        if a.tetes and a.gros_plan:
            cle = tete_du_moment(a, ta, p.repliques)
            spr = a_taille(cle, hp, a.miroir)
        elif a.marche and a.bouge(ta):
            i = int(ta * FPS / PAS / a.marche_pas) % len(a.marche)
            spr = a_taille(('brut', a.marche[i]) if a.brut else a.marche[i], hp, a.miroir)
        elif a.parle and any(r.qui == a.nom and not r.off and r.debut <= ta < r.fin for r in p.repliques):
            # il parle : on enchaîne ses poses de parole, sans répéter deux fois la même
            n = int(ta / a.tempo_parle)
            rnd = random.Random(sum(map(ord, a.nom)) + n)
            i = (n * 3 + rnd.randrange(len(a.parle))) % len(a.parle)
            if i == (((n - 1) * 3 + random.Random(sum(map(ord, a.nom)) + n - 1).randrange(len(a.parle))) % len(a.parle)):
                i = (i + 1) % len(a.parle)
            spr = a_taille(('brut', a.parle[i]) if a.brut else a.parle[i], hp, a.miroir)
        elif a.poses:
            ch = a.poses[0][1]
            for (tp, c) in a.poses:
                if ta >= tp:
                    ch = c
            spr = a_taille(('brut', ch) if a.brut else ch, hp, a.miroir)
        elif a.kit and a.bras:
            tete = tete_du_moment(a, ta, p.repliques) if a.tetes else None
            ag, ad = a.angles(ta)
            cle = ('articule', a.kit[0], a.kit[1], a.kit[2], float(round(ag / 3) * 3), float(round(ad / 3) * 3), tete)
            spr = a_taille(cle, hp, a.miroir)
        elif a.tetes:
            tete = tete_du_moment(a, ta, p.repliques)
            cle = ('pantin', a.image, tete) if tete else a.image
            spr = a_taille(cle, hp, a.miroir)
        else:
            spr = a_taille(('brut', a.image) if a.brut else a.image, hp, a.miroir)
        # petits bonds raides quand il se déplace
        bond = 0
        if a.saut and a.bouge(ta):
            bond = abs(math.sin(ta * 2 * math.pi * 2.5)) * a.saut * H
        # tête qui dodeline quand il parle
        if any(r.qui == a.nom and not r.off and r.debut <= ta < r.fin for r in p.repliques):
            bond += 2 * math.sin(ta * 9)
        rot = a.rot + a.tourne * ta
        if rot:
            spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
        if a.gros_plan:
            px = W / 2 - spr.width / 2 + (ax - 0.5) * 0  # face caméra, centré
            py = H * ay - spr.height - bond
        else:
            px = ax * dw - off_x - spr.width / 2 if p.fond != 'reve' else ax * W - spr.width / 2
            py = ay * Hd - off_y - spr.height - bond if p.fond != 'reve' else ay * H - spr.height - bond
        if a.ombre and p.fond != 'reve' and not a.gros_plan:
            sh = Image.new('L', im.size, 0)
            ImageDraw.Draw(sh).ellipse([px + spr.width * 0.12, ay * Hd - off_y - spr.height * 0.025,
                                        px + spr.width * 0.88, ay * Hd - off_y + spr.height * 0.012], fill=140)
            im = Image.composite(Image.new('RGBA', im.size, (18, 18, 24, 255)), im, sh.filter(ImageFilter.GaussianBlur(1.5)))
        if a.coupe_x is not None:
            lim = int(a.coupe_x * dw - off_x - px)          # en pixels dans le sprite
            if lim <= 0:
                continue
            if lim < spr.width:
                spr = spr.copy(); al = spr.getchannel('A')
                ImageDraw.Draw(al).rectangle([lim, 0, spr.width, spr.height], fill=0)
                spr.putalpha(al)
        im.alpha_composite(spr, (int(px), int(py)))
    im = im.convert('RGB')
    if p.fond == 'reve':
        confettis(im, t); feux(im, t, [(0.25, 0.3, 0.0), (0.75, 0.25, 0.5), (0.5, 0.15, 1.0)])
    # --- ondulation d'entrée dans le rêve
    if p.vague and p.vague[0] <= t < p.vague[1]:
        u = (t - p.vague[0]) / (p.vague[1] - p.vague[0])
        a_ = np.asarray(im); out = np.empty_like(a_)
        amp = 30 * math.sin(math.pi * u)
        for y in range(H):
            out[y] = np.roll(a_[y], int(amp * math.sin(y / 18 + t * 12)), axis=0)
        im = Image.fromarray(out)
        # bascule de couleur, comme quand Angela part dans l'imaginaire
        from PIL import ImageOps
        im = Image.blend(im, ImageOps.posterize(im, 3), 0.5 * math.sin(math.pi * u))
    # --- flash
    for (tf, df) in p.flash:
        if tf <= t < tf + df:
            im = Image.blend(im, Image.new('RGB', im.size, (255, 255, 255)), 0.85)
    # --- cartons et sous-titres
    for c in p.cartons:
        d0, d1, txt, sous = c[:4]
        if d0 <= t < d1:
            dessiner_carton(im, txt, sous, (t - d0) / (d1 - d0), *(c[4:5] or [0.70]))
    for r in p.repliques:
        if r.sous_titre and r.debut <= t < r.fin + 0.25:
            dessiner_sous_titre(im, r.texte, r.qui)
    return im


# ---------------------------------------------------------------- son
def _env(n, att=0.005, rel=0.08):
    t = np.arange(n) / SR
    return np.minimum(1, t / att) * np.exp(-t / rel)


def pluck(f, dur, amp=0.25):
    """Corde pincée (Karplus-Strong) : une sorte de ukulélé de dessin animé."""
    n = int(SR * dur); p = max(2, int(SR / f))
    rnd = np.random.default_rng(int(f * 10))
    buf = rnd.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * amp


@lru_cache(maxsize=64)
def _pluck_c(f, dur, amp):
    return pluck(f, dur, amp)


def musique(duree, bpm=104, reve=None):
    n = int(SR * duree); mix = np.zeros(n)
    noire = 60 / bpm
    # progression un peu bancale, jazzy : Ré m7 – Sol 7 – Do maj7 – La 7
    accords = [[146.8, 174.6, 220.0, 261.6], [196.0, 246.9, 293.7, 349.2], [130.8, 164.8, 196.0, 246.9], [110.0, 138.6, 164.8, 196.0]]
    basses = [73.4, 98.0, 65.4, 55.0]
    t = 0.0; i = 0
    while t < duree:
        mesure = int(t / (4 * noire)) % 4
        ac = accords[mesure]
        for k in range(4):
            tk = t + k * noire
            if tk >= duree:
                break
            s = int(tk * SR)
            # arpège sautillant, deux notes par temps
            for j, dt in enumerate([0, noire / 2]):
                f = ac[(k * 2 + j) % 4] * (2 if j else 1)
                note = _pluck_c(round(f, 1), 0.5, 0.11)
                a = int((tk + dt) * SR); b = min(n, a + len(note))
                if a < n: mix[a:b] += note[: b - a]
            # basse sur le temps
            fb = basses[mesure] * (1 if k % 2 == 0 else 1.5)
            nb = int(SR * noire * 0.9); tt = np.arange(nb) / SR
            bas = 0.16 * np.sin(2 * np.pi * fb * tt) * np.exp(-tt * 4)
            b2 = min(n, s + nb)
            if s < n: mix[s:b2] += bas[: b2 - s]
        t += 4 * noire
    # pendant le rêve : clochettes en plus
    if reve:
        r0, r1 = reve; rnd = np.random.default_rng(5)
        tt = r0
        while tt < r1:
            f = rnd.choice([1046.5, 1318.5, 1568.0, 2093.0]); nb = int(SR * 0.6); x = np.arange(nb) / SR
            cl = 0.07 * np.sin(2 * np.pi * f * x) * np.exp(-x * 5)
            a = int(tt * SR); b = min(n, a + nb)
            mix[a:b] += cl[: b - a]; tt += 0.18
    return mix


def bruit(nom, n=None):
    rnd = np.random.default_rng(abs(hash(nom)) % 2**32)
    if nom == 'boing':
        d = 0.5; x = np.arange(int(SR * d)) / SR; f = 180 + 220 * np.exp(-x * 6) * np.sin(x * 40)
        return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 4)
    if nom == 'whoosh':
        d = 0.7; m = int(SR * d); w = rnd.normal(0, 1, m); x = np.arange(m) / SR
        env = np.sin(np.pi * x / d) ** 2
        w = np.convolve(w, np.ones(30) / 30, mode='same')
        return 0.5 * w * env
    if nom == 'ouaf':
        d = 0.28; m = int(SR * d); x = np.arange(m) / SR
        f = 420 * np.exp(-x * 5) + 160
        tone = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + rnd.normal(0, 0.4, m)
        tone = np.convolve(tone, np.ones(12) / 12, mode='same')
        return 0.45 * tone * np.exp(-x * 9) * np.minimum(1, x / 0.01)
    if nom == 'scratch':
        d = 0.45; m = int(SR * d); x = np.arange(m) / SR
        f = 900 * (1 - x / d) + 120
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) + rnd.normal(0, 0.5, m)
        return 0.4 * s * np.exp(-x * 2)
    if nom == 'pouet':
        d = 0.35; x = np.arange(int(SR * d)) / SR
        return 0.3 * np.sign(np.sin(2 * np.pi * (300 - 150 * x / d) * x)) * np.exp(-x * 5)
    if nom == 'tada':
        out = np.zeros(int(SR * 1.2))
        for i, f in enumerate([523.3, 659.3, 784.0, 1046.5]):
            nb = int(SR * 0.9); x = np.arange(nb) / SR
            a = int(i * 0.08 * SR)
            out[a:a + nb] += 0.12 * (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(4 * np.pi * f * x)) * np.exp(-x * 2.5)
        return out
    if nom == 'pop':
        x = np.arange(int(SR * 0.12)) / SR
        return 0.4 * np.sin(2 * np.pi * (600 + 2000 * x) * x) * np.exp(-x * 40)
    return np.zeros(10)


def babil(texte, voix):
    """Le babillage : une petite note par syllabe, à la hauteur de la voix du personnage."""
    base = {'seb': 150, 'diana': 245, 'kristina': 280}.get(voix, 200)
    formes = formes_du_texte(texte)
    d = duree_replique(texte); n = int(SR * d); out = np.zeros(n)
    rnd = np.random.default_rng(len(texte))
    pas = d / max(1, len(formes))
    for i, f in enumerate(formes):
        if f == 'repos' or f in ('MBP', 'L', 'FV'):
            continue
        hauteur = base * {'A': 1.0, 'O': 0.9, 'OU': 0.8, 'IE': 1.2}[f] * rnd.uniform(0.92, 1.12)
        m = int(SR * min(0.11, pas * 1.4)); x = np.arange(m) / SR
        # une voyelle « bouche » : fondamentale + deux harmoniques
        s = (np.sin(2 * np.pi * hauteur * x) + 0.5 * np.sin(4 * np.pi * hauteur * x) + 0.25 * np.sin(6 * np.pi * hauteur * x))
        s *= np.minimum(1, x / 0.01) * np.exp(-x * 18)
        a = int(i * pas * SR); b = min(n, a + m)
        out[a:b] += 0.16 * s[: b - a]
    return out


# ---------------------------------------------------------------- rendu
def caler(plans):
    """Décale les répliques qui se chevauchent, et allonge le plan si besoin."""
    for p in plans:
        fin = -1
        for r in sorted(p.repliques, key=lambda r: r.debut):
            if r.debut < fin + 0.15:
                r.debut = fin + 0.15
            fin = r.fin
        if p.repliques:
            p.duree = max(p.duree, max(r.fin for r in p.repliques) + 0.5)
    return plans


def rendre(plans, sortie, dossier='rendu', images_cles=None):
    os.makedirs(dossier, exist_ok=True)
    fichiers = []
    t_total = 0.0
    sons = []          # (t_absolu, tableau)
    for i, p in enumerate(plans):
        nom = os.path.join(dossier, f'plan{i:02d}.mp4'); tmp = nom.replace('.mp4', '.tmp.mp4')
        nimg = int(round(p.duree * FPS))
        proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                                 '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                                 '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
        for f in range(nimg):
            im = dessiner_plan(p, f / FPS)
            proc.stdin.write(im.tobytes())
        proc.stdin.close(); proc.wait()
        if proc.returncode != 0:
            raise SystemExit(f'ffmpeg a échoué sur le plan {i}')
        os.replace(tmp, nom); fichiers.append(nom)
        for r in p.repliques:
            if not r.off or True:
                sons.append((t_total + r.debut, babil(r.texte, r.qui)))
        for (tb, nb) in p.bruits:
            sons.append((t_total + tb, bruit(nb)))
        print(f'plan {i:02d} : {p.duree:.1f} s', flush=True)
        t_total += nimg / FPS
    # concat
    liste = os.path.join(dossier, 'liste.txt')
    with open(liste, 'w') as fh:
        for f in fichiers:
            fh.write(f"file '{os.path.abspath(f)}'\n")
    video = os.path.join(dossier, 'video.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', liste, '-c', 'copy', video], check=True)
    return video, t_total, sons


def mixer(t_total, sons, reve, chemin_wav):
    n = int(SR * t_total) + SR
    mix = musique(t_total + 1, reve=reve) * 0.8
    for (t0, s) in sons:
        a = int(t0 * SR); b = min(n, a + len(s))
        if a < n:
            mix[a:b] += s[: b - a]
    mix = mix[:int(SR * t_total)]
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.85
    with wave.open(chemin_wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
