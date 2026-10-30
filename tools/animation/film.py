"""« Bienvenue chez Sébastien Anaconda » : la séquence d'accueil du site, 1 min 30, 16:9.

Le décalage : Sébastien veut faire une présentation solennelle et sérieuse de
l'encyclopédie. Tout le monde lui coupe la parole (Diana, Kristina, les animaux),
il part dans un rêve de grandeur complètement absurde, et à la fin c'est Olympe,
la râleuse, qui conclut l'invitation à sa place.
"""
import sys
from moteur import *

A = 'assets/'
SEB_T = {'repos': A + 'seb-t01-blase.png', 'A': A + 'seb-b01-A.png', 'O': A + 'seb-b02-O.png', 'OU': A + 'seb-b03-OU.png',
         'IE': A + 'seb-b04-I-E.png', 'MBP': A + 'seb-b05-MBP.png', 'FV': A + 'seb-b06-FV.png', 'L': A + 'seb-b07-L.png'}
SEB_GRAND = A + 'seb-t00-tete-maitre.png'; SEB_COIN = A + 'seb-t02-sourire-en-coin.png'
SEB_DEPIT = A + 'seb-t03-depit.png'; SEB_BEAT = A + 'seb-t04-beat.png'; SEB_CRI = A + 'seb-t05-cri.png'
DIA_T = {'repos': A + 'diana-t00.png', 'A': A + 'diana-t01-A.png', 'O': A + 'diana-t01-A.png', 'OU': A + 'diana-t00.png',
         'IE': A + 'diana-t00.png', 'MBP': A + 'diana-t00.png', 'FV': A + 'diana-t00.png', 'L': A + 'diana-t01-A.png'}
KRI_T = {'repos': A + 'kristina-t00.png', 'A': A + 'kristina-t01-A.png', 'O': A + 'kristina-t01-A.png', 'OU': A + 'kristina-t00.png',
         'IE': A + 'kristina-t00.png', 'MBP': A + 'kristina-t00.png', 'FV': A + 'kristina-t00.png', 'L': A + 'kristina-t01-A.png'}

D = os.path.join(MEDIA_LOCAL, 'decors') + '/'
RUE = D + 'aa-decor-10-rue-panorama.png'; SALON = D + 'aa-decor-09-salon.png'
PLAGE = D + 'aa-decor-06-plage-panorama.png'; CHATEAU = D + 'aa-decor-07-tarascon-chateau-panorama.png'
AGI = D + 'aa-decor-05-agility-terne.png'; ARENES = D + 'aa-decor-08-arles-arenes-panorama.png'

def seb(corps, **kw):
    return Acteur('seb', A + corps, tetes=SEB_T, **kw)

KIT = (A + 'seb-k00-corps.png', A + 'seb-bras-g.png', A + 'seb-bras-d.png')
SEB_MARCHE = [A + f'seb-marche-{i}.png' for i in range(1, 5)]
DIA_MARCHE = [A + f'diana-marche-{i}.png' for i in range(1, 5)]
KRI_MARCHE = [A + f'kristina-marche-{i}.png' for i in range(1, 5)]
DJ_TROT = [A + f'django-trot-{i}.png' for i in range(1, 5)]

def sebart(bras, **kw):
    """Sébastien en pantin articulé : bras = [(t, angle_gauche, angle_droit), ...]."""
    return Acteur('seb', KIT[0], tetes=SEB_T, kit=KIT, bras=bras, **kw)

def existe(liste):
    import os
    return liste if all(os.path.exists(f) for f in liste) else None

def dia(**kw):
    return Acteur('diana', A + 'diana-m00.png', **kw)

def kri(**kw):
    return Acteur('kristina', A + 'kristina-m00.png', **kw)

