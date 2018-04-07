#coding=utf-8

import numpy as np
import random
import pdb

from pathos.multiprocessing import ProcessingPool, cpu_count

class optmizer():
    def __init__(self, fun, x):
        self.fun = fun


class individual(object):


    def __init__(self, Nx, InfBound, SupBound):
        self._Nx = Nx
        self._InfBound = InfBound
        self._SupBound = SupBound
        self._diff = self._SupBound - self._InfBound

    def __call__(self, idx=0):
        return self._diff*np.random.random_sample((self._Nx,)) + self._InfBound


class generateOfSring(object):


    def __init__(self, selection, crossover, mutation):
        self._selection = selection
        self._crossover = crossover
        self._mutation = mutation

    def __call__(self, fit, pop, generation):
        father = self._selection(fit)
        individual = self._crossover(pop[father[0]], 
                                     pop[father[1]])
        self._mutation(individual, generation)
        return individual
            

class geneticOptimizer(object):


    def __init__(self,
                 population,
                 spring,
                 mate,
                 objective,
                 epidemic, 
                 sizeOfPopulation,
                 minimalGenerationNumber, 
                 maximalGenerationNumber,
                 statistic=None,
                 verbose=True,
                 error = 10.0**(-8)):

        self._population = population
        self._spring = spring
        self._mate = mate
        self._objective = objective
        self._epidemic = epidemic 
        self._sizeOfPopulation = sizeOfPopulation
        self._error = error 
        self._minimalGenerationNumber = minimalGenerationNumber 
        self._maximalGenerationNumber = maximalGenerationNumber
        self._statistic = statistic
        self._verbose = verbose

        if epidemic:
            print('epidemic:', epidemic)

        if minimalGenerationNumber > maximalGenerationNumber:
            print('fail: minimalGenerationNumber > maximalGenerationNumber')
            os.sys.exit(1)

        self._t = 0
        self._countEpidemic = 0
        self._countNumberOfEpidemicActivate = 0

        self._oldBest = None
        self._actualBest = None

        # gera população inicial e calcula o fitness
        self._fit = np.array(ProcessingPool(ncpus=cpu_count()).map(
            self._objective, self._population))

    def __call__(self):
        while self._t < self._maximalGenerationNumber:

            # incremet generation
            self._t += 1

            # apply generateOfSpring
            oldPopulation = np.copy(self._population)
            oldPopulationFit = np.copy(self._fit)

            def aux(idx, 
                    fit=oldPopulationFit, 
                    pop=oldPopulation, 
                    generation=self._t):

                    return spring(fit, pop, generation)

            self._population = np.array(ProcessingPool(ncpus=cpu_count()).map(
                aux, range(self._sizeOfPopulation)))
            self._fit = np.array(ProcessingPool(ncpus=cpu_count()).map(
                objective, self._population))

            # combine generation
            self._mate(oldPopulation, oldPopulationFit, self._population, self._fit)
        
            # avaliate best individual
            self._oldBest = self._actualBest
            self._actualBest = np.argpartition(self._fit, 1)[:1]
            #self._actualBest = optmizer(x = self._population[actualBest], fun = self._fit[actualBest])
            self._actualBest = (self._population[self._actualBest], self._fit[self._actualBest])
            
            if self._verbose:
                if self._statistic is None:
                    print(self._t, ": ", self._fit.max(), self._fit.min(), self._fit.std())
                    
            # verifiy epidemic
            #if t > 5:
            #    if epidemic:
            #        if oldBest == actualBest:
            #            countEpidemic += 1
            #            print('countEpidemic:', countEpidemic)
            #    
            #        if countEpidemic > 5:
            #            countNumberOfEpidemicActivate += 1
            #            print('epidemic activate')
            #            idFit = np.argpartition(Fit, 5)
            #            Choose = ([ i for i in idFit[:5] ])
            #            notChoose = ([ i for i in islice(count(), 0, Nx) if i not in idFit[:5] ]) 
            #            for l in notChoose:
            #                Pop[l] = (SupBound - InfBound)*np.random.random_sample((Nx,)) + InfBound
            #            countEpidemic = 0
            
            # test criter of convergegion
            #if t > minimalGenerationNumber:
            #    if np.abs((self._actualBest.fun - self._oldBest.fun)/self._actualBest.fun) < error:
            #        return actualBest
