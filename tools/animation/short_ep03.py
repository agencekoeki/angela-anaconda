"""Les Tarasconnades · Épisode 3 · « On est écoutés » — short vertical (9:16) de 2:30 à 2:59, FR / EN / ES.

Usage : LANGUE=fr python3 short_ep03.py                 -> shorts/EP03-fr.mp4 et .srt
        LANGUE=fr python3 short_ep03.py images [k,k…]   -> planche d'images-clés
        python3 controle.py short_ep03                   -> le contrôle (avant toute livraison)

L'idée (Sébastien, 30/10/2026) : un épisode politique et drôle, un peu 1984 : l'IA s'introduit partout, des micros
dans chaque objet ; une rumeur (« insulter son IA, c'est se faire supprimer son compte ») lui fait peur de critiquer
l'outil qu'il utilise ; la vraie question est la dépendance ; et l'IA permet aussi d'en sortir (une IA locale).
Plus de chats que de chiens, et pas de chien du tout (« ils sont en balade »).

La question, posée à la première seconde : « Chut… l'IA nous écoute. »
Le test des trois phrases :
1. Une rumeur fait croire à Sébastien qu'on peut perdre son IA pour l'avoir critiquée : il chuchote et scotche tous les micros de la maison.
2. Plus il se cache, plus cinq paires d'yeux le suivent ; il rêve d'une maison où l'IA écoute tout, puis où tout s'arrête ;
   Diana pose la vraie question : ce n'est pas qu'elle écoute, c'est que toute leur boîte dépend d'elle.
3. Il installe une petite IA chez lui, hors ligne ; il peut enfin critiquer à voix haute… mais les cinq chats ont tout entendu.
La pépite (Diana) : la dépendance. Juin 2025, sous serment au Sénat, le directeur juridique de Microsoft France n'a pas pu
garantir que les données des Français n'iraient jamais aux autorités américaines (CLOUD Act, 2018). (Sans marque à l'écran.)
Le fait corrigé (Kristina) : la règle d'Anthropic du 12/11/2026 interdit la cruauté gratuite et répétée envers les modèles,
pas la critique, et sa sanction est la fin de la conversation, pas le compte.

Installations et récompenses : « Chut… l'IA nous écoute » (0:00) → « Chut… ils nous écoutent » (la boucle) ; le chat qui fixe
(0:03) → les cinq chats ; « Toi, je peux pas » (Titan) → les chats, seuls micros qu'on ne scotche pas ; « Et s'ils coupent ? »
(le rêve) → la petite IA locale ; le t-shirt « Cet incident sera signalé » → la peur d'être signalé.

Cadrage (retour de Sébastien du 30/10/2026 : « les personnages sont vraiment petits par rapport à l'univers ») : en pied,
un humain occupe environ 70 % de la hauteur (h 0,46 × zoom 1,5) ; cam_y = pieds − 0,47 / zoom, pour poser les pieds en bas.
"""
import os
import subprocess
import sys

os.environ['FORMAT'] = 'vertical'
from moteur import *          # noqa: E402

A = 'assets/'
M = lambda n: A + n + '.png'
D = os.path.join(MEDIA_LOCAL, 'decors') + '/'
SALON = D + 'aa-decor-09-salon-vertical.png'
CUISINE = D + 'aa-decor-18-cuisine-vertical.png'
BUREAU1 = D + 'aa-decor-11-bureau-vertical.png'
NUIT = D + 'aa-decor-12-bureau-nuit-vertical.png'
VITRE1 = (0.464, 0.343, 0.592, 0.406)
VITRES = [(0.354, 0.370, 0.454, 0.423), (0.488, 0.370, 0.590, 0.423), (0.630, 0.370, 0.725, 0.423)]


def planche(nom, n=4):
    return [('brut', A + f'{nom}-{i}.png') for i in range(1, n + 1)]


BOUCHES = {'A': M('seb-b01-A'), 'O': M('seb-b02-O'), 'OU': M('seb-b03-OU'), 'IE': M('seb-b04-I-E'),
           'MBP': M('seb-b05-MBP'), 'FV': M('seb-b06-FV'), 'L': M('seb-b07-L')}


def seb_t(repos):
    return dict(BOUCHES, repos=repos)


def fige(chemin):
    return {k: chemin for k in FORMES}


