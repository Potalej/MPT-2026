from funcoes import ler_vi_json
import os
# massas, q0, p0, G, eps = ler_vi_json('valores_iniciais/amortecido_teste1.json')
# pasta_saida = "t6_1"

# massas, q0, p0, G, eps = ler_vi_json('valores_iniciais/amortecido_teste2.json')
# pasta_saida = "t6_2"
# pasta_saida = "t6_2_naoconverge"

massas, q0, p0, G, eps = ler_vi_json('valores_iniciais/amortecido_teste3.json')
pasta_saida = "t6_3"

tf = 10
# Valores iniciais e parametros de N-corpos
# o 2 nao converge para r = 0.05
parametros = {
    "G": G, "amortecedor": eps, "raio": 0.025,
    "vi": {
        "massas": massas,
        "posicoes": q0,
        "momentos": p0
    },

    # Intervalo de integracao
    "t0": 0, 
    "tf": tf,

    # Quantidade de janelas
    "num_janelas": tf * 40,
    
    # Numero maximo de iteracoes
    "max_iter": 30,

    # Metodo fino
    "metodo_fino": "rk4",
    "multip_fino": 32,
    "ordem": 4,

    # Metodo grosseiro
    "metodo_grosseiro": "euler_exp",
    "multip_grosseiro": 1
}

casos = [
    # ["t4/rk4_vs_es/", "rk4", "euler_simp", 4],
    # ["t4/ruth4_vs_es/", "ruth4", "euler_simp", 4],

    # ["relatorio/img/t2/rk2_vs_ee/", "rk2", "euler_exp", 2],
    # ["relatorio/img/t2/rk2_vs_es/", "rk2", "euler_simp", 2],

    # ["relatorio/img/t2/verlet_vs_ee/", "verlet", "euler_exp", 2],
    # ["relatorio/img/t2/verlet_vs_es/", "verlet", "euler_simp", 2],

    [pasta_saida + "/rk4_vs_rk2/", "rk4", "rk2", 2.6],
    [pasta_saida + "/rk4_vs_verlet/", "rk4", "verlet", 2.6],

    [pasta_saida + "/ruth4_vs_rk2/", "ruth4", "rk2", 2.6],
    [pasta_saida + "/ruth4_vs_verlet/", "ruth4", "verlet", 2.6],

    # ["t4/svcp10s35_vs_rk2/", "svcp10s35", "rk2", 10],
    # ["t4/svcp10s35_vs_verlet/", "rk4", "verlet", 3.2],
]

caso = casos[3]
caminho_pymgrit = "saida/" + caso[0]
pasta_saida = "relatorio/img/" + caso[0]
parametros["metodo_fino"] = caso[1]
parametros["metodo_grosseiro"] = caso[2]
parametros["ordem"] = caso[3]

os.makedirs(caminho_pymgrit, exist_ok=True)
os.makedirs(pasta_saida, exist_ok=True)