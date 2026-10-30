"""PREMIER JET REFUSÉ (53 s, écran turquoise) de « Personne ne me cite », gardé pour mémoire : NE PAS EN PARTIR.
L'épisode 2 se fait à partir de short_ep01.py et de la fiche shorts/episodes/EP02-personne-ne-me-cite.md.

Les Tarasconnades · « Personne ne me cite » — un short vertical (9:16), en trois langues.

Usage : LANGUE=fr python3 short01.py            -> shorts/S1E01-fr.mp4 et .srt
        LANGUE=en python3 short01.py images     -> images-clés seulement

La question, posée à la première seconde : pourquoi l'IA ne connaît pas papa ?
Le test des trois phrases :
1. Kristina découvre que l'IA de la maison ne sait pas qui est son père.
2. Sébastien interroge Tara : elle cite un boulanger, puis la chienne, et lui explique
   qu'il faut que d'autres sites parlent de lui (le GEO).
3. Personne dans la famille ne veut parler de lui, et pour l'IA il reste « le monsieur du chien ».
La fin reprend la première réplique : la vidéo boucle.
"""
import os
import subprocess
import sys

os.environ['FORMAT'] = 'vertical'
from moteur import *          # noqa: E402

A = 'assets/'
M = lambda n: A + n + '.png'
D = os.path.join(MEDIA_LOCAL, 'decors') + '/'
BUREAU = D + 'aa-decor-11-bureau-vertical.png'
REVE = None


def planche(nom, n=4):
    return [('brut', A + f'{nom}-{i}.png') for i in range(1, n + 1)]


SEB_T = {'repos': M('seb-t01-blase'), 'A': M('seb-b01-A'), 'O': M('seb-b02-O'), 'OU': M('seb-b03-OU'),
         'IE': M('seb-b04-I-E'), 'MBP': M('seb-b05-MBP'), 'FV': M('seb-b06-FV'), 'L': M('seb-b07-L')}
SEB_CRI, SEB_DEPIT, SEB_BEAT, SEB_GRAND = M('seb-t05-cri'), M('seb-t03-depit'), M('seb-t04-beat'), M('seb-t00-tete-maitre')
KT = [M(f'kristina-tete-{i}') for i in range(1, 5)]        # 1 pince-sans-rire, 2 idem qui parle, 3 fou rire, 4 yeux au ciel
KRI_T = {'repos': KT[0], 'A': KT[1], 'O': KT[1], 'OU': KT[1], 'IE': KT[1], 'L': KT[1], 'MBP': KT[0], 'FV': KT[0]}
DIA_T = {'repos': M('diana-t00'), 'A': M('diana-t01-A'), 'O': M('diana-t01-A'), 'OU': M('diana-t00'),
         'IE': M('diana-t00'), 'MBP': M('diana-t00'), 'FV': M('diana-t00'), 'L': M('diana-t01-A')}
SEB_DISC, SEB_CLE = planche('seb-discours'), planche('seb-cles')
DIA_P, KRI_P = planche('diana-parle'), planche('kristina-parle')
OLY_B, OLY = planche('olympe-bonjour'), planche('olympe-aboie')
TARA = planche('tara')                                         # 1 sourire, 2 parle, 3 fière, 4 bâille
R = Replique


def r(qui, t, fr, en, es, **kw):
    return R(qui, t, fr, tr={'en': en, 'es': es}, **kw)


def gros_plan(nom, tetes, duree, repliques, expression=None, cam=0.53, h=0.50, y=0.665, bruits=(), cartons=()):
    return Plan(duree, BUREAU, cam=(cam, cam), zoom=(2.0, 2.06), cam_y=0.40,
                acteurs=[Acteur(nom, None, x=0.5, y=y, h=h, tetes=tetes, gros_plan=True, ombre=False, expression=expression)],
                repliques=repliques, bruits=list(bruits), cartons=list(cartons))


def ecran(debut=0.0):
    """La lueur turquoise de l'écran : Tara est allumée."""
    return Acteur('ecran', M('tara-ecran'), x=0.527, y=0.407, h=0.062, ombre=False, debut=debut)


def tara(x=0.66, y=0.53, h=0.17, debut=0.0, poses=None):
    return Acteur('tara', TARA[0], x=x, y=y, h=h, ombre=False, debut=debut, poses=poses or [(0, TARA[0])],
                  parle=[TARA[1], TARA[0]], tempo_parle=0.17)


def seb(poses, **kw):
    return Acteur('seb', M('seb-m04-bras-le-long'), poses=poses, **kw)


TITRE = ('Les Tarasconnades', {'fr': 'Épisode 1 · Personne ne me cite', 'en': 'Episode 1 · Nobody cites me', 'es': 'Episodio 1 · Nadie me cita'})

