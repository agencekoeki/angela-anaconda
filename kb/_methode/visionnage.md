---
title: "Méthode de visionnage des épisodes"
scope: "Comment les découpages de kb/episodes/ sont établis : source, planches-contact, transcription, étiquettes, limites. À lire avant de s'appuyer sur une étiquette [VU À L'IMAGE] ou [TRANSCRIPTION AUTO]."
last_updated: 2026-10-29
---

# Méthode de visionnage

C'est la méthode de [l'encyclopédie *The IT Crowd*](https://github.com/agencekoeki/the-it-crowd), adaptée à une série en découpages animés et à une chaîne rangée en compilations.

## Source

- Chaîne YouTube officielle **« Angela Anaconda - Wildbrain »** ([@AngelaAnacondaWildbrain](https://www.youtube.com/@AngelaAnacondaWildbrain)). WildBrain détient le catalogue de Decode Entertainment, qui a produit la série.
- Aucune autre source vidéo n'est utilisée. Des chaînes non officielles mettent en ligne la série entière, mais elles ne servent jamais, même pour combler un trou.
- Chaque découpage donne dans son en-tête l'identifiant de la vidéo (`source_video`) et le minutage du segment dans cette vidéo. Comme la chaîne publie surtout des compilations, ce minutage est indispensable. Voir `couverture-chaine.md`.

## Procédé

1. **Repérage.** Pour la vidéo, on relève le titre, la durée, la description et les chapitres. On cherche le carton-titre de chaque segment : le titre et le scénariste sont incrustés en lettres orangées sur la première image du segment.
2. **Transcription.** On lit la transcription automatique de YouTube, avec ses minutages, pour comprendre qui fait quoi. Elle reste un outil de travail : **aucune réplique n'est recopiée dans les découpages**, même courte.
3. **Planches-contact.** La vidéo est parcourue par sauts réguliers, et les images obtenues sont assemblées dans la page en planches de 32 vignettes, légendées du minutage, sans rien télécharger (`tools/planche-contact.js`). Le pas est de 4 s. On le resserre à 1 ou 2 s sur les cartons-titres, les gags visuels, les transitions vers l'imaginaire et les textes lisibles.
4. **Études de personnages.** Sur les gros plans, des planches à grandes vignettes isolent les expressions du visage, les formes de bouche (au tiers de seconde sur une réplique), les gestes et les poses des bras, et les tenues. Ce qu'elles montrent est décrit avec des mots dans `kb/personnages/`.
5. **Rédaction.** Chaque scène est racontée avec les mots du rédacteur : le lieu, qui est là, ce qui se passe, ce qu'on voit.

## Ce qu'on garde, et où

Les planches sont gardées pour ne pas avoir à tout refaire, mais **elles ne quittent pas l'ordinateur** : elles vont dans `media-local/`, qui est exclu du dépôt par le `.gitignore`. Le dépôt public ne contient que du texte, des liens et du graphisme original.

## Ce que valent les étiquettes

| Étiquette | Ce qu'elle atteste | Ce qu'elle n'atteste pas |
|---|---|---|
| `[VU À L'IMAGE]` + minutage | Le fait est visible sur une image regardée à ce minutage | Ce qui se passe entre deux images échantillonnées |
| `[TRANSCRIPTION AUTO]` + minutage | Le fait se déduit de ce qui est dit, d'après la transcription automatique | Le mot à mot, l'identité du locuteur, le ton |
| `[INTERPRÉTATION]` | Lecture du rédacteur : sens d'un gag, frontière entre réel et imaginaire | Un fait |
| `[À VÉRIFIER]` | Point douteux, noté pour être repris | Rien |

## Limites

- **Échantillonnage** : ce n'est pas un visionnage continu. Un geste de moins de 4 s peut avoir échappé.
- **Son non écouté** : la voix off d'Angela, le faux accent français de Nanette, la musique et les bruitages ne sont pas observés directement.
- **Transcription automatique** : pas de nom de locuteur, des noms propres déformés (« Nanette » devient « Ninnie War », « Abatti » devient « Abati »…). Les graphies retenues sont celles de sources écrites, pas celles de la machine.
- **Définition** : les planches sont des captures réduites à 800 px de large. Les petits textes, comme les cartons-titres, sont parfois à la limite du lisible.
- **Publicités** : elles coupent la lecture. Le script les attend ou les passe, et refait l'image si une pub s'est glissée dedans.
- **Montage de la chaîne** : les compilations enchaînent les segments sans générique. Rien ne garantit que chaque segment soit dans son montage de diffusion d'origine.
