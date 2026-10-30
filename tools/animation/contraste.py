"""Ancien nom du contrôle : voir controle.py (lisibilité, tailles, places, débordements, sous-titres)."""
import runpy
import sys

if __name__ == '__main__':
    sys.argv[0] = 'controle.py'
    runpy.run_module('controle', run_name='__main__')
