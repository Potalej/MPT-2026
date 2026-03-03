import numpy as np
import os

G, eps = 1, 0
massas = np.ones(3)
q0 = np.array([
    [-0.97000436,  0.24308753, 0.0],
    [0.0,         0.0,       0.0],
    [0.97000436, -0.24308753, 0.0]
])
p0 = np.array([
    [0.4662036850, 0.4323657300, 0.0],
    [-0.93240737,  -0.86473146, 0.0],
    [ 0.4662036850, 0.4323657300, 0.0]
])

pasta_saida = "relatorio/img/t1/rk4_vs_ee/"
titulo = "RK2 (Fino), E. S. (Grosseiro)"
tf = 10
# Valores iniciais e parametros de N-corpos
parametros = {
    "G": G, "amortecedor": eps, "raio": 0.0,
    "vi": {
        "massas": massas,
        "posicoes": q0,
        "momentos": p0
    },

    # Intervalo de integracao
    "t0": 0, 
    "tf": tf,

    # Quantidade de janelas
    "num_janelas": tf * 20,
    
    # Numero maximo de iteracoes
    "max_iter": 15,

    # Metodo fino
    "metodo_fino": "rk4",
    "multip_fino": 32,
    "ordem": 4,

    # Metodo grosseiro
    "metodo_grosseiro": "euler_exp",
    "multip_grosseiro": 4
}

casos = [
    ["t1/rk4_vs_ee/", "rk4", "euler_exp", 4],
    ["t1/rk4_vs_es/", "rk4", "euler_simp", 4],

    ["t1/rk2_vs_ee/", "rk2", "euler_exp", 2],
    ["t1/rk2_vs_es/", "rk2", "euler_simp", 2],

    ["t1/verlet_vs_ee/", "verlet", "euler_exp", 2],
    ["t1/verlet_vs_es/", "verlet", "euler_simp", 2],
]

caso = casos[2]
caminho_pymgrit = "saida/" + caso[0]
pasta_saida = "relatorio/img/" + caso[0]
parametros["metodo_fino"] = caso[1]
parametros["metodo_grosseiro"] = caso[2]
parametros["ordem"] = caso[3]

os.makedirs(caminho_pymgrit, exist_ok=True)
os.makedirs(pasta_saida, exist_ok=True)