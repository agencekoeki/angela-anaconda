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
# FORMAT=vertical : les shorts (9:16) ; LANGUE=fr|en|es : la langue des sous-titres et des cartons
VERTICAL = os.environ.get('FORMAT', '') == 'vertical'
if VERTICAL:
    W, H = 1080, 1920
LANGUE = os.environ.get('LANGUE', 'fr')
TAILLE_ST = 66 if VERTICAL else 30            # sous-titres : gros sur téléphone
TAILLE_CARTON = (104, 58) if VERTICAL else (64, 26)
Y_ST = 0.70                  # vertical : la ligne des sous-titres (fraction de la hauteur) ; la bande 0,66–0,76 reste libre de visages
                             # (Sébastien, 30/10 : pas en plein milieu ; plus bas, c'est la légende et les boutons de TikTok)
ST_MIN = 1.5                 # un sous-titre reste au moins 1,5 s à l'écran (lisible même pour un seul mot)
SR = 44100
ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)     # les chemins 'assets/…', 'banque/…', 'polices/…' sont relatifs à l'atelier, d'où qu'on lance le script


def _police_systeme(nom):
    """Une police DejaVu : celle du système (Linux), sinon la copie de polices/ (Windows, Mac)."""
    for c in ('/usr/share/fonts/truetype/dejavu/' + nom, os.path.join(ICI, 'polices', nom)):
        if os.path.exists(c):
            return c
    raise FileNotFoundError(nom + ' : lancer polices/telecharger.sh (voir polices/LISEZ-MOI.md)')


def _media_local():
    """Le dossier media-local (décors, flocages, planches) : $MEDIA_LOCAL, sinon le parent de l'atelier
    (clone du dépôt privé, ou media-local du PC), sinon ../../media-local (dépôt public), sinon l'upload du conteneur."""
    for c in (os.environ.get('MEDIA_LOCAL'), os.path.dirname(ICI), os.path.join(ICI, '..', '..', 'media-local'),
              '/mnt/user-data/uploads/angela-anaconda/media-local'):
        if c and os.path.isdir(os.path.join(c, 'decors')):
            return os.path.abspath(c)
    return None


MEDIA_LOCAL = _media_local()
POLICE = _police_systeme('DejaVuSans-Bold.ttf')
POLICE_CARTON = _police_systeme('DejaVuSerif-Bold.ttf')
POLICE_ST = os.path.join(ICI, 'polices', 'Fredoka.ttf')          # sous-titres : ronde, grasse, « dessin animé » (OFL, Google Fonts)
POLICE_CARTE = os.path.join(ICI, 'polices', 'LuckiestGuy-Regular.ttf')   # la carte-titre (Apache 2.0, Google Fonts)


@lru_cache(maxsize=16)
def police_st(taille, graisse='Bold'):
    if not os.path.exists(POLICE_ST):
        return ImageFont.truetype(POLICE, taille)
    f = ImageFont.truetype(POLICE_ST, taille)
    try:
        f.set_variation_by_name(graisse)
    except Exception:
        pass
    return f


def police_carte(taille):
    return ImageFont.truetype(POLICE_CARTE if os.path.exists(POLICE_CARTE) else POLICE, taille)


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
    cadre: tuple = None          # (x0, y0, x1, y1[, t_fin]) : l'acteur n'est visible que dans ce rectangle (un écran),
                                 # en fraction du décor (ou de l'image pour un fond procédural) ; jusqu'à t_fin
    contour: tuple = None        # (couleur, épaisseur px[, flou px]) : liseré (ou halo flou) qui détache le personnage du fond
    opacite: list = None         # [(t, 0..1), ...] : apparition, disparition
    cible: tuple = None          # (x0, y0, x1, y1) en fraction du décor : la place exacte que l'acteur doit couvrir sans déborder (une vitre)
    flocage: str = None          # un imprimé SEO Addict posé sur le t-shirt rose, dans les poses de face (floquer.py)
    ajuster: bool = False        # avec une cible : l'image est étirée pour couvrir exactement la cible (la lueur d'un écran)
    echelle_libre: bool = False  # taille voulue hors proportions (Tara dans le téléphone, le rêve) : le contrôle des tailles l'ignore

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
    tr: dict = None              # traductions du sous-titre : {'en': …, 'es': …} ; la bouche et le son suivent toujours le texte français

    @property
    def affiche(self):
        return (self.tr or {}).get(LANGUE, self.texte) if LANGUE != 'fr' else self.texte

    @property
    def fin(self):
        return self.debut + duree_replique(self.texte)

    @property
    def fin_st(self):
        return max(self.fin + 0.25, self.debut + ST_MIN)


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
    horloge: list = field(default_factory=list)   # [(debut, fin, '04:30')] : l'heure, en chiffres de réveil cathodique
    noir: tuple = None                             # (debut, fin) : la lumière s'éteint (fondu au noir, les sous-titres restent)
    volet: list = field(default_factory=list)     # [(debut, fin, 'couvre'|'decouvre')] : le volet bleu ondulé des changements de temps
    souvenir: bool = False                         # le passé : sépia, vignette, grain
    bandeaux: list = field(default_factory=list)  # [(debut, fin, texte, sous, yk, taille)] : texte sur bandeau sombre (pépite, appel)
    postits: list = field(default_factory=list)   # [(debut, fin, n, (x0, y0, x1, y1), devant)] : les post-it qui envahissent
    crt: dict = None                               # fond='crt' : {'lignes': [(t, texte)], 'barre': (t0, t1), 'allume': t}
    carte: dict = None                             # la carte-titre qui se retourne (carte.py)
    lumiere: tuple = None                          # (debut, fin) : la lumière revient (fondu depuis le noir)


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


