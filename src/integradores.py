import numpy as np
from src.forcas_ncorpos import forcas_ncorpos as fncorpos

def detectar_aplicar_colisoes (ms, qs, ps, raio):
    for a in range(len(ms)):
        for b in range(a):
            rab = qs[b] - qs[a]
            dist2 = rab @ rab
            if dist2 <= 4*raio**2 and rab @ (ps[b] - ps[a]) < 0:
                ps[a], ps[b] = colidir(ms[a], qs[a], ps[a], ms[b], qs[b], ps[b])
    return ps

def colidir (ma, Ra, Pa, mb, Rb, Pb):
    N = Rb - Ra
    N2 = N @ N

    u1 = (Pa @ N) / ma
    u2 = (Pb @ N) / mb

    k = 2.0 * (u2 - u1) * ma * mb / ((ma + mb) * N2)

    Pa = Pa + k * N
    Pb = Pb - k * N

    return Pa, Pb

def forcas1(massas:np.array, posicoes:np.array, G:float=1.0, eps:float=0.0)->np.array:
    N = massas.shape[0]
    F = np.zeros((N, 3), dtype=posicoes.dtype)
    eps2 = eps * eps

    for a in range(N):
        for b in range(a):
            rab = posicoes[b] - posicoes[a]
            dist2 = 0.0
            dist2 = rab[0] * rab[0] + rab[1] * rab[1] + rab[2] * rab[2]

            den = (dist2 + eps2) ** 1.5
            coef = G * massas[a] * massas[b] / den

            f = coef * rab[0]
            F[a, 0] += f
            F[b, 0] -= f

            f = coef * rab[1]
            F[a, 1] += f
            F[b, 1] -= f
            
            f = coef * rab[2]
            F[a, 2] += f
            F[b, 2] -= f

    return F

def f_q (m:np.array, p:np.array)->np.array:
    """Aplica p/m"""
    return np.array([p[a]/m[a] for a in range(len(m))])

def f_p (m:np.array, q:np.array, G:float=1.0, eps:float=0.0)->np.array:
    """Aplica F(q)"""
    F = np.zeros((len(m), 3), order='F')
    fncorpos.forcas(m, q, G, eps, F)
    return F

def euler_explicito (h:float, m:np.array, q0:np.array, p0:np.array, G:float=1.0, eps:float=0.0)->tuple:
    q1 = q0 + h * f_q(m, p0)
    p1 = p0 + h * f_p(m, q0, G, eps)
    return (q1, p1)

def euler_simpletico (h:float, m:np.array, q0:np.array, p0:np.array, G:float=1.0, eps:float=0.0)->tuple:
    p1 = p0 + h * f_p(m, q0, G, eps)
    q1 = q0 + h * f_q(m, p1)
    return (q1, p1)

def verlet (h:float, m:np.array, q0:np.array, p0:np.array, G:float=1.0, eps:float=0.0)->tuple:
    p1 = p0 + 0.5 * h * f_p(m, q0, G, eps)
    q1 = q0 + h * f_q(m, p1)
    p1 = p1 + 0.5 * h * f_p(m, q1, G, eps)
    return (q1, p1)

def rk2 (h:float, m:np.array, q0:np.array, p0:np.array, G:float=1.0, eps:float=0.0)->tuple:
    k1q = f_q(m, p0)
    k1p = f_p(m, q0, G, eps)

    k2q = f_q(m, p0 + 0.5*h*k1p)
    k2p = f_p(m, q0 + 0.5*h*k1q, G, eps)

    q1 = q0 + h * k2q
    p1 = p0 + h * k2p
    return (q1, p1)

def rk4 (h:float, m:np.array, q0:np.array, p0:np.array, G:float=1.0, eps:float=0.0)->tuple:
    k1q = f_q(m, p0)
    k1p = f_p(m, q0, G, eps)

    k2q = f_q(m, p0 + 0.5*h*k1p)
    k2p = f_p(m, q0 + 0.5*h*k1q, G, eps)

    k3q = f_q(m, p0 + 0.5*h*k2p)
    k3p = f_p(m, q0 + 0.5*h*k2q, G, eps)

    k4q = f_q(m, p0 + h*k3p)
    k4p = f_p(m, q0 + h*k3q, G, eps)
    
    q1 = q0 + h/6 * (k1q + 2*k2q + 2*k3q + k4q)
    p1 = p0 + h/6 * (k1p + 2*k2p + 2*k3p + k4p)
    return (q1, p1)

def ruth4 (h:float, m:np.array, q0:np.array, p0:np.array, G:float=1.0, eps:float=0.0)->tuple:
    d1, c1 =  1.3512071919596578,  0.67560359597982889
    d2, c2 = -1.7024143839193153, -0.17560359597982883
    d3, c3 =  1.3512071919596578, -0.17560359597982883
    d4, c4 =  0.0,                 0.67560359597982889
    
    p1 = p0
    q1 = q0 + c4 * h * f_q(m, p1)
    
    p1 = p1 + d3 * h * f_p(m, q1, G, eps)
    q1 = q1 + c3 * h * f_q(m, p1)

    p1 = p1 + d2 * h * f_p(m, q1, G, eps)
    q1 = q1 + c2 * h * f_q(m, p1)

    p1 = p1 + d1 * h * f_p(m, q1, G, eps)
    q1 = q1 + c1 * h * f_q(m, p1)

    return (q1, p1)

def svcp10s35 (h:float, m:np.array, q0:np.array, p0:np.array, G:float=1.0, eps:float=0.0)->tuple:
    s = [0.07879572252168641926390768,0.31309610341510852776481247,
        0.02791838323507806610952027,-0.22959284159390709415121340,
        0.13096206107716486317465686,-0.26973340565451071434460973,
        0.07497334315589143566613711,0.11199342399981020488957508,
        0.36613344954622675119314812,-0.39910563013603589787862981,
        0.10308739852747107731580277,0.41143087395589023782070412,
        -0.00486636058313526176219566,-0.39203335370863990644808194,
        0.05194250296244964703718290,0.05066509075992449633587434,
        0.04967437063972987905456880,0.04931773575959453791768001,
        0.04967437063972987905456880,0.05066509075992449633587434,
        0.05194250296244964703718290,-0.39203335370863990644808194,
        -0.00486636058313526176219566,0.41143087395589023782070412,
        0.10308739852747107731580277,-0.39910563013603589787862981,
        0.36613344954622675119314812,0.11199342399981020488957508,
        0.07497334315589143566613711,-0.26973340565451071434460973,
        0.13096206107716486317465686,-0.22959284159390709415121340,
        0.02791838323507806610952027,0.31309610341510852776481247,
        0.07879572252168641926390768]
    
    q1, p1 = q0, p0
    F = f_p(m, q1, G, eps)
    for i in range(len(s)-1, 0, -1):
        h_s = s[i] * h
        p1 = p1 + 0.5 * h_s * F
        q1 = q1 + h_s * f_q(m, p1)
        F = f_p(m, q1, G, eps)
        p1 = p1 + 0.5 * h_s * F

    return (q1, p1)