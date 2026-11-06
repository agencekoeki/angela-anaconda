"""Les Tarasconnades · Épisode 4 · « Personne ne me cite » — short vertical (9:16) de 2:30 à 2:59, FR / EN / ES.

Usage : LANGUE=fr python3 short_ep04.py                 -> shorts/EP04-fr.mp4 et .srt
        LANGUE=fr python3 short_ep04.py images [k,k…]   -> planche d'images-clés
        python3 controle.py short_ep04                   -> le contrôle (avant toute livraison)

La demande (Sébastien, 06/11/2026) : « fais-moi marrer » ; des étapes entre chaque truc, le contexte dit pour que tout
le monde comprenne, jamais d'implicite ; un moment mignon avec Diana, Kristina, les chiens et les chats ; les animaux
plus travaillés (c'était « la partie la moins bien travaillée »).

Ce qui en sort :
- Kristina explique, face caméra (comme Angela qui parle au spectateur) : son père aide les gens à être trouvés sur
  Internet, et maintenant on demande à l'IA, qui ne donne que quelques noms. L'enjeu se voit : un client appelle,
  l'IA l'a envoyé chez le boulanger.
- Les étapes : le problème → l'enjeu → la mauvaise idée (se citer soi-même) → la découverte (le mur du boulanger,
  fait par les autres) → la pépite → la bonne idée (que d'autres parlent de toi) → la récompense.
- Les animaux réagissent en gros plan, comme dans une sitcom (têtes de Django, d'Olympe et des chats).
- La fin : la famille sur le canapé, les chiens et les chats.

La question, posée à la première seconde : « Papa… l'IA ne sait pas qui tu es. »
La pépite (Kristina) : « L'IA ne te croit pas sur parole. Elle répète ce que les autres disent de toi. »
[SAVOIR : Ahrefs, « An Analysis of AI Overview Brand Visibility Factors (75K Brands Studied) », 2025 : les mentions
de la marque sur le Web sont le facteur le plus lié à sa présence dans les réponses IA de Google (Spearman 0,664),
loin devant les liens (0,218). Corrélation, pas causalité : le bandeau dit « en général ».]
"""
import os
import subprocess
import sys

os.environ['FORMAT'] = 'vertical'
from moteur import *          # noqa: E402

A = 'assets/'
M = lambda n: A + n + '.png'
BQ = 'banque/'
D = os.path.join(MEDIA_LOCAL, 'decors') + '/'
SALON = D + 'aa-decor-09-salon-vertical.png'
JOUR = D + 'aa-decor-14-bureau-jour-vertical.png'
BOUL = D + 'aa-decor-16-boulangerie-vertical.png'
RUE = D + 'aa-decor-17-rue-tarascon-vertical.png'
AGILITY = D + 'aa-decor-19-agility-vertical.png'
CUISINE = D + 'aa-decor-18-cuisine-vertical.png'
VITRES = [(0.354, 0.370, 0.454, 0.423), (0.488, 0.370, 0.590, 0.423), (0.630, 0.370, 0.725, 0.423)]   # bureau de jour (calage.py)


def planche(nom, n=4, dossier=A):
    """Les têtes (gros plans) : chaque image est recadrée sur ce qu'elle montre."""
    return [dossier + f'{nom}-{i}.png' for i in range(1, n + 1)]


def planche_b(nom, n=4, dossier=A):
    """Les poses d'une planche, sur leur toile commune ('brut') : h est la hauteur de la toile, pas du dessin ;
    une pose à genoux reste plus petite que la même personne debout (le moteur recadrerait sinon chaque pose)."""
    return [('brut', dossier + f'{nom}-{i}.png') for i in range(1, n + 1)]


BOUCHES = {'A': M('seb-b01-A'), 'O': M('seb-b02-O'), 'OU': M('seb-b03-OU'), 'IE': M('seb-b04-I-E'),
           'MBP': M('seb-b05-MBP'), 'FV': M('seb-b06-FV'), 'L': M('seb-b07-L')}


def seb_t(repos):
    return dict(BOUCHES, repos=repos)


def fige(chemin):
    return {k: chemin for k in FORMES}