BLEU_VOLET = (18, 40, 130)      # assez sombre pour que le carton orange s'y lise (contraste ≥ 3:1)
BLEU_RAYURE = (40, 80, 185)


def fond_bleu(t, w, h):
    """Le bleu des changements de temps : aplat saturé, rayures ondulées qui glissent."""
    y = np.arange(h)[:, None]; x = np.arange(w)[None, :]
    onde = np.sin((y + 22 * np.sin(x / 70 + t * 3)) / 26 + t * 4)
    a = np.empty((h, w, 3), np.uint8)
    m = onde > 0.55
    for c in range(3):
        a[..., c] = np.where(m, BLEU_RAYURE[c], BLEU_VOLET[c])
    return Image.fromarray(a)


GLACE_CRT = (0.09, 0.10, 0.91, 0.80)   # la vitre, en fraction de l'image, pour fond='crt'


def fond_crt(t, w, h, crt):
    """Insert plein cadre : la vitre d'un vieil écran cathodique, bleu nuit, qui s'allume et démarre."""
    crt = crt or {}
    im = Image.new('RGB', (w, h), (188, 176, 150))          # le plastique beige
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = [int(v * s) for v, s in zip(GLACE_CRT, (w, h, w, h))]
    d.rounded_rectangle([x0 - 34, y0 - 34, x1 + 34, y1 + 34], radius=70, fill=(150, 140, 118))
    on = t - crt.get('allume', 0.0)
    if on < 0:
        d.rounded_rectangle([x0, y0, x1, y1], radius=60, fill=(22, 26, 24))
    else:
        g = np.zeros((y1 - y0, x1 - x0, 3), np.float32)
        yy = np.linspace(-1, 1, y1 - y0)[:, None]; xx = np.linspace(-1, 1, x1 - x0)[None, :]
        v = np.clip(1 - 0.55 * (xx ** 2 + yy ** 2), 0, 1)
        g[..., 0] = 14 + 16 * v; g[..., 1] = 22 + 30 * v; g[..., 2] = 52 + 60 * v
        g[::4] *= 0.82                                           # les lignes de balayage
        if on < 0.35:                                            # l'allumage : un trait blanc qui s'ouvre
            k = on / 0.35; band = int((y1 - y0) * k / 2) + 2; mid = (y1 - y0) // 2
            g[:] = 6; g[max(0, mid - band):mid + band] = 200 + 55 * (1 - k)
        glace = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
        masque = Image.new('L', glace.size, 0)
        ImageDraw.Draw(masque).rounded_rectangle([0, 0, glace.width - 1, glace.height - 1], radius=60, fill=255)
        im.paste(glace, (x0, y0), masque)
        f = ImageFont.truetype(POLICE_MONO, int(w * 0.07))
        yl = y0 + 70
        for (tl, texte) in crt.get('lignes', []):
            if t >= tl:
                texte = en_langue(texte)
                n = int((t - tl) * 24)                           # la ligne se tape
                d.text((x0 + 60, yl), texte[:n], font=f, fill=(215, 255, 235))
                if TRACE is not None and n:
                    # écrit sur la vitre bleu nuit (contraste connu, environ 14:1) : True = ne pas remesurer contre lui-même
                    TRACE.append(('texte', 'ecran', texte, d.textbbox((x0 + 60, yl), texte[:n], font=f), (215, 255, 235), f.size, True))
            yl += int(f.size * 1.5)
        if crt.get('barre'):
            b0, b1 = crt['barre']
            if t >= b0:
                k = min(1.0, (t - b0) / max(1e-6, b1 - b0))
                bx0, by0, bx1 = x0 + 60, yl + 10, x1 - 60
                d.rectangle([bx0, by0, bx1, by0 + 44], outline=(215, 255, 235), width=4)
                d.rectangle([bx0 + 8, by0 + 8, bx0 + 8 + int((bx1 - bx0 - 16) * k), by0 + 36], fill=(215, 255, 235))
    # le bouton et la petite diode
    d.ellipse([w * 0.80, h * 0.86, w * 0.86, h * 0.86 + w * 0.06], fill=(120, 110, 92), outline=(80, 72, 60), width=4)
    d.ellipse([w * 0.70, h * 0.875, w * 0.725, h * 0.875 + w * 0.025], fill=(90, 245, 120) if on >= 0 else (40, 60, 40))
    return im


