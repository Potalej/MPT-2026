MODULE forcas_ncorpos
  IMPLICIT NONE
  PUBLIC :: forcas, verificar_colisoes
CONTAINS
  SUBROUTINE forcas (massas, posicoes, G, eps, F)
    REAL(8), INTENT(IN) :: massas(:), posicoes(:,:), G, eps
    REAL(8), INTENT(INOUT) :: F(:,:)
    REAL(8) :: dist2, Fab(3), den
    INTEGER :: a, b

    F = 0
    DO a = 1, SIZE(massas)
      DO b = 1, a - 1
        Fab = posicoes(b,:) - posicoes(a,:)
        dist2 = DOT_PRODUCT(Fab, Fab)
        den = SQRT(dist2 + eps*eps)
        Fab = G * massas(a) * massas(b) * Fab / (den**3)
        F(a,:) = F(a,:) + Fab
        F(b,:) = F(b,:) - Fab
      END DO
    END DO
  END SUBROUTINE

  SUBROUTINE verificar_colisoes (massas, posicoes, momentos, raio)
    REAL(8), INTENT(IN) :: massas(:), posicoes(:,:), raio
    REAL(8), INTENT(INOUT) :: momentos(:,:)
    REAL(8) :: dist, ang, qa(3),qb(3), pa(3), pb(3)
    INTEGER :: a, b

    DO a = 1, SIZE(massas)
      qa = posicoes(a,:)
      pa = momentos(a,:)
      DO b = 1, a - 1
        qb = posicoes(b,:)
        pb = momentos(b,:)
        ang = DOT_PRODUCT(qb - qa, pb - pa)
        IF (ang < 0) THEN
          dist = NORM2(qb - qa)
          IF (dist <= 2*raio) THEN
            CALL colidir(massas(a), qa, momentos(a,:), massas(a), qb, momentos(b,:))
          ENDIF
        ENDIF
      END DO
    END DO
  END SUBROUTINE

  SUBROUTINE colidir (ma, Ra, Pa, mb, Rb, Pb)
    IMPLICIT NONE
    REAL(8) :: ma, mb, Ra(3), Pa(3), Rb(3), Pb(3)
    REAL(8) :: Normal(3), norma2, u1, u2, k

    ! vetor normal e normal unitario
    Normal = Rb - Ra
    norma2 = DOT_PRODUCT(Normal, Normal)

    ! calcula a componente normal
    u1 = DOT_PRODUCT(Pa, Normal) / ma
    u2 = DOT_PRODUCT(Pb, Normal) / mb

    ! agora calcula o componente de angulo
    k = 2.0 * (u2 - u1) * ma * mb / ((ma + mb) * norma2)

    ! por fim, aplica a colisao
    Pa = Pa + k * Normal
    Pb = Pb - k * Normal 

END SUBROUTINE colidir

END MODULE forcas_ncorpos