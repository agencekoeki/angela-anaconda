# Le moteur d'animation (état au 30/10/2026, avec les shorts)

Un film est une liste de `Plan` (fichier `film.py`). Chaque plan donne son décor, sa caméra (travelling, zoom), ses acteurs, ses répliques, ses cartons et ses bruitages. `python3 cles.py 3,8 0.2,0.5,0.85` dessine des images-clés pour vérifier. `python3 film.py` rend le film (100 s en moins de deux minutes).

**La règle : l'animation de remplacement.** Chaque pose est une image entière générée d'un bloc (voir `references/animation.md`).

- `planche_cycle.py` : découpe une planche de 4 poses côte à côte, calées sur la même ligne de sol (parole, gestes, marche, course, galop).
- `planche_composantes.py` : découpe une planche dont les poses se chevauchent sans se toucher (un saut), en gardant leur hauteur ; `--ancre arriere` garde les pattes arrière en place (une révérence).
- `moteur.py` :
  - `Acteur(poses=[(t, image)…])` : l'image entière change au temps donné ; `('brut', chemin)` garde la toile commune de la planche ;
  - `Acteur(marche=[…], marche_pas=1)` : cycle joué pendant les déplacements ;
  - `Acteur(gros_plan=True, tetes=…, expression=…)` : la tête entière qui parle, la bouche suit le texte (A, O, OU, I/É, M/B/P, F/V, L, repos) ;
  - `coupe_x` : l'acteur disparaît au-delà d'un x du décor (entrée de tunnel) ; un trajet `(t, x, y, taille)` le rapetisse quand il s'éloigne ;
  - les personnages bougent sur deux images (12 poses par seconde), la caméra en continu ; les répliques ne se chevauchent pas (`caler`) ; le rêve a son fond saturé, ses confettis et son ondulation ; cartons orange, sous-titres, babillage et bruitages de synthèse, musique de ukulélé.
- `detourage_vert.py` : détoure une planche sur fond vert #00B140 (peau ramenée au gris ; `--flashy a-b` garde vive une plage de teinte, `--flashy-epais`, `--frange` et `--frange-haut` nettoient le vert dans les cheveux). Réglages par personnage dans le skill koeki-anaconda, `references/chatgpt.md`.
- `planche_creux.py` : découpe une planche de 4 poses qui se touchent, aux creux de densité (têtes, Tara).
- **Les shorts verticaux** (`FORMAT=vertical`, `LANGUE=fr|en|es`) : `short_ep01.py` (« Juste une petite idée », 2:43), `short_ep02.py` (« Le nom parfait », l'EMD par l'histoire vraie du Pull Moche, 2:35 ; ses vraies captures d'écran sont posées sur la vitre de l'écran cathodique par `capture()`, et vivent dans `captures/` de l'atelier privé, jamais ici), `short_ep03.py` (« On est écoutés », 2:34 : le premier au nouveau cadrage, personnages plus grands, `cadre_pied`, inserts sur les objets, chats un peu plus grands que nature avec un halo clair), `short01.py` (premier jet refusé de « Personne ne me cite » : 53 s, écran turquoise ; **ne pas en partir**, la fiche de cet épisode, devenu le 4, est `shorts/episodes/EP04-…`). Procédés ajoutés au moteur pour que l'image raconte : `Plan.horloge` (le radio-réveil), `Plan.volet` et `fond='bleu'` (le volet bleu ondulé des changements de temps), `Plan.souvenir` (le passé : sépia sur le décor, grain et vignette sur tout), `fond='crt'` (l'insert plein cadre d'un vieil écran qui démarre, texte écrit à l'écran), `Acteur.cadre` (un personnage visible seulement derrière une vitre), `Acteur.contour` (liseré ou lueur), `Acteur.opacite`, `Plan.postits`, `Plan.bandeaux` (pépite et appel sur bandeau sombre), `Plan.noir` et `Plan.lumiere`. Sous-titres : une réplique à la fois, 1,5 s au moins, dans la zone sûre.
- `controle.py <épisode>` (ancien nom `contraste.py`) : le contrôle avant livraison. Lisibilité (personnage contre fond, textes), **tailles** (proportions entre personnages sur la même ligne de sol), **places** (ce qui doit couvrir une vitre ne déborde pas, et la vitre tombe sur celle du décor), personnage coupé par le bord, **sous-titre sur un visage**.
- `calage.py decor.png x0,y0,x1,y1 [--vue v.jpg]` : retrouve le rectangle exact d'une vitre (ou d'une fenêtre, d'un tableau) dans un décor, à partir d'une estimation.
- `carte.py` : la carte-titre façon carte de jeu, qui brille, se retourne et devient le volet bleu (`Plan.carte`).
- `floquer.py` : pose un flocage SEO Addict sur le t-shirt rose de Sébastien, dans les poses de face (`Acteur.flocage`).
- `polices/` : Fredoka (sous-titres) et Luckiest Guy (carte-titre), licences libres ; `telecharger.sh` les récupère.
- (historique) `contraste.py` : l'ancien nom de `controle.py`, qui y renvoie. Le contrôle de lisibilité (chaque personnage se détache-t-il du fond ? chaque texte se lit-il ?). Rapport et planche des défauts dans `controle/`. Pas de livraison avec une ERREUR. `test_contraste.py` garde les cas d'étalonnage (Tara sur écran turquoise, Tara sur écran bleu nuit, l'appel collé aux cheveux, l'appel sur bandeau).
- `pantin.py`, `articule.py` : l'ancienne méthode (une tête posée sur un corps, des bras qui pivotent). Gardés pour mémoire, à ne plus utiliser pour animer : trop raide, jonctions visibles.

## Lancer

- Les images (`assets/`, `banque/`) et les décors sont dans `media-local`, jamais dans un dépôt public ; ils sont dans le dépôt **privé** `agencekoeki/sebastien-anaconda-atelier` (le dossier `atelier-animation/` y contient ces scripts et les images à côté).
- Dépendances : `pip install numpy pillow scipy scikit-image`, `ffmpeg`. Polices : `polices/` (`telecharger.sh`) ; DejaVu vient du système sous Linux, sinon de `polices/`.
- Les scripts se lancent d'où l'on veut : `moteur.py` se place dans son dossier et trouve `media-local` seul (`MEDIA_LOCAL`, voir `_media_local()`).
- `python3 short_ep01.py images` (planche d'images-clés), `python3 controle.py short_ep01`, puis `REPRENDRE=1 bash rendre3.sh` en arrière-plan (12 à 15 min par langue en vertical) et `bash livraison/compresser.sh EP01`. Pour les épisodes 2 et 3 : `bash rendre3-ep02.sh` et `bash rendre3-ep03.sh`, les trois langues l'une après l'autre (sur deux cœurs, compter bien plus longtemps).