def gros_plan(nom, tetes, decor, cam, duree, texte, bruits=(), expression=None, repliques=None, h=1.02, y=1.10):
    reps = repliques or [R(nom, 0.4, texte)]
    return Plan(duree, decor, cam=(cam, cam), zoom=(2.4, 2.5), cam_y=0.45,
                acteurs=[Acteur(nom, None, x=cam, y=y, h=h, tetes=tetes, gros_plan=True, ombre=False, expression=expression)],
                repliques=reps, bruits=list(bruits))

def planche(nom, n=4):
    """Les poses d'une planche, sur leur toile commune (pas de recadrage pose par pose)."""
    return [('brut', A + f'{nom}-{i}.png') for i in range(1, n + 1)]

def geste(t0, t1, images, tempo=0.42, ordre=None):
    """Une suite de poses de remplacement de t0 à t1 : [(t, image), ...]."""
    ordre = ordre or list(range(len(images)))
    out = []; t = t0; k = 0
    while t < t1 - 1e-6:
        out.append((t, images[ordre[k % len(ordre)]])); t += tempo; k += 1
    return out

SEB_DISC = planche('seb-discours')      # 1 bras grands ouverts, 2 index levé, 3 main sur le cœur, 4 paumes en avant
SEB_CLE = planche('seb-cles')           # 1 doigt pointé vers nous, 2 affalé boudeur, 3 saut bras levés, 4 « c'est par là »
DIA_P = planche('diana-parle')          # 1 poings sur les hanches, 2 main qui explique, 3 bras croisés, 4 fou rire
KRI_P = existe([A + f'kristina-parle-{i}.png' for i in range(1, 5)]) and planche('kristina-parle')
SEB_RUN = existe([A + f'seb-course-{i}.png' for i in range(1, 5)]) and planche('seb-course')
DJ_ASSIS = existe([A + f'django-assis-{i}.png' for i in range(1, 5)]) and planche('django-assis')
DJ_SAUT = planche('django-saut')        # 1 appel, 2 envol, 3 en l'air, 4 réception
OLY = planche('olympe-aboie')
OLY_B = existe([A + f'olympe-bonjour-{i}.png' for i in range(1, 5)]) and planche('olympe-bonjour')   # 1 debout, 2 descend, 3 étirée, 4 se relève           # 1 menton sur les pattes, 2 tête levée, 3 aboie, 4 contente d'elle
PAT = planche('patchy-galop')
M = lambda nom: A + nom + '.png'

def seb(poses=None, parle=None, **kw):
    kw.setdefault('h', 0.62)
    return Acteur('seb', M('seb-m04-bras-le-long'), poses=poses, parle=parle, **kw)

def dia(poses=None, parle=DIA_P, **kw):
    kw.setdefault('h', 0.60)
    return Acteur('diana', M('diana-m00'), poses=poses, parle=parle, **kw)

def kri(poses=None, parle=None, **kw):
    kw.setdefault('h', 0.58)
    return Acteur('kristina', M('kristina-m00'), poses=poses, parle=parle if parle is not None else KRI_P, **kw)