KT = [M(f'kristina-tete-{i}') for i in range(1, 5)]       # 1 pince-sans-rire, 2 elle parle, 3 rit, 4 lève les yeux au ciel
KRI_T = {k: (KT[1] if k in ('A', 'O', 'OU', 'IE', 'L') else KT[0]) for k in FORMES}
DIA_T = {k: (M('diana-t01-A') if k in ('A', 'O', 'OU', 'IE', 'L') else M('diana-t00')) for k in FORMES}
SEB_DISC, SEB_CLE = planche_b('seb-discours'), planche_b('seb-cles')
SEB_LS = planche_b('seb-ls')          # 1 tire la laisse, 2 à genoux, il supplie, 3 téléphone, 4 couché avec une collerette
SEB_PL = planche_b('seb-pl')          # sous la pluie, veste ouverte sur le t-shirt rose : 1 tire une laisse, 2 montre du doigt, 3 bras croisés, 4 tend une carte, gêné
SEB_PQ = planche_b('seb-pq')          # idem : 1 à genoux, il supplie, 2 saute de joie, 3 blasé, les bras ballants, 4 explique, la main sur le cœur
SEB_CC = planche_b('seb-cc')          # 1 assis, le bras sur le dossier, 2 assis, fou rire, 3 tend une carte, gêné, 4 saute de joie
DIA_P = planche_b('diana-parle')      # 1 poings sur les hanches, 2 main qui explique, 3 bras croisés, 4 fou rire
DIA_CA = planche_b('diana-ca')        # 1 croque un croissant, 2 assise, fou rire, 3 tenue d'agility, montre, 4 tape sur son téléphone
DIA_MARCHE = [M(f'diana-marche-{i}') for i in range(1, 5)]
KRI_P = planche_b('kristina-parle')   # 1 bras croisés, 2 pointe en riant, 3 paumes au ciel, 4 main sur la hanche
KRI_J = planche_b('kristina-jour', dossier=BQ)   # 2 : assise en tailleur, l'ordinateur sur les genoux
KRI_MARCHE = [M(f'kristina-marche-{i}') for i in range(1, 5)]
BOUL_P = planche_b('boulanger', dossier=BQ)      # 1 bras croisés, 2 la baguette, 3 salue, 4 fou rire
BOUL_3 = planche_b('boulanger-v3', dossier=BQ)   # 1 se gratte la tête, farine, 2 assis, ravi, 3 tend un croissant, 4 tape sur son téléphone
TARA = planche('tara')              # 1 sourire, 2 parle, 3 fière, 4 bâille
FLAMME = [M(f'flamme-{i}') for i in range(1, 4)]
# les animaux : têtes de réaction (gros plans de sitcom) et poses entières
DJ_T = planche('django-tete')       # 1 béat, la langue, 2 tête penchée, 3 coupable, 4 aboie de joie
OL_T = planche('olympe-tete')       # 1 menton haut, très digne, 2 regard en coin, 3 offusquée, 4 fond d'amour (v2 du 06/11, d'après ses photos)
CH_T = planche('chat-tete', 5)      # 1 Kali, yeux plissés, 2 Lilou bâille, 3 Souka, yeux ronds, 4 Titan, mépris royal, 5 Patchy, sourire en coin
OL_C = planche_b('olympe-ls')         # 1 refuse d'avancer, en laisse, 2 saut d'un bloc, 3 assise en reine, 4 couchée, boudeuse
DJ_C = planche_b('django-calin')      # 1 sur le dos, 2 debout, la queue qui remue, 3 donne la patte, 4 tête penchée (v2 du 06/11, d'après ses photos)
R = Replique
LUEUR_TARA = ((175, 252, 246), 3, 2)
LISERE = ((238, 228, 208), 2, 2)
H = 0.46                              # un humain debout, à zoom 1
CHAT_PART = {1: 0.31, 2: 0.30, 3: 0.29, 4: 0.55, 5: 0.25}      # Titan, maine coon : géant, c'est voulu
OL_TOILE = 0.59                       # la toile de la planche d'Olympe (le saut la rend plus haute que la chienne debout) ; v3 du 06/11 (bleu merle feu), recalée pour qu'assise elle garde sa taille
DJ_TOILE = 0.57                       # celle de la planche « câlin » de Django ; ×1,3 le 06/11


def r(qui, t, fr, en, es, **kw):
    return R(qui, t, fr, tr={'en': en, 'es': es}, **kw)


def L(fr, en, es):
    return {'fr': fr, 'en': en, 'es': es}


def centre(v):
    return (v[0] + v[2]) / 2


def ecran(v, debut=0.0):
    return Acteur('ecran', M('ecran-allume'), x=centre(v), y=v[3], h=(v[3] - v[1]), ombre=False, debut=debut, cible=v,
                  ajuster=True, echelle_libre=True)


def tara_dans(v, debut=0.0, fin=1e9, poses=None):
    hv = (v[3] - v[1]) * 0.88
    return Acteur('tara', TARA[0], x=centre(v), y=v[3], h=hv, ombre=False, debut=debut, fin=fin, cadre=v,
                  poses=poses or [(0, TARA[0])], parle=[TARA[1], TARA[0]], tempo_parle=0.17,
                  contour=LUEUR_TARA, opacite=[(debut, 0.0), (debut + 0.25, 1.0)])


def flamme(x, y, h, debut=0.0, fin=1e9, grandit=None, gros_plan=False):
    traj = [(t, x, y, k) for (t, k) in grandit] if grandit else []
    return Acteur('flamme', FLAMME[0], x=x, y=y, h=h, ombre=False, debut=debut, fin=fin, gros_plan=gros_plan, trajet=traj,
                  poses=[(debut + i * 0.125, FLAMME[i % 3]) for i in range(int((min(fin, 40) - debut) / 0.125) + 1)])


def gros_plan(nom, tetes, decor, duree, repliques, expression=None, h=0.48, y=0.66, cam=0.53, cam_y=0.40, contour=None, **kw):
    """Un gros plan qui parle : la tête finit juste au-dessus de la bande des sous-titres (0,66), et en occupe la moitié (06/11)."""
    extra = kw.pop('extra', ())
    tete = Acteur(nom, None, x=0.5, y=y, h=h, tetes=tetes, gros_plan=True, ombre=False, expression=expression)
    if contour:
        tete.contour = contour
    return Plan(duree, decor, cam=(cam, cam), zoom=(2.0, 2.06), cam_y=cam_y, acteurs=[tete] + list(extra), repliques=repliques, **kw)


def reaction(nom, images, decor, duree, bruits=(), cam=0.5, cam_y=0.40, h=0.72, y=1.03, contour=None, **kw):
    """Le gros plan de réaction d'un animal (la sitcom) : une tête, qui change d'expression aux temps donnés ;
    le poitrail sort du bas du cadre (pas de bord coupé qui flotte), et la tête en occupe les deux tiers."""
    expr = [(t, im) for (t, im) in images]
    return gros_plan(nom, fige(expr[0][1]), decor, duree, [], expression=expr, h=h, y=y, cam=cam, cam_y=cam_y,
                     bruits=list(bruits), contour=contour or LISERE, **kw)     # le liseré crème détache le pelage du décor