def dessiner_volet(im, t, v0, v1, sens):
    """Le volet bleu ondulé : il couvre l'image de haut en bas (fin de plan) ou la découvre (début du plan suivant)."""
    u = (t - v0) / max(1e-6, v1 - v0)
    u = u * u * (3 - 2 * u)
    amp = H * 0.035
    x = np.arange(W)
    bord = (u * (H + 2 * amp) - amp) + amp * np.sin(x / (W / 2.4) * 2 * np.pi + t * 7)
    yy = np.arange(H)[:, None]
    m = (yy < bord[None, :]) if sens == 'couvre' else (yy > bord[None, :])
    bleu = np.asarray(fond_bleu(t, W, H))
    a = np.asarray(im).copy()
    a[m] = bleu[m]
    return Image.fromarray(a)


def filtre_souvenir(im, t, sepia=0.7):
    """Le passé : sépia (sur le décor), vignette, grain qui bouge sur deux images."""
    a = np.asarray(im).astype(np.float32) / 255
    if sepia:
        g = a @ np.array([0.30, 0.59, 0.11], np.float32)
        sep = np.stack([g * 1.07 + 0.05, g * 0.95 + 0.03, g * 0.78], -1)
        a = (1 - sepia) * a + sepia * sep
    yy = np.linspace(-1, 1, H)[:, None]; xx = np.linspace(-1, 1, W)[None, :]
    a *= np.clip(1.08 - 0.42 * (xx ** 2 * 0.8 + yy ** 2), 0, 1)[..., None]
    rnd = np.random.default_rng(int(t * FPS / PAS))
    a += rnd.normal(0, 0.025, (H, W, 1)).astype(np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


POSTIT = [(250, 228, 96), (250, 168, 190), (168, 228, 146), (150, 200, 250), (255, 190, 110)]


def dessiner_postits(im, t, t0, t1, n, zone, graine=3):
    """Les idées qui s'accumulent : des post-it qui poppent un à un, de travers."""
    if t < t0:
        return im
    rnd = random.Random(graine)
    x0, y0, x1, y1 = zone
    vis = n if t >= t1 else int(n * (t - t0) / max(1e-6, t1 - t0)) + 1
    im = im.convert('RGBA')
    for k in range(n):
        px = rnd.uniform(x0, x1) * W; py = rnd.uniform(y0, y1) * H
        rot = rnd.uniform(-14, 14); col = rnd.choice(POSTIT); c = W * rnd.uniform(0.065, 0.085)
        if k >= vis:
            continue
        tk = t0 + (t1 - t0) * k / max(1, n)
        s = min(1.0, 0.4 + (t - tk) / 0.15) if t - tk < 0.15 else 1.0
        cc = int(c * s)
        p = Image.new('RGBA', (cc, cc), col + (255,))
        d = ImageDraw.Draw(p)
        d.rectangle([0, 0, cc - 1, int(cc * 0.18)], fill=tuple(max(0, v - 30) for v in col) + (255,))
        for j in range(3):
            yl = int(cc * (0.38 + 0.18 * j))
            d.line([cc * 0.14, yl, cc * (0.86 - 0.2 * (j == 2)), yl + rnd.randint(-2, 2)], fill=(60, 60, 90, 255), width=max(2, cc // 26))
        p = p.rotate(rot, resample=Image.BICUBIC, expand=True)
        ombre = Image.new('RGBA', p.size, (0, 0, 0, 0)); ombre.putalpha(p.getchannel('A').point(lambda v: v * 0.35))
        im.alpha_composite(ombre, (int(px - p.width / 2 + 4), int(py - p.height / 2 + 5)))
        im.alpha_composite(p, (int(px - p.width / 2), int(py - p.height / 2)))
    return im.convert('RGB')


def dessiner_bandeau(im, texte, sous, k, yk=0.16, taille=1.0):
    """La pépite et l'appel : texte jaune et blanc sur un bandeau bleu nuit, qui entre par la gauche."""
    texte, sous = en_langue(texte), en_langue(sous)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(POLICE, int((76 if VERTICAL else 44) * taille))
    f2 = ImageFont.truetype(POLICE, int((56 if VERTICAL else 26) * taille))
    larg_max = W * (0.80 if yk < 0.3 else 0.74)          # en haut, hors de la colonne des boutons : un peu plus large
    while d.textlength(texte, font=f) > larg_max and f.size > 24:
        f = ImageFont.truetype(POLICE, f.size - 2)
    lignes2 = []
    if sous:
        mots = sous.split(); l = ''
        for m in mots:
            if d.textlength((l + ' ' + m).strip(), font=f2) > larg_max:
                lignes2.append(l); l = m
            else:
                l = (l + ' ' + m).strip()
        lignes2.append(l)
    hb = f.size * 1.5 + len(lignes2) * f2.size * 1.3 + 30
    yc = H * yk
    entree = min(1.0, k * 6) if k < 1 else 1.0
    entree = 1 - (1 - entree) ** 3
    dx = int(-W * (1 - entree))
    d.rounded_rectangle([W * 0.07 + dx, yc - 20, W * 0.93 + dx, yc + hb], radius=26, fill=(16, 20, 46), outline=(255, 214, 60), width=5)
    d.text((W / 2 + dx, yc + f.size * 0.8), texte, font=f, fill=(255, 214, 60), anchor='mm')
    yl = yc + f.size * 1.55 + f2.size * 0.5
    for l in lignes2:
        d.text((W / 2 + dx, yl), l, font=f2, fill=(255, 255, 255), anchor='mm'); yl += f2.size * 1.3
    if TRACE is not None:
        larg = max([d.textlength(texte, font=f)] + [d.textlength(l, font=f2) for l in lignes2])
        TRACE.append(('texte', 'bandeau', texte, (int(W / 2 - larg / 2 + dx), int(yc), int(W / 2 + larg / 2 + dx), int(yc + hb - 30)), (255, 214, 60), min(f.size, f2.size if sous else f.size), True))


TRACE = None     # controle.py y range ce qui est dessiné : acteurs (position, masque) et textes (boîte, couleur, taille)


def texte_contour(d, xy, texte, police, fill, contour=(0, 0, 0), ep=3, anchor='mm'):
    d.text(xy, texte, font=police, fill=fill, stroke_width=ep, stroke_fill=contour, anchor=anchor)
    if TRACE is not None:
        bb = d.textbbox(xy, texte, font=police, anchor=anchor, stroke_width=ep)
        TRACE.append(('texte', 'lettres', texte, bb, fill, police.size, False, contour, ep))


def en_langue(v):
    """Un texte, ou un dictionnaire {'fr': …, 'en': …, 'es': …}."""
    if isinstance(v, dict):
        return v.get(LANGUE) or v.get('fr')
    return v


def dessiner_carton(im, texte, sous, k, yk=0.70, taille=1.0):
    """Carton orange, lettres découpées un peu de travers, comme les cartons-titres de la série."""
    texte, sous = en_langue(texte), en_langue(sous)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(POLICE_CARTON, int(TAILLE_CARTON[0] * taille)); f2 = ImageFont.truetype(POLICE_CARTON, int(TAILLE_CARTON[1] * taille))
    # un titre trop long pour la largeur se réduit
    while d.textlength(texte, font=f) > W * (0.78 if VERTICAL else 0.88) and f.size > 20:
        f = ImageFont.truetype(POLICE_CARTON, f.size - 4)
    global TRACE
    trace, TRACE = TRACE, None          # le carton se trace en entier, pas lettre par lettre
    rnd = random.Random(len(texte))
    x = W * 0.5; y = H * yk
    larg = d.textlength(texte, font=f)
    cx = x - larg / 2
    for ch in texte:
        lw = d.textlength(ch, font=f)
        dy = rnd.uniform(-6, 6)
        texte_contour(d, (cx + lw / 2, y + dy), ch, f, (255, 140, 30), (14, 5, 0), 4 if not VERTICAL else 7)
        cx += lw
    bb = [x - larg / 2, y - f.size * 0.62, x + larg / 2, y + f.size * 0.62]
    if sous:
        while d.textlength(sous, font=f2) > W * ((0.84 if yk < 0.35 else 0.78) if VERTICAL else 0.9) and f2.size > 14:
            f2 = ImageFont.truetype(POLICE_CARTON, f2.size - 2)
        texte_contour(d, (x, y + f.size * 0.9), sous, f2, (255, 170, 70), (14, 5, 0), 3 if not VERTICAL else 6)
    TRACE = trace
    if TRACE is not None:
        TRACE.append(('texte', 'carton', texte, tuple(int(v) for v in bb), (255, 140, 30), f.size, False, (14, 5, 0), 7))
        if sous:
            sb = d.textbbox((x, y + f.size * 0.9), sous, font=f2, anchor='mm')
            TRACE.append(('texte', 'carton-sous', sous, sb, (255, 170, 70), f2.size, False, (14, 5, 0), 6))


POLICE_MONO = _police_systeme('DejaVuSansMono-Bold.ttf')


def dessiner_horloge(im, texte, t, xk=0.5):
    """Un radio-réveil : chiffres turquoise sur fond noir, dans un boîtier beige, qui clignotent à l'apparition."""
    texte = en_langue(texte)
    d = ImageDraw.Draw(im)
    taille = int((84 if VERTICAL else 56))
    f = ImageFont.truetype(POLICE_MONO, taille)
    larg = d.textlength(texte, font=f)
    x0 = W * xk - larg / 2 - taille * 0.45; y0 = H * (0.135 if VERTICAL else 0.06)   # vertical : sous la barre des applis
    x1 = W * xk + larg / 2 + taille * 0.45; y1 = y0 + taille * 1.45
    d.rounded_rectangle([x0 - 10, y0 - 10, x1 + 10, y1 + 10], radius=18, fill=(196, 184, 160), outline=(60, 50, 40), width=4)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(10, 18, 16))
    if t < 0.5 and int(t * 8) % 2 == 1:
        return                                    # le clignotement du réglage
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), texte, font=f, fill=(90, 245, 225), anchor='mm')