R = Replique
plans = [
    # 1. travelling sur la rue, Sébastien arrive en marchant et s'arrête de dos
    Plan(7.0, RUE, cam=(0.18, 0.62), zoom=(1.0, 1.0), cam_y=0.5,
         acteurs=[Acteur('seb', A + 'seb-s1-de-dos-v2.png', x=0.62, y=0.93, h=0.62, marche=SEB_MARCHE,
                         trajet=[(0, 0.20, 0.93), (5.2, 0.62, 0.93)], saut=0.004)],
         cartons=[(0.6, 3.4, 'Sébastien Anaconda', 'dans : « Bienvenue, ou presque »')],
         bruits=[(0.2, 'tada')]),
    # 2. il se retourne d'un coup et nous pointe du doigt, puis part dans son discours
    Plan(5.0, RUE, cam=(0.62, 0.62), zoom=(1.5, 1.6), cam_y=0.62,
         acteurs=[seb(poses=[(0, M('seb-m04-bras-le-long')), (0.25, SEB_CLE[0])]
                      + geste(2.3, 5.0, SEB_DISC, 0.5, [1, 0, 3, 2, 0]), x=0.62, y=0.93)],
         repliques=[R('seb', 0.5, "Ah ! Te voilà enfin !"), R('seb', 2.4, "J'ai préparé un discours.")],
         bruits=[(0.0, 'whoosh'), (0.25, 'pop')]),
    # 3. gros plan face caméra, solennel : têtes entières qui parlent, comme Diana
    gros_plan('seb', SEB_T, RUE, 0.62, 7.0, None, h=1.04, y=1.12,
              expression=[(0, SEB_T['repos']), (3.2, SEB_GRAND), (3.5, SEB_T['repos']), (6.4, SEB_COIN)],
              repliques=[R('seb', 0.3, "Mesdames, messieurs. Bienvenue dans l'encyclopédie."),
                         R('seb', 3.6, "Ici, chaque épisode est découpé scène par scène.")]),
    # 4. Diana entre, il continue en grands gestes
    Plan(4.0, RUE, cam=(0.55, 0.57), zoom=(1.35, 1.35), cam_y=0.6,
         acteurs=[seb(poses=geste(0, 4.0, SEB_DISC, 0.45, [0, 2, 1, 3]), x=0.64, y=0.93),
                  dia(poses=[(0, DIA_P[0])], x=0.30, y=0.93, trajet=[(0, 0.22, 0.93), (1.8, 0.48, 0.93)], saut=0.006,
                      marche=existe(DIA_MARCHE), parle=None)],
         repliques=[R('seb', 0.2, "… scène par scène, et sans…")], bruits=[(1.4, 'pop')]),
    # 4b. gros plan Diana, face caméra
    gros_plan('diana', DIA_T, RUE, 0.48, 3.6, "Chéri, tu parles tout seul dans la rue."),
    # 4c. il se vexe, s'affale ; elle croise les bras
    Plan(3.4, RUE, cam=(0.57, 0.57), zoom=(1.35, 1.35), cam_y=0.6,
         acteurs=[seb(poses=[(0, SEB_DISC[0]), (0.4, SEB_CLE[1])], x=0.64, y=0.93),
                  dia(poses=[(0, DIA_P[0]), (1.4, DIA_P[2])], x=0.48, y=0.93)],
         repliques=[R('seb', 0.5, "Je présente le site, Doudou.")]),
    # 5. Kristina débarque
    Plan(2.6, RUE, cam=(0.60, 0.62), zoom=(1.35, 1.35), cam_y=0.6,
         acteurs=[seb(poses=[(0, SEB_CLE[1])], x=0.64, y=0.93), dia(poses=[(0, DIA_P[2])], x=0.48, y=0.93),
                  kri(x=0.80, y=0.93, trajet=[(0, 1.02, 0.93), (1.8, 0.80, 0.93)], saut=0.006, marche=existe(KRI_MARCHE),
                      poses=[(0, KRI_P[0])] if KRI_P else None)],
         bruits=[(1.2, 'pop')]),
    # 5b. gros plan Kristina
    gros_plan('kristina', KRI_T, RUE, 0.80, 3.4, "Papa, personne ne lit les discours !"),
    # 5c. Diana enchaîne, Kristina rit, lui se reprend
    Plan(3.6, RUE, cam=(0.60, 0.60), zoom=(1.35, 1.35), cam_y=0.6,
         acteurs=[seb(poses=[(0, SEB_CLE[1]), (2.0, SEB_DISC[3])], x=0.64, y=0.93),
                  dia(poses=[(0, DIA_P[2])], x=0.48, y=0.93),
                  kri(poses=([(0, KRI_P[1]), (1.6, KRI_P[0])] if KRI_P else None), x=0.80, y=0.93)],
         repliques=[R('diana', 0.3, "Montre-leur plutôt les chiens.")]),
    # 6. Django arrive au trot et se colle au talon
    Plan(7.0, RUE, cam=(0.40, 0.62), zoom=(1.3, 1.3), cam_y=0.62,
         acteurs=[seb(poses=[(0, SEB_DISC[3]), (2.5, M('seb-s2-main-ouverte')), (5.0, M('seb-m02-blase'))], x=0.62, y=0.93),
                  Acteur('django', A + 'django-d1-trot.png', x=0.2, y=0.94, h=0.26, marche=existe(DJ_TROT),
                         trajet=[(0, 0.10, 0.94), (2.0, 0.48, 0.94)], saut=0.006, fin=2.0),
                  Acteur('django', A + 'django-d2-assis-talon.png', x=0.50, y=0.94, h=0.33, debut=2.0, miroir=True,
                         poses=(geste(2.0, 7.0, DJ_ASSIS, 0.6, [0, 1, 0, 2, 3, 0, 1, 3]) if DJ_ASSIS else None))],
         repliques=[R('seb', 2.6, "Voici Django. Il me suit partout."), R('seb', 5.0, "Vraiment partout.")],
         bruits=[(1.9, 'ouaf'), (5.9, 'ouaf')]),
    # 7. agility : on file, travelling
    Plan(5.0, AGI, cam=(0.2, 0.75), zoom=(1.2, 1.2), cam_y=0.62,
         acteurs=[Acteur('seb', A + 'seb-s3-agility-course.png', h=0.55, trajet=[(0, -0.1, 0.95), (5, 1.05, 0.95)], saut=0.015,
                         marche=SEB_RUN or None, marche_pas=1),
                  Acteur('django', A + 'django-d1-trot.png', h=0.25, trajet=[(0, 0.05, 0.96), (5, 1.20, 0.96)], saut=0.02,
                         marche=existe(DJ_TROT), marche_pas=1)],
         repliques=[R('seb', 1.0, "Et le dimanche, on fait de l'agility.", sous_titre=True, off=True)],
         bruits=[(0.5, 'whoosh'), (2.5, 'ouaf')]),
    # 7b. plan fixe : Django saute la haie, puis file dans le tunnel… et disparaît
    Plan(7.0, AGI, cam=(0.5, 0.5), zoom=(1.0, 1.0), cam_y=0.5,
         acteurs=[seb(poses=[(0, SEB_DISC[0]), (0.9, SEB_CLE[2]), (2.0, SEB_DISC[0]), (2.6, SEB_CLE[3]), (5.4, SEB_CLE[1])],
                      x=0.58, y=0.74, h=0.40),
                  Acteur('django', A + 'django-d1-trot.png', h=0.25, marche=existe(DJ_TROT), marche_pas=1, fin=1.0,
                         trajet=[(0, -0.08, 0.88), (1.0, 0.02, 0.88)]),
                  Acteur('django', DJ_SAUT[0], h=0.34, debut=1.0, fin=2.1, ombre=False,
                         poses=[(1.0, DJ_SAUT[0]), (1.25, DJ_SAUT[1]), (1.55, DJ_SAUT[2]), (1.85, DJ_SAUT[3])],
                         trajet=[(1.0, 0.05, 0.93), (1.25, 0.10, 0.88), (1.55, 0.19, 0.84), (1.85, 0.30, 0.88), (2.1, 0.34, 0.89)]),
                  Acteur('django', A + 'django-d1-trot.png', h=0.25, marche=existe(DJ_TROT), marche_pas=1, debut=2.1, ombre=False,
                         coupe_x=0.835, trajet=[(2.1, 0.36, 0.89, 1.0), (4.6, 0.86, 0.715, 0.55), (5.0, 0.95, 0.715, 0.55)])],
         repliques=[R('seb', 0.9, "Hop !"), R('seb', 2.6, "Le tunnel ! Le tunnel !"),
                    R('seb', 5.6, "… Django ?")],
         bruits=[(1.05, 'boing'), (1.9, 'pop'), (4.6, 'whoosh')]),
    # 8. salon : Olympe ne se lève pas, elle lève juste la tête pour engueuler ; Patchy traverse en taureau
    Plan(9.0, SALON, cam=(0.5, 0.5), zoom=(1.15, 1.15), cam_y=0.6,
         acteurs=[dia(poses=[(0, DIA_P[0]), (4.2, DIA_P[3]), (6.8, DIA_P[2])], x=0.16, y=0.83, h=0.60),
                  kri(poses=([(0, KRI_P[3]), (4.2, KRI_P[1]), (6.8, KRI_P[0])] if KRI_P else None), x=0.28, y=0.85, h=0.57),
                  seb(poses=[(0, SEB_DISC[3]), (2.4, SEB_DISC[1]), (4.0, SEB_CLE[1]), (7.0, M('seb-m02-blase'))], x=0.80, y=0.87, h=0.62),
                  Acteur('olympe', OLY[0], x=0.48, y=0.93, h=0.36,
                         poses=[(0, OLY[0]), (3.0, OLY[1]), (4.0, OLY[2]), (4.3, OLY[1]), (4.5, OLY[2]), (4.8, OLY[1]),
                                (5.6, OLY[2]), (5.9, OLY[1]), (6.6, OLY[3]), (8.2, OLY[0])]),
                  Acteur('patchy', PAT[0], h=0.24, marche=PAT, marche_pas=1, trajet=[(5.0, -0.15, 0.98), (6.4, 1.15, 0.98)], debut=5.0, fin=6.4)],
         repliques=[R('seb', 0.6, "Olympe, viens dire bonjour."),
                    R('seb', 2.6, "Olympe ?"),
                    R('olympe', 4.1, "OUAF !"),
                    R('seb', 7.0, "… Et ça, c'était Patchy.")],
         bruits=[(4.0, 'ouaf'), (4.5, 'ouaf'), (5.0, 'whoosh'), (5.6, 'ouaf')]),
    # 9. retour : gros plan dépit, têtes entières
    gros_plan('seb', SEB_T, RUE, 0.62, 5.0, None, h=1.04, y=1.12,
              expression=[(0, SEB_DEPIT), (2.9, SEB_BEAT), (3.4, SEB_GRAND)],
              repliques=[R('seb', 0.4, "Personne ne m'écoute jamais."), R('seb', 3.4, "Sauf… dans mes rêves.")]),
    # 10. le rêve : apesanteur, sauts, absurde
    Plan(10.0, fond='reve', vague=(0, 1.0),
         acteurs=[Acteur('seb', SEB_CLE[2], x=0.5, y=0.88, h=0.72, rot=-8, tourne=2.0, ombre=False,
                         poses=geste(0, 6.0, [SEB_CLE[2], SEB_DISC[0], SEB_CLE[0], SEB_DISC[1]], 0.33)
                               + geste(6.0, 10.0, [SEB_CLE[2], SEB_DISC[0]], 0.17)),
                  Acteur('django', DJ_SAUT[2], h=0.36, trajet=[(0, 0.15, 0.60), (10, 0.30, 0.40)], tourne=35, ombre=False,
                         poses=geste(0, 10, [DJ_SAUT[1], DJ_SAUT[2]], 0.5)),
                  Acteur('patchy', PAT[2], h=0.20, trajet=[(0, 0.95, 0.35), (10, 0.72, 0.55)], tourne=-50, ombre=False,
                         marche=PAT, marche_pas=2)],
         repliques=[R('seb', 1.2, "Je suis le roi de l'encyclopédie !"),
                    R('seb', 3.8, "Cent trente segments ! Zéro dialogue recopié !"),
                    R('seb', 6.2, "AAAAAH !")],
         bruits=[(0.0, 'scratch'), (6.0, 'boing'), (8.5, 'pouet')], flash=[(9.6, 0.4)]),
    # 11. réveil sur la plage, tout le monde le regarde
    Plan(8.0, PLAGE, cam=(0.35, 0.55), zoom=(1.25, 1.25), cam_y=0.6,
         acteurs=[seb(poses=[(0, M('seb-m02-blase')), (5.8, SEB_CLE[3])], x=0.46, y=0.92, h=0.58),
                  dia(poses=[(0, DIA_P[0]), (3.0, DIA_P[1]), (5.5, DIA_P[3])], x=0.30, y=0.92, h=0.56),
                  kri(poses=([(0, KRI_P[3]), (2.6, KRI_P[0])] if KRI_P else None), x=0.62, y=0.92, h=0.54)],
         repliques=[R('kristina', 0.6, "Il a encore rêvé qu'il était roi."),
                    R('diana', 3.2, "Bon. On les invite, ou pas ?"),
                    R('seb', 5.8, "Oui. C'est par là…")]),
    # 12. toute la famille dans le salon ; Olympe dit enfin bonjour, au visiteur, à sa façon : raide
    Plan(7.5, SALON, cam=(0.48, 0.50), zoom=(1.12, 1.18), cam_y=0.62,
         acteurs=[dia(poses=[(0, DIA_P[0]), (3.0, DIA_P[3])], x=0.22, y=0.82, h=0.50),
                  seb(poses=[(0, SEB_DISC[2]), (3.0, SEB_DISC[0])], x=0.50, y=0.81, h=0.51),
                  kri(poses=([(0, KRI_P[0]), (3.0, KRI_P[1])] if KRI_P else None), x=0.77, y=0.83, h=0.48),
                  Acteur('django', A + 'django-d2-assis-talon.png', x=0.63, y=0.85, h=0.27,
                         poses=(geste(0, 7.5, DJ_ASSIS, 0.6, [0, 1, 3, 0, 2]) if DJ_ASSIS else None)),
                  Acteur('olympe', OLY_B[0] if OLY_B else OLY[1], x=0.40, y=0.91, h=0.31 if OLY_B else 0.36,
                         poses=([(0, OLY_B[0]), (1.4, OLY_B[1]), (1.7, OLY_B[2]), (5.6, OLY_B[3]), (6.4, OLY_B[0])] if OLY_B else
                                [(0, OLY[1]), (0.4, OLY[2]), (0.7, OLY[1]), (0.9, OLY[2]), (1.3, OLY[3])])),
                  Acteur('patchy', PAT[0], h=0.22, marche=PAT, marche_pas=1, trajet=[(6.3, -0.15, 0.99), (7.5, 1.15, 0.99)], debut=6.3)],
         repliques=[R('seb', 0.3, "Olympe… dis bonjour."), R('kristina', 2.6, "Ooooh !")],
         cartons=[(2.6, 7.5, 'Entrez donc.', '(Olympe a dit bonjour.)', 0.10)],
         bruits=[(1.7, 'pop'), (2.6, 'tada'), (6.3, 'whoosh')]),
]

caler(plans)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'images':
        # images-clés pour vérifier avant le rendu complet
        import os
        os.makedirs('cles', exist_ok=True)
        for i, p in enumerate(plans):
            for k in (0.3, 0.7):
                dessiner_plan(p, p.duree * k).save(f'cles/p{i:02d}-{int(k*100)}.jpg', quality=88)
        print('ok')
    else:
        video, t_total, sons = rendre(plans, 'film.mp4')
        i_reve = next(i for i, p in enumerate(plans) if p.fond == 'reve'); t_reve = sum(p.duree for p in plans[:i_reve])
        mixer(t_total, sons, (t_reve, t_reve + plans[i_reve].duree), 'rendu/son.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', 'rendu/son.wav', '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', 'film.mp4'], check=True)
        print('film.mp4', round(t_total, 1), 's')