KT = [M(f'kristina-tete-{i}') for i in range(1, 5)]       # 1 pince-sans-rire, 2 elle parle, 3 rit, 4 lève les yeux au ciel
KRI_T = {k: (KT[1] if k in ('A', 'O', 'OU', 'IE', 'L') else KT[0]) for k in FORMES}
DIA_T = {k: (M('diana-t01-A') if k in ('A', 'O', 'OU', 'IE', 'L') else M('diana-t00')) for k in FORMES}
PARANO = planche('seb-parano')                  # 1 chuchote, 2 « chut », 3 déchire le scotch, 4 regarde derrière lui, figé
SEB_DISC, SEB_CLE = planche('seb-discours'), planche('seb-cles')
DIA_P = planche('diana-parle')                  # 1 poings sur les hanches, 2 main qui explique, 3 bras croisés, 4 fou rire
DIA_MARCHE = [A + f'diana-marche-{i}.png' for i in range(1, 5)]
KRI_P = planche('kristina-parle')
TARA = planche('tara')                          # 1 sourire, 2 parle, 3 fière, 4 bâille
TARA_L = [M(f'tara-locale-{i}') for i in range(1, 5)]   # la Tara maison, hors ligne (ambre)
FLAMME = [M(f'flamme-{i}') for i in range(1, 4)]
R = Replique
LUEUR_TARA = ((175, 252, 246), 3, 2)
LUEUR_LOCALE = ((255, 226, 150), 3, 2)
LISERE = ((238, 228, 208), 2, 2)       # un halo clair de papier découpé : un chat noir sur un sol sombre se perdait (contrôle du 30/10)
LISERE_SOMBRE = ((40, 32, 48), 2, 2)   # sur le boîtier beige du rêve, c'est le chat blanc qui se perdait

# les cinq chats (planche « espions ») : 1 Kali, 2 Lilou, 3 Souka, 4 Titan, 5 Patchy ; hauteur assis en part d'un humain debout
# (un chat assis fait 25 à 30 cm, un maine coon un peu plus : on force un peu, c'est un dessin animé ; Sébastien, 30/10 :
# « le chien, il est ridiculement petit »)
CHAT_PART = {1: 0.31, 2: 0.30, 3: 0.29, 4: 0.40, 5: 0.25}


def chat(n, x, y, humain, gauche_a=None, debut=0.0, fin=1e9, fondu=0.0, contour=None):
    """Le chat n, assis, qui fixe la caméra ; gauche_a=t : à partir de t, il tourne la tête vers la gauche (il suit quelqu'un)."""
    poses = [(0, M(f'chats-face-{n}'))] + ([(gauche_a, M(f'chats-gauche-{n}'))] if gauche_a is not None else [])
    op = [(debut, 0.0), (debut + fondu, 1.0)] if fondu else None
    return Acteur('chat', M(f'chats-face-{n}'), x=x, y=y, h=humain * CHAT_PART[n], poses=poses, debut=debut, fin=fin, opacite=op,
                  contour=contour or LISERE)


def r(qui, t, fr, en, es, **kw):
    return R(qui, t, fr, tr={'en': en, 'es': es}, **kw)


def L(fr, en, es):
    return {'fr': fr, 'en': en, 'es': es}


def centre(v):
    return (v[0] + v[2]) / 2


def ecran(v, debut=0.0):
    return Acteur('ecran', M('ecran-allume'), x=centre(v), y=v[3], h=(v[3] - v[1]), ombre=False, debut=debut, cible=v,
                  ajuster=True, echelle_libre=True)


def tara_dans(v, debut=0.0, fin=1e9, poses=None, locale=False):
    hv = (v[3] - v[1]) * 0.88
    img = TARA_L if locale else [p[1] for p in TARA]
    return Acteur('tara', img[0], x=centre(v), y=v[3], h=hv, ombre=False, debut=debut, fin=fin, cadre=v,
                  poses=poses or [(0, img[0])], parle=[img[1], img[0]], tempo_parle=0.17,
                  contour=LUEUR_LOCALE if locale else LUEUR_TARA, opacite=[(debut, 0.0), (debut + 0.25, 1.0)])


def flamme(x, y, h, debut=0.0, fin=1e9, grandit=None, gros_plan=False):
    traj = [(t, x, y, k) for (t, k) in grandit] if grandit else []
    return Acteur('flamme', FLAMME[0], x=x, y=y, h=h, ombre=False, debut=debut, fin=fin, gros_plan=gros_plan, trajet=traj,
                  poses=[(debut + i * 0.125, FLAMME[i % 3]) for i in range(int((min(fin, 40) - debut) / 0.125) + 1)])


def gros_plan(nom, tetes, decor, duree, repliques, expression=None, h=0.40, y=0.62, cam=0.53, cam_y=0.40, **kw):
    extra = kw.pop('extra', ())
    tete = Acteur(nom, None, x=0.5, y=y, h=h, tetes=tetes, gros_plan=True, ombre=False, expression=expression)
    return Plan(duree, decor, cam=(cam, cam), zoom=(2.0, 2.06), cam_y=cam_y, acteurs=[tete] + list(extra), repliques=repliques, **kw)


