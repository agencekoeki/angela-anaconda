"""Les Tarasconnades · Épisode 5 · « Olympe a plus d'avis que moi » — short vertical (9:16) de 2:30 à 2:59, FR / EN / ES.

Usage : LANGUE=fr python3 short_ep05.py                 -> shorts/EP05-fr.mp4 et .srt
        LANGUE=fr python3 short_ep05.py images [k,k…]   -> planche d'images-clés
        python3 controle.py short_ep05                   -> le contrôle (avant toute livraison)

La demande (Sébastien, 06/11/2026) : drôle, des étapes, le contexte dit (rien d'implicite), un moment mignon avec la
famille, les chiens et les chats, et les animaux plus travaillés.

Les étapes : le problème (2 avis contre 214 pour le club, qui parlent tous d'Olympe) → le contexte (Kristina explique
ce qu'est un avis et pourquoi on les compare) → les trois tricheries, chacune effacée, avec la règle dite en une phrase
(la famille n'est pas cliente ; un cadeau contre un avis ; des avis inventés) → ce que fait Diana (elle demande, elle
répond) → la pépite → il ose → la récompense → Titan, qui « laisse un avis ».

La pépite (Diana) : « Plus d'avis, de bonnes notes : ça peut te faire remonter. Mais ça se demande. »
[SAVOIR : Aide Fiche d'établissement Google, « Conseils pour améliorer votre classement local » (answer/7091) : « un
nombre élevé d'avis et des notes positives peuvent aider à améliorer le classement local » ; on conseille d'y répondre ;
on ne peut pas payer pour être mieux classé. Règlement des contenus Google Maps (answer/7400114) : interdits, le contenu
qui ne repose pas sur une expérience réelle, celui publié en échange d'un avantage, l'engagement artificiel. Google
fournit lui-même un lien et un QR code pour demander des avis (answer/16816815). Consultés le 30/10/2026.]
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
NUIT = D + 'aa-decor-12-bureau-nuit-vertical.png'
AGILITY = D + 'aa-decor-19-agility-vertical.png'
JOUR = D + 'aa-decor-14-bureau-jour-vertical.png'
BOUL = D + 'aa-decor-16-boulangerie-vertical.png'
RUE = D + 'aa-decor-17-rue-tarascon-vertical.png'
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
SEB_CC = planche_b('seb-cc')          # 1 assis, le bras sur le dossier, 2 assis, fou rire, 3 tend une carte, gêné, 4 saute de joie
DIA_P = planche_b('diana-parle')      # 1 poings sur les hanches, 2 main qui explique, 3 bras croisés, 4 fou rire
DIA_CA = planche_b('diana-ca')        # 1 croque un croissant, 2 assise, fou rire, 3 tenue d'agility, montre, 4 tape sur son téléphone
DIA_MARCHE = [M(f'diana-marche-{i}') for i in range(1, 5)]
KRI_P = planche_b('kristina-parle')   # 1 bras croisés, 2 pointe en riant, 3 paumes au ciel, 4 main sur la hanche
KRI_J = planche_b('kristina-jour', dossier=BQ)   # 2 : assise en tailleur, l'ordinateur sur les genoux
KRI_MARCHE = [M(f'kristina-marche-{i}') for i in range(1, 5)]
BOUL_P = planche_b('boulanger', dossier=BQ)      # 1 bras croisés, 2 la baguette, 3 salue, 4 fou rire
BOUL_3 = planche_b('boulanger-v3', dossier=BQ)   # 1 se gratte la tête, farine, 2 assis, ravi, 3 tend un croissant, 4 tape sur son téléphone
DJ_ASSIS = planche_b('django-assis')   # 1 langue, regard levé, 2 tête penchée, 3 penchée de l'autre côté, 4 aboie
TITAN = planche_b('titan')            # 1 assis en roi, 2 avachi, 3 marche fière, 4 bâille
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


def gros_plan(nom, tetes, decor, duree, repliques, expression=None, h=0.40, y=0.62, cam=0.53, cam_y=0.40, **kw):
    extra = kw.pop('extra', ())
    tete = Acteur(nom, None, x=0.5, y=y, h=h, tetes=tetes, gros_plan=True, ombre=False, expression=expression)
    return Plan(duree, decor, cam=(cam, cam), zoom=(2.0, 2.06), cam_y=cam_y, acteurs=[tete] + list(extra), repliques=repliques, **kw)


def reaction(nom, images, decor, duree, bruits=(), cam=0.5, cam_y=0.40, h=0.56, y=0.86, **kw):
    """Le gros plan de réaction d'un animal (la sitcom) : une tête, qui change d'expression aux temps donnés."""
    expr = [(t, im) for (t, im) in images]
    return gros_plan(nom, fige(expr[0][1]), decor, duree, [], expression=expr, h=h, y=y, cam=cam, cam_y=cam_y,
                     bruits=list(bruits), **kw)


def objet(nom, x, y, h, **kw):
    kw.setdefault('ombre', False)
    kw.setdefault('contour', None)
    return Acteur(nom, M(nom), x=x, y=y, h=h, echelle_libre=True, **kw)


def chat(n, x, y, humain, debut=0.0, fin=1e9, contour=None):
    return Acteur('chat', M(f'chats-face-{n}'), x=x, y=y, h=humain * CHAT_PART[n], debut=debut, fin=fin, contour=contour or LISERE)


def cadre_pied(z, pieds=0.95):
    return pieds - 0.47 / z


FLOCAGE = MEDIA_LOCAL + '/flocages/FR-030 - 4,9 étoiles (2 avis) - pour t-shirt foncé.png'


def seb(poses, **kw):
    kw.setdefault('flocage', FLOCAGE)
    return Acteur('seb', poses[0][1], poses=poses, **kw)


def de_dos(x=0.53, y=0.95, h=H, **kw):
    return Acteur('seb', M('seb-s1-de-dos-v2'), x=x, y=y, h=h, **kw)


def pouf(t, x=0.5, y=0.62, h=0.34):
    """Le faux avis part en fumée : trois images de fumée qui grossissent et s'effacent (dans un plan d'écran)."""
    return Acteur('fumee', M('fumee-1'), x=x, y=y, h=h, ombre=False, echelle_libre=True, debut=t, fin=t + 0.9,
                  poses=[(t, M('fumee-1')), (t + 0.3, M('fumee-2')), (t + 0.6, M('fumee-3'))],
                  opacite=[(t, 0.0), (t + 0.08, 1.0), (t + 0.6, 1.0), (t + 0.9, 0.0)])


def masque_texte(t, y0=0.38, y1=0.70):
    """La vitre vide (la même image que le fond) posée sur les lignes de l'avis supprimé, sous la fumée."""
    return Acteur('fumee', M('crt-vide'), x=0.5, y=1.0, h=1.0, ombre=False, echelle_libre=True, debut=t,
                  cadre=(0.10, y0, 0.90, y1))


