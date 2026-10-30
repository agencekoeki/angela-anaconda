---
title: "L'univers Sébastien Anaconda"
scope: "La bible des personnages originaux qui illustrent le site : Sébastien Anaconda et sa ménagerie. Ce sont des personnages inventés, dessinés à la manière de la série mais qui n'en reprennent aucun personnage."
last_updated: 2026-10-29
---

# L'univers Sébastien Anaconda

Le site ne réutilise aucune image de la série. Il est illustré par des personnages originaux : Sébastien, dessiné à la manière de la série, avec ses chiens et ses chats. Ce dossier en est la bible. Pour chaque personnage, il dit :

- ce qui le rend **reconnaissable**, c'est-à-dire ce qu'on vérifie sur chaque image ;
- son **caractère**, tel que Sébastien le raconte ;
- ses **poses signatures**, tirées de ce caractère. Elles forment la liste des images à produire ;
- son **comportement sur le site**, c'est-à-dire l'animation qui en découle ;
- le **prompt d'ancrage**, la description fixe envoyée avec l'image maître.

| Fiche | Qui |
|---|---|
| [sebastien.md](sebastien.md) | Sébastien Anaconda |
| [diana.md](diana.md) | Diana, dite Doudou |
| [kristina.md](kristina.md) | Kristina |
| [menagerie/django.md](menagerie/django.md) | Django, berger australien bleu merle |
| [menagerie/olympe.md](menagerie/olympe.md) | Olympe, colley à poil long bleu merle |
| [menagerie/titan.md](menagerie/titan.md) | Titan, maine coon blanc |
| [menagerie/souka.md](menagerie/souka.md) | Souka, chat gris argenté |
| [menagerie/lilou.md](menagerie/lilou.md) | Lilou, chatte « vache » |
| [menagerie/patchy.md](menagerie/patchy.md) | Patchy, petit chat gris masqué |
| [menagerie/kali.md](menagerie/kali.md) | Kali, chatte toute noire |
| [scene-accueil.md](scene-accueil.md) | La scène d'accueil du site, une minute |
| [a-faire.md](a-faire.md) | Tout ce qu'il reste à faire |

## La méthode d'ancrage

Un générateur d'images dérive d'une image à l'autre. Pour l'en empêcher :

1. **Une image maître par personnage.** Elle est validée à l'œil contre les photos de référence.
2. **Une étoile, pas une chaîne.** Chaque variation part de l'image maître, jamais de la variation d'avant : une photocopie de photocopie accumule la dérive. Chaque variation ne change qu'une chose, que ce soit la pose, l'expression, la tenue ou l'accessoire.
3. **Cinq ou six variations validées** forment ensuite un jeu de références. C'est seulement alors qu'on lance les grandes séries.
4. **Un fond uni.** Les images sont générées sur un aplat d'une seule couleur, puis détourées en local pour obtenir des PNG transparents.
5. **L'étalonnage, sur le décor seulement.** `tools/tv1999.py` assombrit, désature et adoucit le contraste du décor. Le personnage est posé ensuite, intact, pour que ses couleurs vives sortent. Le filtre ne met **aucun flou**, ni grain, ni ligne : un flou voulu passerait pour une image mal compressée. L'image reste nette, comme non compressée.

## La règle des couleurs

**Le monde est terne, les personnages sont flashy.** Comme dans la série, les décors restent sourds, grisâtres et un peu sombres, des couleurs de vieille télé cathodique. Seuls les personnages portent de la couleur vive : le t-shirt rose fluo de Sébastien, les animaux et les autres membres de la famille. Si un décor attire l'œil plus qu'un personnage, il est raté.

**Une pièce vraiment flashy par personnage**, qui perce l'image : le t-shirt rose fluo de Sébastien, les cheveux roux flamboyants de Diana, le carré roux de Kristina. `tools/detourage.py --flashy` pousse cette teinte-là et elle seule.

## Les deux styles

- **Les décors** : de la 3D low-poly bon marché de la fin des années 1990, sous une lumière plate. Les ombres de contact sont dures et sombres, les textures photo (pierre, brique, bitume) sont floues et étirées sur des formes simples. Les couleurs sont sourdes : verts olive ou bleu-vert, ciel bleu délavé, murs beige grisâtre. Les décorations sont collées au mur comme des gommettes. Les décors sont vides et un peu mélancoliques.
- **Les humains** : une photo de visage photocopiée en noir et blanc, une peau grise et plate, des membres fins comme des cure-pipes sans articulations visibles, des vêtements en vraies textures de tissu froissé, et des décors 3D simples aux couleurs en aplat.
- **Les animaux** : un modèle low-poly de jeu vidéo de 1998, aux facettes visibles. La texture est floue et basse résolution, la pose raide, la lumière plate, les couleurs sourdes et les yeux peints.

Les animaux sont beaucoup plus « cartoon » que les humains, qui sont gris, presque décharnés, et portent toute la lumière dans leurs expressions. Pour que les deux mondes tiennent ensemble, **un animal est presque toujours à l'écran avec un humain** : on ne le laisse pas seul dans un plan (consigne de Sébastien, 30/10/2026).

## L'animation

On anime par **remplacement** : chaque pose est une image entière générée d'un bloc, jamais une tête posée sur un corps ni un bras qui pivote. En gros plan, la tête entière parle (une image par forme de bouche) ; en plan large, on enchaîne des planches de quatre poses (parole, gestes, marche, course, saut). C'est ce qui a donné vie à Diana et Kristina, et c'est la règle pour tous, animaux compris.

## Où sont les images

- **Les images brutes et les références photo** restent sur le poste, dans `media-local/`, qui est exclu de Git.
- **Seules les découpes validées** sont publiées, dans `docs/`, pour le site.
