#conding=utf-8

import numpy as np
import random

class chooseAndNotChoose(object):
    
    def __init__(self, numberOfBest, soup):
        self._numberOfBest = numberOfBest
        self._soup = soup

    def __call__(self, oldPop, oldFit, newPop, newFit):
    
        # create the set of pairs: best candidates 
        # + soup to keep genetic variance
        # select best candidates
        idFit = np.argpartition(oldFit, self._numberOfBest) # seleciona os melhores candidatos
    
        choose = [ i for i in idFit[:self._numberOfBest] ]
        notChoose = [ i for i in range(len(newFit)) if i not in choose ]
    
        # seleciona randômicamente indivíduos da população, 
        # para manter variablidade genética    
        soupChoose = random.sample(notChoose, self._soup) 
    
        choose += soupChoose # candidatos salvos
        
        for l in choose:
            newPop[l] = oldPop[l] 
            newFit[l] = oldFit[l]

class chooseAndNotChoose(object):
    
    def __init__(self, numberOfBest, soup):
        self._numberOfBest = numberOfBest
        self._soup = soup

    def __call__(self, oldPop, oldFit, newPop, newFit):
    
        # create the set of pairs: best candidates 
        # + soup to keep genetic variance
        # select best candidates
        idFit = np.argpartition(oldFit, self._numberOfBest) # seleciona os melhores candidatos
    
        choose = [ i for i in idFit[:self._numberOfBest] ]
        notChoose = [ i for i in range(len(newFit)) if i not in choose ]
    
        # seleciona randômicamente indivíduos da população, 
        # para manter variablidade genética    
        soupChoose = random.sample(notChoose, self._soup) 
    
        choose += soupChoose # candidatos salvos
        
        for l in choose:
            newPop[l] = oldPop[l] 
            newFit[l] = oldFit[l]

def simplemate(oldPop, oldFit, newPop, newFit):
    return newPop
