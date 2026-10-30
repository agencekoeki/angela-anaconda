"""Les Tarasconnades · Épisode 2 · « Le nom parfait » — short vertical (9:16) de 2:30 à 2:59, FR / EN / ES.

Usage : LANGUE=fr python3 short_ep02.py                 -> shorts/EP02-fr.mp4 et .srt
        LANGUE=fr python3 short_ep02.py images [k,k…]   -> planche d'images-clés
        python3 controle.py short_ep02                   -> le contrôle (avant toute livraison)

Le concept : l'EMD (exact match domain), le nom de domaine qui reprend mot pour mot la requête.
L'histoire vraie : Le Pull Moche, la boutique de Sébastien et Diana (lepullmoche.shop).

La question, posée à la première seconde : « C'est quoi, ce truc ? » — « Notre meilleur nom de domaine. »
(Comment un pull peut-il être un nom de domaine, et est-ce le nom qui a fait le succès ?)
Le test des trois phrases :
1. Le jour de la Journée du pull moche 2016, Sébastien achète lepullmoche.shop, persuadé que le nom suffira à être premier.
2. Rien ne bouge (page 9, puis pire) ; Diana prend la main et remplit le site de pulls moches drôles, puis dessine le leur ;
   ça décolle (la télé, 1 159 visiteurs en même temps, 301 000 clics en six mois).
3. Aujourd'hui, Tara montre que les clics venaient de « pull de Noël », absent du nom ; et le .com, lui, a brûlé avec sa sauvegarde.
La pépite : un nom de domaine ne classe pas un site (depuis la mise à jour EMD de 2012, Google juge ce qu'il y a dedans).

Les faits (voir la fiche shorts/episodes/EP02-le-nom-parfait.md, chacun sourcé) :
- lepullmoche.shop et lepullmoche.com enregistrés le 16/12/2016 à 06:23:09 et 06:23:11 UTC (RDAP) = 07:23 à Paris,
  le 3e vendredi de décembre, la Journée internationale du pull moche ;
- 1 159 utilisateurs actifs en même temps (Analytics, temps réel, capture du 14/09/2019, soir de reportage télé) ;
- Search Console, 6 derniers mois au 05/02/2021 : 301 k clics, 3,94 M impressions ;
- Analytics (Search Console), 01/10/2020 → 23/01/2021 : « pull de noel » 44 518 clics, position 3,1 ;
  « pull moche » 3 942 clics, position 1,1 ;
- l'incendie du centre de données de l'hébergeur, mars 2021 : le .com et sa sauvegarde étaient au même endroit (Sébastien).

Installations et récompenses : « un nom de domaine » (0:03) → la boucle (fin) ; le .com acheté « au cas où » (0:20) → il brûle ;
« Le nom suffit » (0:28) → « pull de Noël » n'est même pas dans le nom ; la couronne du rêve → elle tombe ;
le t-shirt de Sébastien (Dernière sauvegarde : —) visible tout l'épisode → le clin d'œil après l'incendie.
"""
import os
import subprocess
import sys

os.environ['FORMAT'] = 'vertical'
from moteur import *          # noqa: E402

A = 'assets/'
M = lambda n: A + n + '.png'
C = 'captures/'                                   # les vraies captures (recadrées depuis media-local/recherche-pullmoche)
D = os.path.join(MEDIA_LOCAL, 'decors') + '/'
SALON = D + 'aa-decor-09-salon-vertical.png'
BUREAU1 = D + 'aa-decor-11-bureau-vertical.png'
NUIT = D + 'aa-decor-12-bureau-nuit-vertical.png'
JOUR = D + 'aa-decor-14-bureau-jour-vertical.png'
SERVEURS = D + 'aa-decor-21-salle-serveurs-vertical.png'


def planche(nom, n=4):
    return [('brut', A + f'{nom}-{i}.png') for i in range(1, n + 1)]


BOUCHES = {'A': M('seb-b01-A'), 'O': M('seb-b02-O'), 'OU': M('seb-b03-OU'), 'IE': M('seb-b04-I-E'),
           'MBP': M('seb-b05-MBP'), 'FV': M('seb-b06-FV'), 'L': M('seb-b07-L')}


def seb_t(repos):
    return dict(BOUCHES, repos=repos)


def fige(chemin):
    return {k: chemin for k in FORMES}


