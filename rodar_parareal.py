from funcoes import *
from config import *

infos = aplicar_parareal(parametros, tol=parametros["ordem"], arquivo=pasta_saida + "info_pint", caminho_pymgrit=caminho_pymgrit)
print(f"Tempo: {infos['tempo_parareal']}")