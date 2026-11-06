#!/bin/bash
# rend l'épisode 4 dans les trois langues, l'un après l'autre (deux cœurs : ffmpeg prend le second)
cd "$(dirname "$0")"
for L in fr en es; do
  LANGUE=$L python3 short_ep04.py > rendu-ep04-$L.log 2>&1; echo "04 $L EXIT $?" >> rendu-ep04-$L.log
done
tail -n1 rendu-ep04-*.log
