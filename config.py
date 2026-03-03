import numpy as np
import ncorpos_utilidades as nut
import testes

#### Problema de 3 corpos - Lemniscata
from testes.t1_lemniscata import *

#### Problema de 5 corpos - Coreografia
# from testes.t2_ccnmas5 import *

#### Problema de 5 corpos - Joao
# from testes.t3_joao import *

#### Problema de 12 corpos - Coreografia
# from testes.t4_ccnmas12 import *

#### Teste geral
# from testes.t5_gerar import *

#### Teste colisoes
# from testes.t6_colisoes import *

# Integrais primeiras
E0 = nut.energia_total(massas, q0, p0, G, eps)
J0 = nut.momento_angular_total(q0, p0)

nt_slices = parametros["num_janelas"] + 1
nt_fino = parametros["multip_fino"] * (nt_slices - 1) + 1
nt_gros = parametros["multip_grosseiro"] * (nt_slices - 1) + 1
N_dt_per_slice = int((nt_fino-1)/(nt_slices-1))