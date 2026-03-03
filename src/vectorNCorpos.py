from pymgrit.core.vector import Vector
import numpy as np

class VectorNCorpos (Vector):

    def __init__ (self, N, value):
        # Chama o construtor da classe acima
        super().__init__()
        # inicializa
        self.N = N
        if type(value) == int: self.value = np.zeros((2,N,3))
        else: self.value = value

    def set_values (self, value):
        self.value = value

    def get_values (self):
        return self.value

    def clone (self):
        return VectorNCorpos(self.N, self.value)

    def clone_zero (self):
        return VectorNCorpos(self.N, 0)

    def clone_rand (self):
        return VectorNCorpos(self.N, np.random.rand((2,self.N,3)))

    def __add__ (self, outro):
        tmp = VectorNCorpos(self.N, 0)
        tmp.set_values(self.get_values() + outro.get_values())
        return tmp

    def __sub__ (self, outro):
        tmp = VectorNCorpos(self.N, 0)
        tmp.set_values(self.get_values() - outro.get_values())
        return tmp

    def __mul__ (self, escalar):
        tmp = VectorNCorpos(self.N, 0)
        tmp.set_values(self.get_values() * escalar)
        return tmp

    def norm (self):
        return np.linalg.norm(self.value)

    def pack (self):
        return self.value

    def unpack (self, value):
        self.value = value