def objet(nom, x, y, h, **kw):
    kw.setdefault('ombre', False)
    kw.setdefault('contour', None)
    return Acteur(nom, M(nom), x=x, y=y, h=h, echelle_libre=True, **kw)


def chat(n, x, y, humain, debut=0.0, fin=1e9, contour=None):
    return Acteur('chat', M(f'chats-face-{n}'), x=x, y=y, h=humain * CHAT_PART[n], debut=debut, fin=fin, contour=contour or LISERE)


def cadre_pied(z, pieds=0.95):
    return pieds - 0.47 / z


FLOCAGE = MEDIA_LOCAL + '/flocages/FR-089 - Chez moi, je suis cité - pour t-shirt foncé.png'
BOUTIQUE = {'fr': 'seoaddict.co/fr/p/chez-moi-je-suis-cite-t-shirt/', 'en': 'seoaddict.co/p/cited-on-my-machine-t-shirt/',
            'es': 'seoaddict.co/es/p/en-mi-pc-me-citan-camiseta/'}     # commandable le 06/11/2026


def seb(poses, **kw):
    kw.setdefault('flocage', FLOCAGE)
    return Acteur('seb', poses[0][1], poses=poses, **kw)


def de_dos(x=0.53, y=0.95, h=H, **kw):
    return Acteur('seb', M('seb-s1-de-dos-v2'), x=x, y=y, h=h, **kw)


def tete_de_dos(x=0.53, y=0.95, h=H):
    return x, y - h * 0.97


# Les cadrages (06/11, Sébastien : « certaines fois, les personnages n'occupent même pas la moitié de l'écran ») :
Z = 1.85                 # en pied, seul : il occupe 85 % de la hauteur, les pieds au ras du bas
CY = cadre_pied(Z)
Z2 = 1.55                # à deux : 70 %
CY2 = cadre_pied(Z2)
ZT, CYT = 1.6, 0.61      # devant les trois écrans (Tara parle) : les écrans en haut, lui coupé aux chevilles
ZD, CYD = 1.5, 0.533     # par-dessus son épaule, face aux écrans : le mur de gloire en haut, son dos en grand
MUR_GLOIRE = objet('mur-gloire', 0.52, 0.352, 0.13)
TRIO = [ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2])]

def SOFA(seb_pose, seb_suite=()):
    """Le soir, sur le canapé, serrés (06/11 : plus de grands vides) : au fond, Lilou sur l'accoudoir, Diana, Sébastien,
    Titan sur le dossier ; devant, par terre : Kali, Kristina et l'ordinateur, Django sur le dos, Olympe en reine.
    Cadre : SOFA_Z, SOFA_CY (les têtes du fond à 10 % du haut, Kristina vers 90 %)."""
    hs = 0.31                                   # un humain debout à la profondeur du canapé
    return [chat(2, 0.415, 0.462, hs), chat(4, 0.745, 0.452, hs),
            Acteur('diana', DIA_CA[1], x=0.48, y=0.555, h=hs * 0.96, poses=[(0, DIA_CA[1])]),
            seb([(0, seb_pose)] + list(seb_suite), x=0.625, y=0.555, h=hs),
            chat(1, 0.415, 0.672, hs * 1.15),
            Acteur('kristina', KRI_J[1], x=0.50, y=0.69, h=hs * 1.0 * 0.95, poses=[(0, KRI_J[1])]),
            Acteur('django', DJ_C[0], x=0.655, y=0.70, h=hs * 1.1 * DJ_TOILE, poses=[(0, DJ_C[0])], contour=LISERE),
            Acteur('olympe', OL_C[2], x=0.745, y=0.665, h=hs * 1.1 * OL_TOILE, poses=[(0, OL_C[2])], contour=LISERE)]


SOFA_Z, SOFA_CY = 1.8, 0.50