def objet(nom, x, y, h, **kw):
    kw.setdefault('ombre', False)
    kw.setdefault('contour', LISERE)
    return Acteur(nom, M(nom), x=x, y=y, h=h, echelle_libre=True, **kw)


def cadre_pied(z, pieds=0.95):
    """cam_y qui pose les pieds (à `pieds` dans le décor) en bas de l'écran, au zoom z."""
    return pieds - 0.47 / z


FLOCAGE = MEDIA_LOCAL + '/flocages/FR-450 - Cet incident sera signalé - pour t-shirt foncé.png'
BOUTIQUE = {'fr': 'seoaddict.co/fr/p/cet-incident-sera-signale-t-shirt/', 'en': 'seoaddict.co/p/this-incident-will-be-reported-t-shirt/',
            'es': 'seoaddict.co/es/p/se-informara-de-este-incidente-camiseta/'}


def seb(poses, **kw):
    kw.setdefault('flocage', FLOCAGE)
    return Acteur('seb', M('seb-m04-bras-le-long'), poses=poses, **kw)


def de_dos(x=0.53, y=0.95, h=0.46, **kw):
    return Acteur('seb', M('seb-s1-de-dos-v2'), x=x, y=y, h=h, **kw)


Z = 1.5                                      # le zoom ordinaire des plans en pied (un personnage)
CY = cadre_pied(Z)
Z2 = 1.3                                     # à deux en pied : un peu plus large, sinon l'un des deux sort du cadre
CY2 = cadre_pied(Z2)
H = 0.46                                     # un humain debout, à zoom 1