ST = [M(f'seb-tete-nuit-{i}') for i in range(1, 5)]       # 1 épuisé mais surexcité, 2 l'idée, 3 solennel, 4 endormi
KT = [M(f'kristina-tete-{i}') for i in range(1, 5)]       # 1 pince-sans-rire, 2 elle parle, 3 rit, 4 lève les yeux au ciel
KRI_T = {k: (KT[1] if k in ('A', 'O', 'OU', 'IE', 'L') else KT[0]) for k in FORMES}
SEB_DISC, SEB_CLE = planche('seb-discours'), planche('seb-cles')
SEB_PULL = planche('seb-pull')                  # 1 fier (pouces vers le renne), 2 victoire, 3 royal, 4 penaud
KRI_PULL = planche('kristina-pull')             # 1 tient le pull à bout de bras, 2 le pose contre elle, 3 le porte (pouce), 4 bras croisés, yeux au ciel
DIA_STY = planche('diana-styliste')             # 1 dessine, 2 montre le croquis, 3 « pousse-toi », 4 brandit le pull fini
DIA_P = planche('diana-parle')                  # 1 poings sur les hanches, 2 main qui explique, 3 bras croisés, 4 fou rire
DIA_MARCHE = [A + f'diana-marche-{i}.png' for i in range(1, 5)]
KRI_MARCHE = [A + f'kristina-marche-{i}.png' for i in range(1, 5)]
DJ_ASSIS = planche('django-assis')
DJ_SAUT = [A + f'django-saut-{i}.png' for i in range(1, 5)]
OLY_B = planche('olympe-bonjour')
TARA = planche('tara')                          # 1 sourire, 2 parle, 3 fière, 4 bâille
FLAMME = [M(f'flamme-{i}') for i in range(1, 4)]
R = Replique
LUEUR_TARA = ((175, 252, 246), 3, 2)


def taille_animal(humain, part, toile=1.0):
    return humain * part / toile


def r(qui, t, fr, en, es, **kw):
    return R(qui, t, fr, tr={'en': en, 'es': es}, **kw)


def L(fr, en, es):
    return {'fr': fr, 'en': en, 'es': es}


def flamme(x, y, h, debut=0.0, fin=1e9, grandit=None, gros_plan=False, graine=0):
    traj = [(t, x, y, k) for (t, k) in grandit] if grandit else []
    return Acteur('flamme', FLAMME[0], x=x, y=y, h=h, ombre=False, debut=debut, fin=fin, gros_plan=gros_plan, trajet=traj,
                  poses=[(debut + i * 0.125, FLAMME[(i + graine) % 3]) for i in range(int((min(fin, 40) - debut) / 0.125) + 1)])


def tara(x, y, h, debut=0.0, fin=1e9, poses=None, trajet=None):
    return Acteur('tara', TARA[0], x=x, y=y, h=h, ombre=False, debut=debut, fin=fin, poses=poses or [(0, TARA[0])],
                  parle=[TARA[1], TARA[0]], tempo_parle=0.17, contour=LUEUR_TARA, trajet=trajet or [])


def gros_plan(nom, tetes, decor, duree, repliques, expression=None, h=0.40, y=0.62, cam=0.53, cam_y=0.40, **kw):
    extra = kw.pop('extra', ())
    tete = Acteur(nom, None, x=0.5, y=y, h=h, tetes=tetes, gros_plan=True, ombre=False, expression=expression)
    return Plan(duree, decor, cam=(cam, cam), zoom=(2.0, 2.06), cam_y=cam_y, acteurs=[tete] + list(extra), repliques=repliques, **kw)


def capture(chemin, h, y=0.62, x=0.5, debut=0.0, fin=1e9, trajet=None):
    """Une vraie capture d'écran, posée sur la vitre bleu nuit de l'écran cathodique (fond='crt')."""
    return Acteur('capture', chemin, x=x, y=y, h=h, ombre=False, debut=debut, fin=fin, cadre=GLACE_CRT, echelle_libre=True,
                  opacite=[(debut, 0.0), (debut + 0.25, 1.0)], trajet=trajet or [])


def glose(t, en, es):
    """Une ligne d'écran qui traduit le mot-clé français (« pull moche » = ugly sweater), en anglais et en espagnol seulement :
    sans elle, on ne voit pas que le nom de domaine EST le mot-clé."""
    return [] if LANGUE == 'fr' else [(t, L('', en, es))]


def accessoire(nom, chemin, x, y, h, **kw):
    kw.setdefault('ombre', False)
    return Acteur(nom, chemin, x=x, y=y, h=h, echelle_libre=True, **kw)


# le flocage SEO Addict de l'épisode : « Dernière sauvegarde : — » (n° 197), qui récolte l'incendie
FLOCAGE = MEDIA_LOCAL + '/flocages/FR-197 - Dernière sauvegarde - pour t-shirt foncé.png'
BOUTIQUE = {'fr': 'seoaddict.co/fr/p/derniere-sauvegarde-t-shirt/', 'en': 'seoaddict.co/p/last-backup-t-shirt/',
            'es': 'seoaddict.co/es/p/ultima-copia-camiseta/'}


