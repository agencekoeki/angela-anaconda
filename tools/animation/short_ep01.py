"""Les Tarasconnades · Épisode 1 · « Juste une petite idée » — short vertical (9:16) de 2:30 à 2:59, FR / EN / ES.

Usage : LANGUE=fr python3 short_ep01.py                 -> shorts/EP01-fr.mp4 et .srt
        LANGUE=fr python3 short_ep01.py images [k,k…]   -> planche d'images-clés
        python3 contraste.py short_ep01                  -> contrôle de lisibilité (avant toute livraison)

La question, posée à la première seconde : l'IA devait me faire gagner du temps… où est-il passé ?
(On dit « l'IA » d'abord : « Tara » seul, au début, fait décrocher ; Sébastien, 30/10/2026.)
Le test des trois phrases :
1. Tara, l'IA de la maison, finit tout en un clin d'œil ; alors Sébastien a « juste une petite idée » de plus, encore et encore.
2. Même Diana, la lucide, attrape le feu, au lit, sur son téléphone : ils rêvent de ne plus jamais dormir.
3. À 3 h, Kristina met tout le monde au lit (même Tara dort) ; à 4 h 30, Sébastien se réveille avec une petite idée.
La pépite : le paradoxe de Jevons (1865) — plus c'est efficace, plus on en consomme.

L'image raconte, la réplique ponctue :
- Tara n'est jamais présentée par une phrase. On la voit naître dans l'ordinateur (écran qui s'allume,
  démarrage écrit à l'écran, elle apparaît derrière la vitre), vivre dans les écrans (« Terminé ! »),
  puis en sortir (elle traverse la vitre) ; elle vit aussi dans le téléphone de Diana, et y rentre dormir.
- Le temps se dit par l'heure du radio-réveil (LUN., MER., JEU., VEN.) et par le volet bleu ondulé.
- Le passé se dit par l'image sépia ; le rêve, par l'ondulation et les couleurs saturées.
- Les idées se voient : la flamme sur la tête, les écrans qui se multiplient, les post-it qui envahissent les murs.
Installations et récompenses : « Vendredi, 14 h, fini » → « Chéri, c'est vendredi » ; Tara dans l'écran → Tara
hors de l'écran ; Tara qui bâille au bureau → « Même Tara dort » ; 4 h 30 au début → 4 h 30 à la fin (la boucle).
"""
import os
import subprocess
import sys

os.environ['FORMAT'] = 'vertical'
from moteur import *          # noqa: E402

A = 'assets/'
M = lambda n: A + n + '.png'
D = '/mnt/user-data/uploads/angela-anaconda/media-local/decors/'
BUREAU1 = D + 'aa-decor-11-bureau-vertical.png'     # avant : un seul écran
JOUR = D + 'aa-decor-14-bureau-jour-vertical.png'    # après : trois écrans
NUIT = D + 'aa-decor-12-bureau-nuit-vertical.png'
CHAMBRE = D + 'aa-decor-13-chambre-nuit-vertical.png'
PLAGE = D + 'aa-decor-15-plage-vertical.png'


def planche(nom, n=4):
    return [('brut', A + f'{nom}-{i}.png') for i in range(1, n + 1)]


BOUCHES = {'A': M('seb-b01-A'), 'O': M('seb-b02-O'), 'OU': M('seb-b03-OU'), 'IE': M('seb-b04-I-E'),
           'MBP': M('seb-b05-MBP'), 'FV': M('seb-b06-FV'), 'L': M('seb-b07-L')}
ST = [M(f'seb-tete-nuit-{i}') for i in range(1, 5)]       # 1 épuisé mais surexcité, 2 l'idée, 3 solennel, 4 endormi


def seb_t(repos):
    return dict(BOUCHES, repos=repos)


def fige(chemin):
    """Une tête sans bouches de rechange : elle garde son expression même quand il parle."""
    return {k: chemin for k in FORMES}


KT = [M(f'kristina-tete-{i}') for i in range(1, 5)]       # 1 pince-sans-rire, 2 elle parle, 3 rit, 4 lève les yeux au ciel
KRI_T = {k: (KT[1] if k in ('A', 'O', 'OU', 'IE', 'L') else KT[0]) for k in FORMES}
SEB_DISC, SEB_CLE, SEB_MARCHE = planche('seb-discours'), planche('seb-cles'), [A + f'seb-marche-{i}.png' for i in range(1, 5)]
DIA_P, DIA_N = planche('diana-parle'), planche('diana-pyjama')    # pyjama : 1 tape, 2 chut, 3 l'idée, 4 endormie
DIA_MARCHE = [A + f'diana-marche-{i}.png' for i in range(1, 5)]
KRI_P, KRI_N = planche('kristina-parle'), planche('kristina-nuit')  # nuit : 1 bras croisés, 2 « au lit ! », 3 emporte tout, 4 bâille
KRI_MARCHE = [A + f'kristina-marche-{i}.png' for i in range(1, 5)]
DJ_ASSIS, DJ_SAUT = planche('django-assis'), [A + f'django-saut-{i}.png' for i in range(1, 5)]
OLY_B, OLY = planche('olympe-bonjour'), planche('olympe-aboie')
TARA = planche('tara')                                              # 1 sourire, 2 parle, 3 fière, 4 bâille
FLAMME = [M(f'flamme-{i}') for i in range(1, 4)]
R = Replique
LUEUR_TARA = ((175, 252, 246), 3, 2)                                # Tara brille : une fine lueur claire la détache de tous les fonds
# ---------------------------------------------------------------- les proportions (Sébastien, 30/10/2026 : « attention à la taille »)
# Un humain debout mesure environ 1,80 m. Hauteur VISIBLE de chaque animal, en part de la hauteur d'un humain
# debout placé à la même profondeur (on pose les chiens sur la même ligne de sol que les humains) :
#   Django assis (berger australien, sommet de la tête) 0,42 ; Django qui court 0,36 ;
#   Olympe debout 0,38 ; Olympe couchée, tête levée 0,25 ; Tara hors de l'écran (tarasque de poche) 0,25.
# Les poses « brut » gardent la toile commune de leur planche : on divise par la part de la toile qu'occupe la pose la plus haute.
def taille_animal(humain, part, toile=1.0):
    return humain * part / toile


