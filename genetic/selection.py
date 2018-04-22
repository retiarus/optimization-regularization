#coding=utf-8

import numpy as np
import pdb

def tournamentSelection(fit, k=6):
    sizeOfPopulation = len(fit)
    fatherSet = np.random.randint(low=0, high=sizeOfPopulation, size=k)
    set = [fit[i] for i in fatherSet]

    idFit = np.argpartition(set, 2) # seleciona os melhores candidatos
    fathers = tuple(i for i in idFit[:2])
    
    return fathers

#def mySelection(Population, Fit, k = 4):
    # seleciona os melhores candidatos
#    idFit = np.argpartition(Fit, NumberOfBest) 
#    Choose = [ i for i in idFit[:NumberOfBest] ]
#    
#    fathers = np.random.choice(Choose, size=2)
 
#    return tuple(fathers)
