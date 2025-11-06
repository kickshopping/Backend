"""
Imprime la conexión STRCNX usada por el backend config
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STRCNX
print('STRCNX =', STRCNX)