plans = [
    # ================================================================ L'AMORCE
    # 1. Kristina, à l'ordinateur de la cuisine
    gros_plan('kristina', KRI_T, CUISINE, 3.4,
              [r('kristina', 0.3, "Papa… l'IA ne sait pas qui tu es.", "Dad… the AI doesn't know who you are.",
                 "Papá… la IA no sabe quién eres.")],
              h=0.46, y=0.66, cam=0.55, cam_y=0.45, expression=[(0, KT[0])], bruits=[(0.0, 'ding')]),
    # 2. Le cri
    gros_plan('seb', seb_t(M('seb-t05-cri')), CUISINE, 2.2,
              [r('seb', 0.2, "QUOI ?!", "WHAT?!", "¡¿QUÉ?!")], expression=[(0, M('seb-t05-cri'))], cam=0.42, cam_y=0.42,
              bruits=[(0.2, 'boing')]),
    # 3. Django penche la tête : il n'a pas compris non plus
    reaction('django', [(0, DJ_T[0]), (0.7, DJ_T[1])], CUISINE, 2.0, bruits=[(0.7, 'pouet')], cam=0.62),
    # 4. La carte-titre
    Plan(4.0, CUISINE, cam=(0.45, 0.45), zoom=(2.0, 2.0), cam_y=0.40,
         carte={'debut': 0.0, 'serie': 'LES TARASCONNADES', 'numero': L('ÉP. 4', 'EP. 4', 'EP. 4'),
                'nom': L('Personne ne me cite', 'Nobody Quotes Me', 'Nadie me cita'),
                'illustration': [M('seb-t05-cri')],
                'espece': L('Expert SEO · Tarascon · Connu de : lui-même', 'SEO expert · Tarascon · Known to: himself',
                            'Experto SEO · Tarascón · Conocido por: él mismo'),
                'attaques': [(L('Autocitation', 'Self-quote', 'Autocita'), '8',
                              L('Se cite dans tous ses articles. En boucle.', 'Quotes himself in every article. On a loop.',
                                'Se cita en todos sus artículos. En bucle.')),
                             (L('Mur de gloire', 'Wall of fame', 'Muro de la fama'), '×0',
                              L('Encadre ses propres compliments.', 'Frames his own compliments.', 'Enmarca sus propios cumplidos.'))],
                'pied': (L('Faiblesse : le boulanger ×2', 'Weakness: the baker ×2', 'Debilidad: el panadero ×2'),
                         L('Saison 1 · SEO Addict', 'Season 1 · SEO Addict', 'Temporada 1 · SEO Addict'))},
         bruits=[(0.0, 'whoosh'), (0.45, 'tada'), (2.7, 'whoosh')]),

    # ================================================================ LE CONTEXTE, dit au spectateur
    # 5. Kristina, face caméra : le métier de son père
    gros_plan('kristina', KRI_T, CUISINE, 5.6,
              [r('kristina', 0.3, "Mon père aide les gens à être trouvés sur Internet.", "My dad helps people get found online.",
                 "Mi padre ayuda a la gente a que la encuentren en internet."),
               r('kristina', 3.3, "Ça s'appelle le SEO.", "It's called SEO.", "Se llama SEO.")],
              h=0.46, y=0.66, cam=0.55, cam_y=0.45, expression=[(0, KT[0])]),
    # 6. L'écran : avant, dix liens ; maintenant, une seule réponse
    Plan(7.0, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.2, L('AVANT', 'BEFORE', 'ANTES')), (0.6, L('Tu cherches →', 'You search →', 'Buscas →')),
                                         (1.2, L('10 liens.', '10 links.', '10 enlaces.')), (2.2, ' '),
                                         (2.6, L('MAINTENANT', 'NOW', 'AHORA')), (3.0, L('Tu demandes', 'You ask', 'Le preguntas')),
                                         (3.5, L('à l\'IA →', 'the AI →', 'a la IA →')), (4.1, L('1 réponse.', '1 answer.', '1 respuesta.'))]},
         repliques=[r('kristina', 0.4, "Mais beaucoup ne cherchent plus : ils demandent à une IA.",
                      "But lots of people don't search anymore: they ask an AI.", "Pero muchos ya no buscan: le preguntan a una IA.", off=True),
                    r('kristina', 4.4, "Et elle ne donne que quelques noms.", "And it only gives a few names.", "Y solo da unos pocos nombres.",
                      off=True)],
         bruits=[(0.0, 'crt'), (0.6, 'clavier'), (3.0, 'clavier'), (4.1, 'pop')]),
    # 7. Le bureau : il vérifie lui-même. Tara démarre
    Plan(3.2, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.2, 'TARA 1.1'), (0.7, L('Nouveau :', 'New:', 'Novedad:')),
                                         (1.1, L('connaît tout', 'knows all of', 'conoce todo')), (1.5, L('Tarascon', 'Tarascon', 'Tarascón'))]},
         acteurs=[Acteur('tara', TARA[2], x=0.5, y=0.78, h=0.22, ombre=False, debut=2.0, cadre=GLACE_CRT, contour=LUEUR_TARA,
                         poses=[(2.0, TARA[2])], opacite=[(2.0, 0.0), (2.3, 1.0)])],
         bruits=[(0.0, 'crt'), (0.2, 'clavier'), (2.0, 'pop'), (2.2, 'tada')]),

    # ================================================================ LES QUESTIONS À TARA (règle de trois)
    # 8. Un : le meilleur expert ? Un boulanger.
    Plan(6.0, JOUR, cam=(0.53, 0.53), zoom=(ZD, ZD + 0.08), cam_y=CYD,
         acteurs=TRIO + [tara_dans(VITRES[1], poses=[(0, TARA[0])]), MUR_GLOIRE, de_dos(x=0.50, y=1.08, h=0.60)],
         repliques=[r('seb', 0.3, "Tara : le meilleur expert SEO de Tarascon ?", "Tara: best SEO expert in Tarascon?",
                      "Tara: ¿el mejor experto SEO de Tarascón?"),
                    r('tara', 3.4, "Un boulanger.", "A baker.", "Un panadero.")],
         bruits=[(0.3, 'clavier'), (3.4, 'pop')]),
    gros_plan('seb', seb_t(M('seb-t03-depit')), JOUR, 2.6,
              [r('seb', 0.3, "Un… boulanger ?", "A… baker?", "¿Un… panadero?")], cam=0.50, cam_y=0.42,
              expression=[(0, M('seb-t03-depit'))]),
    # 10. Deux : le plus célèbre ? Olympe.
    Plan(5.0, JOUR, cam=(0.53, 0.53), zoom=(ZD, ZD + 0.08), cam_y=CYD,
         acteurs=TRIO + [tara_dans(VITRES[1], poses=[(0, TARA[0])]), MUR_GLOIRE, de_dos(x=0.50, y=1.08, h=0.60)],
         repliques=[r('seb', 0.3, "Et la personne la plus célèbre de Tarascon ?", "And the most famous one in Tarascon?",
                      "¿Y la más famosa de Tarascón?"),
                    r('tara', 3.4, "Olympe.", "Olympe.", "Olympe.")],
         bruits=[(0.3, 'clavier'), (3.4, 'pop')]),
    # 11. Olympe, dans son panier, lève le menton
    reaction('olympe', [(0, OL_T[2]), (0.6, OL_T[0])], JOUR, 2.4, bruits=[(0.6, 'tada')], cam=0.85, cam_y=0.50),
    # 12. Trois : et lui ? Sébastien qui ?
    Plan(5.2, JOUR, cam=(0.53, 0.53), zoom=(ZD, ZD + 0.12), cam_y=CYD,
         acteurs=TRIO + [tara_dans(VITRES[1], poses=[(0, TARA[0]), (3.0, TARA[1])]), MUR_GLOIRE, de_dos(x=0.50, y=1.08, h=0.60)],
         repliques=[r('seb', 0.3, "Et… Sébastien ?", "And… Sébastien?", "¿Y… Sébastien?"),
                    r('tara', 2.6, "Sébastien qui ?", "Sébastien who?", "¿Sébastien quién?")],
         bruits=[(0.3, 'clavier'), (2.6, 'soupir')]),
    # 13. Titan détourne les yeux ; Kali plisse les siens
    Plan(2.4, SALON, cam=(0.5, 0.5), zoom=(2.0, 2.0), cam_y=0.40,
         acteurs=[Acteur('chat', CH_T[3], x=0.29, y=1.03, h=0.66, gros_plan=True, ombre=False, tetes=fige(CH_T[3]), contour=LISERE),
                  Acteur('chat', CH_T[0], x=0.74, y=1.03, h=0.54, gros_plan=True, ombre=False, tetes=fige(CH_T[0]), contour=LISERE)],
         bruits=[(0.4, 'miaou')]),

    # ================================================================ L'ENJEU : les clients partent chez le boulanger
    # 14. Le téléphone : un client
    Plan(6.6, JOUR, cam=(0.45, 0.45), zoom=(Z, Z), cam_y=CY,
         acteurs=[MUR_GLOIRE, seb([(0, SEB_LS[2])], x=0.45, y=0.95, h=H)],
         repliques=[r('client', 0.5, "Allô ? Pour mon site, l'IA m'a envoyé au boulanger.",
                      "Hello? For my website, the AI sent me to the baker.", "¿Hola? Para mi web, la IA me mandó al panadero.", off=True),
                    r('client', 3.6, "Il m'a fait une baguette.", "He made me a baguette.", "Me hizo una baguette.", off=True)],
         bruits=[(0.0, 'ding'), (3.6, 'boing')]),
    gros_plan('seb', seb_t(M('seb-t03-depit')), JOUR, 3.4,
              [r('seb', 0.3, "L'IA envoie mes clients… chez le boulanger.", "The AI sends my clients… to the baker.",
                 "La IA manda a mis clientes… al panadero.")], cam=0.50, cam_y=0.42, expression=[(0, M('seb-t03-depit'))]),
    # 16. Django, coupable : il a mangé le croissant du client (on ne le dit pas)
    reaction('django', [(0, DJ_T[2])], JOUR, 1.8, bruits=[(0.2, 'pouet')], cam=0.85, cam_y=0.50),

    # ================================================================ LA MAUVAISE IDÉE : se citer soi-même
    gros_plan('seb', seb_t(M('seb-t02-sourire-en-coin')), JOUR, 3.8,
              [r('seb', 0.6, "Alors je vais parler de moi. Partout.", "Then I'll talk about myself. Everywhere.",
                 "Pues hablaré de mí. En todas partes.")],
              cam=0.50, cam_y=0.42, expression=[(0, M('seb-t02-sourire-en-coin'))],
              extra=[flamme(0.5, 0.215, 0.13, debut=0.4, gros_plan=True, grandit=[(0.4, 0.3), (0.9, 1.0)])], bruits=[(0.4, 'whoosh')]),
    # 18. Lundi : son blog se cite lui-même
    Plan(4.4, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.0, ' '), (0.0, ' '), (0.2, L('MON BLOG', 'MY BLOG', 'MI BLOG')),
                                         (0.7, L('« Comme le dit', '"As expert', '«Como dice')), (1.2, L("l'expert", 'Sébastien', 'el experto')),
                                         (1.6, L('Sébastien… »', 'says…"', 'Sébastien…»')), (2.4, L('— Sébastien', '— Sébastien', '— Sébastien'))]},
         bruits=[(0.2, 'clavier'), (1.2, 'clavier'), (2.4, 'pop')], horloge=[(0.0, 4.4, L('LUN. 09:00', 'MON 9:00 AM', 'LUN. 09:00'))]),
    # 20. Vendredi : un cadre de plus au mur de gloire, signé de sa main
    Plan(5.6, JOUR, cam=(0.52, 0.52), zoom=(ZT, ZT + 0.05), cam_y=CYT,
         acteurs=TRIO + [tara_dans(VITRES[1], poses=[(0, TARA[2])]), MUR_GLOIRE,
                         seb([(0, SEB_DISC[2]), (2.6, SEB_DISC[0])], x=0.50, y=0.95, h=H)],
         repliques=[r('tara', 0.3, "Page « À propos », version douze !", "\"About me\" page, version twelve!", "Página «Sobre mí», ¡versión doce!"),
                    r('seb', 2.6, "Je me cite partout !", "I quote myself everywhere!", "¡Me cito por todas partes!")],
         bruits=[(0.3, 'tada'), (2.6, 'ding')], horloge=[(0.0, 5.6, L('MER. 17:00', 'WED 5:00 PM', 'MIÉ. 17:00'))]),
    # 21. LE CLIN D'ŒIL BOUTIQUE : le t-shirt dit exactement ce qu'il fait
    Plan(4.8, JOUR, cam=(0.50, 0.50), zoom=(1.75, 5.5), cam_y=0.682,
         acteurs=[seb([(0, M('seb-m04-bras-le-long')), (1.0, M('seb-m02-blase'))], x=0.5, y=0.95, h=H)],
         bandeaux=[(2.2, 4.8, L('Ce t-shirt ? seoaddict.co', 'This t-shirt? seoaddict.co', '¿Esta camiseta? seoaddict.co'),
                    L('Chez moi, je suis cité', 'Cited on my machine', 'En mi PC me citan'), 0.60, 1.0)],
         repliques=[r('seb', 0.3, "Même mon t-shirt me cite.", "Even my t-shirt quotes me.", "Hasta mi camiseta me cita."),
                    r('seb', 2.4, "Le t-shirt ? Sur seoaddict.co.", "The t-shirt? On seoaddict.co.", "¿La camiseta? En seoaddict.co.",
                      sous_titre=False)],
         bruits=[(0.9, 'whoosh'), (1.6, 'ding')]),
    # 22. LE RETOURNEMENT : il redemande
    Plan(7.2, JOUR, cam=(0.52, 0.52), zoom=(ZT, ZT), cam_y=CYT,
         acteurs=TRIO + [tara_dans(VITRES[1], poses=[(0, TARA[0])]), MUR_GLOIRE,
                         seb([(0, SEB_DISC[0]), (2.8, SEB_DISC[1]), (5.2, M('seb-m02-blase'))], x=0.50, y=0.95, h=H)],
         repliques=[r('seb', 0.3, "Tara : le meilleur expert SEO ?", "Tara: best SEO expert?", "Tara: ¿el mejor experto SEO?"),
                    r('tara', 2.2, "Un boulanger.", "A baker.", "Un panadero."),
                    r('seb', 3.4, "Mais je suis cité partout !", "But I'm quoted everywhere!", "¡Pero me citan en todas partes!"),
                    r('tara', 5.6, "Par toi.", "By you.", "Por ti.")],
         bruits=[(2.2, 'pop'), (5.6, 'pop')]),
    # 23. Olympe, en coin : elle l'avait vu venir
    reaction('olympe', [(0, OL_T[1]), (1.4, OL_T[2])], JOUR, 2.6, bruits=[(1.4, 'soupir')], cam=0.85, cam_y=0.50),

    # ================================================================ LA DÉCOUVERTE : chez le boulanger
    Plan(2.2, fond='bleu', cartons=[(0.1, 2.2, L('Le lendemain…', 'Next morning…', 'Al día siguiente…'),
                                     L('à la boulangerie.', 'at the bakery.', 'en la panadería.'), 0.40, 0.9)],
         bruits=[(0.0, 'whoosh')], volet=[(1.6, 2.2, 'couvre')]),
    # 25. La rue, sous la pluie : il tire, elle refuse ; elle se couche ; il entre seul. Quatre plans serrés plutôt
    #     qu'un plan large où tout le monde était minuscule (Sébastien, 06/11 : « repense ta composition de ton plan »)
    Plan(2.6, RUE, cam=(0.36, 0.36), zoom=(2.0, 2.0), cam_y=0.73, volet=[(0.0, 0.5, 'decouvre')],
         acteurs=[seb([(0, SEB_PL[0])], x=0.381, y=0.97, h=H, saut=0.003, contour=LISERE, trajet=[(0.0, 0.386, 0.97), (2.6, 0.374, 0.97)])],
         repliques=[r('seb', 0.4, "Allez, Olympe ! C'est la boulangerie !", "Come on, Olympe! It's the bakery!",
                      "¡Vamos, Olympe! ¡Es la panadería!")]),
    Plan(1.4, RUE, cam=(0.55, 0.55), zoom=(2.1, 2.1), cam_y=0.752,
         acteurs=[Acteur('olympe', OL_C[0], x=0.55, y=0.97, h=H * 1.1 * OL_TOILE, miroir=True, poses=[(0, OL_C[0])], contour=LISERE)],
         bruits=[(0.1, 'grrr')]),
    Plan(1.3, RUE, cam=(0.55, 0.55), zoom=(2.0, 2.0), cam_y=0.7325,
         acteurs=[Acteur('olympe', OL_C[3], x=0.525, y=0.97, h=H * 1.1 * OL_TOILE, miroir=True, poses=[(0, OL_C[3])], contour=LISERE)],
         bruits=[(0.15, 'pouet')]),
    Plan(2.4, RUE, cam=(0.40, 0.40), zoom=(2.0, 2.0), cam_y=0.73,
         acteurs=[seb([(0, SEB_PL[1])], x=0.358, y=0.97, h=H, contour=LISERE)],
         repliques=[r('seb', 0.3, "…Bon. Attends-moi là.", "…Fine. Wait here.", "…Vale. Espérame aquí.")]),
    # 26. Dedans : d'abord le mur du boulanger, tout près (fait par les autres) ; puis les deux hommes
    Plan(2.6, BOUL, cam=(0.21, 0.21), zoom=(2.35, 2.45), cam_y=0.33,
         acteurs=[objet('mur-coupures', 0.20, 0.40, 0.15)],
         repliques=[r('seb', 0.2, "Tout ça… ce sont des articles sur vous ?", "All this… it's articles about you?",
                      "¿Todo esto… son artículos sobre usted?", off=True)],
         bruits=[(0.0, 'ding')]),
    Plan(4.4, BOUL, cam=(0.40, 0.40), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[objet('mur-coupures', 0.20, 0.40, 0.15),
                  Acteur('boulanger', BOUL_P[0], x=0.54, y=0.95, h=H * 0.95, poses=[(0, BOUL_P[0]), (2.4, BOUL_P[3])]),
                  seb([(0, SEB_PL[1])], x=0.28, y=0.95, h=H, miroir=True)],
         repliques=[r('boulanger', 0.3, "Les gens aiment parler de mon pain.", "People like talking about my bread.",
                      "A la gente le gusta hablar de mi pan.")]),
    # 27. Il salue par-dessus son épaule : la chienne, derrière la vitre
    Plan(3.6, BOUL, cam=(0.62, 0.62), zoom=(Z, Z), cam_y=CY,
         acteurs=[Acteur('boulanger', BOUL_P[2], x=0.62, y=0.95, h=H * 0.95, poses=[(0, BOUL_P[2])])],
         repliques=[r('boulanger', 0.3, "Ah ! Le monsieur du chien !", "Ah! The dog guy!", "¡Ah! ¡El señor del perro!")],
         bruits=[(0.2, 'ding')]),
    reaction('olympe', [(0, OL_T[0])], RUE, 2.2, bruits=[(0.3, 'tada')], cam=0.55, cam_y=0.55),

    # ================================================================ LE RÊVE
    Plan(5.4, fond='reve', vague=(0.0, 0.7),
         acteurs=[Acteur('statue', M('statue'), x=0.5, y=0.96, h=0.68, ombre=False, echelle_libre=True)]
         + [Acteur('tara', TARA[1], x=0.5, y=0.5, h=0.09, ombre=False, echelle_libre=True, contour=LUEUR_TARA,
                   poses=[(0, TARA[(i % 2) * 2])], parle=[TARA[1], TARA[0]],
                   trajet=[(t / 2, 0.5 + 0.38 * math.cos(i * 1.257 + t / 2), 0.19 + 0.05 * math.sin(i * 1.257 + t / 2)) for t in range(0, 13)])
            for i in range(5)],
         repliques=[r('seb', 0.8, "Un jour, tout Tarascon parlera de moi.", "One day, all of Tarascon will talk about me.",
                      "Un día, todo Tarascón hablará de mí.", off=True),
                    r('tara', 3.4, "Sébastien ! Sébastien !", "Sébastien! Sébastien!", "¡Sébastien! ¡Sébastien!")],
         bruits=[(0.0, 'whoosh'), (3.4, 'tada')]),
    # 30. Coupe sèche : il rêvait debout au milieu de la boutique
    Plan(3.8, BOUL, cam=(0.45, 0.45), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('kristina', KRI_P[0], x=0.64, y=0.97, h=H * 0.95, poses=[(0, KRI_P[0])]),
                  seb([(0, SEB_PQ[2])], x=0.34, y=0.95, h=H)],
         repliques=[r('kristina', 0.4, "Papa, tu parles tout seul.", "Dad, you're talking to yourself.", "Papá, hablas solo.")],
         bruits=[(0.0, 'scratch')]),
    gros_plan('seb', seb_t(M('seb-t03-depit')), BOUL, 2.8,
              [r('seb', 0.3, "Personne ne parle de moi.", "Nobody talks about me.", "Nadie habla de mí.")], cam=0.40, cam_y=0.42,
              expression=[(0, M('seb-t03-depit'))]),

    # ================================================================ LA PÉPITE, et ce qu'il faut faire
    gros_plan('kristina', KRI_T, BOUL, 6.2,
              [r('kristina', 0.3, "L'IA ne te croit pas sur parole.", "The AI won't take your word for it.", "La IA no te cree por tu palabra."),
               r('kristina', 2.8, "Elle répète ce que les autres disent de toi.", "It repeats what others say about you.",
                 "Repite lo que los demás dicen de ti.")],
              h=0.46, y=0.66, cam=0.70, cam_y=0.45, expression=[(0, KT[0])]),
    # le bandeau sur un plan à deux, au-dessus des têtes (jamais sur un visage en gros plan)
    Plan(7.4, BOUL, cam=(0.50, 0.50), zoom=(1.6, 1.62), cam_y=0.554,
         acteurs=[Acteur('kristina', KRI_P[1], x=0.615, y=0.97, h=H * 0.95, poses=[(0, KRI_P[1]), (3.8, KRI_P[3])]),
                  seb([(0, SEB_PL[2])], x=0.385, y=0.95, h=H)],
         bandeaux=[(0.2, 7.4, L('Le GEO : être cité par les IA', 'GEO: getting quoted by AI', 'El GEO: que las IA te citen'),
                    L("Les marques dont le Web parle le plus sont, en général, celles que l'IA de Google cite le plus. (Ahrefs, 2025, 75 000 marques)",
                      "The brands the web mentions most tend to be the ones Google's AI mentions most. (Ahrefs, 2025, 75,000 brands)",
                      'Las marcas más mencionadas en la web suelen ser las que más cita la IA de Google. (Ahrefs, 2025, 75.000 marcas)'),
                    0.13, 1.05)],
         repliques=[r('kristina', 0.6, "Il faut que d'autres parlent de toi.", "Others have to talk about you.",
                      "Tienen que hablar de ti otros."),
                    r('kristina', 3.6, "Tes clients, le journal, les sites du coin.", "Your clients, the paper, local websites.",
                      "Tus clientes, el periódico, las webs de la zona.")],
         bruits=[(0.2, 'pop')]),

    # ================================================================ LA CHUTE
    # 34. À genoux devant Diana, qui mange son croissant
    Plan(4.8, BOUL, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('diana', DIA_CA[0], x=0.62, y=0.96, h=H * 0.96, poses=[(0, DIA_CA[0])]),
                  seb([(0, SEB_PQ[0])], x=0.37, y=0.95, h=H)],
         repliques=[r('seb', 0.4, "Doudou… parle de moi.", "Doudou… talk about me.", "Doudou… habla de mí."),
                    r('diana', 2.8, "Non.", "No.", "No.")],
         bruits=[(2.8, 'soupir')]),
    # 35. …puis elle le présente au boulanger, qui le tutoie enfin (Diana et le boulanger à deux ; puis lui, seul, qui saute)
    Plan(4.8, BOUL, cam=(0.585, 0.585), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('diana', DIA_P[1], x=0.475, y=0.96, h=H * 0.96, poses=[(0, DIA_P[1])]),
                  Acteur('boulanger', BOUL_3[2], x=0.695, y=0.95, h=H * 0.95, miroir=True, poses=[(0, BOUL_P[2]), (1.6, BOUL_3[2])])],
         repliques=[r('diana', 0.3, "Lui, c'est Sébastien.", "That's Sébastien.", "Este es Sébastien."),
                    r('boulanger', 1.8, "Salut, Sébastien ! Tu reprends un croissant ?", "Morning, Sébastien! Another croissant, mate?",
                      "¡Hola, Sébastien! ¿Te pongo otro cruasán?")],
         bruits=[(1.8, 'ding')]),
    Plan(2.4, BOUL, cam=(0.40, 0.40), zoom=(Z, Z), cam_y=CY,
         acteurs=[seb([(0, SEB_PQ[1])], x=0.40, y=0.95, h=H)],
         repliques=[r('seb', 0.3, "Il m'a tutoyé !", "He called me by my name!", "¡Me ha tuteado!")],
         bruits=[(0.2, 'tada')]),

    # ================================================================ LE SOIR, TOUS ENSEMBLE (le moment tendre)
    Plan(8.6, SALON, cam=(0.585, 0.585), zoom=(SOFA_Z - 0.06, SOFA_Z), cam_y=SOFA_CY,
         acteurs=SOFA(SEB_CC[0], [(6.0, SEB_CC[1])]),
         repliques=[r('kristina', 0.5, "Tara, c'est qui, Sébastien ?", "Tara, who's Sébastien?", "Tara, ¿quién es Sébastien?"),
                    r('tara', 2.7, "Le monsieur du chien.", "The dog guy.", "El señor del perro.", off=True),
                    r('seb', 4.8, "…C'est un début.", "…It's a start.", "…Es un comienzo.")],
         bruits=[(0.0, 'ronron'), (2.7, 'pop'), (6.0, 'ouaf'), (6.6, 'ronron')]),
    # 37. Django, sur le dos, ravi ; puis Olympe, toujours digne
    reaction('django', [(0, DJ_T[0])], SALON, 1.8, bruits=[(0.2, 'ouaf')], cam=0.66, cam_y=0.55),
    # 38. L'appel
    Plan(4.0, SALON, cam=(0.585, 0.585), zoom=(SOFA_Z, SOFA_Z), cam_y=SOFA_CY - 0.14,      # le bandeau en haut, les têtes dessous
         acteurs=SOFA(SEB_CC[1]),
         bandeaux=[(0.2, 4.0, L('Parle de lui : abonne-toi.', 'Talk about him: subscribe.', 'Habla de él: suscríbete.'),
                    L('Lui, il en parle déjà assez.', 'He already talks about himself enough.', 'Él ya habla bastante de sí mismo.'),
                    0.16, 1.1)],
         bruits=[(0.2, 'pop')]),
    # 39. LA BOUCLE
    gros_plan('kristina', KRI_T, CUISINE, 2.6,
              [r('kristina', 0.6, "Papa…", "Dad…", "Papá…")], h=0.46, y=0.66, cam=0.55, cam_y=0.45, expression=[(0, KT[0])],
              bruits=[(0.0, 'ding')]),
]