def seb(poses, **kw):
    kw.setdefault('flocage', FLOCAGE)
    return Acteur('seb', M('seb-m04-bras-le-long'), poses=poses, **kw)


def de_dos(x=0.53, y=0.93, h=0.45, **kw):
    return Acteur('seb', M('seb-s1-de-dos-v2'), x=x, y=y, h=h, **kw)


def tete_de_dos(x=0.53, y=0.93, h=0.45):
    return x, y - h * 0.97


def pulls_qui_volent(n=8, cy=0.40, rx=0.40, ry=0.21, h=0.085):
    """Le rêve : une ribambelle de pulls moches qui tournent (comme les Tara du rêve de l'épisode 1)."""
    out = []
    for k in range(n):
        traj = [(tt, 0.5 + rx * math.cos(2 * math.pi * (k / n + tt / 8)), cy + ry * math.sin(2 * math.pi * (k / n + tt / 8)))
                for tt in [i * 0.5 for i in range(14)]]
        out.append(accessoire('pull', M('pull-vole') if k % 2 else M('pull-objet'), traj[0][1], traj[0][2], h,
                              rot=(k * 37) % 40 - 20, tourne=25 if k % 2 else -25, trajet=traj))
    return out


TITRE = ('Les Tarasconnades', L('Ép. 2 · Le nom parfait', 'Ep. 2 · The perfect name', 'Ep. 2 · El nombre perfecto'))

