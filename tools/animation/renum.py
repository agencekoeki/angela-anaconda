"""Décale d'un rang les épisodes DEBUT à FIN des shorts, quand un nouvel épisode s'intercale.

Usage : python3 renum.py <dépôt angela-anaconda> <DEBUT> <FIN>            (montre le diff)
        python3 renum.py <dépôt angela-anaconda> <DEBUT> <FIN> appliquer  (écrit)

Il touche les listes (« ép. 3, 4 et 5 »), les plages (« 3 à 13 »), les flèches (« 3 → 4 »),
les noms EPnn cités dans le texte et les lignes de tableau « | n · ». Il saute `archives/`.
Il NE renomme PAS les fichiers `shorts/episodes/EPnn-*.md` (git mv à la main, du plus grand
au plus petit) et peut se tromper sur une phrase qui mêle numéro d'épisode et autre nombre :
relire le diff ligne par ligne. Écrit le 30/10/2026 pour l'insertion de « On est écoutés » (3 à 13).
"""
import re, sys, os, glob, difflib
ROOT = sys.argv[1]; DEBUT, FIN = int(sys.argv[2]), int(sys.argv[3]); APPLY = len(sys.argv) > 4
files = [f for f in glob.glob(ROOT + '/shorts/**/*.md', recursive=True) if '/archives/' not in f]
files += [ROOT + '/univers/banque-images.md', ROOT + '/univers/boulanger.md', ROOT + '/tools/animation/README.md']
NUM = r'\d{1,2}'
LISTE = re.compile(r'(?P<pre>(?:[ÉéEe]p(?:isodes?|\.)|[ÉE]P\.)\s?)(?P<nums>' + NUM + r'(?:(?:,\s?|\s(?:et|à|ou)\s|\s?[–→]\s?|-)' + NUM + r'(?![\d.,]\d))*)(?![\d.]\d|:\d)')
def sh(m):
    n = int(m.group(0)); return str(n + 1) if DEBUT <= n <= FIN else m.group(0)
def shift_list(m):
    return m.group('pre') + re.sub(r'\d+', sh, m.group('nums'))
def traiter(t):
    t = LISTE.sub(shift_list, t)
    t = re.sub(r'(?<!archives/)EP(\d\d)(?=[-_ .`…])', lambda m: 'EP%02d' % (int(m.group(1)) + 1) if DEBUT <= int(m.group(1)) <= FIN else m.group(0), t)
    t = re.sub(r'(?m)^\| (\d{1,2}) · ', lambda m: '| %d · ' % (int(m.group(1)) + 1) if DEBUT <= int(m.group(1)) <= FIN else m.group(0), t)
    return t
for f in files:
    a = open(f, encoding='utf-8').read(); b = traiter(a)
    if a != b:
        for l in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm='', n=0):
            if l.startswith(('+', '-')) and not l.startswith(('+++', '---')):
                print(os.path.basename(f), l[:230])
        if APPLY: open(f, 'w', encoding='utf-8').write(b)
