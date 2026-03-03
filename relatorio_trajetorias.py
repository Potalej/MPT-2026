from src.integradores import *
import numpy as np
from funcoes import ler_vi_json
import matplotlib.pyplot as plt

#### Problema de 3 corpos - Lemniscata
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

tf = 2
h = 0.001
qntd_passos = int(tf / h)

corpos = [[] for m in massas]
q, p = q0.copy(), p0.copy()

plt.figure(figsize=(4,4))
plt.grid(True)

for _ in range(qntd_passos):
  q,p = ruth4(h, massas, q, p, G, eps)
  for i,qi in enumerate(q):
    corpos[i].append(qi)
  
for i, corpo in enumerate(corpos):
  x,y,z = list(zip(*corpo))
  plt.plot(x,y)
  
  p = p0[i]
  plt.quiver(x[0],y[0],p[0],p[1],angles='xy',scale=10,width=7e-3)
  plt.scatter(x[0],y[0])

plt.xlim(-1.2,1.2)
plt.ylim(-1.2,1.2)
plt.title("Lemniscata")
plt.tight_layout()
plt.savefig("img/vi/lemniscata.png")



# #### Problema de 12 corpos - Coreografia
massas, q0, p0, G, eps = ler_vi_json('valores_iniciais/CCNMAS12_1.json')
tf = 8
h = 0.001
qntd_passos = int(tf / h)

corpos = [[] for m in massas]
q, p = q0.copy(), p0.copy()

plt.figure(figsize=(4,4))
plt.grid(True)

for _ in range(qntd_passos):
  q,p = ruth4(h, massas, q, p, G, eps)
  for i,qi in enumerate(q):
    corpos[i].append(qi)
  
for i, corpo in enumerate(corpos):
  x,y,z = list(zip(*corpo))
  plt.plot(x,y)
  
  p = p0[i]
  plt.quiver(x[0],y[0],p[0],p[1],angles='xy')
  plt.scatter(x[0],y[0])

plt.xlim(-1.2,1.2)
plt.ylim(-1.2,1.2)
plt.title("Coreografia-Doicu 12 corpos (1)")
plt.tight_layout()
plt.savefig("img/vi/ccnmas12_1.png")


#### Problema de 5 corpos - Coreografia
massas, q0, p0, G, eps = ler_vi_json('valores_iniciais/CCNMAS5_1.json')
tf = 8
h = 0.001
qntd_passos = int(tf / h)

corpos = [[] for m in massas]
q, p = q0.copy(), p0.copy()

plt.figure(figsize=(4,4))
plt.grid(True)

for _ in range(qntd_passos):
  q,p = ruth4(h, massas, q, p, G, eps)
  for i,qi in enumerate(q):
    corpos[i].append(qi)
  
for i, corpo in enumerate(corpos):
  x,y,z = list(zip(*corpo))
  plt.plot(x,y)
  
  p = p0[i]
  plt.quiver(x[0],y[0],p[0],p[1],angles='xy')
  plt.scatter(x[0],y[0])

plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)
plt.title("Coreografia-Doicu 5 corpos (1)")
plt.tight_layout()
plt.savefig("img/vi/ccnmas5_1.png")




#### Problema de 5 corpos - Joao
G, eps = 1.0, 0.0
massas = np.ones(5)
q0 = np.array([[-1., 0., 0.], [0., -1., 0.], [1., 0., 0.], [0., 1., 0.], [0.0, 0.0, 0.]])
p0 = np.array([[0., -1., 0.], [1., 0., 0.], [0., 1., 0.], [-1., 0., 0.], [0.0, 0.0, 0.]])
tf = 8
h = 0.001
qntd_passos = int(tf / h)

corpos = [[] for m in massas]
q, p = q0.copy(), p0.copy()

plt.figure(figsize=(4,4))
plt.grid(True)

for _ in range(qntd_passos):
  q,p = ruth4(h, massas, q, p, G, eps)
  for i,qi in enumerate(q):
    corpos[i].append(qi)
  
for i, corpo in enumerate(corpos):
  x,y,z = list(zip(*corpo))
  plt.plot(x,y)
  
  p = p0[i]
  plt.quiver(x[0],y[0],p[0],p[1],angles='xy')
  plt.scatter(x[0],y[0])

plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)
plt.title("Coreografia de 5 corpos")
plt.tight_layout()
plt.savefig("img/vi/joao_5.png")