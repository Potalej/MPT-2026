from funcoes import *
from config import *
import numpy as np
import ncorpos_utilidades as nut
import pickle
import sys

nproc = int(sys.argv[1])
arquivo_ref  = pasta_saida + "info_referencia"
arquivo_pint = pasta_saida + "info_pint"

with open(f'{arquivo_pint}.pickle', 'rb') as f:
  info_pint = pickle.load(f)
  
with open(f'{arquivo_ref}.pickle', 'rb') as f:
  info_ref = pickle.load(f)

print("E0:", E0, "\n")

print("# PARAREAL # \nSetup:", info_pint['time_setup'],'\nSolve:', info_pint['time_solve'])
print("\n# SEQUENCIAL # \nSetup:", info_ref['time_setup'],'\nSolve:', info_ref['time_solve'])
print()

# Pós-processamento
ts_ref, us_ref = pp_referencia(caminho_pymgrit)
sol_pint = pp_pint(caminho_pymgrit, info_pint, nproc)

# Erro nas integrais primeiras da referencia
q_ref,p_ref = np.array(list(zip(*us_ref)))
E_ref = nut.energia_total(massas, q_ref[-1], p_ref[-1], G, eps)
J_ref = nut.momento_angular_total(q_ref[-1], p_ref[-1])
print("Erro na E da referencia:", abs(E_ref - E0))
print("Erro no J da referencia:", abs(J_ref[2] - J0[2]))
print(E_ref)

# Erro nas integrais primeiras do parareal
us_parareal = sol_pint[-1][1]
q_parareal, p_parareal = np.array(list(zip(*us_parareal)))

E_parareal = nut.energia_total(massas, q_parareal[-1], p_parareal[-1], G, eps)
J_parareal = nut.momento_angular_total(q_parareal[-1], p_parareal[-1])
print("Erro na E do Parareal:", abs(E_parareal - E0))
print("Erro no J do Parareal:", np.abs(J_parareal[2] - J0[2]))

exit()
# Plotando
# plotagem_pint(sol_pint, 
#     # quais_iteracoes= [i for i in range(len(sol_pint)) if i % 4 == 0 and i > 0], 
#     quais_iteracoes = [-1],
#     quais_plotar   = [ 0 ]
#     )

# plotagem_referencia(us_ref, [0,1,2,3,4,5,6,7,8,9,10,11])

plt.title(r"Trajetórias de referência no intervalo $[0,8]$")
q_ref, p_ref = np.array(list(zip(*us_ref)))
q_ref = np.array(list(zip(*q_ref)))
for corpo in q_ref:
  x,y,z = np.array(list(zip(*corpo)))
  plt.scatter(x[0],y[0])
  # tf = int(np.ceil(3.5 * 2.6 * 640))
  # plt.scatter(x[tf],y[tf],c='black')
  # plt.plot(x[:tf],y[:tf])
  plt.plot(x,y)

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')

plt.tight_layout()
plt.legend()
plt.xlim(-1.2,1.2)
plt.ylim(-1.2,1.2)
plt.axis('equal')

plt.savefig(pasta_saida + 'trajetorias1.png')

exit()

## Erros
erro_final, erro_durante, erro_durante_energia, erro_durante_angular = calcular_erros(massas, eps, ts_ref, us_ref, sol_pint, N_dt_per_slice)
plotar_erros_final(titulo, erro_final)
plt.savefig(pasta_saida + 'erro_final.png')
plotar_erros_processo(titulo, ts_ref, erro_durante, N_dt_per_slice)
plt.savefig(pasta_saida + 'erro_durante.png')


plotar_erros_processo_energia(titulo, ts_ref, erro_durante_energia, N_dt_per_slice)
plt.savefig(pasta_saida + 'erro_durante_energia.png')

plotar_erros_processo_angular(titulo, ts_ref, erro_durante_angular, N_dt_per_slice)
plt.savefig(pasta_saida + 'erro_durante_angular.png')