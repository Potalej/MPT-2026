from funcoes import *
from config import *
import numpy as np
import ncorpos_utilidades as nut
import pickle
import os
import sys
import matplotlib.pyplot as plt

subdir = "t1"

dir_base = "relatorio/img/" + subdir
diretorios = [k for k in os.listdir(dir_base) if ".png" not in k]
diretorios = sorted(diretorios)
pastas = [dir_base + "/" + pasta + "/" for pasta in diretorios]

dir_base_pymgrit = "saida/" + subdir
pastas_pymgrit = [dir_base_pymgrit  + "/" + pasta for pasta in diretorios]

nproc = int(sys.argv[1])

for qual in ["erro", "energia", "angular"]:

    totais = []
    tempos_pint = []
    tempos_ref = []

    fig, ax = plt.subplots(figsize=(7,4))
    plt.xlabel('Iteração')
    plt.yscale('log')

    for i, pasta in enumerate(pastas):
        arquivo_ref  = pasta + "info_referencia"
        arquivo_pint = pasta + "info_pint"

        with open(f'{arquivo_pint}.pickle', 'rb') as f:
            info_pint = pickle.load(f)
        
        with open(f'{arquivo_ref}.pickle', 'rb') as f:
            info_ref = pickle.load(f)

        caminho_pymgrit = pastas_pymgrit[i]

        ts_ref, us_ref = pp_referencia(caminho_pymgrit)
        sol_pint = pp_pint(caminho_pymgrit, info_pint, nproc)

        erro_final, erro_durante, erro_durante_energia, erro_durante_angular = calcular_erros(massas, eps, ts_ref, us_ref, sol_pint, N_dt_per_slice)
        
        label = diretorios[i].replace("_", " ")
        if "es" in label: marcador = "o"
        elif "rk2" in label: marcador = "s"
        elif "verlet" in label: marcador = "^"

        if "ruth4" in label: cor, ls = "purple", "--"
        elif "rk4" in label: cor, ls = "orange", "-"
        elif "verlet" in label: cor, ls = "blue", "-"
        elif "rk2" in label: cor, ls = "green", "-"
        
        if qual == "erro":
            plt.plot(erro_final, marker = marcador, label=label, c=cor, linestyle=ls)
        elif qual == "energia":
            plt.plot(erro_durante_energia[:,-1], marker = marcador, label=label, c=cor, linestyle=ls)
        elif qual == "angular":
            plt.plot(erro_durante_angular[:,-1], marker = marcador, label=label, c=cor, linestyle=ls)

    plt.legend()

    if qual == "erro":
        plt.ylabel(r'$\log{|u^k_{N} - u_{ref,N}|/|u_{ref,N}|}$')
        plt.suptitle("Erro relativo ao final de cada iteração")

    elif qual == "energia":
        plt.ylabel(r'$\log{|E_N^k - E_0|}$')
        plt.suptitle("Erro na energia total ao final de cada iteração")

    elif qual == "angular":
        plt.ylabel(r'$\log{|J_N^k - J_0|}$')
        plt.suptitle("Erro no momento angular total final de cada iteração")

    plt.title(rf"$N_P={nproc}$, $t_f=10$, $N=200$, $m_G=4$, $tol=dt_F^p$", fontsize=10)
    # plt.title(rf"$N_P={nproc}$, $t_f=8$, $N=160$, $tol=dt_F^p$, $p=3.2$", fontsize=10)

    plt.tight_layout()
    if qual == "erro":      plt.savefig(f"relatorio/img/{subdir}/erro_final.png")
    elif qual == "energia": plt.savefig(f"relatorio/img/{subdir}/erro_final_energia.png")
    elif qual == "angular": plt.savefig(f"relatorio/img/{subdir}/erro_final_angular.png")