def etoiles_qui_tombent(n=14, duree=6.0):
    import random as _r
    g = _r.Random(4)
    out = []
    for i in range(n):
        x = g.uniform(0.08, 0.92); t0 = g.uniform(0, duree - 1.5); v = g.uniform(0.35, 0.6)
        out.append(Acteur('etoile', M('etoile'), x=x, y=0.0, h=g.uniform(0.04, 0.07), ombre=False, echelle_libre=True,
                          debut=t0, trajet=[(t0, x, 0.0), (t0 + 1.0 / v, x + g.uniform(-0.05, 0.05), 1.05)], tourne=g.uniform(-90, 90)))
    return out


Z = 1.5
CY = cadre_pied(Z)
Z2 = 1.3
CY2 = cadre_pied(Z2)
TRIO = [ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2])]
PORTAIL = objet('portail-qr', 0.86, 0.97, 0.36)
ARDOISE = objet('ardoise-' + LANGUE, 0.22, 0.47, 0.13)

def SOFA(seb_pose, seb_suite=(), titan_marche=False, kristina=True):
    """Le soir, sur le canapé (même mise en place que l'ép. 4) : Diana, Sébastien ; Kristina par terre ; Django donne la
    patte, Olympe en reine ; Lilou sur le canapé, Kali sur le carrelage ; Titan sur l'accoudoir, ou qui arrive."""
    hs = 0.31
    titan = (Acteur('titan', TITAN[2], x=0.95, y=0.62, h=hs * 0.62, miroir=True, trajet=[(0.2, 1.0, 0.62), (1.8, 0.70, 0.60)],
                    poses=[(0, TITAN[2]), (1.8, TITAN[0])], contour=LISERE) if titan_marche else chat(4, 0.79, 0.452, hs))
    out = [chat(2, 0.34, 0.452, hs), titan,
           Acteur('diana', DIA_CA[1], x=0.45, y=0.555, h=hs * 0.96, poses=[(0, DIA_CA[1])]),
           seb([(0, seb_pose)] + list(seb_suite), x=0.63, y=0.555, h=hs),
           chat(1, 0.33, 0.66, hs * 1.15),
           Acteur('django', DJ_C[2], x=0.71, y=0.665, h=hs * 1.1 * DJ_TOILE, poses=[(0, DJ_C[2])]),
           Acteur('olympe', OL_C[2], x=0.86, y=0.65, h=hs * 1.1 * OL_TOILE, poses=[(0, OL_C[2])])]
    if kristina:
        out.append(Acteur('kristina', KRI_P[1], x=0.50, y=0.70, h=hs * 1.25 * 0.95, poses=[(0, KRI_P[1])]))
    return out