plans = [
    # ---------------------------------------------------------------- L'AMORCE (0 s)
    # 1. Le salon, le soir : il chuchote à la caméra ; Kali, assise, le fixe
    Plan(3.6, SALON, cam=(0.55, 0.55), zoom=(1.7, 1.75), cam_y=cadre_pied(1.7),
         acteurs=[Acteur('seb', PARANO[1], x=0.48, y=0.95, h=H, poses=[(0, PARANO[1])]),
                  chat(1, 0.67, 0.95, H)],
         repliques=[r('seb', 0.3, "Chut… l'IA nous écoute.", "Shh… the AI is listening.", "Chis… la IA nos escucha.")],
         bruits=[(0.0, 'scratch')]),
    # 2. Le chat, en gros : il fixe la caméra
    Plan(2.4, SALON, cam=(0.62, 0.62), zoom=(4.4, 4.6), cam_y=cadre_pied(4.4, 0.95),
         acteurs=[chat(1, 0.62, 0.95, H)], bruits=[(0.3, 'pop')]),
    # 3. La carte-titre
    Plan(4.0, SALON, cam=(0.45, 0.45), zoom=(2.0, 2.0), cam_y=0.40,
         carte={'debut': 0.0, 'serie': 'LES TARASCONNADES', 'numero': L('ÉP. 3', 'EP. 3', 'EP. 3'),
                'nom': L('On est écoutés', "We're being heard", 'Nos escuchan'),
                'illustration': [M('chats-face-1')],
                'espece': L('Maison connectée · Tarascon · Micros : partout', 'Smart home · Tarascon · Mics: everywhere',
                            'Casa conectada · Tarascón · Micros: en todas partes'),
                'attaques': [(L('Micro ouvert', 'Open mic', 'Micro abierto'), '24/24',
                              L('Entend tout. Ne répète rien. Enfin, presque.', 'Hears everything. Repeats nothing. Almost.',
                                'Lo oye todo. No repite nada. Casi.')),
                             (L('Chuchotement', 'Whisper', 'Susurro'), '×0',
                              L('Ne trompe personne. Surtout pas le chat.', 'Fools nobody. Least of all the cat.',
                                'No engaña a nadie. Y menos al gato.'))],
                'pied': (L('Faiblesse : les croquettes', 'Weakness: cat treats', 'Debilidad: el pienso'),
                         L('Saison 1 · SEO Addict', 'Season 1 · SEO Addict', 'Temporada 1 · SEO Addict'))},
         bruits=[(0.0, 'whoosh'), (0.45, 'tada'), (2.7, 'whoosh')]),

    # ---------------------------------------------------------------- LA VEILLE : la rumeur
    Plan(2.2, fond='bleu', cartons=[(0.1, 2.2, L('La veille…', 'The day before…', 'El día anterior…'), None, 0.40, 1.0)],
         bruits=[(0.0, 'whoosh')], volet=[(1.6, 2.2, 'couvre')]),
    # 5. Le bureau : il lit une « info » sur l'écran
    Plan(3.4, BUREAU1, cam=(0.52, 0.52), zoom=(1.3, 1.9), cam_y=0.50, volet=[(0.0, 0.5, 'decouvre')],
         acteurs=[ecran(VITRE1), de_dos(x=0.53, y=0.95, h=H)],
         bruits=[(0.4, 'clavier'), (2.4, 'crt')]),
    # 6. Plein écran : la rumeur (une capture d'écran inventée, montrée comme une rumeur)
    Plan(5.6, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.1, L('INFO OU INTOX ?', 'NEWS OR RUMOR?', '¿NOTICIA O BULO?')),
                                         (0.8, L('« Tu insultes', '"Insult your', '«¿Insultas')), (1.3, L('  ton IA ?', '  AI?', '  a tu IA?')),
                                         (2.0, L('Compte', 'Account', '¡Cuenta')), (2.4, L('supprimé ! »', 'deleted!"', 'borrada!»'))]},
         repliques=[r('seb', 3.4, "Supprimé ?!", "Deleted?!", "¿¡Borrada!?", off=True)],
         bruits=[(0.1, 'clavier'), (2.4, 'boing')]),
    # 7. Gros plan, le cri
    gros_plan('seb', seb_t(M('seb-t05-cri')), BUREAU1, 2.8,
              [r('seb', 0.3, "Mais je la critique tout le temps !", "But I criticise it all the time!", "¡Pero si la critico todo el rato!")],
              expression=[(0, M('seb-t05-cri'))], cam=0.52, cam_y=0.42),
    # 8. Il chuchote à l'écran ; Tara, dans l'écran, ne comprend pas
    Plan(6.4, BUREAU1, cam=(0.56, 0.56), zoom=(1.9, 1.95), cam_y=0.56,
         acteurs=[ecran(VITRE1), tara_dans(VITRE1, poses=[(0, TARA[0][1]), (3.4, TARA[2][1])]),
                  Acteur('seb', PARANO[0], x=0.60, y=0.95, h=H, poses=[(0, PARANO[0])])],
         repliques=[r('seb', 0.4, "Tara… tu es… formidable.", "Tara… you are… wonderful.", "Tara… eres… maravillosa."),
                    r('tara', 3.2, "Merci ! Pourquoi tu chuchotes ?", "Thanks! Why are you whispering?", "¡Gracias! ¿Por qué susurras?")],
         bruits=[(3.2, 'pop')]),
    # 9. LE CLIN D'ŒIL BOUTIQUE : sa peur d'être signalé, écrite sur son t-shirt
    Plan(4.8, BUREAU1, cam=(0.50, 0.50), zoom=(1.3, 5.5), cam_y=0.682,
         acteurs=[seb([(0, M('seb-m04-bras-le-long')), (1.0, M('seb-m02-blase'))], x=0.5, y=0.95, h=H)],
         bandeaux=[(2.2, 4.8, L('Ce t-shirt ? seoaddict.co', 'This t-shirt? seoaddict.co', '¿Esta camiseta? seoaddict.co'),
                    L('Cet incident sera signalé', 'This incident will be reported', 'Se informará de este incidente'), 0.60, 1.0)],
         repliques=[r('seb', 0.3, "Et si on me signale ?", "What if I get reported?", "¿Y si me denuncian?"),
                    r('seb', 2.0, "Le t-shirt ? Sur seoaddict.co.", "The t-shirt? On seoaddict.co.", "¿La camiseta? En seoaddict.co.",
                      sous_titre=False)],
         bruits=[(0.9, 'whoosh'), (1.6, 'ding')]),

    # ---------------------------------------------------------------- LES MICROS PARTOUT (règle de trois)
    # 10. Le salon : tout clignote ; il voit les petits points rouges (la télécommande et l'enceinte sur la table basse, le purificateur)
    Plan(5.0, SALON, cam=(0.50, 0.50), zoom=(Z, Z + 0.05), cam_y=CY,
         acteurs=[objet('telecommande', 0.60, 0.497, 0.07, rot=80), objet('enceinte', 0.68, 0.493, 0.035),
                  objet('purificateur', 0.76, 0.535, 0.09),
                  Acteur('seb', PARANO[3], x=0.40, y=0.95, h=H, poses=[(0, PARANO[3])])],
         repliques=[r('seb', 0.5, "Ça clignote… Ça écoute.", "It's blinking… It's listening.", "Parpadea… Escucha.")],
         bruits=[(0.2, 'bip'), (1.6, 'bip'), (3.0, 'bip')]),
    # 11. Un : la télécommande, en gros, sur la table ; Lilou, sur le canapé, regarde
    Plan(3.0, SALON, cam=(0.57, 0.57), zoom=(4.0, 4.1), cam_y=0.465,
         acteurs=[chat(2, 0.52, 0.452, 0.25), objet('telecommande', 0.60, 0.497, 0.07, rot=80, fin=1.2),
                  objet('telecommande-scotch', 0.60, 0.497, 0.07, rot=80, debut=1.2)],
         repliques=[r('seb', 1.4, "Un.", "One.", "Uno.", off=True)],
         bruits=[(0.4, 'scratch'), (1.2, 'pop')]),
    # 12. Deux : l'enceinte ; Souka, sur le canapé, regarde
    Plan(3.0, SALON, cam=(0.71, 0.71), zoom=(4.0, 4.1), cam_y=0.465,
         acteurs=[chat(3, 0.77, 0.452, 0.25), objet('enceinte', 0.68, 0.493, 0.035, fin=1.2),
                  objet('enceinte-scotch', 0.68, 0.493, 0.035, debut=1.2)],
         repliques=[r('seb', 1.4, "Deux.", "Two.", "Dos.", off=True)],
         bruits=[(0.4, 'scratch'), (1.2, 'pop')]),
    # 13. Trois : il se retourne… Titan. On ne scotche pas un chat.
    Plan(6.4, SALON, cam=(0.52, 0.52), zoom=(Z + 0.1, Z + 0.1), cam_y=cadre_pied(Z + 0.1),
         acteurs=[Acteur('seb', PARANO[2], x=0.38, y=0.95, h=H, poses=[(0, PARANO[2]), (1.4, PARANO[3]), (3.8, M('seb-m02-blase'))]),
                  chat(4, 0.68, 0.95, H)],
         repliques=[r('seb', 0.4, "Trois…", "Three…", "Tres…"),
                    r('seb', 3.8, "…Toi, je peux pas.", "…You, I can't.", "…A ti no puedo.")],
         bruits=[(1.4, 'boing'), (3.0, 'soupir')]),

    # ---------------------------------------------------------------- DIANA, KRISTINA : on rit, puis on vérifie
    # 14. La cuisine : Diana rit
    Plan(7.4, CUISINE, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('diana', M('diana-m00'), x=0.33, y=0.96, h=H * 0.96, marche=DIA_MARCHE, poses=[(0, DIA_P[3])],
                         trajet=[(0.0, -0.15, 0.96), (1.0, 0.33, 0.96)]),
                  Acteur('seb', PARANO[0], x=0.69, y=0.95, h=H, poses=[(0, PARANO[0])])],
         repliques=[r('diana', 1.1, "Chéri… tu scotches la maison ?", "Honey… are you taping up the house?", "Cariño… ¿estás precintando la casa?"),
                    r('seb', 3.4, "Le frigo écoute. Le micro-ondes aussi.", "The fridge listens. The microwave too.",
                      "La nevera escucha. El microondas también."),
                    r('diana', 5.6, "Et les chiens ?", "And the dogs?", "¿Y los perros?")],
         bruits=[(1.1, 'pop'), (5.6, 'soupir')]),
    gros_plan('seb', seb_t(M('seb-t02-sourire-en-coin')), CUISINE, 3.0,
              [r('seb', 0.3, "En balade. Eux, je leur fais confiance.", "Out for a walk. Them, I trust.", "De paseo. En ellos confío.")],
              cam=0.55, cam_y=0.42),
    # 16. Kristina, deux plans : elle a vérifié
    Plan(6.2, CUISINE, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2,
         acteurs=[Acteur('kristina', KRI_P[1], x=0.665, y=0.97, h=H * 0.95, poses=[(0, KRI_P[1])]),
                  Acteur('seb', PARANO[1], x=0.32, y=0.95, h=H, poses=[(0, PARANO[1]), (4.4, M('seb-m02-blase'))])],
         repliques=[r('kristina', 0.3, "Papa. Critiquer, c'est permis.", "Dad. Criticising is allowed.", "Papá. Criticar está permitido."),
                    r('kristina', 2.6, "Ce qui est visé : la cruauté gratuite, répétée.", "What's targeted: needless, repeated cruelty.",
                      "Lo que se persigue: la crueldad gratuita y repetida.")],
         bruits=[(0.3, 'pop')]),
    gros_plan('kristina', KRI_T, CUISINE, 4.6,
              [r('kristina', 0.3, "Et surtout, elle raccroche.", "And mostly, it hangs up.", "Y sobre todo, cuelga."),
               r('seb', 2.6, "…Elle raccroche ?", "…It hangs up?", "…¿Cuelga?", off=True)],
              h=0.36, y=0.62, cam=0.70, cam_y=0.45, expression=[(0, KT[0]), (2.6, KT[2])]),

    # ---------------------------------------------------------------- LA NUIT : les yeux
    # 18. Il chuchote encore ; un à un, les cinq chats arrivent derrière lui
    Plan(8.4, NUIT, cam=(0.50, 0.50), zoom=(1.35, 1.35), cam_y=cadre_pied(1.35),
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]),
                  Acteur('seb', M('seb-s1-de-dos-v2'), x=0.52, y=0.90, h=H * 0.9, poses=[(0, M('seb-s1-de-dos-v2')), (6.0, PARANO[3])]),
                  chat(1, 0.25, 0.98, H, debut=1.0, fondu=0.4), chat(2, 0.375, 0.99, H, debut=2.0, fondu=0.4),
                  chat(4, 0.50, 1.00, H, debut=3.0, fondu=0.4), chat(3, 0.625, 0.99, H, debut=4.0, fondu=0.4),
                  chat(5, 0.75, 0.98, H, debut=5.0, fondu=0.4)],
         repliques=[r('seb', 0.4, "Personne ne m'entend…", "Nobody can hear me…", "Nadie me oye…"),
                    r('seb', 6.4, "…Vous aussi ?!", "…You too?!", "…¿¡Vosotros también!?")],
         bruits=[(1.0, 'pop'), (2.0, 'pop'), (3.0, 'pop'), (4.0, 'pop'), (5.0, 'pop'), (6.0, 'boing')],
         horloge=[(0.0, 8.4, '23:47')]),
    # 19. Il file à gauche sur la pointe des pieds ; les cinq têtes le suivent
    Plan(5.2, NUIT, cam=(0.50, 0.50), zoom=(1.35, 1.35), cam_y=cadre_pied(1.35),
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]),
                  Acteur('seb', PARANO[3], x=0.52, y=0.90, h=H * 0.9, saut=0.006, poses=[(0, PARANO[3])],
                         trajet=[(0.4, 0.52, 0.90), (3.6, -0.25, 0.90)]),
                  chat(1, 0.25, 0.98, H, gauche_a=1.4), chat(2, 0.375, 0.99, H, gauche_a=1.2),
                  chat(4, 0.50, 1.00, H, gauche_a=1.0), chat(3, 0.625, 0.99, H, gauche_a=0.8), chat(5, 0.75, 0.98, H, gauche_a=0.6)],
         bruits=[(0.6, 'pouet'), (2.0, 'pouet')], horloge=[(0.0, 5.2, '23:48')], volet=[(4.6, 5.2, 'couvre')]),

    # ---------------------------------------------------------------- LE RÊVE (1984, en drôle)
    # 20. L'écran géant : Tara qui écoute, les cinq chats en garde
    Plan(6.4, fond='crt', vague=(0.0, 0.7),
         crt={'allume': 0.0, 'lignes': [(0.6, L('TARA T\'ÉCOUTE', 'TARA HEARS YOU', 'TARA TE OYE')),
                                         (1.4, L('Pense en silence.', 'Think quietly.', 'Piensa en silencio.'))]},
         acteurs=[Acteur('tara', TARA[0][1], x=0.5, y=0.66, h=0.30, ombre=False, cadre=GLACE_CRT, contour=LUEUR_TARA,
                         poses=[(0, TARA[2][1])], parle=[TARA[1][1], TARA[0][1]], tempo_parle=0.17),
                  chat(1, 0.12, 0.99, 0.62, contour=LISERE_SOMBRE), chat(2, 0.31, 0.99, 0.62, contour=LISERE_SOMBRE),
                  chat(4, 0.50, 1.00, 0.62, contour=LISERE_SOMBRE), chat(3, 0.69, 0.99, 0.62, contour=LISERE_SOMBRE),
                  chat(5, 0.88, 0.99, 0.62, contour=LISERE_SOMBRE)],
         repliques=[r('tara', 2.6, "Je t'écoute. Toujours.", "I'm listening. Always.", "Te escucho. Siempre."),
                    r('seb', 4.6, "Je n'ai rien dit !", "I didn't say a thing!", "¡No he dicho nada!", off=True)],
         bruits=[(0.0, 'whoosh'), (2.6, 'pop')]),
    # 21. Puis tout s'arrête : la maison sans tuyaux
    Plan(5.0, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.3, L('SERVICE', 'SERVICE', 'SERVICIO')), (0.8, L('INTERROMPU', 'INTERRUPTED', 'INTERRUMPIDO')),
                                         (1.8, L('Frigo : coupé', 'Fridge: cut off', 'Nevera: cortada')),
                                         (2.4, L('Lumière : coupée', 'Lights: cut off', 'Luz: cortada')),
                                         (3.0, L('Boîte : coupée', 'Business: cut off', 'Empresa: cortada'))]},
         repliques=[r('seb', 3.4, "Non ! Pas les tuyaux !", "No! Not the pipes!", "¡No! ¡Las tuberías no!", off=True)],
         bruits=[(0.3, 'crt'), (1.8, 'bip'), (2.4, 'bip'), (3.0, 'bip'), (3.4, 'boing')], noir=(4.4, 5.0)),

    # ---------------------------------------------------------------- LA PÉPITE (coupe sèche : le matin, la cuisine)
    Plan(4.2, CUISINE, cam=(0.50, 0.50), zoom=(Z2, Z2), cam_y=CY2, lumiere=(0.0, 0.4),
         acteurs=[Acteur('diana', DIA_P[1], x=0.32, y=0.96, h=H * 0.96, poses=[(0, DIA_P[2])]),
                  Acteur('seb', M('seb-m02-blase'), x=0.68, y=0.95, h=H, poses=[(0, M('seb-m02-blase'))])],
         repliques=[r('diana', 0.6, "Le vrai problème, ce n'est pas qu'elle écoute.", "The real problem isn't that it listens.",
                      "El problema no es que escuche.")],
         bruits=[(0.0, 'scratch')], horloge=[(0.0, 4.2, '07:30')]),
    gros_plan('diana', DIA_T, CUISINE, 3.6,
              [r('diana', 0.3, "C'est que toute notre boîte tourne chez eux.", "It's that our whole business runs on their servers.",
                 "Es que toda nuestra empresa funciona en sus servidores.")],
              h=0.40, y=0.62, cam=0.32, cam_y=0.45),
    # le bandeau sur un plan à deux, au-dessus des têtes (Sébastien, 30/10 : « attention à la superposition » ; il couvrait le visage de Diana)
    Plan(6.2, CUISINE, cam=(0.50, 0.50), zoom=(1.2, 1.22), cam_y=cadre_pied(1.2),
         acteurs=[Acteur('diana', DIA_P[1], x=0.33, y=0.96, h=H * 0.96, poses=[(0, DIA_P[1])]),
                  Acteur('seb', M('seb-m02-blase'), x=0.68, y=0.95, h=H, poses=[(0, M('seb-m02-blase'))])],
              bandeaux=[(0.2, 6.2, L('La dépendance', 'Dependence', 'La dependencia'),
                         L("Juin 2025, sous serment au Sénat : un géant américain du cloud n'a pas pu garantir que nos données n'iraient jamais aux autorités de son pays.",
                           'June 2025, under oath before the French Senate: a US cloud giant could not guarantee our data would never go to US authorities.',
                           'Junio de 2025, Senado francés, bajo juramento: un gigante de la nube de EE. UU. no pudo garantizar que nuestros datos no irían a su gobierno.'),
                         0.13, 1.0)],
         bruits=[(0.2, 'pop')]),
    gros_plan('seb', seb_t(M('seb-t03-depit')), CUISINE, 3.2,
              [r('seb', 0.3, "Et s'ils coupent… on fait quoi ?", "And if they cut us off… what do we do?", "Y si cortan… ¿qué hacemos?")],
              cam=0.62, cam_y=0.42),

    # ---------------------------------------------------------------- LA SORTIE : une petite IA, à la maison
    # 25. La nuit, une petite idée
    Plan(4.0, NUIT, cam=(0.52, 0.52), zoom=(1.6, 1.65), cam_y=0.52,
         acteurs=[ecran(VITRES[0]), ecran(VITRES[1]), ecran(VITRES[2]), de_dos(x=0.53, y=0.95, h=H),
                  flamme(0.53, 0.95 - H * 0.97, 0.07, debut=0.6, grandit=[(0.6, 0.3), (1.2, 1.2)])],
         repliques=[r('seb', 1.0, "Juste une petite idée…", "Just one tiny idea…", "Solo una ideíta…")],
         bruits=[(0.6, 'whoosh'), (1.4, 'clavier')], horloge=[(0.0, 4.0, '02:10')]),
    # 26. Plein écran : la Tara maison démarre, hors ligne, lentement
    Plan(7.2, fond='crt',
         crt={'allume': 0.0, 'lignes': [(0.3, L('TARA MAISON 0.1', 'HOME TARA 0.1', 'TARA CASERA 0.1')),
                                         (0.9, L('sur ton PC', 'on your PC', 'en tu PC')), (1.5, L('hors ligne ✔', 'offline ✔', 'sin red ✔')),
                                         (2.1, L('Réflexion…', 'Thinking…', 'Pensando…'))],
              'barre': (2.6, 5.6)},
         acteurs=[Acteur('tara', TARA_L[0], x=0.5, y=0.78, h=0.20, ombre=False, debut=5.0, cadre=GLACE_CRT, contour=LUEUR_LOCALE,
                         poses=[(5.0, TARA_L[0])], opacite=[(5.0, 0.0), (5.3, 1.0)])],
         bruits=[(0.3, 'clavier'), (2.6, 'clavier'), (5.0, 'pop')]),
    # 27. Le bureau : la Tara maison, dans l'écran, un peu lente ; lui, ravi
    Plan(6.0, BUREAU1, cam=(0.56, 0.56), zoom=(1.9, 1.95), cam_y=0.56,
         acteurs=[ecran(VITRE1), tara_dans(VITRE1, locale=True, poses=[(0, TARA_L[0]), (3.8, TARA_L[2])]),
                  Acteur('seb', SEB_CLE[2], x=0.62, y=0.95, h=H, poses=[(0, SEB_DISC[0]), (3.8, SEB_CLE[2])])],
         repliques=[r('tara', 0.4, "Je suis… un peu… plus lente.", "I'm… a bit… slower.", "Soy… un poco… más lenta."),
                    r('seb', 3.0, "Mais tu restes ici !", "But you stay right here!", "¡Pero te quedas aquí!")],
         bruits=[(3.0, 'tada')]),

    # ---------------------------------------------------------------- LA CHUTE : les seuls micros qu'on ne scotche pas
    Plan(7.2, SALON, cam=(0.50, 0.50), zoom=(Z, Z), cam_y=CY,
         acteurs=[Acteur('seb', SEB_DISC[0], x=0.50, y=0.87, h=H * 0.92, poses=[(0, SEB_DISC[0]), (3.2, PARANO[3]), (4.8, PARANO[1])]),
                  chat(1, 0.27, 0.965, H, debut=2.6, fondu=0.2), chat(2, 0.385, 0.965, H, debut=2.7, fondu=0.2),
                  chat(4, 0.50, 0.965, H, debut=2.8, fondu=0.2), chat(3, 0.615, 0.965, H, debut=2.9, fondu=0.2),
                  chat(5, 0.73, 0.965, H, debut=3.0, fondu=0.2)],
         repliques=[r('seb', 0.3, "Enfin ! Je peux tout dire ! L'IA, c'est…", "At last! I can say anything! AI is…",
                      "¡Por fin! ¡Puedo decirlo todo! La IA es…"),
                    r('seb', 5.0, "…formidable.", "…wonderful.", "…maravillosa.")],
         bruits=[(0.3, 'tada'), (2.6, 'pop'), (3.2, 'boing')]),
    # 29. L'appel à l'abonnement est la blague
    Plan(4.4, SALON, cam=(0.50, 0.50), zoom=(2.5, 2.5), cam_y=cadre_pied(2.5, 1.0),
         acteurs=[chat(1, 0.385, 1.00, H), chat(4, 0.50, 1.00, H), chat(5, 0.615, 1.00, H)],
         bandeaux=[(0.3, 4.4, L('Abonne-toi.', 'Subscribe.', 'Suscríbete.'),
                    L('Les chats, eux, ont déjà tout entendu.', 'The cats already heard everything.', 'Los gatos ya lo han oído todo.'), 0.16, 1.1)],
         bruits=[(0.3, 'pop')]),
    # 30. LA BOUCLE : Kali fixe la caméra ; lui, tout bas
    Plan(3.6, SALON, cam=(0.62, 0.62), zoom=(4.4, 4.6), cam_y=cadre_pied(4.4, 0.95),
         acteurs=[chat(1, 0.62, 0.95, H)],
         repliques=[r('seb', 0.6, "Chut… ils nous écoutent.", "Shh… they're listening.", "Chis… nos escuchan.", off=True)],
         bruits=[(0.0, 'pop')]),
]

# le t-shirt de l'épisode, dans toutes ses poses de face (floquer.py ignore les autres)
for _p in plans:
    for _a in _p.acteurs:
        if _a.nom == 'seb' and not _a.gros_plan and _a.flocage is None:
            _a.flocage = FLOCAGE
caler(plans)
DUREE = sum(int(round(p.duree * FPS)) / FPS for p in plans)
assert 150 <= DUREE <= 179, f'durée {DUREE:.1f} s : un épisode fait de 2:30 à 2:59, jamais plus'

if __name__ == '__main__':
    os.makedirs('shorts', exist_ok=True)
    nom = f'shorts/EP03-{LANGUE}'
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
        dossier = f'rendu-ep03-{LANGUE}'
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
