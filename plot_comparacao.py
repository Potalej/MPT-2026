from funcoes import *
from config import *
import numpy as np
import ncorpos_utilidades as nut
import pickle
import os
import sys

dir_base = "relatorio/img/t6_2"
diretorios = [p for p in os.listdir(dir_base) if ".png" not in p]
diretorios = sorted(diretorios)
pastas = [dir_base + "/" + pasta + "/" for pasta in diretorios]

nproc = int(sys.argv[1])

totais = []
tempos_pint = []
tempos_ref = []

for pasta in pastas:
    arquivo_ref  = pasta + "info_referencia"
    arquivo_pint = pasta + "info_pint"

    with open(f'{arquivo_pint}.pickle', 'rb') as f:
        info_pint = pickle.load(f)
    
    with open(f'{arquivo_ref}.pickle', 'rb') as f:
        info_ref = pickle.load(f)

    t_setup_pint, t_solve_pint = info_pint['time_setup'], info_pint['time_solve']
    t_setup_ref,  t_solve_ref  = info_ref['time_setup'],  info_ref['time_solve']
    
    total = t_solve_pint + t_solve_ref
    t_pint = t_solve_pint / total * 100
    t_ref  = t_solve_ref  / total * 100

    totais.append(total)
    tempos_pint.append(t_pint)
    tempos_ref.append(t_ref)

nomes = [pasta.replace('_', ' ') for pasta in diretorios]

fig, ax = plt.subplots(figsize=(7,4))
ax.bar(nomes, tempos_pint, label="Parareal")
ax.bar(nomes, tempos_ref, bottom=tempos_pint, label="Referência")
ax.axhline(50, c='black', linestyle='--')
ax.set_ylabel("Porcentagem (%)")
ax.set_ylim(0,100)
ax.legend()
plt.suptitle("Percentual de tempo computacional")
plt.title(rf"50 corpos, raio=0.025, $N_P={nproc}$, $t_f=10$, $N=200$, $tol=dt_F^3$", fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(dir_base + "/tempo_computacional.png")