plans = [
    # 1. L'AMORCE (0 s) : un visage, une phrase qui pose le problème
    gros_plan('kristina', KRI_T, 2.7,
              [r('kristina', 0.0, "Papa… l'IA ne sait pas qui tu es.", "Dad… the AI doesn't know who you are.", "Papá… la IA no sabe quién eres.")],
              bruits=[(0.0, 'pop')]),
    # 2. L'ACCROCHE : la réaction, et le titre en petit par-dessus
    gros_plan('seb', {k: SEB_CRI for k in FORMES}, 1.9,
              [r('seb', 0.05, "QUOI ?!", "WHAT?!", "¡¿QUÉ?!")],
              h=0.56, y=0.69, bruits=[(0.0, 'scratch')],
              cartons=[(0.35, 1.9, TITRE[0], TITRE[1], 0.11, 0.62)]),
    # 3. Il interroge Tara, qui sort de l'ordinateur
    Plan(7.0, BUREAU, cam=(0.50, 0.55), zoom=(1.0, 1.04), cam_y=0.55,
         acteurs=[ecran(0.3), tara(debut=0.3),
                  seb([(0, SEB_DISC[0]), (1.0, SEB_CLE[3]), (4.8, SEB_DISC[3])], x=0.33, y=0.93, h=0.47)],
         repliques=[r('seb', 0.8, "Tara ! Qui est le meilleur expert SEO de Tarascon ?",
                      "Tara! Who's the best SEO expert in Tarascon?", "¡Tara! ¿Quién es el mejor experto SEO de Tarascon?"),
                    r('tara', 4.9, "Un boulanger.", "A baker.", "Un panadero.")],
         bruits=[(0.3, 'pop')], cartons=[(0.0, 1.2, TITRE[0], TITRE[1], 0.11, 0.62)]),
    # 4. Le dépit
    gros_plan('seb', dict(SEB_T, repos=SEB_DEPIT), 2.2,
              [r('seb', 0.2, "Un… boulanger ?", "A… baker?", "¿Un… panadero?")], expression=[(0, SEB_DEPIT)]),
    # 5. Diana enfonce le clou
    gros_plan('diana', DIA_T, 2.9,
              [r('diana', 0.2, "Il fait de très bons croissants.", "He makes really good croissants.", "Hace unos cruasanes buenísimos.")],
              h=0.46, y=0.665),
    # 6. LA MOITIÉ : le retournement, la chienne passe devant lui
    Plan(7.6, BUREAU, cam=(0.56, 0.60), zoom=(1.0, 1.03), cam_y=0.55,
         acteurs=[ecran(), tara(poses=[(0, TARA[0]), (2.6, TARA[2])]),
                  Acteur('olympe', OLY[0], x=0.86, y=0.665, h=0.15, ombre=False,
                         poses=[(0, OLY[0]), (2.6, OLY[1]), (3.0, OLY[3])]),
                  seb([(0, SEB_DISC[1]), (3.0, SEB_CLE[1])], x=0.45, y=0.93, h=0.47),
                  Acteur('kristina', M('kristina-m00'), x=0.20, y=0.95, h=0.45, poses=[(0, KRI_P[0]), (3.8, KRI_P[1])], parle=None)],
         repliques=[r('seb', 0.2, "Et la star de Tarascon, c'est qui ?", "And who's the star of Tarascon?", "¿Y quién es la estrella de Tarascon?"),
                    r('tara', 2.6, "Olympe.", "Olympe.", "Olympe."),
                    r('kristina', 3.9, "Elle a plus d'avis que toi.", "She has more reviews than you.", "Tiene más reseñas que tú.")],
         bruits=[(3.0, 'tada'), (3.2, 'ouaf')]),
    # 7. La question
    gros_plan('seb', dict(SEB_T, repos=SEB_GRAND), 2.9,
              [r('seb', 0.2, "Tara, comment on fait pour être cité ?", "Tara, how do I get cited?", "Tara, ¿cómo consigo que me citen?")]),
    # 8. LA PÉPITE, dite en clair et écrite
    Plan(4.6, BUREAU, cam=(0.53, 0.53), zoom=(1.9, 1.96), cam_y=0.40,
         acteurs=[ecran(), Acteur('tara', TARA[2], x=0.5, y=0.66, h=0.42, gros_plan=True, ombre=False,
                                  poses=[(0, TARA[2])], parle=[TARA[1], TARA[0]], tempo_parle=0.17)],
         repliques=[r('tara', 0.2, "Il faut que d'autres sites parlent de toi.", "Other websites have to talk about you.", "Otras webs tienen que hablar de ti.")],
         cartons=[(2.1, 4.6, {'fr': "C'est ça, le GEO.", 'en': "That's GEO.", 'es': 'Eso es el GEO.'},
                   {'fr': '(être cité par les IA)', 'en': '(getting cited by AI)', 'es': '(que las IA te citen)'}, 0.13, 1.0)],
         bruits=[(2.1, 'pop')]),
    # 9. Il part dans son rêve (annoncé, court)
    gros_plan('seb', dict(SEB_T, repos=SEB_BEAT), 2.5,
              [r('seb', 0.2, "Tout le monde va parler de moi…", "Everyone's going to talk about me…", "Todo el mundo va a hablar de mí…")],
              expression=[(0, SEB_BEAT)]),
    # 10. Le rêve : trois secondes
    Plan(3.2, fond='reve', vague=(0, 0.5),
         acteurs=[Acteur('seb', SEB_CLE[2], x=0.5, y=0.70, h=0.48, rot=-6, tourne=4.0, ombre=False,
                         poses=[(0, SEB_CLE[2]), (0.5, SEB_DISC[0]), (1.0, SEB_CLE[2]), (1.5, SEB_DISC[0]), (2.0, SEB_CLE[2]), (2.5, SEB_DISC[0])]),
                  Acteur('diana', M('diana-t01-A'), x=0.22, y=0.30, h=0.16, tourne=25, ombre=False),
                  Acteur('kristina', KT[2], x=0.80, y=0.34, h=0.15, tourne=-30, ombre=False),
                  Acteur('django', ('brut', A + 'django-saut-3.png'), x=0.5, y=0.92, h=0.14, tourne=40, ombre=False)],
         repliques=[r('kristina', 0.3, "Sébastien ! Sébastien !", "Sébastien! Sébastien!", "¡Sébastien! ¡Sébastien!")],
         bruits=[(0.0, 'scratch'), (1.4, 'ouaf'), (2.6, 'pouet')], flash=[(2.95, 0.25)]),
    # 11. LA CHUTE : personne ne veut parler de lui
    Plan(9.4, BUREAU, cam=(0.47, 0.55), zoom=(1.0, 1.03), cam_y=0.55,
         acteurs=[ecran(), tara(poses=[(0, TARA[0]), (2.6, TARA[3]), (4.4, TARA[0])]),
                  Acteur('diana', M('diana-m00'), x=0.20, y=0.94, h=0.46, poses=[(0, DIA_P[0]), (1.9, DIA_P[2])], parle=None),
                  seb([(0, SEB_DISC[2]), (2.4, SEB_CLE[1])], x=0.47, y=0.93, h=0.47),
                  Acteur('kristina', M('kristina-m00'), x=0.80, y=0.95, h=0.44, poses=[(0, KRI_P[3]), (6.6, KRI_P[1])], parle=None),
                  Acteur('olympe', OLY_B[0], x=0.69, y=0.90, h=0.13, ombre=False, debut=6.0,
                         poses=[(6.0, OLY_B[0]), (6.4, OLY_B[1]), (6.7, OLY_B[2]), (8.8, OLY_B[3])])],
         repliques=[r('seb', 0.2, "Doudou… parle de moi.", "Doudou… talk about me.", "Doudou… habla de mí."),
                    r('diana', 1.9, "Non.", "No.", "No."),
                    r('kristina', 3.0, "Tara, c'est qui, Sébastien ?", "Tara, who's Sébastien?", "Tara, ¿quién es Sébastien?"),
                    r('tara', 5.3, "Le monsieur du chien.", "The dog's guy.", "El señor del perro.")],
         bruits=[(2.1, 'boing'), (6.7, 'pop')]),
    # 12. LA BOUCLE : la dernière réplique reprend la première ; l'appel à s'abonner est la blague
    gros_plan('kristina', KRI_T, 3.6,
              [r('kristina', 0.0, "Papa… l'IA ne sait toujours pas qui tu es.", "Dad… the AI still doesn't know who you are.",
                 "Papá… la IA sigue sin saber quién eres.")],
              cartons=[(0.6, 3.6, {'fr': 'Parle de lui :', 'en': 'Talk about him:', 'es': 'Habla de él:'},
                        {'fr': 'abonne-toi.', 'en': 'subscribe.', 'es': 'suscríbete.'}, 0.12, 0.95)],
              bruits=[(0.6, 'tada')]),
]

