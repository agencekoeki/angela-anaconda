---
title: "Sébastien Anaconda"
personnage: "Sébastien Anaconda"
statut_image_maitre: "en cours"
last_updated: 2026-10-29
---

# Sébastien Anaconda

## Reconnaissable à

- Le visage est une photo en noir et blanc très contrastée, façon photocopie, aux blancs laiteux. La seule couleur du visage, ce sont les **iris bleu vif**, comme les taches de rousseur d'Angela sont sa seule touche de couleur.
- Le crâne est rasé, avec une barbe courte poivre et sel, des **lunettes de vue** à monture rectangulaire foncée et des oreilles bien dégagées. Comme chez Angela, la tête est grosse sur un corps filiforme.
- **Le visage est légèrement asymétrique, et c'est un trait de reconnaissance.** Il faut le garder sur chaque visage de rechange, sans jamais le forcer en grimace :
  - la paupière droite (à gauche de l'image quand il est de face) tombe un peu ;
  - l'œil droit se ferme parfois à moitié, selon la direction du regard ;
  - le coin droit de la bouche se lève moins que le gauche, si bien que le sourire monte surtout à gauche.
  
  C'est justement l'esprit du sourire en coin d'Angela.
- La peau est **grise partout** : visage, cou, bras, mains et jambes. C'est un gris argenté froid, pâle, plat, sans modelé et sans la moindre teinte rose. Le détourage (`tools/detourage.py`) ramène au gris tout ce qui est peu saturé.
- **Le t-shirt reste rose HYPER FLASHY** : un rose fuchsia saturé, presque fluo. C'est la tache de couleur du personnage, et le contraste avec la peau grise est voulu. On ne l'adoucit jamais.
- Les membres sont fins comme des cure-pipes, **sans articulation visible**. Les mains sont découpées, avec des doigts filiformes.
- Les vêtements sont de vraies textures de tissu froissé photographié, rigides, posées sur des formes simples.
- **La tenue d'été** :
  - un t-shirt rose à manches courtes ;
  - un boardshort de surf, rayé en diagonale gris anthracite et noir, avec un panneau latéral à damier de losanges blancs, un fin passepoil rouge, et ni marque ni logo ;
  - des tongs de plage épaisses et confortables, gris foncé.
- **Le tatouage**, sur le bas de la jambe gauche : un lézard d'inspiration polynésienne. Son corps est noir plein, orné de motifs tribaux, avec un cercle concentrique sur l'extérieur et l'arrière du mollet. Ses pattes à quatre doigts atteignent l'intérieur du tibia, l'une à mi-mollet, l'autre au-dessus de la malléole intérieure. La queue passe devant la cheville et s'enroule sur le dessus du pied, vers le gros orteil.
- **Les chaussures fermées**, pour l'agility et les balades avec les chiens : des chaussures de trail basses, un peu massives.
  - La tige est en mesh bleu pétrole (sarcelle), plus foncée, gris ardoise, sur l'avant et le bas des côtés.
  - Une **bande orange vif** fait le tour au ras de la semelle intermédiaire, de la pointe au talon.
  - Le col du talon est rembourré de noir, avec un pare-pierre gris clair à l'avant.
  - La semelle blanche porte de gros crampons en dents de scie.
  - **Les lacets sont mouchetés orange et noir.** C'est le détail qui les fait reconnaître.
  - Elles se portent avec des socquettes blanches. Elles n'ont aucun logo.
- **Une deuxième paire de lunettes**, à monture claire (vue sur une photo aux pivoines).
- **Les accessoires possibles** : des lunettes de sport à verres miroir, un sac à dos noir à bretelles rouges, une laisse, et le sweat rouge à capuche (celui sur lequel Patchy grimpait).

## La liste de production

Elle reprend le catalogue d'Angela (`kb/personnages/angela.md`, codes E et P). Chaque élément est une variation en étoile, depuis l'image maître (`media-local/sebastien-banque/aa-seb-m04-bras-le-long.png`, issue de `aa-seb-m01-asymetrie.png`), avec une seule chose changée à la fois. Il anime par **remplacement** : têtes entières en gros plan, poses entières en plan large (skill koeki-anaconda, `references/animation.md`).

**Fait au 30/10/2026** (`media-local/sebastien-banque/`, découpes dans `media-local/atelier-animation/assets/`) :
- les têtes entières : t00 grand sourire (maître), t01 blasé, t02 sourire en coin, t03 dépit, t04 béat, t05 cri ;
- les têtes de bouche, en étoile depuis t01 : A, O, OU, I/É, M/B/P, F/V, L ;
- les poses : m02 blasé (doigt vers nous), m03 sourire en coin, m04 bras le long, m05 sweat rouge, m06 poings sur les hanches, s1 de dos, s2 main ouverte, s3 course d'agility ;
- les planches de quatre poses : la marche, le discours (bras ouverts, index levé, main sur le cœur, paumes en avant), les poses clés (doigt pointé vers nous, affalé boudeur, saut bras levés, « c'est par là »), la course en tenue d'agility.

**À faire** :
- les têtes E07 dédain, E13 soupçon, E11 émerveillé, E09 plainte, E10 regard noir, E12 langue tirée, E14 yeux baissés, E15 ensommeillé ;
- une série loufoque pour l'imaginaire ;
- les poses P05 à P26, et celles propres à Sébastien : Patchy perché sur son épaule (en sweat rouge), assis en tailleur avec un chat ;
- les tenues : l'hiver, un pyjama, l'imaginaire (pompier, astronaute, chef d'orchestre) ;
- des scènes d'ancrage d'après ses photos (les meilleures le montrent à l'agility : il est presque toujours derrière l'appareil).

**Les photos de référence** : `media-local/references/sebastien/` (16 photos), deux photos de téléphone pour le tatouage, une photo de famille pour le boardshort.

## Le prompt d'ancrage

> Original cut-out puppet character. Face: high-contrast black-and-white photocopy of the man in the reference photo, milky whites, bright blue irises as the only colour. Shaved head, short salt-and-pepper beard, dark rectangular glasses. Subtle natural facial asymmetry to keep in every expression: his RIGHT upper eyelid (viewer's left) droops slightly and that eye can look a little more closed; the RIGHT corner of his mouth (viewer's left) lifts less, so smiles rise mostly on his left side (viewer's right). Subtle, never a grimace. Pale flat COOL SILVER-GREY skin everywhere, never pink, pipe-cleaner thin limbs with no visible joints, cut-out hands with spindly fingers. Clothes made of real photographed crumpled fabric, stiff, on simple shapes: HYPER FLASHY saturated fuchsia-pink short-sleeved t-shirt, charcoal/black diagonal-striped surf boardshorts with a white diamond-grid side panel and thin red piping (no logo), thick dark-grey beach flip-flops. Polynesian lizard tattoo on the LEFT lower leg as described. Big head: head height = 27.5% of the total height. Eye-level, frontal, stiff staging, 4:3, no text, no logo.
