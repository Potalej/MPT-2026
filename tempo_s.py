import matplotlib.pyplot as plt
import numpy as np

k = np.linspace(0, 20, 100)

Np = 15
parametros = [
  ['1/32', 1/32, 1, 4],
  ['4/32', 4/32, 1, 4],
  ['1/32', 1/32, 2, 4],
  ['4/32', 4/32, 2, 4],
]

plt.figure(figsize=(6,3))
for a_txt, a, Rc, Rf in parametros:
  S = 1. / ((1. + k) * a * Rc/Rf + k / Np)
  plt.plot(k, S, label=rf"$\alpha={a_txt}$, $R_C={Rc}$, $R_F={Rf}$")

plt.title(r"Função $S(k)$ para $N_P=15$")
plt.axhline(1, linestyle='--', c='black')
plt.xticks([2*i for i in range(11)])
plt.ylim(0,3)
plt.legend()
plt.savefig("relatorio/img/funcao_S.png")