import numpy as np
from src import integradores
from src.vectorNCorpos import VectorNCorpos
from pymgrit.core.application import Application
from src.forcas_ncorpos import forcas_ncorpos as fncorpos

class NCorpos(Application):

    def __init__(self, G, eps, raio, massas, u0, method, *args, **kwargs):
        ## Inicialização da classe mãe
        super().__init__(*args, **kwargs)

        self.massas = massas
        self.eps = eps
        self.N = len(massas)
        self.G = G
        self.u0 = u0
        self.method = method

        qs, ps = self.u0
        for a in range(self.N):
            for b in range(a):
                rab = qs[b] - qs[a]
                dist2 = rab @ rab
                if dist2 <= 4*raio**2 and rab @ (ps[b] - ps[a]) < 0:
                    print("Detectada colisão inicial!")
                    exit()

        # sobre choques elasticos
        self.raio = raio
        self.colidir = (raio > 0)

        ## Checa que o método escolhido está implementado
        assert self.method in ["euler_exp", "euler_simp","verlet","rk2","rk4","ruth4", "svcp10s35"], "Método de integração temporal não implementado: " + self.method

        # Construir o vetor para aramazenar a solução em qualquer instante
        self.vector_template = VectorNCorpos(self.N, np.zeros(self.N))

        # Define a condição inicial
        self.vector_t_start = VectorNCorpos(self.N, u0)

    # Execução de um passo de tempo
    def step(self, u_start: VectorNCorpos, t_start: float, t_stop: float) -> VectorNCorpos:
        h = t_stop - t_start
        
        valores = u_start.get_values()
        q0, p0 = valores[0], valores[1]

        parametros = [h, self.massas, q0, p0, self.G, self.eps]

        if self.method == "euler_exp":
            q1, p1 = integradores.euler_explicito(*parametros)
        
        elif self.method == "euler_simp":
            q1, p1 = integradores.euler_simpletico(*parametros)

        elif self.method == "verlet":
            q1, p1 = integradores.verlet(*parametros)

        elif self.method == "rk2":
            q1, p1 = integradores.rk2(*parametros)

        elif self.method == "rk4":
            q1, p1 = integradores.rk4(*parametros)

        elif self.method == "ruth4":
            q1, p1 = integradores.ruth4(*parametros)

        elif self.method == "svcp10s35":
            q1, p1 = integradores.svcp10s35(*parametros)

        if self.colidir:
            p1 = np.array(p1, order='F')
            fncorpos.verificar_colisoes(self.massas, np.array(q1, order='F'), p1, self.raio)
            # p1 = integradores.detectar_aplicar_colisoes(self.massas, q1, p1, self.raio)

        return VectorNCorpos(self.N, np.array([q1, p1]))
