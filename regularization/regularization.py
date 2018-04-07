import numpy as np
import os
from itertools import islice, count
'''
Refularization Module
'''

#class Regularization(object):
#    def __init__(self, Nx, name, Aux = None):
#        self._Nx = Nx
#        self._Aux = Aux
#        self.reg = self.__reg__(self.Nx, self.Aux)
#        self.name = name
#
#    def __call__(self, f):
#        if len(f) != self.Nx:
#            return None
#        else:
#            return self.reg(f)
#
#    def __reg__(self, Nx, aux):
#        None
#
#class TikhonovOrder02(Regularization):
#    def __reg__(self, Nx, aux):
#        Omega = np.zeros((self.Nx, self.Nx))
#
#        # Tikhonovo of order 0 - identity matrix
#        for i in islice(count(), 0, self.Nx):
#            self.Omega[i][i] = 1
#
#        return lambda f: np.sum(self.Omega.dot(f)**2.0)

class NoRegularization(object):
    def __init__(self, Nx):
        self.Nx = Nx
        self.Omega = np.zeros((self.Nx, self.Nx))

    def __call__(self, f):
        if len(f) != self.Nx:
            return None
        else:
            return np.linalg.norm(self.Omega.dot(f), 2)

class TikhonovOrder0(object):
    def __init__(self, Nx):
        self._Nx = Nx
        self._Omega = np.zeros((self._Nx, self._Nx))
        self.name = 'Tikhonov Order 0'
        self.type = 'tikhonovorder0'

        # Tikhonovo of order 0 - identity matrix
        for i in islice(count(), 0, self._Nx):
            self._Omega[i][i] = 1

    def __call__(self, f):
        if len(f) != self._Nx:
            return None
        else:
            return np.sum(self._Omega.dot(f)**2.0)

class TikhonovOrder1(object):
    def __init__(self, Nx):
        self._Nx = Nx
        self._Omega = np.zeros((self._Nx, self._Nx))
        self.name = 'Tikhonov Order 1'
        self.type = 'tikhonovorder1'

        for i in islice(count(), 0, self._Nx-1):
            self._Omega[i][i] = -1.
            if i + 1 < self._Nx:
                self._Omega[i][i+1] = 1.

    def __call__(self, f):
        if len(f) != self._Nx:
            return None
        else:
            return np.sum(self._Omega.dot(f)**2.0)

class TikhonovOrder2(object):
    def __init__(self, Nx):
        self._Nx = Nx
        self._Omega = np.zeros((self._Nx, self._Nx))
        self.name = 'Tikhonov Order 2'
        self.type = 'tikhonovorder2'

        for i in islice(count(), 1, self._Nx-1):
            self._Omega[i][i] = -2.
            if i + 1 < Nx:
                self._Omega[i][i+1] = 1.
            if i - 1 >= 0:
                self._Omega[i][i-1] = 1.

    def __call__(self, f):
        if len(f) != self._Nx:
            return None
        else:
            return np.sum(self._Omega.dot(f)**2.0)

class MaxEntropy0(object):
    def __init__(self, Nx):
        self.name = 'Max Entropy Order 0'
        self.type = 'maxentropy0'

        self._Nx = Nx
        self._Smax = np.log(self._Nx)
        self._chi = 0.1

    def __call__(self, f):
        if len(f) != self._Nx:
            return None
        else:
            fmin = np.min(f)
            p = f - fmin + self._chi
            psum = np.sum(p)
            s = p/psum
            return 1.0 - np.sum(s*np.log(s))/self._Smax

class MaxEntropy1(object):
    def __init__(self, Nx):
        self.name = 'Max Entropy Order 1'
        self.type = 'maxentropy1'

        self._Nx = Nx
        self._Omega = np.zeros((self._Nx, self._Nx))
        self._Smax = np.log(self._Nx-1)
        self._chi = 0.1

        for i in islice(count(), 0, self._Nx-1):
            self._Omega[i][i] = -1.
            if i + 1 < self._Nx:
                self._Omega[i][i+1] = 1.

        print(self._Omega)

    def __call__(self, f):
        if len(f) != self._Nx:
            return None
        else:
            fmin = np.min(f)
            fmax = np.max(f)
            p = self._Omega.dot(f) + (fmax-fmin) + self._chi
            if np.min(p) < 0:
                print('alert')
                os.sys.exit('1')
            psum = np.sum(p[0:self._Nx-1])
            s = p/psum
            if np.min(s) < 0:
                print('alert')
                os.sys.exit('1')
            return 1.0 - np.sum(s*np.log(s))/self._Smax

class MaxEntropy2(object):
    def __init__(self, Nx):
        self.name = 'Max Entropy Order 2'
        self.type = 'maxentropy2'

        self._Nx = Nx
        self._Omega = np.zeros((self._Nx, self._Nx))
        self._Smax = np.log(self._Nx-2)
        self._chi = 0.1

        for i in islice(count(), 1, self._Nx-1):
            self._Omega[i][i] = -2.
            if i + 1 < Nx:
                self._Omega[i][i+1] = 1.
            if i - 1 >= 0:
                self._Omega[i][i-1] = 1.

        print(self._Omega)

    def __call__(self, f):
        if len(f) != self._Nx:
            return None
        else:
            fmin = np.min(f)
            fmax = np.max(f)
            p = self._Omega.dot(f) + 2*(fmax-fmin) + self._chi
            if np.min(p) < 0:
                print(p)
                print('alert')
                os.sys.exit('1')
            psum = np.sum(p[1:self._Nx-1])
            s = p/psum
            return 1.0 - np.sum(s*np.log(s))/self._Smax
