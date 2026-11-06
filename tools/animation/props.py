"""Usage : MEDIA_LOCAL=<dossier media-local> python3 props.py

Accessoires dessinés en Python pour les ép. 4 et 5 (aucune génération) : mur de gloire, mur de coupures,
portail et carte au motif carré (pas un vrai QR code), statue, fumée, étoile, sachet, ardoise."""
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
import os
ICI = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ICI, 'assets') + '/'; B = os.path.join(ICI, 'banque') + '/'; O = A        # écrit dans assets/
rnd = random.Random(7)


def tete(chemin, h):
    im = Image.open(chemin).convert('RGBA'); bb = im.getchannel('A').getbbox(); im = im.crop(bb)
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def gris(im):
    a = im.getchannel('A'); g = ImageOps.grayscale(im.convert('RGB')); g = ImageOps.autocontrast(g, 2)
    out = Image.merge('RGBA', (g, g, g, a)); return out


def griffonnage(d, x0, y0, x1, y1, lignes, col=(120, 110, 100), ep=3):
    pas = (y1 - y0) / max(1, lignes)
    for i in range(lignes):
        y = y0 + pas * (i + 0.5); x = x0; pts = []
        fin = x1 - rnd.uniform(0, (x1 - x0) * 0.35)
        while x < fin:
            pts.append((x, y + rnd.uniform(-3, 3))); x += rnd.uniform(6, 12)
        if len(pts) > 1:
            d.line(pts, fill=col, width=ep)