LISERE_CHIEN = None                                                 # essayé (fil sombre, halo) : inutile, et ça s'éloigne de l'épisode alpha

# les vitres des écrans, en fraction du décor : (x0, y0, x1, y1)
# (retrouvées par calage.py dans les décors ; controle.py vérifie qu'elles y tombent toujours)
VITRE1 = (0.464, 0.343, 0.592, 0.406)                                         # bureau d'avant
VITRES = [(0.354, 0.370, 0.454, 0.423), (0.488, 0.370, 0.590, 0.423), (0.630, 0.370, 0.725, 0.423)]   # bureau de jour
VITRES_N = VITRES                                                             # bureau de nuit : même meuble (l'ancienne mesure à l'œil était fausse, Sébastien l'a vu)


def r(qui, t, fr, en, es, **kw):
    return R(qui, t, fr, tr={'en': en, 'es': es}, **kw)


def L(fr, en, es):
    return {'fr': fr, 'en': en, 'es': es}


def centre(v):
    return (v[0] + v[2]) / 2


def ecran(v, debut=0.0):
    """L'écran allumé : une lueur bleu nuit posée sur la vitre (Tara, turquoise, s'y détache)."""
    return Acteur('ecran', M('ecran-allume'), x=centre(v), y=v[3], h=(v[3] - v[1]), ombre=False, debut=debut, cible=v,
                  ajuster=True, echelle_libre=True)


def tara_dans(v, debut=0.0, fin=1e9, poses=None, sortie=None):
    """Tara derrière la vitre v ; sortie=(t0, t1, x, y, grandeur) : elle traverse la vitre et vient dans la pièce."""
    hv = (v[3] - v[1]) * 0.88
    traj = []
    cadre = v
    if sortie:
        t0, t1, x, y, g = sortie
        traj = [(t0, centre(v), v[3], 1.0), (t1, x, y, g)]
        cadre = v + (t0 + 0.12,)
    return Acteur('tara', TARA[0], x=centre(v), y=v[3], h=hv, ombre=False, debut=debut, fin=fin, cadre=cadre, trajet=traj,
                  poses=poses or [(0, TARA[0])], parle=[TARA[1], TARA[0]], tempo_parle=0.17, contour=LUEUR_TARA,
                  opacite=[(debut, 0.0), (debut + 0.25, 1.0)])


def tara(x, y, h, debut=0.0, fin=1e9, poses=None, trajet=None):
    return Acteur('tara', TARA[0], x=x, y=y, h=h, ombre=False, debut=debut, fin=fin, poses=poses or [(0, TARA[0])],
                  parle=[TARA[1], TARA[0]], tempo_parle=0.17, contour=LUEUR_TARA, trajet=trajet or [])


def flamme(x, y, h, debut=0.0, fin=1e9, grandit=None, gros_plan=False):
    """La flamme de l'idée au-dessus d'une tête ; grandit=[(t, taille)] pour la faire monter (ou s'éteindre)."""
    traj = [(t, x, y, k) for (t, k) in grandit] if grandit else []
    return Acteur('flamme', FLAMME[0], x=x, y=y, h=h, ombre=False, debut=debut, fin=fin, gros_plan=gros_plan, trajet=traj,
                  poses=[(debut + i * 0.125, FLAMME[i % 3]) for i in range(int((min(fin, 40) - debut) / 0.125) + 1)])


def gros_plan(nom, tetes, decor, duree, repliques, expression=None, h=0.40, y=0.62, cam=0.53, cam_y=0.40, **kw):
    """Face caméra, la tête dans la zone sûre (sous l'heure, au-dessus des sous-titres)."""
    extra = kw.pop('extra', ())
    tete = Acteur(nom, None, x=0.5, y=y, h=h, tetes=tetes, gros_plan=True, ombre=False, expression=expression)
    return Plan(duree, decor, cam=(cam, cam), zoom=(2.0, 2.06), cam_y=cam_y, acteurs=[tete] + list(extra), repliques=repliques, **kw)


# le flocage SEO Addict de l'épisode (un par épisode, en vente sur seoaddict.co) : posé sur le t-shirt rose dans les poses de face
FLOCAGE = '/mnt/user-data/uploads/angela-anaconda/media-local/flocages/FR-271 - Timer oublié 72 h - pour t-shirt foncé.png'
BOUTIQUE = {'fr': 'seoaddict.co/fr/p/timer-oublie-72-h-t-shirt/', 'en': 'seoaddict.co/p/forgotten-timer-72-h-t-shirt/',
            'es': 'seoaddict.co/es/p/timer-olvidado-72-h-camiseta/'}


def seb(poses, **kw):
    kw.setdefault('flocage', FLOCAGE)
    return Acteur('seb', M('seb-m04-bras-le-long'), poses=poses, **kw)


def de_dos(x=0.53, y=0.93, h=0.45, **kw):
    return Acteur('seb', M('seb-s1-de-dos-v2'), x=x, y=y, h=h, **kw)


def tete_de_dos(x=0.53, y=0.93, h=0.45):
    """Le haut de la tête de Sébastien vu de dos : là où pousse la flamme."""
    return x, y - h * 0.97


TITRE = ('Les Tarasconnades', L('Ép. 1 · Juste une petite idée', 'Ep. 1 · Just one tiny idea', 'Ep. 1 · Solo una ideíta'))
J = lambda fr, en, es: L(fr, en, es)