def dessiner_sous_titre(im, texte, qui):
    d = ImageDraw.Draw(im)
    f = police_st(TAILLE_ST) if VERTICAL else ImageFont.truetype(POLICE, TAILLE_ST)
    couleur = {'seb': (255, 255, 255), 'diana': (255, 210, 190), 'kristina': (255, 230, 170),
               'tara': (110, 245, 235)}.get(qui, (235, 235, 235))
    # coupe en lignes si trop long ; la ponctuation haute reste collée au mot (« Tarascon ? »)
    mots = []
    for m in texte.split():
        if mots and m in ('?', '!', ':', ';', '?!', '!?', '»', '…'):
            mots[-1] += '\u00a0' + m
        else:
            mots.append(m)
    lignes = [''];
    for m in mots:
        if d.textlength(lignes[-1] + ' ' + m, font=f) > W * (0.72 if VERTICAL else 0.8):
            lignes.append(m)
        else:
            lignes[-1] = (lignes[-1] + ' ' + m).strip()
    pas = int(TAILLE_ST * 1.25)
    if VERTICAL:
        # au-dessus du tiers bas (la légende et les boutons des applications occupent le bas)
        # sous-titres centrés à Y_ST (70 %), dans la bande 0,66–0,76 ; plus bas vivent la légende et les boutons des applis
        y = int(H * Y_ST) - pas * (len(lignes) - 1) // 2
    else:
        y = H - 40 - 38 * (len(lignes) - 1)
    for l in lignes:
        texte_contour(d, (W / 2, y), l, f, couleur, (0, 0, 0), 7 if VERTICAL else 4)
        y += pas


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


