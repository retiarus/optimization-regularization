#coding=utf-8

import numpy as np


class nonuniform(object):

    def __init__(self, 
                 linf, 
                 lsup,
                 degreeOfnonUniformity, 
                 maximalGenerationNumber):

        self._lsup = lsup
        self._linf = linf
        self._b = degreeOfnonUniformity
        self._T = maximalGenerationNumber

    def __call__(self, x, t):

        number = np.random.choice(range(0, len(x)), 2)
        for j in number:
            if np.random.choice([0, 1]) == 0:
                x[j] += self._delta(t, self._lsup - x[j])
            else:
                x[j] -= self._delta(t, x[j] - self._linf)
        
    def _delta(self, t, x):
        return x*(1-np.random.rand()**((1-t/self._T)**self._b))
