#!/bin/bash
# rend les épisodes 4 et 5 dans les trois langues, l'un après l'autre (le conteneur n'a que deux cœurs : ffmpeg prend le second)
# REPRENDRE=1 bash rendre-ep45.sh : ne refait que les plans dont le fichier rendu-ep0N-<langue>/planNN.mp4 a été supprimé
cd "$(dirname "$0")"
for E in 04 05; do
  for L in fr en es; do
    LANGUE=$L python3 short_ep$E.py > rendu-ep$E-$L.log 2>&1; echo "$E $L EXIT $?" >> rendu-ep$E-$L.log
  done
done
tail -n1 rendu-ep0[45]-*.log