def _choisir_sprite(a, p, ta, hp):
    spr, a._src = _choisir_sprite_cle(a, p, ta, hp)
    return spr


def _nom_cle(cle):
    while isinstance(cle, tuple):
        cle = cle[1] if cle[0] in ('brut',) else cle[-1] if cle[0] == 'pantin' else cle[1]
    return os.path.basename(str(cle))


def _choisir_sprite_cle(a, p, ta, hp):
    if a.tetes and a.gros_plan:
        _k = tete_du_moment(a, ta, p.repliques)
        return a_taille(_k, hp, a.miroir), _nom_cle(_k)
    if a.marche and a.bouge(ta):
        i = int(ta * FPS / PAS / a.marche_pas) % len(a.marche)
        _k = ('brut', a.marche[i]) if a.brut else a.marche[i]
        return a_taille(_k, hp, a.miroir), _nom_cle(_k)
    if a.parle and any(r.qui == a.nom and not r.off and r.debut <= ta < r.fin for r in p.repliques):
        # il parle : on enchaîne ses poses de parole, sans répéter deux fois la même
        n = int(ta / a.tempo_parle)
        rnd = random.Random(sum(map(ord, a.nom)) + n)
        i = (n * 3 + rnd.randrange(len(a.parle))) % len(a.parle)
        if i == (((n - 1) * 3 + random.Random(sum(map(ord, a.nom)) + n - 1).randrange(len(a.parle))) % len(a.parle)):
            i = (i + 1) % len(a.parle)
        _k = ('brut', a.parle[i]) if a.brut else a.parle[i]
        return a_taille(_k, hp, a.miroir), _nom_cle(_k)
    if a.poses:
        ch = a.poses[0][1]
        for (tp, c) in a.poses:
            if ta >= tp:
                ch = c
        _k = ('brut', ch) if a.brut else ch
        return a_taille(_k, hp, a.miroir), _nom_cle(_k)
    if a.kit and a.bras:
        tete = tete_du_moment(a, ta, p.repliques) if a.tetes else None
        ag, ad = a.angles(ta)
        cle = ('articule', a.kit[0], a.kit[1], a.kit[2], float(round(ag / 3) * 3), float(round(ad / 3) * 3), tete)
        _k = cle
        return a_taille(_k, hp, a.miroir), _nom_cle(_k)
    if a.tetes:
        tete = tete_du_moment(a, ta, p.repliques)
        _k = ('pantin', a.image, tete) if tete else a.image
        return a_taille(_k, hp, a.miroir), _nom_cle(_k)
    _k = ('brut', a.image) if a.brut else a.image
    return a_taille(_k, hp, a.miroir), _nom_cle(_k)


def _interp(pts, t):
    if t <= pts[0][0]:
        return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            return v0 + (v1 - v0) * (t - t0) / max(1e-6, t1 - t0)
    return pts[-1][1]


_LISERE = {}
_FLOQUE = {}


def _floque(spr, chemin, src):
    from floquer import floquer, POSES_DE_FACE
    if not src.startswith(POSES_DE_FACE):
        return spr
    cle = (id(spr), chemin)
    deja = _FLOQUE.get(cle)
    if deja is not None and deja[0] is spr:
        return deja[1]
    f = floquer(spr, chemin) or spr
    if len(_FLOQUE) > 300:
        _FLOQUE.clear()
    _FLOQUE[cle] = (spr, f)
    return f