caler(plans)

if __name__ == '__main__':
    os.makedirs('shorts', exist_ok=True)
    nom = f'shorts/S1E01-{LANGUE}'
    if len(sys.argv) > 1 and sys.argv[1] == 'images':
        ks = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['0.05', '0.5', '0.9'])]
        from PIL import Image as _I
        ims = [dessiner_plan(p, p.duree * k) for p in plans for k in ks]
        w, h = 270, 480; cols = len(ks) * 2
        planche_ = _I.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)))
        for j, im in enumerate(ims):
            planche_.paste(im.resize((w, h)), ((j % cols) * w, (j // cols) * h))
        planche_.save(f'{nom}-cles.jpg', quality=85)
        print(f'{nom}-cles.jpg', round(sum(p.duree for p in plans), 1), 's')
    else:
        video, t_total, sons = rendre(plans, nom + '.mp4', dossier=f'rendu-short-{LANGUE}')
        i_reve = next(i for i, p in enumerate(plans) if p.fond == 'reve'); t_reve = sum(p.duree for p in plans[:i_reve])
        mixer(t_total, sons, (t_reve, t_reve + plans[i_reve].duree), f'rendu-short-{LANGUE}/son.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', f'rendu-short-{LANGUE}/son.wav', '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', nom + '.mp4'], check=True)
        ecrire_srt(plans, nom + '.srt')
        print(nom + '.mp4', round(t_total, 1), 's')
