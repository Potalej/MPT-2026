import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as sp_linalg

import pymgrit
from pymgrit.core.mgrit import Mgrit

from time import time
import json
import pickle

from src.parareal import Parareal
from src.ncorposapp import NCorpos

import ncorpos_utilidades as nut
import os

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def ler_vi_json (arquivo:str):
    with open(arquivo, 'r') as arq:
        arq_json = json.load(arq)
    massas = arq_json['valores_iniciais']['massas']
    posicoes = arq_json['valores_iniciais']['posicoes']
    momentos = arq_json['valores_iniciais']['momentos']
    G = arq_json['G']
    if 'integracao' in arq_json: eps = arq_json['integracao']['amortecedor']
    else: eps = arq_json['amortecedor']
    return np.array(massas), np.array(posicoes), np.array(momentos), G, eps

def converter_3d_para_2d (vetor):
    return vetor[:,:-1]

def converter_2d_para_3d (vetor):
    shape = list(vetor.shape)
    shape[-1] = 3
    zeros = np.zeros(shape)
    zeros[:,:,:2] = vetor
    return zeros
  
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

## Função para armazenar a solução do método Parareal em cada iteração
def output_parareal(self, caminho_pymgrit):
    ## Nome do arquivo de saída
    fname = 'ncorpos_iter' + str(self.solve_iter) + '_rank' + str(self.comm_time_rank)
    fname = caminho_pymgrit + "/" + fname
    # Salva a solução em um arquivo
    np.save(fname,
                [[[self.t[0][i], self.u[0][i]] for i in self.index_local[0]]])

## Função para armazenar a solução de referência
def output_ref(self, caminho_pymgrit):
    # Nome do arquivo de saída
    fname = 'ncorpos_ref_rank' + str(self.comm_time_rank)
    fname = caminho_pymgrit + "/" + fname
    # Salva a solução em um arquivo
    np.save(fname,
                [[[self.t[0][i], self.u[0][i]] for i in self.index_local[0]]])

def aplicar_parareal (parametros:dict, tol:bool=False, arquivo:str="", caminho_pymgrit:str=""):
    # u0
    q0, p0 = parametros["vi"]["posicoes"], parametros["vi"]["momentos"]
    u0 = np.array([q0, p0])

    # Numero de janelas dos metodos
    nt_slices = parametros["num_janelas"] + 1
    nt_fino = parametros["multip_fino"] * (nt_slices - 1) + 1
    nt_gros = parametros["multip_grosseiro"] * (nt_slices - 1) + 1
    N_dt_per_slice = int((nt_fino-1)/(nt_slices-1))

    # Se for usar um valor de tolerancia
    tolerancia = 0.0
    if tol:
        tolerancia = ((parametros["tf"] - parametros["t0"])/nt_fino)**parametros["ordem"]

    # Instancia do nivel 0
    ncorpos_level_0 = NCorpos(
        G       = parametros["G"],
        eps     = parametros["amortecedor"],
        raio    = parametros["raio"],
        massas  = parametros["vi"]["massas"],
        u0      = u0,
        t_start = parametros["t0"],
        t_stop  = parametros["tf"],
        method  = parametros["metodo_fino"],
        nt      = nt_fino
    )

    # Instancia do nivel 1
    ncorpos_level_1 = NCorpos(
        G       = parametros["G"],
        eps     = parametros["amortecedor"],
        raio    = parametros["raio"],
        massas  = parametros["vi"]["massas"],
        u0      = u0,
        t_start = parametros["t0"],
        t_stop  = parametros["tf"],
        method  = parametros["metodo_grosseiro"],
        nt      = nt_gros
    )

    # Array contendo todos os niveis de discretização
    problema = [ncorpos_level_0, ncorpos_level_1]

    # Instancia do Parareal
    parareal = Parareal(
        problem = problema,
        nt_slices = nt_slices,
        max_iter = parametros["max_iter"],
        output_parareal= lambda self: output_parareal(self, caminho_pymgrit),
        tol = tolerancia
    )

    # Agora executa
    tempo_parareal = time()
    info_pint = parareal.solve()
    tempo_parareal = time() - tempo_parareal
    
    # E salva em um arquivo se for o caso
    if len(arquivo) > 0:
        with open(arquivo + ".pickle", 'wb') as f:
            pickle.dump(info_pint, f)
    
    return {
        "tempo_parareal": tempo_parareal,
        "info_pint": info_pint,
        "N_dt_per_slice": N_dt_per_slice
    }
    
