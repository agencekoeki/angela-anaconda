#!/bin/bash
# Deux copies de chaque vidéo d'épisode :
#  - pub/     : une copie allégée, 2 passes à 3 500 kb/s (~70 Mo), pour le dépôt privé (GitHub refuse plus de 100 Mo par fichier)
#  - apercu/  : la copie à regarder, 2 passes à 1 200 kb/s (~27 Mo)
# La vidéo à PUBLIER est l'original du rendu (shorts/EPnn-xx.mp4, CRF 18, ~8 Mb/s, ~160 Mo) : c'est le débit que YouTube
# recommande pour du 1080p, et Sébastien l'a dit le 30/10/2026 (« si la vidéo fait 600 Mo, on s'en fout »). La limite de
# GitHub ne décide pas de la qualité publiée ; vers le PC, l'original passe en morceaux de 20 Mo dans un tar.
# Usage : bash livraison/compresser.sh EP01
cd "$(dirname "$0")/.."
EP=$1
for L in fr en es; do
  for Q in "pub 3500k" "apercu 1200k"; do
    set -- $Q; D=$1; B=$2
    ( cd livraison && ffmpeg -y -loglevel error -i ../shorts/$EP-$L.mp4 -c:v libx264 -preset medium -b:v $B -pass 1 -passlogfile p$D-$L -an -f mp4 /dev/null \
      && ffmpeg -y -loglevel error -i ../shorts/$EP-$L.mp4 -c:v libx264 -preset medium -b:v $B -pass 2 -passlogfile p$D-$L -c:a aac -b:a 160k -movflags +faststart $D/$EP-$L.tmp.mp4 \
      && mv $D/$EP-$L.tmp.mp4 $D/$EP-$L.mp4 ) &
  done
done
wait
ls -la livraison/pub livraison/apercu