plans = [
    # ================================================================ L'AMORCE
    gros_plan('seb', seb_t(M('seb-t05-cri')), JOUR, 3.8,
              [r('seb', 0.3, "Deux avis. Et la chienne… 214 ?!", "Two reviews. And the dog… 214?!", "Dos reseñas. Y la perra… ¡¿214?!")],
              expression=[(0, M('seb-t05-cri'))], cam=0.50, cam_y=0.42, bruits=[(0.0, 'ding')],
              horloge=[(0.0, 3.8, L('SAM. 10:00', 'SAT 10:00 AM', 'SÁB. 10:00'))]),
    # 2. Olympe, dans son panier : elle le savait
    reaction('olympe', [(0, OL_T[1]), (1.0, OL_T[0])], JOUR, 2.4, bruits=[(1.0, 'tada')], cam=0.85, cam_y=0.50),
    # 3. La carte-titre
    Plan(4.0, JOUR, cam=(0.45, 0.45), zoom=(2.0, 2.0), cam_y=0.40,
         carte={'debut': 0.0, 'serie': 'LES TARASCONNADES', 'numero': L('ÉP. 5', 'EP. 5', 'EP. 5'),
                'nom': L("Olympe a plus d'avis que moi", 'My Dog Has More Reviews', 'Olympe tiene más reseñas'),
                'illustration': [OL_T[0]],
                'espece': L('Expert SEO · Tarascon · Note : 4,5 (2 avis)', 'SEO expert · Tarascon · Rating: 4.5 (2 reviews)',
                            'Experto SEO · Tarascón · Nota: 4,5 (2 reseñas)'),
                'attaques': [(L('Avec plaisir !', 'My pleasure!', '¡Un placer!'), L('0 avis', '0 reviews', '0 reseñas'),
                              L('Rend un client heureux. Oublie de demander.', 'Makes a client happy. Forgets to ask.',
                                'Hace feliz a un cliente. Se olvida de pedir.')),
                             (L('Rafraîchir', 'Refresh', 'Actualizar'), '03:12',
                              L('Recharge la page. Rien ne change.', 'Reloads the page. Nothing changes.', 'Recarga la página. Nada cambia.'))],
                'pied': (L('Faiblesse : Olympe ×214', 'Weakness: Olympe ×214', 'Debilidad: Olympe ×214'),
                         L('Saison 1 · SEO Addict', 'Season 1 · SEO Addict', 'Temporada 1 · SEO Addict'))},
         bruits=[(0.0, 'whoosh'), (0.45, 'tada'), (2.7, 'whoosh')]),

    # ================================================================ LE CONTEXTE
    gros_plan('kristina', KRI_T, JOUR, 7.2,
              [r('kristina', 0.3, "Les avis, ce sont les étoiles sous ton nom quand on te cherche.",
                 "Reviews are the stars under your name when people look you up.",
                 "Las reseñas son las estrellas bajo tu nombre cuando te buscan."),
               r('kristina', 4.4, "Les gens les comparent avant de choisir.", "People compare them before choosing.",
                 "La gente las compara antes de elegir.")],
              h=0.36, y=0.62, cam=0.30, cam_y=0.45, expression=[(0, KT[0])]),
    # 5. L'écran : les deux fiches
    Plan(5.6, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.2, L('EXPERT SEO', 'SEO EXPERT', 'EXPERTO SEO')), (0.6, L('Sébastien', 'Sébastien', 'Sébastien')),
                                         (1.0, L('★ 4,5 · 2 avis', '★ 4.5 · 2 reviews', '★ 4,5 · 2 reseñas')), (1.6, ' '),
                                         (2.2, L("CLUB D'AGILITY", 'AGILITY CLUB', 'CLUB DE AGILITY')),
                                         (2.6, L('★ 4,9 · 214 avis', '★ 4.9 · 214 rev.', '★ 4,9 · 214 res.'))]},
         repliques=[r('kristina', 2.4, "Le club d'agility de maman : deux cent quatorze.",
                      "Mum's agility club: two hundred and fourteen.", "El club de agility de mamá: doscientas catorce.", off=True)],
         bruits=[(0.0, 'crt'), (1.0, 'pop'), (2.6, 'boing')]),
    # 6. Diana : ils parlent tous d'Olympe
    Plan(5.6, JOUR, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('diana', DIA_CA[3], x=0.33, y=0.96, h=H * 0.96, poses=[(0, DIA_CA[3])]),
                  seb([(0, SEB_LS[2]), (3.0, M('seb-m02-blase'))], x=0.68, y=0.95, h=H)],
         repliques=[r('diana', 0.3, "Et presque tous les avis parlent d'Olympe.", "And nearly every review is about Olympe.",
                      "Y casi todas las reseñas hablan de Olympe."),
                    r('seb', 3.4, "Mais pourquoi ?!", "But why?!", "¡¿Pero por qué?!")],
         bruits=[(0.3, 'ding')]),
    # 7. Les avis
    Plan(5.0, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.2, '★★★★★'), (0.4, L('« La colley m\'a', '"The collie told', '«La collie me')),
                                         (0.8, L('  engueulé. »', '  me off."', '  echó la bronca.»')), (2.2, '★★★★★'),
                                         (2.4, L('« Elle m\'a fait', '"She bowed', '«Me hizo una')), (2.8, L('  la révérence. »', '  to me."', '  reverencia.»'))]},
         repliques=[r('diana', 0.6, "Inoubliable, il paraît.", "Unforgettable, apparently.", "Inolvidable, por lo visto.", off=True)],
         bruits=[(0.2, 'ding'), (2.2, 'ding')]),
    reaction('olympe', [(0, OL_T[2]), (1.2, OL_T[0])], JOUR, 2.4, bruits=[(0.2, 'grrr'), (1.2, 'tada')], cam=0.85, cam_y=0.50),
    # 9. Au club, elle ne fait rien
    Plan(4.0, AGILITY, cam=(0.45, 0.45), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('olympe', OL_C[3], x=0.60, y=0.82, h=H * 0.55 * OL_TOILE, poses=[(0, OL_C[3])]),
                  seb([(0, M('seb-m02-blase'))], x=0.25, y=0.95, h=H)],
         repliques=[r('seb', 0.3, "Elle ne fait rien ! Elle est couchée !", "She does nothing! She's lying down!",
                      "¡No hace nada! ¡Está tumbada!")],
         bruits=[(2.8, 'ding')]),
    gros_plan('seb', seb_t(M('seb-t02-sourire-en-coin')), JOUR, 3.6,
              [r('seb', 0.6, "Moi aussi, je vais avoir des avis.", "I'm getting reviews too.", "Yo también tendré reseñas.")],
              cam=0.50, cam_y=0.42, expression=[(0, M('seb-t02-sourire-en-coin'))],
              extra=[flamme(0.5, 0.25, 0.12, debut=0.4, gros_plan=True, grandit=[(0.4, 0.3), (0.9, 1.0)])], bruits=[(0.4, 'whoosh')]),

    # ================================================================ LES TROIS TRICHERIES
    # 11. Un : Doudou
    Plan(5.6, CUISINE, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('diana', DIA_P[2], x=0.33, y=0.96, h=H * 0.96, poses=[(0, DIA_P[2])]),
                  seb([(0, SEB_LS[2])], x=0.68, y=0.95, h=H)],
         repliques=[r('seb', 0.3, "Doudou, tu me mets cinq étoiles ?", "Doudou, give me five stars?", "Doudou, ¿me pones cinco estrellas?"),
                    r('diana', 2.8, "Je n'ai jamais été ta cliente.", "I've never been your client.", "Nunca he sido tu clienta.")]),
    Plan(4.6, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.1, L('NOUVEL AVIS', 'NEW REVIEW', 'NUEVA RESEÑA')), (0.4, '★★★★★'),
                                         (0.7, L('« Il est', '"He is', '«Es')), (1.0, L('  formidable. »', '  wonderful."', '  estupendo.»'))]},
         acteurs=[masque_texte(2.0, 0.17, 0.52), pouf(1.8, 0.5, 0.52, 0.36)],
         repliques=[r('kristina', 1.9, "La famille n'est pas cliente : faux avis, il saute.", "Family aren't clients: fake review, it's removed.",
                      "La familia no es clienta: reseña falsa, la quitan.", off=True)],
         bruits=[(0.4, 'pop'), (1.8, 'pouf')]),
    # 13. Deux : le croissant
    Plan(5.6, BOUL, cam=(0.36, 0.36), zoom=(1.25, 1.25), cam_y=cadre_pied(1.25),
         acteurs=[ARDOISE, Acteur('boulanger', BOUL_P[3], x=0.58, y=0.95, h=H * 0.95, poses=[(0, BOUL_P[0]), (2.8, BOUL_P[3])]),
                  seb([(0, SEB_CC[2])], x=0.20, y=0.95, h=H)],
         repliques=[r('seb', 0.3, "Un avis contre un croissant ?", "One review for one croissant?", "¿Una reseña por un cruasán?"),
                    r('boulanger', 2.8, "Il est gratuit, celui-là ?", "Is that one free?", "¿Y ese es gratis?")],
         bruits=[(2.8, 'boing')]),
    Plan(4.4, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.1, L('NOUVEL AVIS', 'NEW REVIEW', 'NUEVA RESEÑA')), (0.4, '★★★★★'),
                                         (0.7, L('« Bon croissant. »', '"Nice croissant."', '«Buen cruasán.»'))]},
         acteurs=[masque_texte(1.6, 0.17, 0.42), pouf(1.4, 0.5, 0.42, 0.36)],
         repliques=[r('kristina', 1.6, "Un avis contre un cadeau : interdit aussi.", "A review for a gift: also forbidden.",
                      "Una reseña a cambio de un regalo: también prohibido.", off=True)],
         bruits=[(0.4, 'pop'), (1.4, 'pouf')]),
    # 15. Trois : Tara
    Plan(5.0, JOUR, cam=(0.53, 0.53), zoom=(1.25, 1.25), cam_y=0.50,
         acteurs=TRIO + [tara_dans(VITRES[1], poses=[(0, TARA[0]), (2.6, TARA[1])]), de_dos()],
         repliques=[r('seb', 0.3, "Tara, écris-moi deux cents avis.", "Tara, write me two hundred reviews.", "Tara, escríbeme doscientas reseñas."),
                    r('tara', 2.4, "Non. Inventer, c'est interdit.", "No. Making them up is forbidden.", "No. Inventarlas está prohibido.")],
         bruits=[(2.4, 'pop')]),
    reaction('olympe', [(0, OL_T[2])], JOUR, 2.0, bruits=[(0.2, 'ouaf')], cam=0.85, cam_y=0.50),
    # 17. La nuit : il rafraîchit sa page
    Plan(4.4, NUIT, cam=(0.50, 0.50), zoom=(Z, Z), cam_y=CY,
         acteurs=TRIO + [seb([(0, SEB_LS[2])], x=0.42, y=0.95, h=H),
                         Acteur('django', DJ_C[0], x=0.68, y=0.96, h=H * 0.85 * DJ_TOILE, poses=[(0, DJ_C[0])])],
         repliques=[r('seb', 1.9, "…Toujours deux.", "…Still two.", "…Siguen siendo dos.")],
         bruits=[(0.5, 'pop'), (1.3, 'pop'), (1.9, 'soupir')], horloge=[(0.0, 4.4, '03:12')]),
    # 18. LE CLIN D'ŒIL BOUTIQUE
    Plan(4.8, NUIT, cam=(0.50, 0.50), zoom=(1.3, 5.5), cam_y=0.682,
         acteurs=[seb([(0, M('seb-m04-bras-le-long')), (1.0, M('seb-m02-blase'))], x=0.5, y=0.95, h=H)],
         bandeaux=[(2.2, 4.8, L('Ce t-shirt ? seoaddict.co', 'This t-shirt? seoaddict.co', '¿Esta camiseta? seoaddict.co'),
                    L('4,9 étoiles (2 avis)', '4.9 stars (2 reviews)', '4,9 estrellas (2 reseñas)'), 0.60, 1.0)],
         repliques=[r('seb', 0.3, "Même mon t-shirt a deux avis.", "Even my t-shirt has two reviews.", "Hasta mi camiseta tiene dos reseñas."),
                    r('seb', 2.4, "Le t-shirt ? Sur seoaddict.co.", "The t-shirt? On seoaddict.co.", "¿La camiseta? En seoaddict.co.",
                      sous_titre=False)],
         bruits=[(0.9, 'whoosh'), (1.6, 'ding')], horloge=[(0.0, 0.9, '03:13')]),

    # ================================================================ CE QUE FAIT DIANA
    Plan(2.2, fond='bleu', cartons=[(0.1, 2.2, L('Samedi…', 'Saturday…', 'El sábado…'),
                                     L("au club d'agility.", 'at the agility club.', 'en el club de agility.'), 0.40, 1.0)],
         bruits=[(0.0, 'whoosh')], volet=[(1.6, 2.2, 'couvre')]),
    # 20. Elle demande, et montre le code
    Plan(5.8, AGILITY, cam=(0.58, 0.58), zoom=(Z2, Z2), cam_y=CY2, volet=[(0.0, 0.5, 'decouvre')],
         acteurs=[PORTAIL, Acteur('olympe', OL_C[2], x=0.70, y=0.86, h=H * 0.85 * OL_TOILE, poses=[(0, OL_C[2])]),
                  Acteur('diana', DIA_CA[2], x=0.40, y=0.96, h=H * 0.96, poses=[(0, DIA_CA[2])])],
         repliques=[r('diana', 0.6, "Un petit avis pour Olympe ?", "A little review for Olympe?",
                      "¿Una reseñita para Olympe?"),
                    r('diana', 2.8, "Le code est là !", "The code's right here!", "¡El código está aquí!")],
         bruits=[(3.8, 'ding'), (4.6, 'ding')]),
    # 21. Elle répond à chacun ; derrière, Olympe saute la haie d'un bloc
    Plan(5.4, AGILITY, cam=(0.36, 0.36), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('olympe', OL_C[1], x=0.0, y=0.62, h=H * 0.62 * OL_TOILE, trajet=[(1.0, -0.1, 0.60), (2.6, 0.45, 0.60)], poses=[(0, OL_C[1])]),
                  Acteur('diana', DIA_CA[3], x=0.30, y=0.96, h=H * 0.96, poses=[(0, DIA_CA[3])]),
                  seb([(0, M('seb-m02-blase'))], x=0.62, y=0.95, h=H)],
         repliques=[r('diana', 0.3, "Merci d'être venus !", "Thanks for coming!", "¡Gracias por venir!"),
                    r('seb', 2.6, "C'est tout ?", "That's it?", "¿Eso es todo?"),
                    r('diana', 3.6, "Je demande. Je réponds.", "I ask. I reply.", "Pido. Respondo.")],
         bruits=[(1.0, 'boing'), (2.0, 'boing')]),
    # 22. Lui essaie : il n'ose pas
    Plan(5.4, AGILITY, cam=(0.55, 0.55), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[PORTAIL, Acteur('olympe', OL_C[3], x=0.66, y=0.84, h=H * 0.55 * OL_TOILE, poses=[(0, OL_C[3])]),
                  seb([(0, SEB_CC[2]), (3.4, M('seb-m04-bras-le-long'))], x=0.42, y=0.95, h=H)],
         repliques=[r('seb', 0.3, "Vous me… euh…", "Would you… er…", "Me… eh…"),
                    r('seb', 2.6, "…Belle journée !", "…Lovely day!", "…¡Buen día!")],
         bruits=[(2.4, 'pouet')]),
    reaction('olympe', [(0, OL_T[1]), (1.0, OL_T[2])], AGILITY, 2.4, bruits=[(1.0, 'soupir')], cam=0.70, cam_y=0.62),
    # 24. Le rêve : couché comme elle, sous une pluie d'étoiles
    Plan(5.0, fond='reve', vague=(0.0, 0.7),
         acteurs=etoiles_qui_tombent() + [
             Acteur('seb', SEB_LS[3], x=0.40, y=0.80, h=0.42, ombre=False, poses=[(0, SEB_LS[3])]),
             Acteur('olympe', OL_C[2], x=0.88, y=0.95, h=0.42 * 0.7 * OL_TOILE * 2.1, ombre=False, echelle_libre=True, poses=[(0, OL_C[2])])],
         repliques=[r('seb', 0.6, "Je ne fais rien… et on m'adore !", "I do nothing… and they adore me!", "No hago nada… ¡y me adoran!"),
                    r('olympe', 3.3, "Grrr…", "Grrr…", "Grrr…", off=True)],
         bruits=[(0.0, 'whoosh'), (3.3, 'grrr')]),
    # 25. Coupe sèche
    Plan(3.8, JOUR, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('kristina', KRI_P[0], x=0.68, y=0.97, h=H * 0.95, poses=[(0, KRI_P[0])]),
                  seb([(0, SEB_LS[2])], x=0.32, y=0.95, h=H)],
         repliques=[r('kristina', 0.3, "Papa. Tu en as demandé combien ?", "Dad. How many did you ask for?", "Papá. ¿Cuántas has pedido?")],
         bruits=[(0.0, 'scratch')]),
    gros_plan('seb', seb_t(M('seb-t03-depit')), JOUR, 3.0,
              [r('seb', 0.3, "…Zéro. Je n'ose pas.", "…None. I don't dare.", "…Ninguna. No me atrevo.")], cam=0.50, cam_y=0.42,
              expression=[(0, M('seb-t03-depit'))]),

    # ================================================================ LA PÉPITE
    gros_plan('diana', DIA_T, JOUR, 6.2,
              [r('diana', 0.3, "Plus d'avis, de bonnes notes : ça peut te faire remonter.", "More reviews, good ratings: that can lift you up.",
                 "Más reseñas, buenas notas: eso puede subirte."),
               r('diana', 3.9, "Mais ça se demande.", "But you have to ask.", "Pero hay que pedirlas.")],
              h=0.40, y=0.62, cam=0.32, cam_y=0.45),
    Plan(6.8, JOUR, cam=(0.50, 0.50), zoom=(1.2, 1.22), cam_y=cadre_pied(1.2),
         acteurs=[Acteur('diana', DIA_P[1], x=0.33, y=0.96, h=H * 0.96, poses=[(0, DIA_P[1])]),
                  seb([(0, M('seb-m02-blase'))], x=0.68, y=0.95, h=H)],
         bandeaux=[(0.2, 6.8, L('Le SEO local', 'Local SEO', 'El SEO local'),
                    L("Beaucoup d'avis et de bonnes notes peuvent aider le classement local (Google). Demander : oui. Acheter : non.",
                      'Many reviews and good ratings can help local ranking (Google). Asking: yes. Buying: no.',
                      'Muchas reseñas y buenas notas pueden ayudar al posicionamiento local (Google). Pedirlas: sí. Comprarlas: no.'),
                    0.13, 1.0)],
         repliques=[r('diana', 0.6, "Et tu réponds à chacun. Même aux grincheux.", "And you reply to each one. Even the grumpy ones.",
                      "Y respondes a cada una. Incluso a las gruñonas.")],
         bruits=[(0.2, 'pop')]),
    # 29. Il répète devant Django, qui penche la tête à chaque essai
    Plan(4.6, JOUR, cam=(0.52, 0.52), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[seb([(0, SEB_CC[2])], x=0.34, y=0.95, h=H),
                  Acteur('django', DJ_C[3], x=0.72, y=0.95, h=H * DJ_TOILE, poses=[(0, DJ_C[3])])],
         repliques=[r('seb', 0.3, "Tu me laisses un avis ?", "Leave me a review?", "¿Me dejas una reseña?"),
                    r('seb', 2.4, "…Un avis ?", "…A review?", "…¿Una reseña?")],
         bruits=[(1.4, 'pouet')]),
    # Django, en gros : il penche la tête, il ne comprend pas, il est ravi quand même
    reaction('django', [(0, DJ_T[1]), (1.0, DJ_T[0])], JOUR, 2.0, bruits=[(0.1, 'pouet')], cam=0.72, cam_y=0.50),

    # ================================================================ LA CHUTE
    Plan(6.4, JOUR, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('boulanger', BOUL_3[1], x=0.68, y=0.95, h=H * 0.95, poses=[(0, BOUL_3[1]), (1.6, BOUL_P[2])]),
                  seb([(0, M('seb-m04-bras-le-long')), (2.6, SEB_CC[2])], x=0.30, y=0.95, h=H)],
         repliques=[r('boulanger', 0.3, "Merci ! C'est parfait !", "Thanks! It's perfect!", "¡Gracias! ¡Es perfecto!"),
                    r('seb', 2.6, "Tu me laisses un avis ?", "Would you leave me a review?", "¿Me dejas una reseña?"),
                    r('boulanger', 4.4, "Avec plaisir !", "With pleasure!", "¡Con mucho gusto!")],
         bruits=[(4.4, 'tada')]),
    Plan(4.2, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.1, L('NOUVEL AVIS', 'NEW REVIEW', 'NUEVA RESEÑA')), (0.4, '★★★★★'),
                                         (0.7, L('« Très bon', '"Great expert.', '«Muy buen')), (1.0, L('  expert.', '  The dog', '  experto.')),
                                         (1.4, L('Il manquait', '  was missing."', 'Faltaba')), (1.7, L('  la chienne. »', ' ', '  la perra.»'))]},
         repliques=[r('seb', 2.0, "Merci ! La chienne te salue.", "Thanks! The dog says hi.", "¡Gracias! La perra te saluda.", off=True)],
         bruits=[(0.1, 'ding'), (2.0, 'clavier')]),

    # ================================================================ LE SOIR : Titan laisse un avis
    Plan(5.4, SALON, cam=(0.57, 0.57), zoom=(1.38, 1.44), cam_y=0.46,
         acteurs=SOFA(SEB_CC[0], [(2.6, M('seb-m02-blase'))], titan_marche=True, kristina=False),
         repliques=[r('seb', 2.6, "Titan ! Pas sur mon téléphone !", "Titan! Not on my phone!", "¡Titan! ¡En mi teléfono no!")],
         bruits=[(0.3, 'ronron'), (1.8, 'miaou'), (2.2, 'ding')]),
    Plan(4.2, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.1, L('NOUVEL AVIS', 'NEW REVIEW', 'NUEVA RESEÑA')), (0.4, '★'),
                                         (0.7, L('« Miaou. »', '"Meow."', '«Miau.»')), (1.0, '— Titan')]},
         acteurs=[masque_texte(2.0, 0.17, 0.48), pouf(1.8, 0.5, 0.48, 0.36)],
         repliques=[r('seb', 1.6, "Il n'a jamais été mon client !", "He's never been my client!", "¡Nunca ha sido mi cliente!", off=True)],
         bruits=[(0.4, 'pop'), (1.8, 'pouf')]),
    # 34. Toute la famille rit ; Olympe, elle, en est à 216
    Plan(5.6, SALON, cam=(0.57, 0.57), zoom=(1.38, 1.44), cam_y=0.46,
         acteurs=SOFA(SEB_CC[1]),
         repliques=[r('kristina', 0.3, "Trois avis, papa !", "Three reviews, dad!", "¡Tres reseñas, papá!"),
                    r('diana', 2.4, "Olympe : deux cent seize.", "Olympe: two hundred and sixteen.", "Olympe: doscientas dieciséis.")],
         bruits=[(0.3, 'tada'), (2.4, 'ding'), (3.0, 'ding')]),
    # 35. L'appel
    Plan(4.0, SALON, cam=(0.57, 0.57), zoom=(1.44, 1.44), cam_y=0.46,
         acteurs=SOFA(SEB_CC[1]),
         bandeaux=[(0.2, 4.0, L('Abonne-toi.', 'Subscribe.', 'Suscríbete.'),
                    L('Pas de croissant en échange : c\'est interdit.', 'No croissant in exchange: it\'s against the rules.',
                      'Sin cruasán a cambio: está prohibido.'), 0.16, 1.1)],
         bruits=[(0.2, 'pop')]),
    # 36. LA BOUCLE
    gros_plan('seb', seb_t(M('seb-t05-cri')), JOUR, 3.6,
              [r('seb', 0.3, "Trois avis. Et la chienne… 216 ?!", "Three reviews. And the dog… 216?!", "Tres reseñas. Y la perra… ¡¿216?!")],
              expression=[(0, M('seb-t05-cri'))], cam=0.50, cam_y=0.42, bruits=[(0.0, 'ding')],
              horloge=[(0.0, 3.6, L('SAM. 10:00', 'SAT 10:00 AM', 'SÁB. 10:00'))]),
]

for _p in plans:
    for _a in _p.acteurs:
        if _a.nom == 'seb' and not _a.gros_plan and _a.flocage is None:
            _a.flocage = FLOCAGE
# dehors, c'est l'automne : il pleut un peu (Sébastien, 06/11/2026)
for _p in plans:
    if _p.decor in (RUE, AGILITY):
        _p.pluie = 0.5
caler(plans)
DUREE = sum(int(round(p.duree * FPS)) / FPS for p in plans)
if os.environ.get("SANS_ASSERT") is None: assert 150 <= DUREE <= 179, f'durée {DUREE:.1f} s : un épisode fait de 2:30 à 2:59, jamais plus'

if __name__ == '__main__':
    os.makedirs('shorts', exist_ok=True)
    nom = f'shorts/EP05-{LANGUE}'
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
        dossier = f'rendu-ep05-{LANGUE}'
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