def aplicar_referencia (parametros:dict, tol:bool=False, arquivo:str="", caminho_pymgrit:str=""):
    # u0
    q0, p0 = parametros["vi"]["posicoes"], parametros["vi"]["momentos"]
    u0 = np.array([q0, p0])

    # Numero de janelas dos metodos
    nt_slices = parametros["num_janelas"] + 1
    nt_fino = parametros["multip_fino"] * (nt_slices - 1) + 1
    N_dt_per_slice = int((nt_fino-1)/(nt_slices-1))

    # Se for usar um valor de tolerancia
    tolerancia = 0.0
    if tol:
        tolerancia = ((parametros["tf"] - parametros["t0"])/nt_fino)**parametros["ordem"]

    # Instancia do nivel 0
    ncorpos_level_0 = NCorpos(
        G       = parametros["G"],
        eps     = parametros["amortecedor"],
        raio    = parametros["raio"],
        massas  = parametros["vi"]["massas"],
        u0      = u0,
        t_start = parametros["t0"],
        t_stop  = parametros["tf"],
        method  = parametros["metodo_fino"],
        nt      = nt_fino
    )

    # Roda a simulacao de referencia
    problema_referencia = [ncorpos_level_0]
    mgrit_ref = Mgrit(
        problem = problema_referencia,
        output_fcn = lambda self: output_ref(self, caminho_pymgrit),
        max_iter = 1
    )
    tempo_referencia = time()
    info_ref = mgrit_ref.solve()
    tempo_referencia = time() - tempo_referencia
    
    if len(arquivo) > 0:
        with open(arquivo + ".pickle", 'wb') as f:
            pickle.dump(info_ref, f)

    return {
        "tempo_referencia": tempo_referencia,
        "info_ref": info_ref,
        "N_dt_per_slice": N_dt_per_slice
    }
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def pp_referencia (caminho_pymgrit):
    ######################################
    ## Leitura da solução de referência ##
    ######################################
    sol_ref = np.load(caminho_pymgrit + "/ncorpos_ref_rank0.npy", allow_pickle=True).tolist()[0]

    ## Extrair os instantes de tempo nos quais a solução está calculada (primeira coluna),
    ## guardando apenas os instantes definindo as janelas de tempo
    ## (por padrão, pymgrit retorna a solução em toda a discretização temporal fina)
    ts_ref = np.array([j[0] for j in sol_ref])

    ## Extrair a solução em cada instante de tempo (segunda coluna)
    us_ref = np.array([j[1].get_values() for j in sol_ref])

    ## Ordernar em tempo crescente
    idx = np.argsort(ts_ref)
    ts_ref = ts_ref[idx]
    us_ref = us_ref[idx]

    return ts_ref, us_ref

def pp_pint (caminho_pymgrit, info_pint, nproc):
    ####################################################
    ## Determinação do número de iterações realizadas ##
    ####################################################
    total_iterations = len(info_pint['conv']) + 1

    ####################################################
    ## Leitura da solução do método paralelo no tempo ##
    ####################################################
    sol_pint = []
    # Percorrer as iterações
    for i in range(total_iterations):
        sol_iteration = []
        
        # Coletar a solução armazenada por cada processador
        for j in range(nproc):
            # Ler a solução da iteração na forma de pares (t_i, y_i)
            sol_proc = np.load(caminho_pymgrit + "/ncorpos_iter" + str(i) + "_rank" + str(j) + ".npy", allow_pickle=True).tolist()[0]
            sol_iteration += sol_proc
        
        # sol_iteration += np.load(caminho_pymgrit + "/ncorpos_iter" + str(i) + "_rank0.npy", allow_pickle=True).tolist()[0]
        
        # Ler os instantes definindo as janelas de tempo (primeira coluna)
        ts = np.array([j[0] for j in sol_iteration])
        # Ler as respectivas soluções (segunda coluna)
        us = np.array([j[1].get_values() for j in sol_iteration])
        
        # Ordenar em tempo crescente
        idx = np.argsort(ts)
        ts = ts[idx]
        us = us[idx]
        
        # Concatena a solução da iteração ao final da lista completa
        sol_pint.append([ts, us])
    
    return sol_pint
  

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def plotar_trajetorias (us, quais_plotar:list=[], label=""):
    # Separa a solucao em particulas
    posicoes = np.array(list(zip(*us)))[0]
    corpos = np.array(list(zip(*posicoes)))

    if len(quais_plotar) == 0: 
        quais_plotar = [{"ind": i, "traco": 0, "cor": 0} for i in range(len(corpos))]
    for qual in quais_plotar:
        corpo = corpos[qual["ind"]]
        x, y, z = list(zip(*corpo))

        cor = qual["cor"]
        traco = qual["traco"]
        if traco == 0: traco = "-"

        if cor != 0: 
            if len(label) > 0:
                plt.plot(x, y, traco, c=cor, label=label)
            else:
                plt.plot(x, y, traco, c=cor)
        else: 
            if len(label) > 0:
                plt.plot(x, y, traco, label=label)
            else:
                plt.plot(x, y, traco)

