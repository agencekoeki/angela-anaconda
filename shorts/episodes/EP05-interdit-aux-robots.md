---
title: "Les Tarasconnades · Ép. 5 · « Interdit aux robots »"
theme: "L'exploration par les robots, robots.txt et l'indexation : bloquer l'exploration n'empêche pas l'indexation"
duree: "2:49 (169.6 s), 35 plans"
format: "9:16, 1080 × 1920, 24 i/s ; FR, EN, ES"
flocage: "T-shirt « noindex, nofollow introverti » (n° 010, section 02 Code & balises)"
last_updated: 2026-10-30
statut: "v2, deuxième passe le 30/10/2026"
---

# Ép. 5 · Interdit aux robots

**[À CONFIRMER par Sébastien] Kristina a-t-elle un bureau chez ses parents ?** Toute la fiche le suppose : elle travaille chez vous, dans une pièce à elle, et c'est là qu'elle prépare une surprise pour son père. Si ce n'est pas le cas, on garde l'histoire en changeant de pièce (l'atelier, le garage, le bureau de Diana).

**La question** (posée à la première seconde, par Sébastien) : pourquoi le robot n'entre pas dans le bureau de ma fille ? On dit « le robot » à l'ouverture ; son nom, Rampette, vient quand Sébastien le sort du carton. Même règle pour l'IA : le prénom « Tara » s'écrit au démarrage de l'ordinateur (« TARA 1.3 · Plan de la maison : introuvable »).

**Le test des trois phrases**
1. Kristina et Diana préparent une surprise pour Sébastien ; pour savoir quoi, il lâche Rampette, un petit robot qui « lit » toutes les pièces pour l'IA, mais Rampette s'arrête net devant le bureau de Kristina, qui porte un panneau « interdit aux robots ».
2. Le panneau n'arrête que les robots polis (le chat fonce dedans), et l'IA parle quand même du bureau, parce que toute la maison en parle (Diana a écrit « surprise » sur le frigo).
3. Kristina enlève le panneau, laisse entrer le robot et lui dit « pas un mot » : l'IA sait enfin ce qu'elle prépare… et n'a pas le droit de le dire ; la surprise, c'est son nouveau site, qui gardera son « pas un mot » jusqu'à lundi.

**La pépite**, dite par Kristina (2:11) et écrite sur le bandeau : « Pour qu'il n'en parle pas… il faut le laisser entrer. Et lui dire : pas un mot. » C'est la vraie différence entre **bloquer l'exploration** (robots.txt, le panneau sur la porte) et **empêcher l'indexation** (la règle noindex, la carte « pas un mot »).
- [SAVOIR : Google Search Central, « Introduction to robots.txt », mis à jour le 10/12/2025, https://developers.google.com/search/docs/crawling-indexing/robots/intro] Le fichier robots.txt dit aux robots des moteurs quelles adresses ils peuvent explorer ; Google écrit que ce n'est « pas un mécanisme pour garder une page web hors de Google » (« it is not a mechanism for keeping a web page out of Google ») et qu'une page bloquée par robots.txt peut quand même apparaître dans les résultats, mais **sans description** (« its URL can still appear in search results, but the search result won't have a description »). C'est le « Bureau de Kristina. Aucune information disponible. » de Tara (1:29).
- [SAVOIR : même page] « Googlebot et les autres robots respectables obéissent aux instructions d'un fichier robots.txt, d'autres robots peuvent ne pas le faire » (« While Googlebot and other respectable web crawlers obey the instructions in a robots.txt file, other crawlers might not ») ; pour protéger une information, Google conseille d'autres méthodes, comme le mot de passe. C'est Rampette qui obéit, Django qui s'assoit, Patchy qui fonce, et Diana : « Un panneau, ce n'est pas une serrure. » (1:17)
- [SAVOIR : Google Search Central, « Block Search indexing with noindex », mis à jour le 10/12/2025, https://developers.google.com/search/docs/crawling-indexing/block-indexing] Pour que la règle noindex fonctionne, la page **ne doit pas être bloquée par robots.txt** (« For the noindex rule to be effective, the page or resource must not be blocked by a robots.txt file ») : sinon, le robot ne verra jamais la règle (« the crawler will never see the noindex rule »), et la page peut quand même apparaître dans les résultats, « par exemple si d'autres pages renvoient vers elle » (« for example if other pages link to it »). C'est le post-it du frigo, le plan de la maison et le message de Diana (1:39), et c'est la solution de Kristina : ouvrir la porte et poser la carte « pas un mot ».
- [SAVOIR : IETF, RFC 9309 « Robots Exclusion Protocol », septembre 2022, § 3 « Security Considerations », https://www.rfc-editor.org/rfc/rfc9309.html ; texte de la RFC finale relu le 30/10/2026 sur https://datatracker.ietf.org/doc/rfc9309/] Le protocole « n'est pas un substitut à de vraies mesures de sécurité » (« The Robots Exclusion Protocol is not a substitute for valid content security measures » ; le brouillon -06 disait « more valid »), et lister une adresse dans robots.txt « l'expose publiquement » et la rend « découvrable » (« Listing paths in the robots.txt file exposes them publicly and thus makes the paths discoverable »). C'est Sébastien qui, en lisant le panneau, se demande ce qu'elle cache (1:21).
- [PENSER] « L'IA sait mais n'a pas le droit de le dire » (2:26) est une image : avec noindex, Google peut explorer la page mais ne l'affiche pas dans ses résultats. La série fait de Tara le moteur de recherche de la maison ; un vrai assistant d'IA a ses propres robots et ses propres règles, ce qui n'est pas le sujet de l'épisode.
- [PENSER] La surprise (un site en construction qu'on garde hors de Google jusqu'au lancement, « Lundi, on enlève le "pas un mot" ») est un usage courant de noindex ; pour un vrai site en travaux, le mot de passe protège mieux encore (voir la page robots.txt citée plus haut). On ne le dit pas dans l'épisode.
- [PENSER] Le t-shirt porte « noindex, nofollow » ; l'épisode ne parle que de noindex (nofollow, qui dit de ne pas suivre les liens, n'y joue aucun rôle). Kristina montre le premier mot.

## Ce que l'image raconte (sans le dire)

- **Le panneau est robots.txt.** On ne le dit pas : on le montre deux fois, le panneau sur la porte (0:05) puis le vrai fichier sur l'écran de Sébastien (1:06), qui dit la même chose en toutes lettres.
- **Lire n'est pas raconter.** Rampette lit les pièces (le cône turquoise, « Cuisine : lue ✓ ») ; Tara raconte (elle répond aux questions). Le robot qui lit et l'IA qui répond sont deux personnages : c'est toute la différence entre exploration et indexation, sans un mot de jargon.
- **Qui obéit au panneau** : le robot poli, le chien sage, et pas le chat (règle de trois, 0:55 à 1:14).
- **Comment Tara connaît le bureau** : trois vignettes reliées par des flèches (1:39) ; on comprend « les autres en parlent » avant que Tara le dise ; et Diana avoue, morte de rire, que le post-it du frigo, c'est elle (1:50).
- **La complicité** : Diana et Kristina préparent la surprise ensemble, se font des clins d'œil, pouffent derrière lui (0:15, 1:50, 2:26) ; il les regarde l'une, puis l'autre. On rit de lui avec elles.
- **La surprise** : on ne la voit pas quand Rampette la scanne (l'écran est tourné vers le mur, il s'illumine dans le cône, 2:19) ; on la découvre avec Sébastien à la fin (2:36).
- **La voix ment** (0:42) : « Rien ne lui échappera. » Coupe, douze secondes plus tard : il fait demi-tour devant un panneau en carton.
- **Tara n'est jamais présentée** : l'écran s'allume, le démarrage s'écrit (« TARA 1.3 · Plan de la maison : introuvable »), elle apparaît derrière la vitre ; trois secondes plus tard, elle avoue qu'elle n'a jamais visité la maison.

## Installations et récompenses

| Installé | Récolté |
|---|---|
| Rampette s'arrête devant la porte au panneau (0:05) | Rampette s'arrête sur le seuil d'une porte ouverte, sans panneau, et Kristina le fait entrer (2:46) : la boucle |
| « TARA 1.3 · Plan de la maison : introuvable » (0:25) | « Je n'ai jamais visité la maison. » (0:28) |
| Kristina et Diana : « Rien. » — « Demande à ton IA. » (0:15) | La surprise, révélée (2:36) |
| « Tara, Kristina prépare quoi ? » — « Je ne sais pas. » (0:28) | « Je sais. Mais je n'ai pas le droit de le dire. » (2:26) |
| « Pour tout savoir, il faut tout visiter. » (0:35) | « Pour qu'il n'en parle pas… il faut le laisser entrer. » (2:11) |
| Le panneau sur la porte (0:55) | Le vrai fichier robots.txt (1:06) ; Kristina décroche le panneau (2:19) |
| « Qu'est-ce qu'elle cache ? » (1:21) | Le rêve : il scanne même la porte au panneau (2:00) ; le « Non. » de Kristina (2:06) |
| Le post-it du frigo, dans les vignettes de Tara (1:39) | « C'est moi. J'ai écrit "surprise" sur le frigo. » (1:50) |
| Le t-shirt « noindex, nofollow introverti » au clin d'œil (1:25) | « C'était écrit sur ton t-shirt. » (2:32) : la solution était sous son nez depuis la moitié de l'épisode |
| Tara : « Bureau de Kristina. Aucune information disponible. » (1:29) | La ligne ne s'écrit plus (2:26) ; et le nouveau site : « Lundi, on enlève le "pas un mot". » (2:36) |

## La carte-titre (0:09)

Pour la première fois, la carte présente **un autre personnage que Sébastien** : Rampette.
- **Nom** : Interdit aux robots
- **Ligne d'espèce** : Robot d'exploration · Fer-blanc · Très poli
- **Illustration** : Rampette qui scanne, le cône turquoise pâle
- **Attaque 1** : *Lecture* — dégâts **8 pattes** — « Lit toutes les pièces. Sauf une. »
- **Attaque 2** : *Demi-tour* — dégâts **100 %** — « Obéit au panneau. Le chat, non. »
- **Faiblesse** : un panneau en carton · pied : Saison 1 · 4/12
- EN : *No Robots Allowed* · Crawler robot · Tin · Very polite · *Reading* 8 legs « Reads every room. Except one. » · *U-turn* 100% « Obeys the sign. The cat doesn't. » · Weakness: a cardboard sign · Season 1 · 4/12
- ES : *Prohibido robots* · Robot rastreador · Hojalata · Muy educado · *Lectura* 8 patas « Lee todas las habitaciones. Menos una. » · *Media vuelta* 100 % « Obedece al cartel. El gato, no. » · Debilidad: un cartel de cartón · Temporada 1 · 4/12

## Le minutage

| # | Début | Durée | Moment | Décor | Personnages et poses | Ce qui se passe à l'image | Réplique (FR) |
|---|---|---|---|---|---|---|---|
| 1 | 0:00 | 5,0 s | **l'amorce** | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Sébastien, tête blasée (`seb-t01`), penché, l'œil plissé | gros plan ; un *bip* de Rampette à la première image ; le radio-réveil : DIM. 10:00 | Sébastien : « Pourquoi le robot n'entre pas dans le bureau de ma fille ? » |
| 3 | 0:05 | 4,0 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Rampette (planche : en marche, puis renversé) ; Sébastien flou au fond | Rampette trottine vers la porte au panneau (un petit robot barré, sans texte), freine des huit pattes, bascule sur le dos ; *bip* triste | — |
| 4 | 0:09 | 4,2 s | **la carte-titre** | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » (derrière la carte) | — | la carte arrive en tournoyant, brille, se retourne ; c'est Rampette qui est dessus | — |
| 5 | 0:13 | 2,0 s |  | volet bleu | — | carton : « Ce matin… » | — |
| 6 | 0:15 | 7,0 s | le monde d'avant | cuisine (`aa-decor-18`) | Kristina (chemise noire du bureau, grandes lunettes dorées) qui traverse, un grand rouleau sous le bras ; Diana assise, un café, qui lui fait un clin d'œil ; Sébastien qui tend le cou | Kristina passe avec un mystérieux rouleau de papier ; Diana et elle échangent un regard complice et pouffent ; Sébastien les regarde l'une, puis l'autre | Sébastien : « Vous préparez quoi, toutes les deux ? » — Kristina : « Rien. » — Diana : « Demande à ton IA. » |
| 7 | 0:22 | 3,6 s |  | bureau de jour (`aa-decor-14`) | Sébastien de dos (`seb-s1-de-dos-v2`), qui s'assoit ; Django assis à ses pieds | l'écran s'allume tout seul ; la caméra plonge dedans | — |
| 8 | 0:25 | 3,0 s |  | plein écran « CRT » (bleu nuit) | Tara (`tara-1`) | le démarrage s'écrit : « TARA 1.3 · Plan de la maison : introuvable » ; Tara apparaît derrière la vitre | — |
| 9 | 0:28 | 6,8 s | **le déclencheur** | bureau de jour (`aa-decor-14`) | Sébastien de dos (`seb-s1-de-dos-v2`) ; Tara derrière la vitre (`tara-2`) | Tara hausse ses six petites épaules | Sébastien : « Tara, Kristina prépare quoi ? » — Tara : « Je ne sais pas. Je n'ai jamais visité la maison. » |
| 10 | 0:35 | 6,6 s |  | bureau de jour (`aa-decor-14`) | Tara fière (`tara-3`) ; un carton sur le bureau ; Rampette (planche : debout) ; Sébastien de face, bras ouverts (planche discours) | *pop* : le carton s'ouvre, Rampette en sort, son gros œil s'allume ; Sébastien le présente comme un trophée | Tara : « Pour tout savoir, il faut tout visiter. » — Sébastien : « Rampette ! Va tout lire ! » |
| 11 | 0:42 | 3,0 s | **la voix ment** | bureau de jour (`aa-decor-14`) | Sébastien, tête solennelle (`seb-tete-nuit-3`) ou discours index levé | gros plan, contre-plongée | Sébastien : « Rien ne lui échappera. » |
| 12 | 0:45 | 5,0 s | les tentatives (1) | cuisine (`aa-decor-18`) | Rampette qui scanne (cône turquoise pâle) ; Diana qui soulève sa tasse pour le laisser passer | il balaie la pièce de son cône ; le moteur écrit au-dessus de lui : « Cuisine : lue ✓ » ; *bip-bip* | Diana : « Il lit le frigo ? » |
| 13 | 0:50 | 5,0 s | (2) | salon (`aa-decor-09-salon-vertical`) | Rampette qui scanne ; Titan avachi sur le canapé (TI1) ; Django qui suit Rampette (trot) ; Sébastien qui suit, fier, les mains dans le dos (marche) | Titan fait le sourd, il est scanné quand même ; « Salon : lu ✓ » ; Django colle Rampette comme une ombre | — |
| 13 | 0:55 | 6,4 s | (3) le motif casse · **le premier tiers** | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Rampette (debout, puis une révérence polie à faire, puis en marche dans l'autre sens) ; Sébastien qui arrive | Rampette ne scanne que le panneau, s'incline, fait demi-tour ; « Bureau de Kristina : interdit » ; Sébastien lui montre la porte, il secoue son gros œil : non | Sébastien : « Mais vas-y ! » |
| 14 | 1:01 | 4,4 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Kristina dans l'entrebâillement (chemise noire, lunettes dorées, planche parole : bras croisés et yeux au ciel) | la porte s'entrouvre, sourcil levé ; elle referme, *clac* | Kristina : « Il sait lire, lui. » |
| 15 | 1:06 | 4,0 s |  | insert : **capture réelle** | — | l'écran de Sébastien : un vrai fichier robots.txt, sur un site de test, qui dit en toutes lettres la même chose que le panneau (« User-agent: * » / « Disallow: /bureau-de-kristina/ ») ; la ligne Disallow se surligne (voir « Captures ») | — |
| 16 | 1:10 | 4,2 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Django (trot, puis assis, `django-d2-assis-talon`) | Django arrive, renifle le panneau, s'assoit devant la porte, sage ; Sébastien à côté de lui | — |
| 17 | 1:14 | 3,4 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Patchy (la charge du taureau, `patchy-pa1-charge-v2`, puis le galop) ; Sébastien et Django | Patchy traverse le plan tête baissée et fonce dans la porte, qui s'ouvre et se referme ; *boing* | Kristina (off) : « PATCHY ! » |
| 18 | 1:17 | 3,6 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Diana qui passe, tasse à la main (marche) | elle ne s'arrête même pas | Diana : « Un panneau, ce n'est pas une serrure. » |
| 19 | 1:21 | 4,2 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Sébastien, tête soupçon (à faire, E13), la flamme de la curiosité | gros plan ; il fixe le panneau, la flamme pousse | Sébastien : « …Qu'est-ce qu'elle cache ? » |
| 20 | 1:25 | 4,2 s | **le clin d'œil boutique** | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Sébastien de face (`seb-m04`, puis `seb-m02` qui pointe) | la caméra plonge sur le t-shirt : « noindex, nofollow introverti » ; il pointe la caméra ; *dring* ; bandeau « Ce t-shirt ? seoaddict.co · « noindex, nofollow introverti » » | Sébastien (babillé, sans sous-titre) : « Le t-shirt ? Sur seoaddict.co. » |
| 21 | 1:29 | 10,0 s | **le retournement** (la moitié) | bureau de jour (`aa-decor-14`) | Sébastien de dos ; Tara derrière la vitre (`tara-2`) ; Kristina qui surgit derrière lui (planche parole : paumes au ciel) | sur l'écran, une ligne s'écrit : « Bureau de Kristina » et, dessous, « Aucune information disponible » | Sébastien : « Tara : le bureau de Kristina ? » — Tara : « Bureau de Kristina. Aucune information disponible. » — Kristina : « Comment elle connaît mon bureau ?! » |
| 22 | 1:39 | 6,0 s |  | plein écran « CRT » (bleu nuit) | Tara, toute petite, qui montre du doigt (`tara-2`) | trois vignettes s'allument, reliées par des flèches à « Bureau de Kristina » : le post-it du frigo (« Kristina : surprise ! », de la main de Diana), le plan de la maison punaisé au bureau, la bulle d'un message de Diana | Tara : « Tout le monde en parle. » |
| 23 | 1:45 | 4,6 s |  | insert : **capture réelle** | — | un vrai résultat de recherche Google pour une page bloquée par robots.txt : le titre, l'adresse, et à la place de la description, la mention que Google n'a pas d'information sur cette page (voir « Captures ») | — |
| 24 | 1:50 | 6,0 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Diana qui repasse, tasse à la main, pouffe (fou rire) ; Kristina, poings serrés, puis qui rit avec elle | Diana avoue, l'air faussement coupable ; Kristina la fusille du regard… et éclate de rire avec elle ; derrière la porte, Sébastien colle l'oreille | Diana : « C'est moi. J'ai écrit « surprise » sur le frigo. » — Kristina : « Doudou ! » |
| 25 | 1:56 | 3,8 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Sébastien, tête sourire en coin (`seb-t02`), la flamme qui grossit | gros plan ; il a tout entendu ; le regard part au plafond | Sébastien : « Une surprise… pour moi. » |
| 26 | 2:00 | 6,0 s | **le rêve** | fond « rêve » + château (`aa-decor-07`) saturé | Sébastien en araignée de fer-blanc (à faire : son buste sur le corps rond de Rampette, huit pattes de métal, un gros œil-caméra en guise de lunettes) ; Rampette, le vrai, qui le suit, inquiet | l'ondulation et les clochettes ; il cavale sur les toits de Tarascon et lit tout de son cône turquoise ; les étiquettes s'écrivent : « Château : lu ✓ », « Boulangerie : lue ✓ », « Olympe : lue ✓ » (elle grogne) ; il arrive devant une porte avec un panneau… et la scanne quand même | Sébastien : « Je lis tout ! Même les surprises ! » |
| 27 | 2:06 | 2,2 s |  | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Kristina, tête regard noir (à faire, E10) | coupe sèche (*scratch*) ; gros plan | Kristina : « Non. » |
| 28 | 2:08 | 3,6 s | **tout est perdu** | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Kristina assise par terre contre sa porte, le panneau sur les genoux (à faire) ; Diana assise à côté d'elle, la tasse entre les mains ; Rampette qui s'approche, l'œil penché (debout) | elle regarde le panneau ; Rampette pose une patte sur son genou | Kristina : « Mon panneau ne sert à rien. » |
| 29 | 2:11 | 7,4 s | **la pépite** | couloir, la porte du bureau de Kristina (à faire) + calque « panneau » | Kristina, têtes de gros plan (parle, puis sourire en coin) ; Rampette au bord du cadre | gros plan de Kristina ; l'idée s'allume ; le bandeau : « robots.txt bloque l'exploration, pas l'indexation » / « Pour rester hors de Google : noindex… et laisser le robot le lire. » | Kristina : « Pour qu'il n'en parle pas… il faut le laisser entrer. » — Kristina : « Et lui dire : pas un mot. » |
| 30 | 2:19 | 7,0 s | **la chute** | bureau de Kristina, de jour (à faire) | Kristina (décroche le panneau, à faire) ; Rampette (marche, scanne, s'incline) ; sur le clavier, une carte (une bouche fermée par une fermeture éclair) ; l'écran de Kristina, tourné vers le mur | elle ouvre grand la porte ; Rampette entre, scanne le bureau : son cône passe sur l'écran tourné vers le mur, qui s'illumine (on ne voit pas ce qu'il montre) ; il lit la carte, hoche l'œil, ressort sur la pointe des pattes | Kristina : « Tu regardes. Tu ne racontes rien. » |
| 31 | 2:26 | 6,6 s |  | bureau de jour (`aa-decor-14`) | Sébastien de dos, puis tête dépit ; Tara derrière la vitre, polie (`tara-1`) ; à la porte, Diana et Kristina, bras dessus bras dessous, qui pouffent | sur l'écran, la ligne « Bureau de Kristina » ne s'écrit plus ; Tara sourit, polie | Sébastien : « Tara, Kristina prépare quoi ? » — Tara : « Je sais. Mais je n'ai pas le droit de le dire. » |
| 32 | 2:32 | 3,8 s |  | bureau de jour (`aa-decor-14`) | Kristina (planche parole : pointe du doigt en riant) ; Diana, fou rire ; Sébastien de face, il baisse les yeux sur son t-shirt (tête yeux baissés, à faire, E14) | elle montre l'imprimé « noindex » sur le t-shirt de son père ; il le découvre ; Diana rit avec elle | Kristina : « C'était écrit sur ton t-shirt. » |
| 33 | 2:36 | 6,0 s | **la révélation** | bureau de Kristina, de jour (à faire) | Kristina qui retourne son écran (planche « jour » : l'ordinateur, en montrant la caméra) ; Diana, les mains jointes ; Sébastien, tête béate (`seb-t04`) ; Olympe sur le seuil | la surprise : sur l'écran, **le nouveau site de Sébastien** (une page d'accueil dessinée : sa photo… et, plus grande, celle d'Olympe) ; un bandeau en haut de la page : « pas un mot » (le noindex, en image) ; Sébastien fond | Kristina : « Surprise ! Ton nouveau site. » — Diana : « Lundi, on enlève le « pas un mot ». » |
| 34 | 2:42 | 3,4 s | l'appel | couloir, la porte du bureau de Kristina, sans panneau (à faire) | Rampette qui avance vers la caméra (en marche) | le bandeau, en grand : « Abonne-toi : ici, aucun panneau. » | Kristina (off, sans sous-titre) : « Abonne-toi : ici, aucun panneau. » |
| 35 | 2:46 | 3,6 s | **la boucle** | couloir, la porte du bureau de Kristina, sans panneau (à faire) | Rampette sur le seuil (debout) ; Kristina dans l'embrasure | la porte grande ouverte, sans panneau ; Rampette s'arrête quand même sur le seuil, *bip* ; Kristina lui fait signe d'entrer | Kristina : « Entre. Mais pas un mot. » |

**Total : 169,6 s (2:49)**, dans la fourchette de 150 à 179 s. 35 plans. Chaque réplique tient dans son plan (au moins 1,5 s par sous-titre, dans les trois langues).

Repères (bible, § 7) : la carte-titre à 0:09 ; le déclencheur à 0:28 ; le premier tiers à 0:55 (33 %) ; le clin d'œil boutique à 1:25 ; le retournement à 1:29 (53 %) ; le rêve à 2:00 (71 %) ; tout est perdu à 2:08 ; la pépite à 2:11 (78 %) ; la chute à 2:19 ; la boucle à 2:46.

## Les répliques (FR, EN, ES)

La traduction garde le gag, pas les mots. « Rampette », « Tara » et « Patchy » restent des noms propres dans les trois langues. Les textes à l'écran se traduisent aussi :
- démarrage : « TARA 1.3 · Plan de la maison : introuvable » / « TARA 1.3 · House map: not found » / « TARA 1.3 · Plano de la casa: no encontrado »
- cartons : « Ce matin… » / « This morning… » / « Esta mañana… » ; radio-réveil « DIM. 10:00 » / « SUN 10:00 AM » / « DOM. 10:00 »
- étiquettes de Rampette : « Cuisine : lue ✓ » / « Kitchen: read ✓ » / « Cocina: leída ✓ » ; « Salon : lu ✓ » / « Living room: read ✓ » / « Salón: leído ✓ » ; « Bureau de Kristina : interdit » / « Kristina's office: forbidden » / « Despacho de Kristina: prohibido » ; dans le rêve : « Château : lu ✓ », « Boulangerie : lue ✓ », « Olympe : lue ✓ » (traduits dans le tableau)
- l'écran de Tara : « Bureau de Kristina » / « Aucune information disponible » — « Kristina's office » / « No information available » — « Despacho de Kristina » / « No hay información disponible »
- le post-it du frigo : « Kristina : surprise ! » / « Kristina: surprise! » / « Kristina: ¡sorpresa! » ; la bulle du message de Diana : une icône de porte et un cœur, sans texte
- le nouveau site, sur l'écran de Kristina : « Sébastien · SEO · Tarascon · (en construction : pas un mot) » (traduit dans le tableau)
- bandeau de la pépite : « robots.txt bloque l'exploration, pas l'indexation » / « Pour rester hors de Google : noindex… et laisser le robot le lire. » — EN « robots.txt blocks crawling, not indexing » / « To stay out of Google: noindex… and let the robot read it. » — ES « robots.txt bloquea el rastreo, no la indexación » / « Para quedar fuera de Google: noindex… y dejar que el robot lo lea. »
- bandeau de l'appel : « Abonne-toi : ici, aucun panneau. » — EN « Subscribe: no sign here. » — ES « Suscríbete: aquí no hay cartel. »
- clin d'œil : « Ce t-shirt ? seoaddict.co · « noindex, nofollow introverti » » (le titre du modèle d'après les fiches EN et ES de la boutique)

| # | Qui | FR | EN | ES |
|---|---|---|---|---|
| 1 | Sébastien | Pourquoi le robot n'entre pas dans le bureau de ma fille ? | Why won't the robot go into my daughter's office? | ¿Por qué el robot no entra en el despacho de mi hija? |
| 6 | Sébastien | Vous préparez quoi, toutes les deux ? | What are you two up to? | ¿Qué estáis tramando, vosotras dos? |
| 6 | Kristina | Rien. | Nothing. | Nada. |
| 6 | Diana | Demande à ton IA. | Ask your AI. | Pregúntale a tu IA. |
| 8 | *écran* | TARA 1.3 · Plan de la maison : introuvable | TARA 1.3 · House map: not found | TARA 1.3 · Plano de la casa: no encontrado |
| 9 | Sébastien | Tara, Kristina prépare quoi ? | Tara, what's Kristina up to? | Tara, ¿qué prepara Kristina? |
| 9 | Tara | Je ne sais pas. Je n'ai jamais visité la maison. | No idea. I've never seen the house. | No lo sé. Nunca he visitado la casa. |
| 10 | Tara | Pour tout savoir, il faut tout visiter. | To know everything, you must visit everything. | Para saberlo todo, hay que visitarlo todo. |
| 10 | Sébastien | Rampette ! Va tout lire ! | Rampette! Go read everything! | ¡Rampette! ¡Ve a leerlo todo! |
| 11 | Sébastien | Rien ne lui échappera. | Nothing will escape him. | Nada se le escapará. |
| 12 | Diana | Il lit le frigo ? | Is he reading the fridge? | ¿Está leyendo la nevera? |
| 13 | Sébastien | Mais vas-y ! | Go on! | ¡Venga, entra! |
| 14 | Kristina | Il sait lire, lui. | At least he can read. | Él, al menos, sabe leer. |
| 17 | Kristina (off) | PATCHY ! | PATCHY! | ¡PATCHY! |
| 18 | Diana | Un panneau, ce n'est pas une serrure. | A sign isn't a lock. | Un cartel no es una cerradura. |
| 19 | Sébastien | …Qu'est-ce qu'elle cache ? | …What's she hiding? | …¿Qué esconde? |
| 20 | Sébastien (babillé, sans sous-titre) | Le t-shirt ? Sur seoaddict.co. | The t-shirt? On seoaddict.co. | ¿La camiseta? En seoaddict.co. |
| 21 | Sébastien | Tara : le bureau de Kristina ? | Tara: Kristina's office? | Tara: ¿el despacho de Kristina? |
| 21 | Tara | Bureau de Kristina. Aucune information disponible. | Kristina's office. No information available. | Despacho de Kristina. No hay información disponible. |
| 21 | Kristina | Comment elle connaît mon bureau ?! | How does she know my office?! | ¡¿Cómo conoce mi despacho?! |
| 22 | Tara | Tout le monde en parle. | Everybody talks about it. | Todo el mundo habla de él. |
| 24 | Diana | C'est moi. J'ai écrit « surprise » sur le frigo. | My fault. I wrote "surprise" on the fridge. | Fui yo. Escribí «sorpresa» en la nevera. |
| 24 | Kristina | Doudou ! | Doudou! | ¡Doudou! |
| 25 | Sébastien | Une surprise… pour moi. | A surprise… for me. | Una sorpresa… para mí. |
| 26 | Sébastien | Je lis tout ! Même les surprises ! | I read everything! Even surprises! | ¡Lo leo todo! ¡Hasta las sorpresas! |
| 26 | *étiquettes* | Château : lu ✓ · Boulangerie : lue ✓ · Olympe : lue ✓ | Castle: read ✓ · Bakery: read ✓ · Olympe: read ✓ | Castillo: leído ✓ · Panadería: leída ✓ · Olympe: leída ✓ |
| 27 | Kristina | Non. | No. | No. |
| 28 | Kristina | Mon panneau ne sert à rien. | My sign is useless. | Mi cartel no sirve para nada. |
| 29 | Kristina | Pour qu'il n'en parle pas… il faut le laisser entrer. | To keep him from talking… you have to let him in. | Para que no hable de él… hay que dejarle entrar. |
| 29 | Kristina | Et lui dire : pas un mot. | And tell him: not a word. | Y decirle: ni una palabra. |
| 30 | Kristina | Tu regardes. Tu ne racontes rien. | You look. You don't tell. | Miras. No cuentas nada. |
| 31 | Sébastien | Tara, Kristina prépare quoi ? | Tara, what's Kristina up to? | Tara, ¿qué prepara Kristina? |
| 31 | Tara | Je sais. Mais je n'ai pas le droit de le dire. | I know. But I'm not allowed to say. | Lo sé. Pero no puedo decirlo. |
| 32 | Kristina | C'était écrit sur ton t-shirt. | It was written on your t-shirt. | Lo ponía en tu camiseta. |
| 33 | Kristina | Surprise ! Ton nouveau site. | Surprise! Your new website. | ¡Sorpresa! Tu nueva web. |
| 33 | Diana | Lundi, on enlève le « pas un mot ». | Monday, we take off the "not a word". | El lunes quitamos el «ni una palabra». |
| 33 | *écran* | Sébastien · SEO · Tarascon · (en construction : pas un mot) | Sébastien · SEO · Tarascon · (under construction: not a word) | Sébastien · SEO · Tarascón · (en obras: ni una palabra) |
| 34 | Kristina (off, sans sous-titre) | Abonne-toi : ici, aucun panneau. | Subscribe: no sign here. | Suscríbete: aquí no hay cartel. |
| 35 | Kristina | Entre. Mais pas un mot. | Come in. But not a word. | Entra. Pero ni una palabra. |

## Le son

- **Première image** : un *bip* de Rampette, sec.
- **Rampette** : sa voix est à inventer dans le moteur (des cliquetis métalliques et un petit *bip* par syllabe) ; huit petites pattes qui tapotent le carrelage ; *bip-bip* joyeux quand une pièce est « lue », *bip* descendant et triste devant le panneau ; il bascule sur le dos avec un *pouet*.
- **La carte-titre** : *whoosh*, *tada*, *whoosh*.
- **La cuisine** : le froissement du grand rouleau de Kristina, les deux rires étouffés de Diana et de Kristina (babil).
- **Tara** : *crt*, *clavier*, *pop* + *tada* au démarrage (trois secondes) ; ses réponses en gazouillis de modem.
- **Le carton de Rampette** : *pop*.
- **La porte** : *clac* quand Kristina referme ; *boing* quand Patchy fonce dedans ; Django s'assoit en silence (c'est le gag).
- **Les inserts réels** : *clavier* ; un petit *ding* quand la ligne Disallow se surligne.
- **L'aveu de Diana** : son fou rire, puis celui de Kristina par-dessus.
- **Le clin d'œil** : *whoosh*, *ding*.
- **Le rêve** : l'ondulation et **les clochettes** ; ses huit pattes de fer-blanc qui cavalent sur les tuiles ; un *bip* par étiquette « lu ✓ » ; le grognement d'Olympe.
- **La sortie du rêve** : *scratch*.
- **La pépite** : la musique se tait, *pop* au bandeau.
- **La chute** : la porte qui s'ouvre en grand (sans grincement) ; Rampette sur la pointe des pattes (cliquetis ralentis) ; l'écran de Kristina qui s'illumine dans le cône (*pop* doux).
- **La révélation** : *tada*, puis le ukulélé qui reprend, tendre.
- Musique : le ukulélé, avec une petite marche pizzicato pour la tournée de Rampette, qui s'arrête net devant la porte.

## Ce qu'il faut fabriquer

Toutes les images partent de l'image maître du personnage, jointe au prompt (méthode en étoile, une seule chose changée à la fois), sur fond vert uni **#00B140**, puis détourage local. Aucune marque, aucun texte lisible. Les décors sont verticaux (2:3, 1024 × 1536), ternes, « CRT », et passent par l'étalonnage du décor seulement.

**Déjà là** : le bureau de jour, la cuisine, le salon vertical, le château ; Rampette (planche de 4 poses : debout, en marche, qui scanne, renversé) ; Kristina (têtes, planche parole, planche « jour » découpée : `banque/kristina-jour-1..4`, garde-robe : la chemise noire du bureau et les grandes lunettes dorées) ; Diana (marche, planche parole, planche expressions découpée : fou rire) ; Sébastien (têtes, discours, de dos, m02, m04) ; Django (trot, assis au talon) ; Patchy (la charge, le galop) ; Titan (TI1, à vérifier) ; Olympe (o1) ; Tara ; la flamme ; la carte-titre.

**À fabriquer**

1. **Le couloir, avec la porte du bureau de Kristina** (décor vertical, plans 1 à 3, 13 à 20, 24, 25, 27 à 29, 34, 35).
   > Vertical 2:3 background, cheap late-1990s low-poly 3D, flat lighting, hard dark contact shadows, blurry stretched photo textures, muted greyish "old CRT TV" colours: the upstairs corridor of a Provençal stone house, terracotta tiled floor, beige-grey plaster walls, a closed wooden door in the centre at the far end of the corridor, a small console table with a lamp, one framed abstract picture stuck on the wall like a sticker. Empty and slightly melancholic. Eye-level, frontal, stiff staging. No characters, no text, no logo.
2. **Le panneau de la porte** (calque).
   > A small hand-made cardboard door sign hanging from a string, drawn with thick marker: a cute tin spider-robot silhouette with one big eye, crossed out by a big red diagonal bar inside a red circle. Slightly crumpled cardboard texture, 1998 cheap 3D look. Isolated on plain flat chroma green background #00B140, NO letters, no logo.
3. **Le bureau de Kristina, de jour** (décor vertical, plans 30 et 33) : la pièce où elle travaille, chez ses parents.
   > Vertical 2:3 background, cheap late-1990s low-poly 3D, flat lighting, muted greyish colours: a small home office in a Provençal stone house used by a young adult woman, a wooden desk with a computer monitor turned towards the wall, a keyboard, a desk lamp, a mug of pens, a corkboard with blank sketches, a big rolled-up poster leaning in a corner, a few houseplants, a string of fairy lights. Decorations stuck on the walls like stickers. Empty. No characters, no text, no logo.
4. **La carte « pas un mot »** (calque, posée sur le clavier).
   > A small white folded card standing on a keyboard, with only a hand-drawn pictogram: a closed mouth sealed by a zip fastener. Cheap 1998 3D look. Plain flat chroma green background #00B140, no letters.
5. **Rampette, poses de plus** (planche de 4, plans 13, 30, 35) : une révérence polie (l'avant du corps baissé, une patte avant levée comme un chapeau) ; qui secoue son gros œil de gauche à droite (« non ») ; sur la pointe des pattes ; renversé **sur le dos** (la pose faite le montre sur le côté).
   > Using the attached master sheet of this character (a small dented tin-plate spider robot the size of a cat, round riveted body with rust spots, eight articulated metal legs, one big round camera eye with a painted iris, a tiny antenna; low-poly 1998 PlayStation-era 3D, visible facets, blurry low-res texture, flat lighting, muted colours), sheet of 4 poses: a polite bow, front lowered, one front leg raised like tipping a hat; shaking its big eye left to right meaning "no"; tiptoeing on the very tips of its legs; fallen flat on its back, legs in the air. Plain flat chroma green background #00B140, no text.
6. **Kristina, planche de 4 poses dans la chemise noire du bureau** (plans 5, 28, 30, 33) : elle traverse avec un grand rouleau sous le bras, un clin d'œil ; assise par terre, adossée à sa porte, un panneau sur les genoux ; elle décroche le panneau ; elle retourne l'écran de son ordinateur vers la caméra, rayonnante.
   > Using the attached master image of this young woman (red-copper chin-length bob with a straight fringe kept in COLOUR, big gold square retro glasses, dental braces, small nose ring, pearl choker; pale grey skin, pipe-cleaner limbs) in a black shirt over a striped t-shirt. Sheet of 4 full-body poses: walking with a big rolled-up poster under her arm, winking; sitting on the floor, back against a door, a small cardboard sign on her knees, deflated; unhooking a sign from a door handle; turning a computer monitor towards the viewer with both hands, beaming, braces showing. Stiff cut-out puppet style, real photographed fabric. Plain flat chroma green background #00B140, no text, no logo.
7. **Sébastien en araignée de fer-blanc** (le rêve, plan 26) : son buste sur le corps rond de Rampette.
   > Using the attached master image (same face, glasses, asymmetric smile, grey skin, HYPER FLASHY fuchsia-pink t-shirt) and the attached tin robot sheet: the man's head and pink-t-shirted torso fused onto a round dented tin-plate body with eight articulated metal legs, galloping, a turquoise scanning cone coming out of his glasses, gleeful. Low-poly 1998 look for the metal parts, photocopied face. Plain flat chroma green background #00B140, no text, no logo.
8. **Les têtes de Sébastien et de Kristina qui manquent** : Sébastien E13 soupçon (plan 19) et E14 yeux baissés (plan 32) ; Kristina regard noir (plan 27). Une tête par prompt, en étoile depuis la tête maître, une seule expression changée.
9. **Les trois vignettes de Tara** (plan 22) : le post-it du frigo, le plan de la maison punaisé, une bulle de message avec une icône de porte et un cœur ; le moteur peut les dessiner comme ses post-it.
10. **La page d'accueil du nouveau site** (plan 33) : dessinée dans le moteur, sur l'écran de Kristina (sa photo en petit, celle d'Olympe en grand, le bandeau « pas un mot ») ; aucune capture d'un vrai site.

**Dans le moteur** : le démarrage « TARA 1.3 » (trois secondes) ; les étiquettes qui s'écrivent au-dessus de Rampette (« Cuisine : lue ✓ ») et dans le rêve, dans le style du démarrage de Tara ; le cône de scan (la pose existe) qui balaie ; la porte qui s'ouvre et se referme (deux états du décor, ou un calque) ; la voix de Rampette.

**Captures et enregistrements d'écran**

1. **Un vrai fichier robots.txt** (plan 15, 4 s). Sur un site de test de Kōeki (pas un site de client), créer un dossier `/bureau-de-kristina/` et un robots.txt qui contient « User-agent: * » et « Disallow: /bureau-de-kristina/ » ; l'ouvrir dans le navigateur, à son adresse, et enregistrer l'écran ; surligner la ligne Disallow au montage. **Anonymisation** : flouter le nom de domaine dans la barre d'adresse et tout onglet ouvert ; pas de favori ni d'avatar visible.
2. **Un vrai résultat Google sans description** (plan 23, 4,6 s). Il faut un résultat pour une page bloquée par robots.txt et pourtant indexée : la chercher d'abord sur les sites de Kōeki (le rapport « Indexation des pages » de la Search Console liste ces pages), ou, à défaut, sur une page publique connue pour l'être. Enregistrer la page de résultats sur ordinateur ou sur mobile. **Anonymisation** : flouter le nom de domaine, le titre s'il nomme une entreprise ou une personne, et les résultats voisins ; garder l'interface. [PENSER : le libellé exact affiché par Google à la place de la description est à relever sur la capture elle-même ; la documentation dit seulement que le résultat « n'aura pas de description »]
3. **(Facultatif, pour le commentaire épinglé)** le rapport « Indexation des pages » de la Search Console d'un site de Kōeki montrant le motif des pages indexées malgré le blocage par robots.txt, domaine flouté. [PENSER : libellé français exact à relever à la capture]

## Le clin d'œil boutique (1:25, 4,2 s)

Dans le couloir, juste après « Qu'est-ce qu'elle cache ? », pendant que Sébastien, la flamme sur la tête, fixe la porte : la caméra plonge sur le t-shirt rose, l'imprimé **« noindex, nofollow introverti »** (n° 010), il pointe la caméra, *dring*, bandeau « Ce t-shirt ? seoaddict.co · « noindex, nofollow introverti » ». Il colle deux fois : l'introvertie de l'histoire, c'est la porte de Kristina ; et le mot « noindex », que personne ne remarque à 1:25, est la solution que Kristina lui mettra sous le nez à 2:32 (« C'était écrit sur ton t-shirt »). C'est le seul épisode où le t-shirt est aussi une installation. Fichier : `media-local/flocages/FR-010 - … - pour t-shirt foncé.png` [PENSER : nom exact à relever sur le Drive] ; fiche produit FR, EN, ES à relever et à vérifier (commandable ou non) avant la mise en ligne.

## Titre et description proposés pour YouTube (à valider)

- **FR** : « Pourquoi le robot n'entre pas dans le bureau de ma fille 🚫🤖 · Les Tarasconnades ép. 5 »
  « Un panneau "interdit aux robots" sur la porte… et l'IA parle quand même du bureau. Parce que robots.txt empêche d'explorer, pas d'indexer : une page bloquée peut apparaître dans Google, sans description, si d'autres pages parlent d'elle. Pour rester hors de Google, c'est noindex, et le robot doit pouvoir le lire (documentation de Google Search Central). Le t-shirt de Sébastien : seoaddict.co/fr/… #robotstxt #seo #indexation »
  - commentaire épinglé : « Vous aussi, vous avez une page "interdite aux robots"… qui sort quand même dans Google ? 👀 »
- **EN** : « Why won't the robot go into my daughter's office 🚫🤖 · Les Tarasconnades ep. 5 »
  « A "no robots" sign on the door… and the AI still talks about the office. Because robots.txt stops crawling, not indexing: a blocked page can still show up in Google, without a description, if other pages talk about it. To stay out of Google, use noindex, and let the robot read it (Google Search Central documentation). Sébastien's t-shirt: [EN link] #robotstxt #seo #indexing »
  - pinned comment: « Do you also have a "no robots" page… that still shows up on Google? 👀 »
- **ES** : « ¿Por qué el robot no entra en el despacho de mi hija? 🚫🤖 · Les Tarasconnades ep. 5 »
  « Un cartel de "prohibido robots" en la puerta… y la IA sigue hablando del despacho. Porque robots.txt impide rastrear, no indexar: una página bloqueada puede salir en Google, sin descripción, si otras páginas hablan de ella. Para quedar fuera de Google: noindex, y que el robot pueda leerlo (documentación de Google Search Central). La camiseta de Sébastien: [enlace ES] #robotstxt #seo #indexación »
  - comentario fijado: « ¿Tú también tienes una página "prohibida a los robots"… que igual sale en Google? 👀 »

## À trancher par Sébastien

- **Le bureau de Kristina** chez vous : existe-t-il ? (voir la ligne en tête de fiche).
- **La surprise** : ton nouveau site, gardé en « pas un mot » (noindex) jusqu'au lancement. Ça te va, ou préfères-tu une autre surprise (un dessin animé de toi, un cadeau) ? La pépite ne change pas.
- **Le flocage** n° 010 « noindex, nofollow introverti » : nom exact du fichier, liens des fiches FR, EN, ES, commandable ou non.
- **La capture du résultat sans description** : sur une page de Kōeki, ou une page publique d'un autre site (floutée) si aucune page de Kōeki ne se trouve dans ce cas.
