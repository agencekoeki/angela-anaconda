---
title: "Les poses de référence pour l'animation"
scope: "La liste courte des poses à fabriquer, sur fond vert ou transparent, pour chaque membre de la clique. Elles servent de références pour l'animation de la scène d'accueil, et pour régénérer plus tard sans dérive."
last_updated: 2026-10-30
---

# Les poses de référence

> Au 30/10/2026, le film d'accueil a été fait avec des **planches de quatre poses entières** (voir `scene-accueil.md` et le skill koeki-anaconda, `references/animation.md`). La liste ci-dessous reste la liste des poses signatures ; l'état à jour est dans `a-faire.md` et dans chaque fiche.

Ce n'est pas une banque de 500 images : seulement les poses dont la scène d'accueil a besoin, et une ou deux poses signatures par personnage. Chaque pose part de l'image maître du personnage, sur fond vert ou transparent, en pied.

| Personnage | Code | Pose | Sert à | État |
|---|---|---|---|---|
| Sébastien | S1 | De dos, debout, il attend | Plan 1 | fait (v2 : tête à +7 %) |
| Sébastien | P03 | Le doigt pointé | Plan 2 | fait (maître) |
| Sébastien | P02 | La main ouverte vers Django | Plan 4 | fait |
| Sébastien | S2 | Il court, en tenue d'agility, chaussures de trail | Plan 5 | fait (tête à +6 %) |
| Sébastien | S3 | De trois quarts, il regarde la mer | Plan 7 | à faire |
| Sébastien | P01 | Bras le long du corps | Plans 7 et 8 | fait (m04) |
| Django | D1 | Au trot de profil, queue en panache | Plans 4 et 5 | fait |
| Django | D2 | Assis au talon, il lève les yeux | Plan 4 | fait |
| Django | D3 | En plein saut d'obstacle | Plan 5 | à faire |
| Olympe | O1 | Couchée, elle refuse d'avancer | Plan 6 | fait |
| Olympe | O2 | Couchée, elle aboie, gueule ouverte | Plan 6 | fait |
| Patchy | PA1 | La charge du taureau, en pleine course, tête baissée | Plan 6 | en cours |
| Patchy | PA2 | Une balle dans la gueule | Signature | à faire |
| Souka | SO1 | Assis, dos tourné, hautain | Signature | à faire |
| Lilou | LI1 | Le dos rond, hérissée, elle revient tenir tête | Signature | à faire |
| Kali | KA1 | Assise en « petite barrique », trapue (le portrait est à refaire) | Signature | à faire |
| Titan | TI1 | Avachi comme un coussin, il fait le sourd | Signature | à faire |
| Diana | DI0 | L'image maître, en robe verte | Plus tard | à faire |
| Kristina | KR0 | L'image maître | Plus tard | à faire |

Les règles d'anatomie, vérifiées sur les photos et non d'après la race : Django a une **queue entière**, en panache. Assis, elle repose au sol et s'enroule autour des pattes. En mouvement, elle se relève au-dessus du dos.

Chaque pose humaine passe par `tools/mesure_tete.py` avant d'être validée. La tolérance est de −5 % en plus petit et de +25 % en plus gros, parce qu'une tête plus grosse renforce le style.