plans = [
    # ---------------------------------------------------------------- L'AMORCE (0 s)
    # 1. Kristina sort un pull moche d'un carton, à bout de bras : la question
    Plan(3.4, SALON, cam=(0.52, 0.52), zoom=(1.40, 1.45), cam_y=0.63,
         acteurs=[accessoire('carton', M('carton'), 0.37, 0.96, 0.13),
                  Acteur('kristina', KRI_PULL[0], x=0.57, y=0.97, h=0.44, poses=[(0, KRI_PULL[0])])],
         repliques=[r('kristina', 0.3, "C'est quoi, ce truc ?", "What is this thing?", "¿Qué es esto?")],
         bruits=[(0.0, 'scratch')]),
    # 2. Sébastien, solennel
    gros_plan('seb', seb_t(M('seb-t02-sourire-en-coin')), SALON, 3.2,
              [r('seb', 0.3, "Ça ? Notre meilleur nom de domaine.", "That? Our best domain name.", "¿Eso? Nuestro mejor nombre de dominio.")],
              cam=0.40, cam_y=0.40, bruits=[(0.2, 'tada')]),
    # 3. La carte-titre
    Plan(4.0, SALON, cam=(0.45, 0.45), zoom=(2.0, 2.0), cam_y=0.40,
         carte={'debut': 0.0, 'serie': 'LES TARASCONNADES', 'numero': L('ÉP. 2', 'EP. 2', 'EP. 2'),
                'nom': L('Le nom parfait', 'The perfect name', 'El nombre perfecto'),
                'illustration': [M('pull-objet')],
                'espece': L('Nom de domaine · Tarascon · Taille : XXL moche', 'Domain name · Tarascon · Size: XXL ugly',
                            'Nombre de dominio · Tarascón · Talla: XXL fea'),
                'attaques': [(L('Nom exact', 'Exact name', 'Nombre exacto'), '×1',
                              L('Achète le mot-clé. Attend la gloire.', 'Buys the keyword. Waits for glory.',
                                'Compra la palabra clave. Espera la gloria.')),
                             (L('Mi-moche, mi-caustique', 'Half ugly, half snarky', 'Medio feo, medio mordaz'), '∞',
                              L("Vend un pull en disant de ne pas l'acheter.", "Sells a sweater by saying don't buy it.",
                                'Vende un jersey diciendo que no lo compres.'))],
                'pied': (L('Faiblesse : le même serveur', 'Weakness: the same server', 'Debilidad: el mismo servidor'),
                         L('Saison 1 · SEO Addict', 'Season 1 · SEO Addict', 'Temporada 1 · SEO Addict'))},
         bruits=[(0.0, 'whoosh'), (0.45, 'tada'), (2.7, 'whoosh')]),

    # ---------------------------------------------------------------- 2016 (le passé, en sépia)
    # 4. Le volet bleu : la date, et la fête du jour (vrai : le 3e vendredi de décembre)
    Plan(2.6, fond='bleu', cartons=[(0.1, 2.6, L('16 décembre 2016…', 'December 16, 2016…', '16 de diciembre de 2016…'),
                                     L('Journée du pull moche', 'Ugly Christmas Sweater Day', 'Día del jersey feo navideño'), 0.40, 1.0)],
         bruits=[(0.0, 'whoosh')], volet=[(2.0, 2.6, 'couvre')]),
    # 5. 7 h 23 : l'idée (« pull moche »… personne n'a le nom !)
    Plan(5.0, BUREAU1, cam=(0.52, 0.52), zoom=(1.25, 1.30), cam_y=0.52, souvenir=True, volet=[(0.0, 0.5, 'decouvre')],
         acteurs=[de_dos(), flamme(*tete_de_dos(), 0.07, debut=1.2, grandit=[(1.2, 0.3), (1.8, 1.2)])],
         repliques=[r('seb', 1.3, "« Pull moche »… personne n'a le nom !", "“Ugly sweater”… nobody has the name!",
                      "«Jersey feo»… ¡nadie tiene el nombre!")],
         bruits=[(0.4, 'clavier'), (1.2, 'whoosh')], horloge=[(0.0, 5.0, L('VEN. 07:23', 'FRI 7:23 AM', 'VIE. 07:23'))]),
    # 6. Plein écran : les deux noms achetés, à deux secondes d'écart (vrai, RDAP)
    Plan(5.4, fond='crt', souvenir=True,
         crt={'allume': 0.0, 'lignes': [(0.3, 'lepullmoche.shop')] + glose(0.6, '(= ugly sweater)', '(= jersey feo)') + [(0.9, L('✔ acheté 07:23:09', '✔ bought 07:23:09', '✔ pagado 07:23:09')),
                                         (2.4, 'lepullmoche.com'), (3.0, L('✔ acheté 07:23:11', '✔ bought 07:23:11', '✔ pagado 07:23:11'))]},
         repliques=[r('seb', 2.3, "Et le .com, au cas où.", "And the .com, just in case.", "Y el .com, por si acaso.", off=True)],
         bruits=[(0.3, 'clavier'), (0.9, 'tada'), (2.4, 'clavier'), (3.0, 'pop')]),
    # 7. Diana arrive : sa théorie
    Plan(8.4, BUREAU1, cam=(0.46, 0.46), zoom=(1.05, 1.08), cam_y=0.55, souvenir=True,
         acteurs=[seb([(0, SEB_DISC[1]), (5.4, SEB_DISC[0])], x=0.62, y=0.93, h=0.46),
                  flamme(0.62, 0.93 - 0.46 * 0.96, 0.07, grandit=[(0, 1.2), (8.0, 1.6)]),
                  Acteur('diana', M('diana-m00'), x=0.27, y=0.97, h=0.45, marche=DIA_MARCHE, poses=[(0, DIA_P[1]), (5.6, DIA_P[2])],
                         trajet=[(0.0, -0.15, 0.97), (1.0, 0.27, 0.97)])],
         repliques=[r('seb', 1.1, "Le nom, c'est le mot-clé !", "The name IS the keyword!", "¡El nombre ES la palabra clave!"),
                    r('seb', 2.9, "On sera premiers demain.", "We'll be number one tomorrow.", "Mañana seremos los primeros."),
                    r('diana', 4.6, "Et dedans, on met quoi ?", "And what goes inside?", "¿Y dentro qué ponemos?"),
                    r('seb', 6.4, "Rien. Le nom suffit.", "Nothing. The name is enough.", "Nada. Basta con el nombre.")],
         bruits=[(1.1, 'tada'), (6.4, 'boing')]),

    # ---------------------------------------------------------------- LES TENTATIVES (règle de trois)
    # 8. Lundi : page 9
    Plan(3.4, fond='crt', souvenir=True,
         crt={'allume': 0.0, 'lignes': [(0.0, ' '), (0.0, ' '), (0.1, '« pull moche »'), (0.6, L('nous :', 'us:', 'nosotros:')), (1.0, L('page 9', 'page 9', 'página 9'))]},
         repliques=[r('seb', 1.6, "Normal. Demain.", "It's fine. Tomorrow.", "Normal. Mañana.", off=True)],
         bruits=[(0.1, 'clavier')], horloge=[(0.0, 3.4, L('LUN. 09:00', 'MON 9:00 AM', 'LUN. 09:00'))]),
    # 9. Mercredi : page 9
    Plan(3.0, fond='crt', souvenir=True,
         crt={'allume': 0.0, 'lignes': [(0.0, ' '), (0.0, ' '), (0.1, '« pull moche »'), (0.4, L('nous :', 'us:', 'nosotros:')), (0.7, L('page 9', 'page 9', 'página 9'))]},
         repliques=[r('seb', 1.2, "Demain !", "Tomorrow!", "¡Mañana!", off=True)],
         bruits=[(0.1, 'clavier')], horloge=[(0.0, 3.0, L('MER. 09:00', 'WED 9:00 AM', 'MIÉ. 09:00'))]),
    # 10. Vendredi : la troisième fois casse le motif — il recule
    Plan(3.4, fond='crt', souvenir=True,
         crt={'allume': 0.0, 'lignes': [(0.0, ' '), (0.0, ' '), (0.1, '« pull moche »'), (0.4, L('nous :', 'us:', 'nosotros:')), (0.7, L('page 12', 'page 12', 'página 12'))]},
         repliques=[r('seb', 1.3, "Il… recule ?!", "It's… going down?!", "¿¡Está… bajando!?", off=True)],
         bruits=[(0.1, 'clavier'), (1.2, 'pouet')], horloge=[(0.0, 3.4, L('VEN. 09:00', 'FRI 9:00 AM', 'VIE. 09:00'))]),
    # 11. Sébastien, en dépit
    gros_plan('seb', seb_t(M('seb-t03-depit')), BUREAU1, 2.8,
              [r('seb', 0.3, "Mais… on a le nom.", "But… we have the name.", "Pero… tenemos el nombre.")],
              cam=0.52, cam_y=0.42, souvenir=True, bruits=[(0.2, 'soupir')]),

    # ---------------------------------------------------------------- LE RETOURNEMENT : Diana prend la main
    # 12. « Pousse-toi. » Diana s'installe
    Plan(6.4, BUREAU1, cam=(0.48, 0.48), zoom=(1.05, 1.08), cam_y=0.55, souvenir=True,
         acteurs=[Acteur('diana', DIA_STY[2], x=0.36, y=0.97, h=0.46, poses=[(0, DIA_STY[2]), (3.4, DIA_STY[0])]),
                  seb([(0, M('seb-m02-blase'))], x=0.68, y=0.93, h=0.46,
                      trajet=[(0.0, 0.62, 0.93), (1.6, 0.62, 0.93), (2.4, 0.75, 0.94)])],
         repliques=[r('diana', 0.4, "Pousse-toi.", "Move over.", "Aparta."),
                    r('diana', 2.6, "Un site, ça se remplit.", "A website needs filling.", "Una web hay que llenarla."),
                    r('diana', 4.5, "De vrais pulls moches.", "With real ugly sweaters.", "Con jerséis feos de verdad.")],
         bruits=[(0.4, 'whoosh'), (3.4, 'clavier')]),
    # 13. Ce qu'elle écrit : vendre en disant de ne pas acheter (le vrai ton du site)
    Plan(5.6, fond='crt', souvenir=True,
         crt={'allume': 0.0, 'lignes': [(0.2, L("« N'achetez pas", '“Do not buy', '«No compres')), (0.8, L(' ce pull. »', ' this sweater.”', ' este jersey.»'))]},
         acteurs=[accessoire('pull', M('pull-objet'), 0.5, 0.62, 0.22)],
         repliques=[r('seb', 2.0, "On vend… en disant de ne pas acheter ?", "We sell… by saying don't buy?", "¿Vendemos… diciendo que no compren?", off=True),
                    r('diana', 4.0, "Mi-moche, mi-caustique.", "Half ugly, half snarky.", "Medio feo, medio mordaz.", off=True)],
         bruits=[(0.2, 'clavier'), (4.0, 'pop')]),
    # 14. Des semaines de nuits : les post-it, les deux flammes
    Plan(5.2, NUIT, cam=(0.52, 0.52), zoom=(1.15, 1.18), cam_y=0.52, souvenir=True,
         acteurs=[Acteur('diana', DIA_STY[0], x=0.30, y=0.96, h=0.45, poses=[(0, DIA_STY[0])]),
                  de_dos(x=0.64), flamme(*tete_de_dos(x=0.64), 0.07, grandit=[(0, 1.0), (5.0, 1.8)])],
         postits=[(0.6, 4.6, 24, (0.06, 0.14, 0.94, 0.42), False, 31)],
         repliques=[r('diana', 0.8, "Une blague par pull.", "One joke per sweater.", "Un chiste por jersey.")],
         bruits=[(0.6, 'clavier'), (3.0, 'clavier')], horloge=[(0.0, 5.2, '03:00')], volet=[(4.6, 5.2, 'couvre')]),

    # ---------------------------------------------------------------- ÇA DÉCOLLE (les vraies captures)
    # 15. Le volet : un soir de 2019, la télé
    Plan(2.2, fond='bleu', cartons=[(0.1, 2.2, L('En 2019…', 'In 2019…', 'En 2019…'),
                                     L('un reportage à la télé', 'a TV report', 'un reportaje en la tele'), 0.40, 1.0)],
         bruits=[(0.0, 'whoosh')]),
    # 16. Le compteur en temps réel (vraie capture)
    Plan(5.4, fond='crt', souvenir=True,
         crt={'allume': 0.0, 'lignes': [(0.2, L('Sur le site,', 'On the site,', 'En la web,')), (0.7, L('en ce moment :', 'right now:', 'ahora mismo:'))]},
         acteurs=[capture(C + 'temps-reel-1159.png', 0.25, y=0.62, debut=1.2)],
         repliques=[r('seb', 2.4, "1 159. En même temps !", "1,159. All at once!", "1.159. ¡A la vez!", off=True)],
         bruits=[(1.2, 'pop'), (2.3, 'tada')]),
    # 17. Seb et Diana sautent de joie, Django aussi
    Plan(4.0, JOUR, cam=(0.50, 0.50), zoom=(1.0, 1.0), cam_y=0.55, souvenir=True,
         acteurs=[seb([(0, SEB_CLE[2])], x=0.66, y=0.93, h=0.46, trajet=[(0, 0.66, 0.93), (0.4, 0.66, 0.90), (0.8, 0.66, 0.93), (1.2, 0.66, 0.90), (1.6, 0.66, 0.93)]),
                  Acteur('diana', DIA_P[3], x=0.32, y=0.97, h=0.45, poses=[(0, DIA_P[3])]),
                  Acteur('django', DJ_SAUT[1], x=0.48, y=0.99, h=0.21, poses=[(0, ('brut', DJ_SAUT[1])), (0.5, ('brut', DJ_SAUT[2])), (1.0, ('brut', DJ_SAUT[3]))])],
         repliques=[r('diana', 1.6, "Et maintenant, notre pull à nous.", "And now, our very own sweater.", "Y ahora, nuestro propio jersey.")],
         bruits=[(0.0, 'tada'), (0.6, 'ouaf'), (1.0, 'boing')]),
    # 18. Diana dessine le leur (sa mère était couturière)
    Plan(5.8, JOUR, cam=(0.42, 0.42), zoom=(1.20, 1.24), cam_y=0.62, souvenir=True,
         acteurs=[Acteur('diana', DIA_STY[0], x=0.40, y=0.97, h=0.46, poses=[(0, DIA_STY[0]), (2.2, DIA_STY[1]), (4.0, DIA_STY[3])])],
         repliques=[r('diana', 0.4, "Ma mère cousait.", "My mother was a seamstress.", "Mi madre era costurera."),
                    r('diana', 2.4, "Moi, je dessine.", "I design.", "Yo diseño.")],
         bruits=[(0.2, 'clavier'), (2.2, 'pop'), (4.0, 'tada')]),
    # 19. Le vrai pull (photo), puis en tête de la recherche (vraie capture)
    Plan(6.0, fond='crt', souvenir=True,
         acteurs=[capture(C + 'photo-vrai-pull.png', 0.34, y=0.60, debut=0.2, fin=3.0),
                  Acteur('capture', C + 'choix-amazon.png', x=0.5, y=0.63, h=0.47, ombre=False, cadre=GLACE_CRT, echelle_libre=True,
                         debut=3.0, opacite=[(3.0, 0.0), (3.3, 1.0)])],
         repliques=[r('seb', 0.6, "Le vrai. Il existe.", "The real one. It exists.", "El de verdad. Existe.", off=True),
                    r('seb', 3.4, "Et il se vend !", "And it sells!", "¡Y se vende!", off=True)],
         bruits=[(0.2, 'pop'), (3.0, 'pop'), (3.4, 'tada')]),
    # 20. Search Console, six mois : 301 000 clics (vraie capture)
    Plan(5.4, fond='crt', souvenir=True,
         crt={'allume': 0.0, 'lignes': [(0.1, L('6 mois :', '6 months:', '6 meses:')), (0.5, L('301 k clics', '301k clicks', '301 k clics'))]},
         acteurs=[capture(C + 'sc-performances.png', 0.19, y=0.62, debut=1.0)],
         repliques=[r('seb', 2.0, "Tu vois ? C'est le nom !", "See? It's the name!", "¿Ves? ¡Es el nombre!", off=True)],
         bruits=[(1.0, 'pop'), (2.0, 'tada')]),

    # ---------------------------------------------------------------- LE RÊVE : le roi du pull moche
    Plan(6.2, fond='reve', vague=(0.0, 0.7),
         acteurs=pulls_qui_volent()
                 + [Acteur('seb', SEB_PULL[2], x=0.5, y=0.70, h=0.40, poses=[(0, SEB_PULL[2]), (3.0, SEB_PULL[1])], ombre=False),
                    accessoire('couronne', M('couronne'), 0.5, 0.315, 0.06, rot=-8, tourne=0,
                               trajet=[(0.0, 0.5, 0.315), (4.8, 0.5, 0.315), (6.2, 0.62, 0.95)])],
         repliques=[r('seb', 0.9, "Le roi du pull moche !", "The king of ugly sweaters!", "¡El rey del jersey feo!"),
                    r('seb', 3.4, "Et tout ça, grâce au nom !", "And all thanks to the name!", "¡Y todo gracias al nombre!")],
         bruits=[(0.0, 'whoosh'), (3.0, 'tada')]),

    # ---------------------------------------------------------------- AUJOURD'HUI : la pépite
    # 22. Coupe sèche : le salon, Kristina essaie le pull contre elle, Tara sur la table basse
    Plan(6.4, SALON, cam=(0.52, 0.52), zoom=(1.12, 1.12), cam_y=0.55,
         cartons=[(0.0, 1.8, L("Aujourd'hui", 'Today', 'Hoy'), None, 0.30, 1.0)],
         acteurs=[tara(0.52, 0.555, 0.06, poses=[(0, TARA[0]), (2.6, TARA[2])]),
                  Acteur('kristina', KRI_PULL[1], x=0.74, y=0.97, h=0.45, poses=[(0, KRI_PULL[1])]),
                  seb([(0, SEB_DISC[0])], x=0.34, y=0.94, h=0.46)],
         repliques=[r('kristina', 0.3, "Donc c'est le nom qui a tout fait ?", "So the name did everything?", "¿Así que el nombre lo hizo todo?"),
                    r('tara', 3.0, "Le nom ? Regarde.", "The name? Look.", "¿El nombre? Mira.")],
         bruits=[(0.0, 'scratch'), (3.0, 'pop')]),
    # 23. Ce que Tara montre (vrais chiffres, Search Console, hiver 2020)
    Plan(6.4, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.0, L('IA de la maison :', 'House AI:', 'IA de casa:')), (0.4, '« pull moche »')]
                                        + glose(0.6, '(ugly sweater)', '(jersey feo)') + [(0.9, L('  3 942 clics', '  3,942 clicks', '  3.942 clics')),
                                         (2.4, '« pull de noel »')] + glose(2.6, '(Xmas sweater)', '(jersey Navidad)') + [
                                         (2.9, L(' 44 518 clics', ' 44,518 clicks', ' 44.518 clics'))]},
         repliques=[r('tara', 3.6, "Et « pull de Noël » n'est pas dans le nom.", "And “Christmas sweater” isn't in the name.",
                      "Y «jersey de Navidad» no está en el nombre.")],
         bruits=[(0.2, 'clavier'), (2.4, 'clavier'), (3.6, 'pop')]),
    # 24. LA PÉPITE : Kristina la dit, le bandeau l'écrit
    gros_plan('kristina', KRI_T, SALON, 8.6,
              [r('kristina', 0.3, "Un nom ne classe pas un site.", "A name doesn't rank a site.", "Un nombre no posiciona una web."),
               r('kristina', 2.9, "C'est dedans qui compte.", "What's inside does.", "Lo que cuenta es lo de dentro.")],
              h=0.36, y=0.62, cam=0.72, cam_y=0.45, expression=[(0, KT[0]), (6.6, KT[2])],
              bandeaux=[(4.4, 8.6, L('EMD : le nom = le mot-clé', 'EMD: the name = the keyword', 'EMD: el nombre = la palabra clave'),
                         L("Pour Google, un mot-clé dans le nom n'a « presque aucun effet ». Il juge ce qu'il y a dedans.",
                           'For Google, a keyword in the name has “almost no effect”. It judges what\'s inside.',
                           'Para Google, una palabra clave en el nombre «casi no tiene efecto». Juzga lo de dentro.'), 0.145, 1.0)],
              bruits=[(4.4, 'pop')]),
    # 25. Diana, tendre
    Plan(4.2, SALON, cam=(0.40, 0.40), zoom=(1.25, 1.25), cam_y=0.52,
         acteurs=[Acteur('diana', DIA_P[1], x=0.38, y=0.97, h=0.46, poses=[(0, DIA_P[1]), (2.6, DIA_P[3])]),
                  seb([(0, M('seb-m02-blase')), (2.6, M('seb-m03-sourire-en-coin'))], x=0.60, y=0.94, h=0.46)],
         repliques=[r('diana', 0.3, "Dedans, il y avait nous.", "What was inside was us.", "Dentro, estábamos nosotros.")],
         bruits=[(2.6, 'soupir')]),
    # 26. Sébastien ne lâche rien
    gros_plan('seb', seb_t(M('seb-t02-sourire-en-coin')), SALON, 3.0,
              [r('seb', 0.3, "N'empêche… quel nom.", "Still… what a name.", "Aun así… qué nombre.")], cam=0.45, cam_y=0.42),
    # 27. Kristina : le .com ?
    gros_plan('kristina', KRI_T, SALON, 2.8,
              [r('kristina', 0.3, "Et le .com ?", "And the .com?", "¿Y el .com?")], h=0.36, y=0.62, cam=0.72, cam_y=0.45,
              expression=[(0, KT[0])]),

    # ---------------------------------------------------------------- LA CHUTE : le .com a brûlé
    # 28. Sébastien, penaud
    gros_plan('seb', seb_t(M('seb-t03-depit')), SALON, 2.6,
              [r('seb', 0.3, "Il a brûlé.", "It burned down.", "Se quemó.")], cam=0.45, cam_y=0.42, bruits=[(0.3, 'boing')]),
    # 29. Mars 2021 : la salle des serveurs en feu (sépia, le passé)
    Plan(6.0, SERVEURS, cam=(0.50, 0.50), zoom=(1.0, 1.08), cam_y=0.50, souvenir=True,
         acteurs=[flamme(x, y, h, graine=k, grandit=[(0.0, 0.2), (0.6 + 0.2 * k, 1.0)])
                  for k, (x, y, h) in enumerate([(0.14, 0.62, 0.20), (0.86, 0.60, 0.22), (0.30, 0.50, 0.14), (0.70, 0.50, 0.15),
                                                 (0.50, 0.40, 0.10), (0.20, 0.36, 0.12), (0.80, 0.36, 0.12)])],
         cartons=[(0.2, 2.4, L('Mars 2021', 'March 2021', 'Marzo de 2021'), L("l'hébergeur prend feu", 'the web host catches fire',
                                                                              'arde el centro de datos'), 0.30, 1.0)],
         repliques=[r('kristina', 2.6, "Et la sauvegarde ?", "And the backup?", "¿Y la copia de seguridad?", off=True),
                    r('seb', 4.3, "…Au même endroit.", "…Same place.", "…En el mismo sitio.", off=True)],
         bruits=[(0.0, 'whoosh'), (0.8, 'crt'), (4.3, 'soupir')]),
    # 30. LE CLIN D'ŒIL BOUTIQUE : le t-shirt de Sébastien disait tout (« Dernière sauvegarde : — »)
    Plan(4.6, SALON, cam=(0.50, 0.50), zoom=(1.0, 5.0), cam_y=0.635,
         acteurs=[seb([(0, M('seb-m04-bras-le-long')), (1.0, M('seb-m02-blase'))], x=0.5, y=0.95, h=0.46)],
         bandeaux=[(1.4, 4.6, L('Ce t-shirt ? seoaddict.co', 'This t-shirt? seoaddict.co', '¿Esta camiseta? seoaddict.co'),
                    L('« Dernière sauvegarde : — »', '“Backup: never. Same server.”', '«Copia: nunca. Mismo servidor.»'), 0.16, 0.9)],
         repliques=[r('seb', 1.5, "Le t-shirt ? Sur seoaddict.co.", "The t-shirt? On seoaddict.co.", "¿La camiseta? En seoaddict.co.",
                      sous_titre=False)],
         bruits=[(0.0, 'whoosh'), (1.4, 'ding')]),
    # 31. Kristina lève les yeux au ciel ; l'appel à l'abonnement est la blague
    gros_plan('kristina', fige(KT[3]), SALON, 4.4, [], h=0.36, y=0.62, cam=0.72, cam_y=0.45,
              bandeaux=[(0.3, 4.4, L('Abonne-toi.', 'Subscribe.', 'Suscríbete.'),
                         L('Nous, on a fait une sauvegarde.', 'We made a backup this time.', 'Esta vez, con copia de seguridad.'), 0.145, 1.1)],
              bruits=[(0.3, 'pop')]),
    # 32. LA BOUCLE : Sébastien, dans le pull, fier, à la caméra
    Plan(4.0, SALON, cam=(0.55, 0.55), zoom=(1.45, 1.50), cam_y=0.63,
         acteurs=[Acteur('seb', SEB_PULL[0], x=0.44, y=0.97, h=0.44, poses=[(0, SEB_PULL[0])])],
         repliques=[r('seb', 0.6, "Ça ? C'est un nom de domaine.", "This? It's a domain name.", "¿Esto? Es un nombre de dominio.")],
         bruits=[(0.4, 'tada')]),
]

caler(plans)
DUREE = sum(int(round(p.duree * FPS)) / FPS for p in plans)
assert 150 <= DUREE <= 179, f'durée {DUREE:.1f} s : un épisode fait de 2:30 à 2:59, jamais plus'

if __name__ == '__main__':
    os.makedirs('shorts', exist_ok=True)
    nom = f'shorts/EP02-{LANGUE}'
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
        dossier = f'rendu-ep02-{LANGUE}'
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
