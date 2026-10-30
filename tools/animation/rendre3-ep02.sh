#!/bin/bash
# rend l'épisode 2 dans les trois langues, l'une après l'autre (le conteneur n'a que deux cœurs : ffmpeg prend le second)
# REPRENDRE=1 bash rendre3-ep02.sh : ne refait que les plans dont le fichier rendu-ep02-<langue>/planNN.mp4 a été supprimé
cd "$(dirname "$0")"
for L in fr en es; do
  LANGUE=$L python3 short_ep02.py > rendu-ep02-$L.log 2>&1; echo "$L EXIT $?" >> rendu-ep02-$L.log
done
tail -n1 rendu-ep02-fr.log rendu-ep02-en.log rendu-ep02-es.log
