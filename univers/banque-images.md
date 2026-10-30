---
title: "La banque d'images de l'univers (hors Git)"
scope: "Ce qui a été fabriqué dans ChatGPT pour les épisodes à venir, où c'est rangé dans media-local, et ce qu'il reste à faire pour s'en servir. Les images elles-mêmes ne sont jamais dans le dépôt."
last_updated: 2026-10-30
---

# La banque d'images

Sébastien, 30/10/2026 : « construis des choses, et on verra plus tard comment on les réutilisera ». Tout est dans `media-local\` sur son PC (exclu de Git).

## Décors verticaux (2:3, 1024 × 1536), `media-local\decors\`

| Fichier | Lieu | Pour |
|---|---|---|
| `aa-decor-09-salon-vertical.png` | le salon | scènes de famille |
| `aa-decor-11-bureau-vertical.png` | le bureau, un seul écran (avant l'IA) ; vitre `VITRE1` dans `short_ep01.py` | ép. 1 |
| `aa-decor-12-bureau-nuit-vertical.png` | le bureau de nuit, trois écrans, lampe ; vitres = celles du bureau de jour | ép. 1 |
| `aa-decor-13-chambre-nuit-vertical.png` | la chambre de nuit | ép. 1 |
| `aa-decor-14-bureau-jour-vertical.png` | le bureau de jour, trois écrans ; vitres `VITRES` dans `short_ep01.py`, retrouvées par `calage.py` | ép. 1 |
| `aa-decor-15-plage-vertical.png` | la plage (l'Espiguette), parasol, serviette rayée, phare | ép. 1 (le passé) |
| `aa-decor-16-boulangerie-vertical.png` | l'intérieur de la boulangerie : comptoir, vitrine de pains, panières, ardoise vierge, porte à clochette | ép. 4 (le boulanger) |
| `aa-decor-17-rue-tarascon-vertical.png` | une ruelle de Tarascon, le château au bout, une devanture de boulangerie | plans d'installation, ép. 4 |
| `aa-decor-18-cuisine-vertical.png` | la cuisine (version verticale de la cuisine validée) | scènes de famille |
| `aa-decor-19-agility-vertical.png` | le terrain d'agility : haie, pneu, palissade, slalom, tunnel | épisodes avec les chiens |
| `aa-decor-20-jardin-vertical.png` | le jardin de la maison : mur de pierre, volets bleu-gris, olivier, lavandes, petite piscine, gamelle | scènes avec les animaux |
| `aa-decor-21-salle-serveurs-vertical.png` | une petite salle de serveurs la nuit : deux rangées de baies, diodes vertes et ambre, néon, carrelage gris ; rien d'écrit | ép. 2 (l'incendie de l'hébergeur, mars 2021) |

## Personnages et animaux (planches de 4 poses)

| Fichier | Qui | Poses | À faire |
|---|---|---|---|
| `proches-banque\boulanger-planche-poses-v2.png` | le boulanger (nouveau) | bras croisés, baguette-trophée, salut, fou rire | **découpée** : `atelier-animation/banque/boulanger-1..4.png` |
| `sebastien-banque\seb-planche-bureau.png` | Sébastien, t-shirt rose | assis qui tape, assis qui se tire les oreilles, debout avec un mug épuisé, endormi sur la chaise | **découpée** : `banque/seb-bureau-1..4.png` ; ajouter `'seb-bureau'` à `PROPORTIONS` (il est assis) |
| `proches-banque\diana-planche-expressions.png` | Diana, robe verte | main sur le front, téléphone à deux pouces, bras croisés sourcil levé, fou rire | **découpée** (`--flashy 10-38 --frange 40 --frange-haut 0.36`) : `banque/diana-jour-1..4.png` |
| `proches-banque\kristina-planche-poses-jour.png` | Kristina, tenue de jour | l'ordinateur sous le bras en montrant la caméra, assise en tailleur à l'ordinateur, mains sur les hanches, pouces levés | **découpée** (`--flashy 0-24 --flashy-epais 4`) : `banque/kristina-jour-1..4.png` |
| `menagerie-poses\souka-planche-poses.png` | Souka | assis, marche, en boule, étirement | fond transparent, découper |
| `menagerie-poses\lilou-planche-poses.png` | Lilou | assise, marche, en pain, sur le dos | fond transparent, découper |
| `menagerie-poses\kali-planche-poses.png` | Kali | assise, marche, dos rond (feulement), endormie | fond transparent ; nettoyer un reste de vert autour des moustaches |
| `menagerie-poses\rampette-planche-poses.png` | Rampette (nouveau) | debout, marche, scanne, renversé | fond transparent |
| `menagerie-poses\titan-planche-poses.png` | Titan | assis en roi, avachi sur le flanc, marche fière, bâillement | fond transparent |
| `proches-banque\diana-planche-garde-robe.png` | Diana, garde-robe | pull rouge et mini-jupe à fleurs, chemise-robe rayée de plage et lunettes écaille, doudoune d'hiver, tenue d'agility fluo | tirées du catalogue des tenues |

## Les tenues de Diana et de Kristina

À la demande de Sébastien (30/10), une recherche dans les photos de famille relève leurs tenues et leurs lunettes (« elles adorent les lunettes ») : catalogue privé dans `media-local\recherche-tenues\diana\` et `…\kristina\` (descriptions, photos de référence, phrases de prompt). Les photos elles-mêmes ne partent nulle part : les tenues se décrivent en mots dans les prompts.
- **Diana** : 15 tenues relevées et 10 paires de lunettes (surtout de soleil : la ronde noir et argent, l'aviateur miroir, le grand papillon noir, l'écaille dorée…). Quatre références restent à confirmer par Sébastien (visage peu visible ou photo à deux).
- **Kristina** : 3 tenues seulement sur des photos où elle est adulte (la chemise noire du bureau, le tee crème et les colliers de perles, la longue robe noire et le petit sac rouge), 2 paires de lunettes de vue (la grande carrée dorée rétro, une fine rectangulaire), un anneau de nez et des colliers superposés constants ; la couleur de ses cheveux change d'une année à l'autre. Planche de garde-robe faite le 30/10 (`proches-banque\kristina-planche-garde-robe.png`) : la chemise noire du bureau avec les grandes lunettes dorées rétro, le tee crème et les colliers de perles avec un jean, la longue robe noire côtelée et le petit sac rouge.
