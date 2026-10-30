import os, sys
os.environ['FORMAT']='vertical'; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur import *
from moteur import MEDIA_LOCAL; D=MEDIA_LOCAL+'/decors/aa-decor-11-bureau-vertical.png'
T='assets/'
def ecran(img): return Acteur('ecran', T+img, x=0.527, y=0.407, h=0.062*1.04*4, ombre=False)
plans=[
 # 1 : Tara devant un écran turquoise (le défaut signalé)
 Plan(2.0, D, cam=(0.527,0.527), zoom=(4,4), cam_y=0.36,
      acteurs=[Acteur('ecran', T+'tara-ecran.png', x=0.527, y=0.409, h=0.065, ombre=False),
               Acteur('tara', T+'tara-1.png', x=0.527, y=0.405, h=0.05, ombre=False, brut=True)]),
 # 2 : Tara dans un écran bleu nuit, avec liseré
 Plan(2.0, D, cam=(0.527,0.527), zoom=(4,4), cam_y=0.36,
      acteurs=[Acteur('ecran', T+'ecran-allume.png', x=0.527, y=0.409, h=0.065, ombre=False),
               Acteur('tara', T+'tara-1.png', x=0.527, y=0.405, h=0.05, ombre=False, brut=True, contour=((175,252,246),3,2))]),
 # 3 : appel à l'abonnement collé aux cheveux de Kristina, et le même en bandeau
 Plan(2.0, D, acteurs=[Acteur('kristina', T+'kristina-tete-1.png', x=0.5, y=0.665, h=0.5, gros_plan=True, ombre=False)],
      cartons=[(0, 2, 'Parle de lui :', 'abonne-toi.', 0.11, 0.62)]),
 Plan(2.0, D, acteurs=[Acteur('kristina', T+'kristina-tete-1.png', x=0.5, y=0.665, h=0.5, gros_plan=True, ombre=False)],
      bandeaux=[(0, 2, 'Abonne-toi demain.', 'Là, dodo.', 0.42, 1.0)]),
]