def _liseré(spr, ep, couleur, flou=0):
    """Le liseré d'un sprite (net, ou flou = un halo d'ombre de papier découpé), gardé en mémoire tant que le sprite existe."""
    cle = (id(spr), ep, couleur, flou)
    deja = _LISERE.get(cle)
    if deja is not None and deja[0] is spr:
        return deja[1]
    # le seuil d'abord : les toiles communes des planches gardent un voile presque transparent partout
    gros = spr.getchannel('A').point(lambda v: 255 if v > 100 else 0).filter(ImageFilter.MaxFilter(2 * ep + 1))
    if flou:
        gros = gros.filter(ImageFilter.GaussianBlur(flou)).point(lambda v: int(v * 0.8))
    fond = Image.new('RGBA', spr.size, couleur + (0,)); fond.putalpha(gros)
    fond.alpha_composite(spr)
    if len(_LISERE) > 200:
        _LISERE.clear()
    _LISERE[cle] = (spr, fond)
    return fond


def dessiner_plan(p, t, monde_cache={}, sans=None):
    """Dessine l'image du plan p au temps t. sans=i : sans l'acteur n° i (pour mesurer le contraste)."""
    ta = math.floor(t * FPS / PAS) * PAS / FPS          # temps « sur deux images »
    k = t / max(1e-6, p.duree)
    k_cam = k * k * (3 - 2 * k)                          # caméra adoucie
    zoom = p.zoom[0] + (p.zoom[1] - p.zoom[0]) * k_cam
    procedural = p.fond in ('reve', 'crt', 'bleu')
    # --- fond
    if procedural:
        cadre = {'reve': lambda: fond_reve(t, W, H), 'crt': lambda: fond_crt(t, W, H, p.crt),
                 'bleu': lambda: fond_bleu(t, W, H)}[p.fond]()
        Hd = H; dw = W; off_x = 0; off_y = 0; echelle = 1.0
    else:
        src = decor_source(p.decor, p.etalonner)
        Hd = round(H * zoom); s = Hd / src.height
        dw = round(src.width * s)
        cx = (p.cam[0] + (p.cam[1] - p.cam[0]) * k_cam) * dw
        off_x = int(min(max(0, cx - W / 2), max(0, dw - W)))
        off_y = int(min(max(0, p.cam_y * Hd - H / 2), Hd - H))
        # on ne redimensionne que la partie cadrée : les zooms serrés restent rapides
        cadre = src.resize((W, H), Image.BILINEAR, box=(off_x / s, off_y / s, min(src.width, (off_x + W) / s), min(src.height, (off_y + H) / s)))
        echelle = zoom
    im = cadre.convert('RGB')
    if TRACE is not None:
        TRACE.append(('camera', dw, Hd, off_x, off_y, procedural))
    if p.souvenir:                                      # le passé : le décor vire au sépia, les personnages gardent leur couleur
        im = filtre_souvenir(im, t, sepia=0.55)
    for (p0, p1, n, zone, devant, *g) in p.postits:
        if not devant:
            im = dessiner_postits(im, t, p0, p1, n, zone, *(g or [3]))
    im = im.convert('RGBA')
    # --- acteurs (dans l'ordre : les premiers derrière)
    for i_a, a in enumerate(p.acteurs):
        if not (a.debut <= t < a.fin) or i_a == sans:
            continue
        ax, ay = a.pos(ta)
        hp = a.h * H * (1 if a.gros_plan else echelle) * a.taille(ta)
        if hp < 2:
            continue
        spr = _choisir_sprite(a, p, ta, hp)
        # petits bonds raides quand il se déplace
        bond = 0
        if a.saut and a.bouge(ta):
            bond = abs(math.sin(ta * 2 * math.pi * 2.5)) * a.saut * H
        # tête qui dodeline quand il parle
        if any(r.qui == a.nom and not r.off and r.debut <= ta < r.fin for r in p.repliques):
            bond += 2 * math.sin(ta * 9)
        if a.flocage:
            spr = _floque(spr, a.flocage, getattr(a, '_src', ''))
        if a.contour:
            couleur, ep, *flou = a.contour
            spr = _liseré(spr, int(ep), tuple(couleur), *(flou or [0]))
        rot = a.rot + a.tourne * ta
        if rot:
            spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
        if a.cible and a.ajuster and not procedural:
            # couvrir exactement la cible (une vitre), quelle que soit la forme de l'image
            c0, c1, c2, c3 = a.cible
            rx0, ry0, rx1, ry1 = c0 * dw - off_x, c1 * Hd - off_y, c2 * dw - off_x, c3 * Hd - off_y
            spr = spr.resize((max(1, round(rx1 - rx0)), max(1, round(ry1 - ry0))), Image.BILINEAR)
            px, py = round(rx0), round(ry0)
        elif a.gros_plan:
            px = W / 2 - spr.width / 2
            py = H * ay - spr.height - bond
        elif procedural:
            px = ax * W - spr.width / 2
            py = ay * H - spr.height - bond
        else:
            px = ax * dw - off_x - spr.width / 2
            py = ay * Hd - off_y - spr.height - bond
        if a.ombre and not procedural and not a.gros_plan:
            sh = Image.new('L', im.size, 0)
            ImageDraw.Draw(sh).ellipse([px + spr.width * 0.12, ay * Hd - off_y - spr.height * 0.025,
                                        px + spr.width * 0.88, ay * Hd - off_y + spr.height * 0.012], fill=140)
            im = Image.composite(Image.new('RGBA', im.size, (18, 18, 24, 255)), im, sh.filter(ImageFilter.GaussianBlur(1.5)))
        masque = None
        if a.coupe_x is not None:
            lim = int(a.coupe_x * dw - off_x - px)          # en pixels dans le sprite
            if lim <= 0:
                continue
            if lim < spr.width:
                masque = Image.new('L', spr.size, 255)
                ImageDraw.Draw(masque).rectangle([lim, 0, spr.width, spr.height], fill=0)
        if a.cadre and (len(a.cadre) < 5 or ta < a.cadre[4]):
            x0, y0, x1, y1 = a.cadre[:4]
            if procedural or a.gros_plan:
                rx0, ry0, rx1, ry1 = x0 * W, y0 * H, x1 * W, y1 * H
            else:
                rx0, ry0, rx1, ry1 = x0 * dw - off_x, y0 * Hd - off_y, x1 * dw - off_x, y1 * Hd - off_y
            m = Image.new('L', spr.size, 0)
            ImageDraw.Draw(m).rectangle([rx0 - px, ry0 - py, rx1 - px, ry1 - py], fill=255)
            masque = m if masque is None else Image.fromarray(np.minimum(np.asarray(m), np.asarray(masque)))
        if a.opacite:
            op = max(0.0, min(1.0, _interp(a.opacite, ta)))
            if op <= 0:
                continue
            if op < 1:
                m = Image.new('L', spr.size, int(255 * op))
                masque = m if masque is None else Image.fromarray((np.asarray(masque).astype(np.uint16) * int(255 * op) // 255).astype(np.uint8))
        if masque is not None:
            spr = spr.copy()
            spr.putalpha(Image.fromarray(np.minimum(np.asarray(spr.getchannel('A')), np.asarray(masque))))
        im.alpha_composite(spr, (int(px), int(py)))
        if TRACE is not None:
            TRACE.append(('acteur', i_a, a.nom, int(px), int(py), np.asarray(spr.getchannel('A')), getattr(a, '_src', '')))
    im = im.convert('RGB')
    for (p0, p1, n, zone, devant, *g) in p.postits:
        if devant:
            im = dessiner_postits(im, t, p0, p1, n, zone, *(g or [3]))
    if p.fond == 'reve':
        confettis(im, t); feux(im, t, [(0.25, 0.3, 0.0), (0.75, 0.25, 0.5), (0.5, 0.15, 1.0)])
    if p.souvenir:
        im = filtre_souvenir(im, t, sepia=0.0)          # sur tout : la vignette et le grain, sans éteindre les couleurs
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
    # --- la lumière qui s'éteint, qui revient
    if p.noir and t >= p.noir[0]:
        k_ = min(1.0, (t - p.noir[0]) / max(1e-6, p.noir[1] - p.noir[0]))
        im = Image.blend(im, Image.new('RGB', im.size, (4, 4, 10)), 0.93 * k_)
    if p.lumiere and t < p.lumiere[1]:
        k_ = max(0.0, (t - p.lumiere[0]) / max(1e-6, p.lumiere[1] - p.lumiere[0]))
        im = Image.blend(im, Image.new('RGB', im.size, (4, 4, 10)), 0.93 * (1 - k_))
    # --- le volet bleu des changements de temps
    for (v0, v1, sens) in p.volet:
        if v0 <= t < v1:
            im = dessiner_volet(im, t, v0, v1, sens)
        elif sens == 'couvre' and t >= v1:
            im = fond_bleu(t, W, H)
    if p.carte:
        from carte import dessiner_carte
        im = dessiner_carte(im, t, p.carte)
    if TRACE is not None:
        TRACE.append(('avant-texte', im.copy()))
    # --- l'heure
    for (h0, h1, txt, *xk) in p.horloge:
        if h0 <= t < h1:
            dessiner_horloge(im, txt, t - h0, *xk)
    # --- cartons, bandeaux et sous-titres
    for c in p.cartons:
        d0, d1, txt, sous = c[:4]
        if d0 <= t < d1:
            dessiner_carton(im, txt, sous, (t - d0) / (d1 - d0), *(c[4:6] or [0.70]))
    for c in p.bandeaux:
        d0, d1, txt, sous = c[:4]
        if d0 <= t < d1:
            dessiner_bandeau(im, txt, sous, (t - d0) / (d1 - d0), *(c[4:6] or [0.16]))
    actifs = [r for r in p.repliques if r.sous_titre and r.debut <= t < r.fin_st]
    if actifs:                                     # une seule réplique à la fois : la plus récente
        r = max(actifs, key=lambda r: r.debut)
        dessiner_sous_titre(im, r.affiche, r.qui)
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
    if nom == 'bip':
        # le radio-réveil : quatre bips carrés
        out = np.zeros(int(SR * 1.0))
        for i in range(4):
            nb = int(SR * 0.09); x = np.arange(nb) / SR
            a = int(i * 0.2 * SR)
            out[a:a + nb] += 0.22 * np.sign(np.sin(2 * np.pi * 1760 * x)) * np.minimum(1, x / 0.003)
        return out
    if nom == 'soupir':
        d = 0.9; m = int(SR * d); x = np.arange(m) / SR
        w = np.convolve(rnd.normal(0, 1, m), np.ones(60) / 60, mode='same')
        return 0.5 * w * np.sin(np.pi * x / d) ** 2 * (1 - 0.5 * x / d)
    if nom == 'ding':
        # la petite cloche du clin d'œil (comme une sonnette de boutique)
        out = np.zeros(int(SR * 1.4))
        for f, a0 in [(1318.5, 0.0), (1760.0, 0.12)]:
            x = np.arange(int(SR * 1.2)) / SR; a_ = int(a0 * SR)
            out[a_:a_ + len(x)] += 0.18 * (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 2.76 * f * x)) * np.exp(-x * 3.5)
        return out
    if nom == 'mer':
        # une vague : souffle filtré qui gonfle et retombe
        d = 3.2; m = int(SR * d); x = np.arange(m) / SR
        w = np.convolve(rnd.normal(0, 1, m), np.ones(140) / 140, mode='same')
        return 0.9 * w * np.sin(np.pi * x / d) ** 3
    if nom == 'clavier':
        # une rafale de touches
        out = np.zeros(int(SR * 1.2))
        for i in range(14):
            a = int((i * 0.075 + rnd.uniform(0, 0.03)) * SR); nb = int(SR * 0.025); x = np.arange(nb) / SR
            out[a:a + nb] += 0.25 * rnd.normal(0, 1, nb) * np.exp(-x * 160)
        return out
    if nom == 'crt':
        # l'allumage d'un tube : un claquement, puis le sifflement aigu qui s'éteint
        d = 1.2; m = int(SR * d); x = np.arange(m) / SR
        clac = 0.5 * rnd.normal(0, 1, m) * np.exp(-x * 60)
        sif = 0.05 * np.sin(2 * np.pi * 15600 * x * 0 + 2 * np.pi * 7800 * x) * np.exp(-x * 2.5)
        return clac + sif
    if nom == 'pop':
        x = np.arange(int(SR * 0.12)) / SR
        return 0.4 * np.sin(2 * np.pi * (600 + 2000 * x) * x) * np.exp(-x * 40)
    return np.zeros(10)


def gazouillis(texte):
    """La voix de Tara, l'IA : des gazouillis de vieux modem, une note carrée glissée par syllabe."""
    formes = formes_du_texte(texte)
    d = duree_replique(texte); n = int(SR * d); out = np.zeros(n)
    rnd = np.random.default_rng(len(texte) + 7)
    pas = d / max(1, len(formes))
    for i, f in enumerate(formes):
        if f == 'repos':
            continue
        f0 = 620 * {'A': 1.0, 'O': 0.85, 'OU': 0.75, 'IE': 1.3, 'MBP': 0.7, 'L': 1.1, 'FV': 1.5}[f] * rnd.uniform(0.9, 1.15)
        m = int(SR * min(0.09, pas * 1.2)); x = np.arange(m) / SR
        glis = f0 * (1 + rnd.choice([-0.35, 0.35]) * x / max(x[-1], 1e-6))
        s = np.sign(np.sin(2 * np.pi * np.cumsum(glis) / SR)) * 0.6 + 0.4 * np.sin(2 * np.pi * 2 * np.cumsum(glis) / SR)
        s *= np.minimum(1, x / 0.004) * np.exp(-x * 22)
        a = int(i * pas * SR); b = min(n, a + m)
        out[a:b] += 0.07 * s[: b - a]
    return out


def ecrire_srt(plans, chemin):
    """Les sous-titres de la langue courante, en fichier .srt (pour YouTube)."""
    def tc(t):
        h = int(t // 3600); m = int(t % 3600 // 60); s_ = t % 60
        return f'{h:02d}:{m:02d}:{int(s_):02d},{int(round((s_ - int(s_)) * 1000)):03d}'
    lignes = []; t0 = 0.0; k = 1
    for p in plans:
        rs = [r for r in sorted(p.repliques, key=lambda r: r.debut) if r.sous_titre]
        for j, r in enumerate(rs):
            fin = min(r.fin_st, rs[j + 1].debut) if j + 1 < len(rs) else r.fin_st
            fin = min(fin, int(round(p.duree * FPS)) / FPS)
            lignes.append(f'{k}\n{tc(t0 + r.debut)} --> {tc(t0 + fin)}\n{r.affiche}\n'); k += 1
        t0 += int(round(p.duree * FPS)) / FPS
    open(chemin, 'w', encoding='utf-8').write('\n'.join(lignes))


def babil(texte, voix):
    """Le babillage : une petite note par syllabe, à la hauteur de la voix du personnage."""
    if voix == 'tara':
        return gazouillis(texte)
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
        if os.environ.get('REPRENDRE') and os.path.exists(nom):
            # reprise après une coupure : le plan est déjà rendu (le fichier n'existe qu'une fois fini, voir os.replace)
            fichiers.append(nom)
            for r in p.repliques:
                sons.append((t_total + r.debut, babil(r.texte, r.qui)))
            for (tb, nb) in p.bruits:
                sons.append((t_total + tb, bruit(nb)))
            print(f'plan {i:02d} : déjà rendu', flush=True)
            t_total += nimg / FPS
            continue
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