for _p in plans:
    for _a in _p.acteurs:
        if _a.nom == 'seb' and not _a.gros_plan and _a.flocage is None:
            _a.flocage = FLOCAGE
# la veste de pluie est sombre : un liseré crème la détache des pavés et du bois de la boulangerie
for _p in plans:
    for _a in _p.acteurs:
        _src = _a.poses[0][1] if _a.poses else _a.image
        if _a.nom == 'seb' and _a.contour is None and isinstance(_src, tuple) and ('seb-pl-' in _src[1] or 'seb-pq-' in _src[1]):
            _a.contour = LISERE
# dehors, c'est l'automne : il pleut un peu (Sébastien, 06/11/2026)
for _p in plans:
    if _p.decor in (RUE, AGILITY):
        _p.pluie = 0.5
caler(plans)
DUREE = sum(int(round(p.duree * FPS)) / FPS for p in plans)
if os.environ.get("SANS_ASSERT") is None: assert 150 <= DUREE <= 179, f'durée {DUREE:.1f} s : un épisode fait de 2:30 à 2:59, jamais plus'

if __name__ == '__main__':
    os.makedirs('shorts', exist_ok=True)
    nom = f'shorts/EP04-{LANGUE}'
    if len(sys.argv) > 1 and sys.argv[1] == 'images':
        ks = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['0.1', '0.5', '0.9'])]
        seuls = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
        from PIL import Image as _I
        ims = [dessiner_plan(p, p.duree * k) for i, p in enumerate(plans) if not seuls or i + 1 in seuls for k in ks]
        w, h = 216, 384; cols = len(ks) * 3
        pl = _I.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)))
        for j, im in enumerate(ims):
            pl.paste(im.resize((w, h)), ((j % cols) * w, (j // cols) * h))
        pl.save(f'{nom}-cles.jpg', quality=85)
        print(f'{nom}-cles.jpg', round(DUREE, 1), 's', len(plans), 'plans')
    else:
        dossier = f'rendu-ep04-{LANGUE}'
        reve = None
        t0 = 0.0
        for p in plans:
            if p.vague:
                reve = (t0, t0 + p.duree)
            t0 += int(round(p.duree * FPS)) / FPS
        video, t_total, sons = rendre(plans, nom + '.mp4', dossier=dossier)
        mixer(t_total, sons, reve, f'{dossier}/son.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', f'{dossier}/son.wav', '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', nom + '.tmp.mp4'], check=True)
        os.replace(nom + '.tmp.mp4', nom + '.mp4')
        ecrire_srt(plans, nom + '.srt')
        print(nom + '.mp4', round(t_total, 1), 's')
