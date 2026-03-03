# Métodos Paralelos no Tempo (Verão 2026)

Exercício-programa do curso MAP5938 - Introdução a métodos numéricos paralelos no tempo (2026). O objetivo foi testar a aplicação do método Parareal através da biblioteca `pymgrit` em algum problema. No caso, escolhi o problema de N-corpos gravitacional.

## Compilando o Fortran

```
python -m numpy.f2py -c -m forcas_ncorpos forcas.f90
```