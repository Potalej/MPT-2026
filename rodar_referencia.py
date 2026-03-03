from funcoes import *
from config import *
import numpy as np
import ncorpos_utilidades as nut

infos_ref = aplicar_referencia(parametros, tol=parametros["ordem"], arquivo=pasta_saida + "info_referencia", caminho_pymgrit=caminho_pymgrit)
print(f"Tempo: {infos_ref['tempo_referencia']}")