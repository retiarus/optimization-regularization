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

def mutGaussian(individual, mu, sigma, prob_atrib_mut):

    assert 0.0 <= prob_atrib_mut <= 1.0
    size = len(individual)
    def aux():
        for i in range(size):
            if np.random.uniform() < prob_atrib_mut:
                attr = individual[i] + np.random.gauss(m, s)
            else:
                attr = individual[i]

            yield attr

    individual = np.fromiter(aux(), float, count=size)

    return individual