def plotagem_pint (sol_pint, quais_iteracoes:list=[], quais_plotar:list=[]):
    if len(quais_iteracoes) == 0: quais_iteracoes = range(len(sol_pint))
    if len(quais_plotar) == 0: quais_plotar = range(len(sol_pint[0]))
    
    for ind_iter in quais_iteracoes:
        ts, us = sol_pint[ind_iter]

        plotar_trajetorias(us, [
            {"ind": i, "traco": 0, "cor":0}
            for i in quais_plotar
        ], r'$k={}$'.format(ind_iter))

def plotagem_referencia (us_ref, quais_plotar:list=[]):
    plotar_trajetorias(us_ref, [
        {"ind": i, "traco": "--", "cor":"black"}
        for i in quais_plotar
    ])
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def calcular_erros (massas, eps, ts_ref, us_ref, sol_pint, fatias:int):
    # ##########################################################
    # ## Cálculo dos erros em relação à solução de referência ##
    # ## (solução sequencial do modelo fino)                  ##
    # ##########################################################
    # Erro nos instante final
    erro_pint_ref_T = []

    # Percorrer as iteracoes e calcular o erro relativo
    for i in range(len(sol_pint)):
        erro = np.linalg.norm(sol_pint[i][1][-1] - us_ref[-1])
        erro = erro / np.linalg.norm(us_ref[-1])
        erro_pint_ref_T.append(erro)
    
    # Erro ao longo do tempo em cada iteração em relacao a solucao
    # de referencia
    ts_ref_fatiado = ts_ref[::fatias]
    us_ref_fatiado = us_ref[::fatias]
    erro_pint_ref_tk = np.empty((len(sol_pint), ts_ref_fatiado.shape[0]))
    # Percorre as iteracoes e armazenaos erros
    for i in range(len(sol_pint)):
        sol_pint_fatiado = sol_pint[i][1][::fatias]
        erro_lista = [
            np.linalg.norm(sol_pint_fatiado[j] - us_ref_fatiado[j])
            for j in range(len(sol_pint_fatiado))
        ]
        erro_pint_ref_tk[i,:] = np.array(erro_lista)
    
    # Erro nas energias
    erro_pint_ref_tk_energia = np.empty((len(sol_pint)+1, ts_ref_fatiado.shape[0]))
    q_ref,p_ref = np.array(list(zip(*us_ref)))
    E0 = nut.energia_total(massas, q_ref[0], p_ref[0], 1.0, eps)
    for i in range(len(sol_pint)):
        sol_pint_fatiado = sol_pint[i][1][::fatias]
        qs, ps = np.array(list(zip(*sol_pint_fatiado)))

        erro_lista = [abs(E0 - nut.energia_total(massas, qs[j], ps[j], 1.0, eps)) for j in range(len(sol_pint_fatiado))]
        erro_pint_ref_tk_energia[i,:] = np.array(erro_lista)
    q_ref, p_ref = q_ref[::fatias], p_ref[::fatias]
    erro_lista = [abs(E0 - nut.energia_total(massas, q_ref[j], p_ref[j], 1.0, eps)) for j in range(len(q_ref))]
    erro_pint_ref_tk_energia[-1,:] = np.array(erro_lista)

    # Erro no momento angular
    erro_pint_ref_tk_angular = np.empty((len(sol_pint)+1, ts_ref_fatiado.shape[0]))
    q_ref,p_ref = np.array(list(zip(*us_ref)))
    J0 = nut.momento_angular_total(q_ref[0], p_ref[0])[-1]
    for i in range(len(sol_pint)):
        sol_pint_fatiado = sol_pint[i][1][::fatias]
        qs, ps = np.array(list(zip(*sol_pint_fatiado)))

        erro_lista = [abs(J0 - nut.momento_angular_total(qs[j],ps[j])[-1]) for j in range(len(sol_pint_fatiado))]
        erro_pint_ref_tk_angular[i,:] = np.array(erro_lista)
    q_ref, p_ref = q_ref[::fatias], p_ref[::fatias]
    erro_lista = [abs(J0 - nut.momento_angular_total(q_ref[j], p_ref[j])[-1]) for j in range(len(q_ref))]
    erro_pint_ref_tk_angular[-1,:] = np.array(erro_lista)

    return erro_pint_ref_T, erro_pint_ref_tk, erro_pint_ref_tk_energia, erro_pint_ref_tk_angular