def cadre(contenu, w, h, bord=(92, 64, 40), passe=(236, 228, 210), ep=18):
    c = Image.new('RGBA', (w, h), bord + (255,)); d = ImageDraw.Draw(c)
    d.rectangle([ep // 3, ep // 3, w - ep // 3 - 1, h - ep // 3 - 1], outline=tuple(int(v * 0.7) for v in bord), width=4)
    d.rectangle([ep, ep, w - ep - 1, h - ep - 1], fill=passe + (255,))
    if contenu is not None:
        ct = contenu.copy(); ct.thumbnail((w - 2 * ep - 16, h - 2 * ep - 10))
        c.alpha_composite(ct, ((w - ct.width) // 2, h - ep - ct.height))
    return c


def coller(fond, im, x, y, rot):
    im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    ombre = Image.new('RGBA', im.size, (0, 0, 0, 0)); ombre.putalpha(im.getchannel('A').point(lambda v: v * 0.45))
    ombre = ombre.filter(ImageFilter.GaussianBlur(5))
    fond.alpha_composite(ombre, (int(x + 7), int(y + 9))); fond.alpha_composite(im, (int(x), int(y)))


# ------------------------------------------------ 1. le mur de gloire (ép. 4) : ses photos, toutes signées de sa main
def mur_gloire():
    W, H = 1100, 760; m = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tetes = ['seb-t00-tete-maitre', 'seb-t02-sourire-en-coin', 'seb-t04-beat', 'seb-t01-blase', 'seb-t02-sourire-en-coin',
             'seb-t00-tete-maitre', 'seb-t04-beat']
    places = [(40, 40, 240, 290, -4), (300, 10, 220, 260, 3), (560, 50, 260, 320, -2), (860, 30, 200, 250, 5),
              (60, 380, 200, 240, 6), (320, 330, 240, 300, -5), (850, 330, 210, 260, -3)]
    for (x, y, w, h, r), t in zip(places, tetes):
        ph = gris(tete(A + t + '.png', h - 40)); c = cadre(ph, w, h)
        d = ImageDraw.Draw(c)   # la signature, de sa main, en bas à droite
        sx = w - 90; sy = h - 46
        d.line([(sx, sy), (sx + 14, sy - 12), (sx + 24, sy + 4), (sx + 40, sy - 10), (sx + 52, sy + 2), (sx + 70, sy - 6)], fill=(30, 30, 140), width=4)
        coller(m, c, x, y, r)
    # le diplôme (griffonnages, un sceau rouge)
    dip = Image.new('RGBA', (300, 220), (0, 0, 0, 0)); c = cadre(None, 300, 220, bord=(160, 128, 60), passe=(244, 236, 214), ep=14)
    d = ImageDraw.Draw(c); griffonnage(d, 40, 40, 260, 150, 5); d.ellipse([200, 150, 250, 200], fill=(170, 40, 40))
    coller(m, c, 580, 400, 2)
    # la médaille
    med = Image.new('RGBA', (90, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(med)
    d.polygon([(25, 0), (65, 0), (55, 110), (35, 110)], fill=(200, 40, 70)); d.ellipse([10, 100, 80, 170], fill=(214, 172, 60), outline=(150, 112, 30), width=5)
    coller(m, med, 470, 610 - 190 + 40, -8)
    return m


# ------------------------------------------------ 2. le mur du boulanger (ép. 4) : ce que LES AUTRES disent de lui
def mur_coupures():
    W, H = 1100, 700; m = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
    liege = Image.new('RGBA', (W, H), (176, 132, 84, 255)); a = np.asarray(liege).copy()
    bruit = np.random.default_rng(3).integers(-22, 22, a.shape[:2])
    for k in range(3):
        a[..., k] = np.clip(a[..., k].astype(int) + bruit, 0, 255)
    liege = Image.fromarray(a.astype(np.uint8)); dl = ImageDraw.Draw(liege)
    dl.rectangle([0, 0, W - 1, H - 1], outline=(110, 76, 44), width=22)
    m.alpha_composite(liege)
    tb = gris(tete(B + 'boulanger-3.png', 400).crop((0, 0, 400 * 420 // 774 + 120, 210)))  # la tête et le haut du boulanger
    tb_full = gris(Image.open(B + 'boulanger-2.png').convert('RGBA'))
    for i, (x, y, w, h, r) in enumerate([(60, 60, 260, 300, -3), (360, 40, 240, 280, 4), (640, 70, 300, 250, -2),
                                         (90, 390, 230, 250, 5), (380, 360, 280, 290, -4)]):
        p = Image.new('RGBA', (w, h), (232, 220, 182, 255)); dp = ImageDraw.Draw(p)
        dp.rectangle([14, 14, w - 14, 46], fill=(60, 56, 50))            # le titre du journal, illisible : un bandeau
        ph = tb_full.copy(); ph.thumbnail((w * 0.55, h * 0.55)); p.alpha_composite(ph, (16, 60))
        griffonnage(dp, 16 + ph.width + 10, 62, w - 16, 60 + ph.height, 5, ep=3)
        griffonnage(dp, 16, 70 + ph.height, w - 16, h - 16, 3, ep=3)
        coller(m, p, x, y, r)
        d2 = ImageDraw.Draw(m); d2.ellipse([x + w // 2 - 9, y + 2, x + w // 2 + 9, y + 20], fill=(200, 40, 40))   # la punaise
    # la plaque de la mairie
    pl = Image.new('RGBA', (220, 120), (184, 150, 70, 255)); dp = ImageDraw.Draw(pl)
    dp.rectangle([6, 6, 213, 113], outline=(120, 92, 30), width=5); griffonnage(dp, 30, 30, 190, 95, 3, col=(90, 64, 20), ep=4)
    coller(m, pl, 720, 380, 0)
    # le guide ouvert et la carte postale du château
    ch = Image.open(os.path.join(os.environ.get('MEDIA_LOCAL', os.path.join(ICI, '..')), 'decors', 'aa-decor-07-tarascon-chateau-panorama.png')).convert('RGBA')
    cp = ch.crop((int(ch.width * 0.25), int(ch.height * 0.25), int(ch.width * 0.55), int(ch.height * 0.65)))
    cp = ImageEnhance.Color(cp).enhance(0.7); cp.thumbnail((240, 160)); cart = cadre(cp, cp.width + 24, cp.height + 24, bord=(245, 240, 230), passe=(245, 240, 230), ep=12)
    coller(m, cart, 720, 530, -5)
    return m


# ------------------------------------------------ 3. le motif carré (pas un vrai QR code, non scannable) et l'étoile
def motif(n=11, cell=22):
    g = np.random.default_rng(11).random((n, n)) > 0.5
    for (cx, cy) in [(0, 0), (n - 3, 0), (0, n - 3)]:   # trois « yeux » d'angle, pour qu'on comprenne ce que c'est
        g[cy:cy + 3, cx:cx + 3] = True; g[cy + 1, cx + 1] = False
    im = Image.new('RGBA', (n * cell + 2 * cell, n * cell + 2 * cell), (250, 250, 246, 255)); d = ImageDraw.Draw(im)
    for y in range(n):
        for x in range(n):
            if g[y, x]:
                d.rectangle([cell + x * cell, cell + y * cell, cell + (x + 1) * cell - 1, cell + (y + 1) * cell - 1], fill=(20, 20, 20))
    return im


def etoile(r=60, col=(255, 206, 40)):
    im = Image.new('RGBA', (2 * r + 12, 2 * r + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(r + 6 + (r if i % 2 == 0 else r * 0.45) * math.sin(i * math.pi / 5), r + 6 - (r if i % 2 == 0 else r * 0.45) * math.cos(i * math.pi / 5)) for i in range(10)]
    d.polygon(pts, fill=col, outline=(150, 100, 10)); d.line(pts + [pts[0]], fill=(150, 100, 10), width=5)
    return im


def portail():
    W, H = 420, 900; m = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
    d.rectangle([W // 2 - 18, 380, W // 2 + 18, H], fill=(110, 80, 52), outline=(70, 50, 30), width=4)   # le poteau
    pl = Image.new('RGBA', (380, 470), (158, 118, 78, 255)); dp = ImageDraw.Draw(pl)
    for y in range(0, 470, 52):
        dp.line([(0, y), (380, y)], fill=(120, 86, 54), width=4)
    dp.rectangle([0, 0, 379, 469], outline=(96, 68, 40), width=8)
    mo = motif(); mo.thumbnail((250, 250)); pl.alpha_composite(mo, ((380 - mo.width) // 2, 170))
    et = etoile(62); pl.alpha_composite(et, ((380 - et.width) // 2, 22))
    pl = pl.rotate(-3, expand=True, resample=Image.BICUBIC); m.alpha_composite(pl, ((W - pl.width) // 2, 10))
    return m


def carte_qr():
    c = Image.new('RGBA', (300, 190), (250, 250, 246, 255)); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, 299, 189], outline=(170, 170, 160), width=4)
    mo = motif(); mo.thumbnail((150, 150)); c.alpha_composite(mo, (20, 20))
    et = etoile(26); c.alpha_composite(et, (200, 30)); c.alpha_composite(etoile(20), (232, 100)); c.alpha_composite(etoile(20), (186, 104))
    return c


# ------------------------------------------------ 4. la statue (le rêve, ép. 4) : la pierre grise, sauf le t-shirt rose
def statue():
    s = Image.open(A + 'seb-discours-3.png').convert('RGBA'); s = s.crop(s.getchannel('A').getbbox())
    a = np.asarray(s).astype(np.float32); r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    rose = (r > 150) & (b > 90) & (g < 120) & (r - g > 80)
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    pierre = 70 + lum * 0.62 + np.random.default_rng(2).normal(0, 9, lum.shape)
    out = a.copy()
    for k, t in enumerate((1.0, 0.98, 0.93)):
        out[..., k] = np.where(rose, a[..., k], np.clip(pierre * t, 0, 255))
    st = Image.fromarray(out.astype(np.uint8), 'RGBA')
    W = int(st.width * 1.5); ped_h = int(st.height * 0.32)
    m = Image.new('RGBA', (W, st.height + ped_h), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
    x0 = (W - int(st.width * 1.2)) // 2
    d.rectangle([x0, st.height, x0 + int(st.width * 1.2), st.height + ped_h], fill=(150, 146, 136), outline=(96, 92, 86), width=8)
    d.rectangle([x0 - 20, st.height + ped_h - 40, x0 + int(st.width * 1.2) + 20, st.height + ped_h], fill=(128, 124, 116))
    d.rectangle([x0 - 10, st.height - 10, x0 + int(st.width * 1.2) + 10, st.height + 26], fill=(168, 164, 154))
    # la couronne de laurier
    cx = (W) // 2; m.alpha_composite(st, ((W - st.width) // 2, 0))
    return m


# ------------------------------------------------ 5. la fumée du faux avis (ép. 5) : trois images, de plus en plus dissipées
def fumee(k):
    W = 360; m = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(m); rr = random.Random(5)
    for i in range(14):
        a = rr.uniform(0, 2 * math.pi); dist = rr.uniform(0, 90) * (0.6 + 0.6 * k); rad = rr.uniform(40, 80) * (1.1 - 0.25 * k)
        x = W / 2 + math.cos(a) * dist; y = W / 2 + math.sin(a) * dist
        g = int(232 - 30 * rr.random())
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(g, g, g, int(255 * (1 - 0.35 * k))), outline=(150, 150, 150, int(255 * (1 - 0.35 * k))), width=5)
    return m


def sachet():
    m = Image.new('RGBA', (200, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
    d.polygon([(20, 30), (180, 30), (190, 255), (10, 255)], fill=(196, 160, 112), outline=(140, 108, 70))
    for x in range(30, 180, 16):
        d.line([(x, 30), (x - 4, 18)], fill=(170, 136, 92), width=3)
    d.rectangle([20, 22, 180, 34], fill=(176, 142, 96))
    return m


def ardoise(textes):
    """L'ardoise de la boulangerie : « 1 avis = 1 croissant », une par langue."""
    from PIL import ImageFont
    out = {}
    for lg, t in textes.items():
        m = Image.new('RGBA', (520, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
        d.rectangle([0, 0, 519, 299], fill=(130, 92, 58)); d.rectangle([18, 18, 501, 281], fill=(44, 50, 46))
        f = ImageFont.truetype(os.path.join(ICI, 'polices', 'Fredoka.ttf'), 64)
        for i, ligne in enumerate(t):
            d.text((260, 105 + i * 92), ligne, font=f, fill=(240, 240, 232), anchor='mm')
        out[lg] = m
    return out


if __name__ == '__main__':
    mur_gloire().save(O + 'mur-gloire.png'); mur_coupures().save(O + 'mur-coupures.png')
    portail().save(O + 'portail-qr.png'); carte_qr().save(O + 'carte-qr.png'); statue().save(O + 'statue.png')
    etoile(70).save(O + 'etoile.png'); sachet().save(O + 'sachet.png')
    for k in range(3):
        fumee(k).save(O + f'fumee-{k + 1}.png')
    for lg, im in ardoise({'fr': ['1 avis', '= 1 croissant'], 'en': ['1 review', '= 1 croissant'], 'es': ['1 reseña', '= 1 cruasán']}).items():
        im.save(O + f'ardoise-{lg}.png')
    print(sorted(os.listdir(O)))
