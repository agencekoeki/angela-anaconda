#!/bin/bash
# rend l'épisode dans les trois langues (deux en parallèle, puis la troisième)
# REPRENDRE=1 bash rendre3.sh : ne refait que les plans dont le fichier rendu-ep01-<langue>/planNN.mp4 a été supprimé
cd "$(dirname "$0")"
(LANGUE=fr python3 short_ep01.py > rendu-fr.log 2>&1; echo "fr EXIT $?" >> rendu-fr.log) &
(LANGUE=en python3 short_ep01.py > rendu-en.log 2>&1; echo "en EXIT $?" >> rendu-en.log) &
wait
LANGUE=es python3 short_ep01.py > rendu-es.log 2>&1; echo "es EXIT $?" >> rendu-es.log
tail -n1 rendu-fr.log rendu-en.log rendu-es.log