plans = [
    # ---------------------------------------------------------------- L'AMORCE (0 s)
    # 1. 4 h 30, le radio-réveil, les yeux cernés : la question
    gros_plan('seb', fige(ST[0]), NUIT, 3.4,
              [r('seb', 0.5, "L'IA devait me faire gagner du temps.", "AI was supposed to save me time.", "La IA tenía que ahorrarme tiempo.")],
              bruits=[(0.0, 'bip')], horloge=[(0.0, 3.4, '04:30')]),
    # 2. Le regard s'allume, la flamme pousse
    gros_plan('seb', fige(ST[1]), NUIT, 3.0,
              [r('seb', 0.4, "…alors j'ai eu une petite idée.", "…so I had one tiny idea.", "…así que tuve una ideíta.")],
              bruits=[(0.25, 'whoosh')], horloge=[(0.0, 3.0, '04:30')],
              extra=[flamme(0.5, 0.25, 0.12, debut=0.25, gros_plan=True, grandit=[(0.25, 0.3), (0.6, 1.0)])]),
    # 3. La carte-titre : la carte de l'épisode arrive, brille, se retourne ; son dos bleu remplit l'écran (Sébastien, 30/10)
    Plan(4.0, NUIT, cam=(0.53, 0.53), zoom=(2.0, 2.0), cam_y=0.40,
         carte={'debut': 0.0, 'serie': 'LES TARASCONNADES', 'numero': L('ÉP. 1', 'EP. 1', 'EP. 1'),
                'nom': L('Juste une petite idée', 'Just one tiny idea', 'Solo una ideíta'),
                'illustration': [ST[1]], 'flamme': FLAMME[0],
                'espece': L('Expert SEO · Tarascon · Taille : une petite idée', 'SEO expert · Tarascon · Size: one tiny idea',
                            'Experto SEO · Tarascón · Tamaño: una ideíta'),
                'attaques': [(L('Petite idée', 'Tiny idea', 'Ideíta'), '∞',
                              L('Transforme deux heures gagnées en une nuit blanche.', 'Turns two hours saved into a sleepless night.',
                                'Convierte dos horas ganadas en una noche en vela.')),
                             (L('Et si, en plus…', 'And on top…', 'Y además…'), '×2',
                              L("Relance l'attaque précédente. Sans fin.", 'Repeats the previous attack. Forever.',
                                'Repite el ataque anterior. Sin fin.'))],
                'pied': (L('Faiblesse : Kristina ×2', 'Weakness: Kristina ×2', 'Debilidad: Kristina ×2'),
                         L('Saison 1 · 1/12', 'Season 1 · 1/12', 'Temporada 1 · 1/12'))},
         bruits=[(0.0, 'whoosh'), (0.45, 'tada'), (2.7, 'whoosh')]),

    # ---------------------------------------------------------------- AVANT (le passé, en sépia)
    # 4. Le volet bleu, le carton du temps
    Plan(2.0, fond='bleu', cartons=[(0.1, 2.0, L('Il y a un an…', 'A year ago…', 'Hace un año…'), None, 0.40, 1.0)],
         bruits=[(0.0, 'whoosh')], volet=[(1.5, 2.0, 'couvre')]),
    # 5. Le vendredi d'avant : un seul écran, éteint à 14 h ; Diana et Kristina débarquent
    Plan(7.6, BUREAU1, cam=(0.50, 0.50), zoom=(1.0, 1.02), cam_y=0.55, souvenir=True, volet=[(0.0, 0.5, 'decouvre')],
         acteurs=[Acteur('django', DJ_ASSIS[0], x=0.36, y=0.92, h=taille_animal(0.46, 0.42), poses=[(0, DJ_ASSIS[0]), (1.4, DJ_ASSIS[3])], contour=LISERE_CHIEN),
                  seb([(0, SEB_DISC[3]), (0.9, SEB_CLE[2])], x=0.52, y=0.93, h=0.46),
                  Acteur('diana', M('diana-m00'), x=0.24, y=0.97, h=0.44, marche=DIA_MARCHE, poses=[(0, DIA_P[1])],
                         trajet=[(2.6, -0.15, 0.97), (3.6, 0.24, 0.97)]),
                  Acteur('kristina', M('kristina-m00'), x=0.77, y=0.98, h=0.42, marche=KRI_MARCHE, miroir=True,
                         poses=[(0, KRI_P[2])], trajet=[(4.2, 1.15, 0.98), (5.2, 0.77, 0.98)])],
         repliques=[r('seb', 0.8, "Vendredi, 14 h. Fini !", "Friday, 2 PM. Done!", "Viernes, 14 h. ¡Terminado!"),
                    r('diana', 3.7, "La plage ?", "Beach?", "¿Playa?"),
                    r('kristina', 5.3, "La plage !", "Beach!", "¡Playa!")],
         bruits=[(0.9, 'tada'), (5.3, 'ouaf')], horloge=[(0.0, 2.6, L('VEN. 14:00', 'FRI 2:00 PM', 'VIE. 14:00'))]),
    # 6. La plage d'avant : on ne faisait rien (la voix dit « rien », Django dit le contraire)
    Plan(9.4, PLAGE, cam=(0.47, 0.50), zoom=(1.0, 1.04), cam_y=0.55, souvenir=True,
         # (Olympe n'est pas venue : elle refuse la plage ; sur le sable, elle s'y confondait)
         acteurs=[                  seb([(0, SEB_DISC[0])], x=0.62, y=0.90, h=0.42),
                  Acteur('diana', DIA_P[1], x=0.40, y=0.93, h=0.42, poses=[(0, DIA_P[1])]),
                  Acteur('kristina', KRI_P[2], x=0.80, y=0.96, h=0.40, poses=[(0, KRI_P[2])]),
                  # Django court devant tout le monde (la voix dit « rien », lui ne s'arrête pas)
                  Acteur('django', DJ_SAUT[0], x=0.5, y=0.99, h=taille_animal(0.42, 0.36, 0.91), marche=DJ_SAUT, brut=True, marche_pas=1, saut=0.01,
                         fin=2.6, trajet=[(0.0, -0.1, 0.99), (2.6, 1.15, 0.97)], contour=LISERE_CHIEN),
                  Acteur('django', DJ_SAUT[0], x=0.5, y=0.99, h=taille_animal(0.42, 0.36, 0.91), marche=DJ_SAUT, brut=True, marche_pas=1, saut=0.01,
                         debut=4.0, trajet=[(4.0, -0.1, 0.99), (6.8, 1.15, 0.99)], contour=LISERE_CHIEN)],
         repliques=[r('seb', 0.6, "Le week-end, on ne faisait rien.", "On weekends, we did nothing.", "Los fines de semana, no hacíamos nada."),
                    r('diana', 3.5, "Rien du tout.", "Nothing at all.", "Nada de nada."),
                    r('kristina', 5.4, "Même pas la vaisselle.", "Not even the dishes.", "Ni siquiera los platos.")],
         bruits=[(0.0, 'mer'), (1.0, 'ouaf'), (3.6, 'mer'), (4.2, 'ouaf'), (6.6, 'mer')], volet=[(8.8, 9.4, 'couvre')]),
    # 7. Le volet bleu : « Puis, un jour… »
    Plan(2.2, fond='bleu', cartons=[(0.1, 2.2, L('Puis, un jour…', 'Then, one day…', 'Y un día…'), None, 0.40, 1.0)],
         bruits=[(0.0, 'whoosh')]),

    # ---------------------------------------------------------------- TARA ARRIVE (l'installation)
    # 8. Le même bureau, en couleurs : l'écran s'allume, la caméra plonge dedans
    # (le bureau est vide : l'ordinateur s'allume tout seul)
    Plan(3.6, BUREAU1, cam=(0.50, 0.527), zoom=(1.0, 3.4), cam_y=0.376, volet=[(0.0, 0.5, 'decouvre')],
         acteurs=[Acteur('django', DJ_ASSIS[0], x=0.40, y=0.86, h=taille_animal(0.40, 0.42), poses=[(0, DJ_ASSIS[3]), (1.1, DJ_ASSIS[1])], contour=LISERE_CHIEN),
                  ecran(VITRE1, debut=1.0)],
         bruits=[(1.0, 'crt'), (2.0, 'whoosh')]),
    # 9. Plein écran : le démarrage s'écrit, puis Tara apparaît derrière la vitre
    Plan(6.8, fond='crt', crt={'allume': 0.0, 'lignes': [(0.4, 'TARA 1.0'), (0.9, L('Intelligence', 'Artificial', 'Inteligencia')),
                                                  (1.3, L('artificielle', 'intelligence', 'artificial')), (1.8, L('Chargement…', 'Loading…', 'Cargando…'))],
                                 'barre': (2.3, 3.4)},
         acteurs=[Acteur('tara', TARA[0], x=0.5, y=0.79, h=0.34, ombre=False, debut=3.6, cadre=GLACE_CRT,
                         poses=[(3.6, TARA[0]), (4.3, TARA[2])], parle=[TARA[1], TARA[0]], tempo_parle=0.17,
                         contour=LUEUR_TARA, opacite=[(3.6, 0.0), (3.9, 1.0)],
                         trajet=[(3.6, 0.5, 0.79, 0.6), (3.9, 0.5, 0.79, 1.0)])],
         repliques=[r('tara', 4.4, "Bonjour ! Je fais quoi ?", "Hello! What shall I do?", "¡Hola! ¿Qué hago?")],
         bruits=[(0.4, 'clavier'), (3.6, 'pop'), (3.7, 'tada')]),
    # 10. Le bureau : Tara, toute petite derrière la vitre, a déjà fini
    Plan(6.0, BUREAU1, cam=(0.52, 0.52), zoom=(1.45, 1.45), cam_y=0.55,     # sa tête au-dessus de la ligne des sous-titres
         acteurs=[ecran(VITRE1), tara_dans(VITRE1, poses=[(0, TARA[0]), (0.9, TARA[2])]),
                  seb([(0, M('seb-s1-de-dos-v2')), (1.9, SEB_CLE[2])], x=0.53, y=0.93, h=0.45)],
         repliques=[r('tara', 0.5, "Terminé !", "Done!", "¡Listo!"),
                    r('seb', 2.1, "Deux heures de gagnées !", "Two hours saved!", "¡Dos horas ganadas!")],
         bruits=[(0.0, 'clavier'), (0.5, 'pop'), (2.0, 'tada')]),
    # 11. Et la flamme pousse
    gros_plan('seb', seb_t(M('seb-t02-sourire-en-coin')), BUREAU1, 4.2,
              [r('seb', 0.9, "Et si j'en profitais… pour une petite idée ?", "What if I used it… for one tiny idea?",
                 "¿Y si lo aprovechara… para una ideíta?")],
              bruits=[(0.5, 'whoosh')], extra=[flamme(0.5, 0.25, 0.12, debut=0.5, gros_plan=True, grandit=[(0.5, 0.3), (0.9, 1.0)])]),
    # 12. Pop, pop : le bureau d'un écran devient le bureau de trois écrans
    Plan(1.4, BUREAU1, cam=(0.52, 0.52), zoom=(1.0, 1.0), cam_y=0.55,
         acteurs=[ecran(VITRE1), de_dos(), flamme(*tete_de_dos(), 0.07)], flash=[(1.15, 0.25)], bruits=[(1.1, 'pop')]),
    Plan(3.4, JOUR, cam=(0.53, 0.53), zoom=(1.25, 1.25), cam_y=0.50,
         acteurs=[ecran(VITRES[0], 0.3), ecran(VITRES[1], 0.0), ecran(VITRES[2], 0.6), tara_dans(VITRES[1], debut=1.0),
                  de_dos(), flamme(*tete_de_dos(), 0.07, grandit=[(0, 1.0), (1.2, 1.4)])],
         bruits=[(0.0, 'pop'), (0.3, 'pop'), (0.6, 'pop'), (1.0, 'tada')]),

    # ---------------------------------------------------------------- LA SEMAINE (règle de trois)
    # 13. Lundi : Tara a fini, Sébastien relance, les post-it commencent
    Plan(5.2, JOUR, cam=(0.53, 0.53), zoom=(1.25, 1.25), cam_y=0.50,
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]), tara_dans(VITRES[0], poses=[(0, TARA[0]), (0.8, TARA[2])]),
                  de_dos(), flamme(*tete_de_dos(), 0.07, grandit=[(0, 1.4), (5.2, 1.7)])],
         postits=[(1.6, 4.5, 6, (0.10, 0.20, 0.90, 0.40), False, 11)],
         repliques=[r('tara', 0.5, "Terminé !", "Done!", "¡Listo!"),
                    r('seb', 1.8, "Et si on…", "What if we…", "¿Y si…?")],
         bruits=[(0.5, 'pop'), (1.6, 'clavier')], horloge=[(0.0, 5.2, L('LUN. 09:00', 'MON 9:00 AM', 'LUN. 09:00'))]),
    # 14. Mercredi : pareil, en plus serré, encore plus de post-it
    Plan(4.8, JOUR, cam=(0.56, 0.56), zoom=(1.55, 1.55), cam_y=0.53,
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]), tara_dans(VITRES[2], poses=[(0, TARA[0]), (0.8, TARA[2])]),
                  de_dos(), flamme(*tete_de_dos(), 0.07, grandit=[(0, 1.7), (4.8, 2.1)])],
         postits=[(0.0, 0.01, 6, (0.10, 0.20, 0.90, 0.40), False, 11), (1.2, 4.0, 10, (0.06, 0.15, 0.94, 0.45), False, 12)],
         repliques=[r('tara', 0.4, "Terminé !", "Done!", "¡Listo!"),
                    r('seb', 1.5, "Et si, en plus…", "And what if, on top…", "¿Y si, además…?")],
         bruits=[(0.4, 'pop'), (1.2, 'clavier')], horloge=[(0.0, 4.8, L('MER. 13:00', 'WED 1:00 PM', 'MIÉ. 13:00'))]),
    # 15. Jeudi : la troisième fois casse le motif — Tara finit sa phrase à sa place ; Olympe s'en va, raide
    Plan(6.6, JOUR, cam=(0.53, 0.53), zoom=(1.25, 1.25), cam_y=0.50,
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]), tara_dans(VITRES[0], poses=[(0, TARA[0]), (2.2, TARA[1]), (3.4, TARA[0])]),
                  de_dos(), flamme(*tete_de_dos(), 0.07, grandit=[(0, 2.1), (6.6, 2.5)]),
                  Acteur('olympe', OLY_B[0], h=taille_animal(0.45, 0.38, 0.98), saut=0.004, debut=4.0, trajet=[(4.0, 0.80, 0.96), (6.6, 1.25, 0.96)])],
         postits=[(0.0, 0.01, 16, (0.06, 0.15, 0.94, 0.45), False, 12), (0.8, 3.6, 12, (0.04, 0.12, 0.96, 0.60), False, 13)],
         repliques=[r('tara', 0.4, "Terminé !", "Done!", "¡Listo!"),
                    r('seb', 1.5, "Et si…", "What if…", "¿Y si…?"),
                    r('tara', 2.5, "…en plus ? Je sais.", "…on top? I know.", "…¿además? Ya lo sé."),
                    r('olympe', 4.4, "Grrr…", "Grrr…", "Grrr…", off=True)],
         bruits=[(0.4, 'pop'), (2.5, 'soupir'), (4.4, 'ouaf')], horloge=[(0.0, 6.6, L('JEU. 17:00', 'THU 5:00 PM', 'JUE. 17:00'))]),

    # ---------------------------------------------------------------- TARA SORT (la récompense)
    # 16. Django fixe l'écran du milieu ; Tara traverse la vitre et vient dans la pièce
    Plan(7.8, JOUR, cam=(0.50, 0.50), zoom=(1.0, 1.0), cam_y=0.55,
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]),
                  Acteur('django', DJ_ASSIS[0], x=0.34, y=0.93, h=taille_animal(0.46, 0.42), marche=[('brut', c) for c in DJ_SAUT], marche_pas=1, saut=0.01, contour=LISERE_CHIEN,
                         poses=[(0, DJ_ASSIS[0]), (2.4, DJ_ASSIS[2])], trajet=[(5.0, 0.34, 0.93), (6.0, -0.25, 0.90)]),
                  tara_dans(VITRES[1], poses=[(0, TARA[0]), (2.2, TARA[2])], sortie=(1.0, 2.4, 0.52, 0.66, 2.6)),
                  de_dos(x=0.76, y=0.95, h=0.46), flamme(*tete_de_dos(0.76, 0.95, 0.46), 0.07, grandit=[(0, 2.5), (7.2, 2.5)])],
         postits=[(0.0, 0.01, 28, (0.04, 0.12, 0.96, 0.60), False, 14)],
         repliques=[r('tara', 3.0, "Je le promène ?", "Shall I walk him?", "¿Lo saco a pasear?")],
         bruits=[(1.0, 'whoosh'), (2.3, 'boing'), (4.8, 'pouet'), (5.1, 'scratch')]),
    # 17. Vendredi, 16 h : Diana entre (et l'heure rappelle le vendredi d'avant)
    Plan(5.0, JOUR, cam=(0.42, 0.42), zoom=(1.0, 1.0), cam_y=0.55,
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]), tara(0.50, 0.66, 0.11, poses=[(0, TARA[2])]),
                  de_dos(x=0.76, y=0.95, h=0.46), flamme(*tete_de_dos(0.76, 0.95, 0.46), 0.07, grandit=[(0, 2.5)]),
                  Acteur('diana', M('diana-m00'), x=0.24, y=0.97, h=0.45, marche=DIA_MARCHE, poses=[(0, DIA_P[3])],
                         trajet=[(0.3, -0.15, 0.97), (1.3, 0.24, 0.97)])],
         postits=[(0.0, 0.01, 28, (0.04, 0.12, 0.96, 0.60), False, 14)],
         repliques=[r('diana', 1.6, "Chéri… c'est vendredi.", "Honey… it's Friday.", "Cariño… es viernes.")],
         horloge=[(0.0, 5.0, L('VEN. 16:00', 'FRI 4:00 PM', 'VIE. 16:00'))]),
    # 18. Sa réponse, solennelle
    gros_plan('seb', seb_t(ST[2]), JOUR, 3.4,
              [r('seb', 0.4, "Doudou… je réinvente le métier.", "Doudou… I'm reinventing the job.", "Doudou… estoy reinventando el oficio.")],
              expression=[(0, ST[2])], extra=[flamme(0.5, 0.25, 0.14, gros_plan=True)]),
    # 18 bis. LE CLIN D'ŒIL BOUTIQUE : on zoome sur son t-shirt (« J'ai oublié d'arrêter le timer »), le bandeau dit où le trouver
    Plan(4.4, JOUR, cam=(0.50, 0.50), zoom=(1.0, 4.2), cam_y=0.668,
         acteurs=[seb([(0, M('seb-m04-bras-le-long')), (0.9, M('seb-m02-blase'))], x=0.5, y=0.95, h=0.46),
                  flamme(0.5, 0.95 - 0.46 * 0.96, 0.07, grandit=[(0, 2.5)])],
         postits=[(0.0, 0.01, 28, (0.04, 0.12, 0.96, 0.60), False, 14)],
         bandeaux=[(1.3, 4.4, L('Ce t-shirt ? seoaddict.co', 'This t-shirt? seoaddict.co', '¿Esta camiseta? seoaddict.co'),
                    L('« Timer oublié : 72 h »', '“Forgotten timer: 72 h”', '«Timer olvidado: 72 h»'), 0.585, 1.0)],
         repliques=[r('seb', 1.4, "Le t-shirt ? Sur seoaddict.co.", "The t-shirt? On seoaddict.co.", "¿La camiseta? En seoaddict.co.",
                      sous_titre=False)],
         bruits=[(0.0, 'whoosh'), (1.3, 'ding')]),
    # 19. Diana, bras croisés, soupire et s'en va
    Plan(4.0, JOUR, cam=(0.42, 0.42), zoom=(1.15, 1.15), cam_y=0.55,
         acteurs=[Acteur('diana', DIA_P[2], x=0.30, y=0.97, h=0.48, marche=DIA_MARCHE, miroir=True, poses=[(0, DIA_P[2])],
                         trajet=[(2.4, 0.30, 0.97), (3.7, -0.20, 0.97)])],
         postits=[(0.0, 0.01, 28, (0.04, 0.12, 0.96, 0.60), False, 14)],
         bruits=[(0.6, 'soupir')]),
    # 20. Vendredi soir : Tara bâille (on s'en souviendra), lui pas
    Plan(5.6, NUIT, cam=(0.53, 0.53), zoom=(1.25, 1.25), cam_y=0.50,
         acteurs=[ecran(VITRES_N[0]), ecran(VITRES_N[1]), ecran(VITRES_N[2]),
                  tara_dans(VITRES_N[2], poses=[(0, TARA[0]), (0.8, TARA[3]), (2.0, TARA[0])]),
                  de_dos(), flamme(*tete_de_dos(), 0.07, grandit=[(0, 2.5)])],
         repliques=[r('seb', 2.4, "Allez… une dernière, et au lit.", "Come on… one last one, then bed.", "Venga… una última y a la cama.")],
         bruits=[(0.8, 'soupir')], horloge=[(0.0, 5.6, L('VEN. 22:30', 'FRI 10:30 PM', 'VIE. 22:30'))],
         volet=[(5.0, 5.6, 'couvre')]),

    # ---------------------------------------------------------------- LE RETOURNEMENT : Diana aussi
    # 21. 23 h : Diana au lit, sur son téléphone… avec Tara
    Plan(7.4, CHAMBRE, cam=(0.52, 0.52), zoom=(1.0, 1.03), cam_y=0.50, volet=[(0.0, 0.5, 'decouvre')],
         acteurs=[Acteur('diana', DIA_N[0], x=0.40, y=0.505, h=0.25, ombre=False, poses=[(0, DIA_N[0]), (3.4, DIA_N[1])]),
                  tara(0.47, 0.40, 0.05, debut=0.8, poses=[(0, TARA[0])]),
                  Acteur('olympe', OLY[0], x=0.50, y=0.585, h=taille_animal(0.47, 0.25), ombre=False),
                  Acteur('seb', M('seb-m04-bras-le-long'), x=0.80, y=0.94, h=0.47, marche=SEB_MARCHE, miroir=True,
                         poses=[(0, SEB_DISC[3]), (5.6, SEB_CLE[1])], trajet=[(1.0, 1.15, 0.94), (2.2, 0.80, 0.94)]),
                  flamme(0.80, 0.94 - 0.47 * 0.96, 0.07, debut=2.2, grandit=[(2.2, 1.2)])],
         repliques=[r('seb', 2.5, "Doudou ? Tu dors ?", "Doudou? You asleep?", "¿Doudou? ¿Duermes?"),
                    r('diana', 3.6, "Chut. Tara a une idée.", "Shh. Tara has an idea.", "Chis. Tara tiene una idea."),
                    r('seb', 5.6, "Toi aussi ?!", "You too?!", "¿¡Tú también!?")],
         bruits=[(0.8, 'pop'), (5.6, 'boing')], horloge=[(0.0, 7.4, '23:00', 0.74)]),
    # 22. Les deux flammes, et la grande idée
    Plan(6.2, CHAMBRE, cam=(0.56, 0.56), zoom=(1.08, 1.10), cam_y=0.52,
         acteurs=[Acteur('diana', DIA_N[2], x=0.40, y=0.505, h=0.25, ombre=False, poses=[(0, DIA_N[2])]),
                  flamme(0.41, 0.505 - 0.25 * 0.97, 0.06, grandit=[(0, 0.3), (0.5, 1.4)]),
                  tara(0.47, 0.40, 0.05, poses=[(0, TARA[2])]),
                  seb([(0, SEB_DISC[1])], x=0.66, y=0.94, h=0.47),
                  flamme(0.66, 0.94 - 0.47 * 0.96, 0.07, grandit=[(0, 1.2), (5.6, 1.8)])],
         postits=[(2.4, 5.0, 26, (0.05, 0.14, 0.95, 0.40), False, 21)],
         repliques=[r('diana', 0.4, "Et si on faisait…", "What if we made…", "¿Y si hiciéramos…?"),
                    r('seb', 2.0, "…un dessin animé ?!", "…a cartoon?!", "…¿¡unos dibujos animados!?")],
         bruits=[(0.0, 'whoosh'), (2.4, 'tada')], horloge=[(0.0, 6.2, '23:40', 0.74)]),
    # 23. LE RÊVE (annoncé par l'ondulation) : les rois des idées, et une ribambelle de Tara
    Plan(6.0, fond='reve', vague=(0.0, 0.7),
         acteurs=[tara(0.5 + 0.38 * math.cos(2 * math.pi * k / 9), 0.42 + 0.20 * math.sin(2 * math.pi * k / 9), 0.07,
                       poses=[(0, TARA[k % 3])],
                       trajet=[(tt, 0.5 + 0.38 * math.cos(2 * math.pi * (k / 9 + tt / 8)), 0.42 + 0.20 * math.sin(2 * math.pi * (k / 9 + tt / 8)))
                               for tt in [i * 0.5 for i in range(13)]]) for k in range(9)]
                 + [Acteur('seb', SEB_DISC[0], x=0.36, y=0.66, h=0.36, rot=-6, poses=[(0, SEB_DISC[0]), (3.0, SEB_CLE[2])], ombre=False),
                    Acteur('diana', DIA_P[1], x=0.66, y=0.66, h=0.34, rot=6, poses=[(0, DIA_P[1])], ombre=False),
                    flamme(0.36, 0.30, 0.08, grandit=[(0, 2.0)]), flamme(0.66, 0.32, 0.08, grandit=[(0, 2.0)])],
         repliques=[r('seb', 1.0, "On ne dormira plus jamais !", "We'll never sleep again!", "¡No dormiremos nunca más!"),
                    r('diana', 3.4, "Plus jamais !", "Never again!", "¡Nunca más!")],
         bruits=[(0.0, 'whoosh'), (3.4, 'tada')]),

    # ---------------------------------------------------------------- 3 H : TOUT EST PERDU, LA PÉPITE
    # 24. Coupe sèche : Kristina à la porte
    Plan(7.0, CHAMBRE, cam=(0.58, 0.58), zoom=(1.08, 1.10), cam_y=0.55,
         acteurs=[Acteur('diana', DIA_N[2], x=0.40, y=0.505, h=0.25, ombre=False, poses=[(0, DIA_N[2])]),
                  flamme(0.41, 0.505 - 0.25 * 0.97, 0.10),
                  tara(0.47, 0.40, 0.05, poses=[(0, TARA[0]), (1.5, TARA[3])]),
                  seb([(0, SEB_DISC[1]), (1.4, M('seb-m02-blase'))], x=0.56, y=0.94, h=0.47),
                  flamme(0.56, 0.94 - 0.47 * 0.96, 0.14),
                  Acteur('kristina', KRI_N[0], x=0.86, y=0.95, h=0.46, poses=[(0, KRI_N[0])])],
         postits=[(0.0, 0.01, 40, (0.04, 0.12, 0.96, 0.42), False, 21)],
         repliques=[r('kristina', 0.4, "Il est trois heures.", "It's three a.m.", "Son las tres."),
                    r('kristina', 2.8, "Vous deviez gagner du temps, non ?", "Weren't you supposed to save time?", "¿No ibais a ahorrar tiempo?")],
         bruits=[(0.0, 'scratch')], horloge=[(0.0, 7.0, '03:00', 0.74)]),
    # 25. Sébastien, en dépit
    gros_plan('seb', seb_t(M('seb-t03-depit')), CHAMBRE, 3.8,
              [r('seb', 0.4, "On en a gagné… et on l'a tout redépensé.", "We saved it… and spent it all again.", "Lo ganamos… y lo volvimos a gastar todo.")],
              cam=0.60, cam_y=0.45),
    # 26. LA PÉPITE : Kristina la dit en clair, le bandeau l'écrit
    gros_plan('kristina', KRI_T, CHAMBRE, 7.0,
              [r('kristina', 0.4, "Plus c'est rapide, plus on en fait.", "The faster it gets, the more we do.", "Cuanto más rápido, más hacemos.")],
              h=0.36, y=0.62, cam=0.70, cam_y=0.45, expression=[(0, KT[0]), (4.6, KT[3])],
              bandeaux=[(2.6, 7.0, L("Le paradoxe de Jevons", "The Jevons paradox", 'La paradoja de Jevons'),
                         L("1865 : plus c'est efficace, plus on en consomme.", '1865: the more efficient, the more we consume.',
                           '1865: cuanto más eficiente, más se consume.'), 0.145, 1.0)],
              bruits=[(2.6, 'pop')]),
    # 27. Les flammes s'éteignent
    Plan(3.8, CHAMBRE, cam=(0.52, 0.52), zoom=(1.2, 1.2), cam_y=0.50,
         acteurs=[Acteur('diana', DIA_N[0], x=0.40, y=0.505, h=0.25, ombre=False, poses=[(0, DIA_N[2]), (1.2, DIA_N[0])]),
                  flamme(0.41, 0.505 - 0.25 * 0.97, 0.10, grandit=[(0.4, 1.0), (1.6, 0.0)]),
                  seb([(0, SEB_DISC[1]), (1.2, M('seb-m02-blase'))], x=0.62, y=0.94, h=0.47),
                  flamme(0.62, 0.94 - 0.47 * 0.96, 0.14, grandit=[(0.6, 1.0), (1.8, 0.0)])],
         postits=[(0.0, 0.01, 40, (0.04, 0.12, 0.96, 0.42), False, 21)],
         bruits=[(0.5, 'soupir')], horloge=[(0.0, 3.8, '03:05', 0.74)]),
    # 28. LA CHUTE : au lit ; Tara bâille et rentre dans le téléphone ; même Tara dort ; la lumière s'éteint
    Plan(7.6, CHAMBRE, cam=(0.58, 0.58), zoom=(1.10, 1.06), cam_y=0.55,
         acteurs=[Acteur('diana', DIA_N[3], x=0.40, y=0.505, h=0.25, ombre=False, poses=[(0, DIA_N[0]), (2.6, DIA_N[3])]),
                  tara(0.47, 0.40, 0.06, poses=[(0, TARA[0]), (0.6, TARA[3]), (2.2, TARA[1])], fin=3.4,
                       trajet=[(0, 0.47, 0.40, 1.0), (2.6, 0.47, 0.40, 1.0), (3.3, 0.40, 0.39, 0.08)]),
                  seb([(0, M('seb-m02-blase'))], x=0.56, y=0.94, h=0.47),
                  Acteur('kristina', KRI_N[1], x=0.81, y=0.95, h=0.46, poses=[(0, KRI_N[1]), (3.6, KRI_N[2]), (5.4, KRI_N[3])]),
                  Acteur('olympe', OLY[3], x=0.31, y=0.70, h=taille_animal(0.47, 0.25))],
         postits=[(0.0, 0.01, 40, (0.04, 0.12, 0.96, 0.42), False, 21)],
         repliques=[r('kristina', 0.2, "Au lit.", "Bed.", "A la cama."),
                    r('tara', 1.6, "Bonne nuit !", "Good night!", "¡Buenas noches!"),
                    r('kristina', 4.0, "Même Tara dort.", "Even Tara's asleep.", "Hasta Tara duerme.")],
         bruits=[(0.6, 'soupir'), (3.0, 'whoosh'), (3.3, 'pop'), (5.6, 'soupir')], noir=(6.2, 7.2), horloge=[(0.0, 6.2, '03:06', 0.74)]),
    # 29. Dans le noir : l'appel à l'abonnement est la blague, en grand, sur son bandeau
    Plan(4.4, CHAMBRE, cam=(0.56, 0.56), zoom=(1.06, 1.06), cam_y=0.55, noir=(0.0, 0.01),
         bandeaux=[(0.3, 4.0, L('Abonne-toi demain.', 'Subscribe tomorrow.', 'Suscríbete mañana.'),
                    L('Là, dodo.', 'Now, sleep.', 'Ahora, a dormir.'), 0.36, 1.25)],
         repliques=[r('kristina', 0.4, "Abonne-toi demain. Là, dodo.", "Subscribe tomorrow. Now, sleep.", "Suscríbete mañana. Ahora, a dormir.",
                      off=True, sous_titre=False)],
         bruits=[(0.3, 'pop')]),
    # 30. LA BOUCLE : 4 h 30, un œil s'ouvre, une petite idée
    gros_plan('seb', fige(ST[3]), NUIT, 3.6,
              [r('seb', 1.5, "Juste une petite idée…", "Just one tiny idea…", "Solo una ideíta…")],
              expression=[(0, ST[3]), (0.9, ST[1])], bruits=[(0.0, 'bip'), (1.2, 'whoosh')], horloge=[(0.0, 3.6, '04:30')],
              lumiere=(0.0, 0.5),
              extra=[flamme(0.5, 0.25, 0.12, debut=1.2, gros_plan=True, grandit=[(1.2, 0.3), (1.6, 1.0)])]),
]