def plotar_erros_final (titulo, erro_pint_ref_T):
    plt.figure(figsize=(7,4))
    plt.xlabel('Iteração')
    plt.ylabel(r'$|u^k_{N} - u_{ref,N}|/|u_{ref,N}|$')
    plt.yscale('log')
    plt.suptitle("Erro relativo ao final de cada iteração")
    plt.title(titulo, fontsize=10)
    plt.plot(erro_pint_ref_T, marker = 'o')

def plotar_erros_processo (titulo, ts_ref, erro_pint_ref_tk, fatias):
    ts_ref_fatiado = ts_ref[::fatias]
    plt.figure(figsize=(7,4))

    for i, erro in enumerate(erro_pint_ref_tk):
        if i % 3 != 0: continue
        plt.plot(ts_ref_fatiado, erro, label=r'$k={}$'.format(i))
        
    plt.yscale('log')
    plt.xlabel(r'$t$')
    plt.ylabel('Erro ' + r'$|u^k_n - u_{ref,n}|/|u_{ref,n}|$')
    plt.suptitle("Erro relativo durante cada iteração")
    plt.title(titulo, fontsize=10)
    plt.legend()
    plt.show()

def plotar_erros_processo_angular (titulo, ts_ref, erro_pint_ref_tk, fatias):
    ts_ref_fatiado = ts_ref[::fatias]
    plt.figure(figsize=(7,4))

    for i, erro in enumerate(erro_pint_ref_tk[:-1]):
        if i < 1 or i > 5: continue
        # if i not in [1, 3, 6, 9, 12]: continue
        # if i not in [1, 5, 10, 15]: continue
        plt.plot(ts_ref_fatiado, erro, label=r'$k={}$'.format(i))

    plt.plot(ts_ref_fatiado, erro_pint_ref_tk[-1], c='black', linestyle='--', label="Ref.")

    plt.suptitle("Erro absoluto no momento angular total nas iterações")
    plt.title(titulo, fontsize=10)
    # plt.tight_layout()
    plt.yscale('log')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$\log{|J(t) - J_0|}$')
    plt.legend(loc='upper left')
    plt.show()

def plotar_erros_processo_energia (titulo, ts_ref, erro_pint_ref_tk, fatias):
    ts_ref_fatiado = ts_ref[::fatias]
    plt.figure(figsize=(7,4))

    for i, erro in enumerate(erro_pint_ref_tk[:-1]):
        if i < 1 or i > 6: continue
        # if i not in [1, 3, 6, 9]: continue
        # if i not in [1, 5, 10, 15]: continue
        plt.plot(ts_ref_fatiado, erro, label=r'$k={}$'.format(i))

    plt.plot(ts_ref_fatiado, erro_pint_ref_tk[-1], c='black', linestyle='--', label="Ref.")

    plt.suptitle("Erro absoluto na energia total nas iterações")
    plt.title(titulo, fontsize=10)
    # plt.tight_layout()
    plt.yscale('log')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$\log{|E(t) - E_0|}$')
    plt.legend(loc='upper left')
    plt.show()