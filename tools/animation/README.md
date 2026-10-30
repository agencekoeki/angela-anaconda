# Le moteur d'animation (état au 30/10/2026)

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
- `pantin.py`, `articule.py` : l'ancienne méthode (une tête posée sur un corps, des bras qui pivotent). Gardés pour mémoire, à ne plus utiliser pour animer : trop raide, jonctions visibles.

Les images (`assets/`) restent dans `media-local`, jamais dans un dépôt.