caler(plans)
DUREE = sum(int(round(p.duree * FPS)) / FPS for p in plans)
assert 150 <= DUREE <= 179, f'durée {DUREE:.1f} s : un épisode fait de 2:30 à 2:59, jamais plus'

if __name__ == '__main__':
    os.makedirs('shorts', exist_ok=True)
    nom = f'shorts/EP01-{LANGUE}'
    if len(sys.argv) > 1 and sys.argv[1] == 'images':
        ks = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['0.1', '0.5', '0.9'])]
        from PIL import Image as _I
        ims = [dessiner_plan(p, p.duree * k) for p in plans for k in ks]
        w, h = 216, 384; cols = len(ks) * 3
        pl = _I.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)))
        for j, im in enumerate(ims):
            pl.paste(im.resize((w, h)), ((j % cols) * w, (j // cols) * h))
        pl.save(f'{nom}-cles.jpg', quality=85)
        print(f'{nom}-cles.jpg', round(DUREE, 1), 's')
    else:
        dossier = f'rendu-ep01-{LANGUE}'
        reve = None
        t0 = 0.0
        for p in plans:
            if p.fond == 'reve':
                reve = (t0, t0 + p.duree)
            t0 += int(round(p.duree * FPS)) / FPS
        video, t_total, sons = rendre(plans, nom + '.mp4', dossier=dossier)
        mixer(t_total, sons, reve, f'{dossier}/son.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', f'{dossier}/son.wav', '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', nom + '.tmp.mp4'], check=True)
        os.replace(nom + '.tmp.mp4', nom + '.mp4')
        ecrire_srt(plans, nom + '.srt')
        print(nom + '.mp4', round(t_total, 1), 's')
