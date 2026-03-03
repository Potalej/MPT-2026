from pymgrit.core.mgrit import Mgrit

class Parareal(Mgrit):
  """
  Classe implementando a interface para o método Parareal

  A classe herda da classe Mgrit da biblioteca pyMGRIT, e utiliza os parâmetros específicos para o método Parareal.
  """

  def __init__(self, problem, nt_slices, max_iter, output_parareal, tol, *args, **kwargs):
      """
      Construtor da classe

      Entradas:
      - problem (array): lista de instâncias da classe Application ([discretizacção fina, discretização grosseira])
      - nt_slices (int): número de instantes definindo as janelas de tempo ( = número de janelas de tempo + 1) de tamanho DT
      - max_iter (int): número máximo de iterações
      - output_parareal (funcão): função que armazena a solução em cada iteração
      - tol (float): critério de parada para as iterações
      """

      ## Identificar número de instantes de tempo nas discretizações fina (0) e grosseira (1)
      nt_level_0 = problem[0].nt
      nt_level_1 = problem[1].nt

      ## Por padrão, a biblioteca Mgrit adota DT = Dt (janelas temporais = passo de tempo grosseiro)
      ## Para forçar um DT específico, adotamos um parâmetro de relaxação igual a DT/Dt
      cf_iter = int((nt_level_1-1)/(nt_slices-1)) - 1

      ## Chama o construtor da classe Mgrit
      super().__init__(
                        problem = problem,
                        output_fcn = output_parareal,
                        output_lvl = 2,                 ## Guarda todas as iterações em arquivos de saída
                        max_iter = max_iter,
                        cf_iter = cf_iter,
                        tol = tol
                      )


