#!/bin/bash
# rend l'épisode 3 dans les trois langues, l'une après l'autre (le conteneur n'a que deux cœurs : ffmpeg prend le second)
# REPRENDRE=1 bash rendre3-ep03.sh : ne refait que les plans dont le fichier rendu-ep03-<langue>/planNN.mp4 a été supprimé
cd "$(dirname "$0")"
for L in fr en es; do
  LANGUE=$L python3 short_ep03.py > rendu-ep03-$L.log 2>&1; echo "$L EXIT $?" >> rendu-ep03-$L.log
done
tail -n1 rendu-ep03-fr.log rendu-ep03-en.log rendu-ep03-es.log
