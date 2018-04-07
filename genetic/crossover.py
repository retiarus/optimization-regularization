#coding=utf-8

import numpy as np


class geometric(object):


    def __init__(self, weight):
        self._weight = weight

    def __call__(self, x, y):
        return self._vecgeometric(x, y)

    def _vecgeometric(self, x, y):
        v = np.vectorize(self._geometric)
        return v(x, y) 

    def _geometric(self, x, y):
        return  (x**self._weight)*(y**(1-self._weight))
