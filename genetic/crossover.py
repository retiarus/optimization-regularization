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

def cxBlend(ind_x, ind_y, alpha=0.5):

    assert 0.0 <= alpha <= 1.0
    def gamma():
        return (1.0 + 2.0*alpha)*np.random.uniform() - alpha

    ind = np.fromiter(((1.0-gamma())*x + gamma()*y for x, y in
                       zip(ind_x, ind_y)),
                      float,
                      count=len(ind_x))
    return ind

