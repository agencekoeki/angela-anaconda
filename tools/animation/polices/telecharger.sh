#!/bin/bash
# Récupère les polices des shorts depuis github.com/google/fonts (licences libres)
cd "$(dirname "$0")"
curl -sSL -o Fredoka.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/Fredoka%5Bwdth%2Cwght%5D.ttf"
curl -sSL -o LuckiestGuy-Regular.ttf "https://raw.githubusercontent.com/google/fonts/main/apache/luckiestguy/LuckiestGuy-Regular.ttf"
ls -la *.ttf
