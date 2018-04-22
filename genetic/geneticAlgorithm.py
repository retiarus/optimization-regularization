# coding=utf-8

import numpy as np
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
                 individual,
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
                 generatePopulation=False,
                 error=10.0**(-8)):

        self._individual = individual
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

                    return self._spring(fit, pop, generation)

            self._population = np.array(ProcessingPool(ncpus=cpu_count()).map(
                aux, range(self._sizeOfPopulation)))
            self._fit = np.array(ProcessingPool(ncpus=cpu_count()).map(
                self._objective, self._population))

            # combine generation
            self._mate(oldPopulation,
                       oldPopulationFit,
                       self._population,
                       self._fit)

            # avaliate best individual
            self._oldBest = self._actualBest
            self._actualBest = np.argpartition(self._fit, 1)[:1]
            self._actualBest = (self._population[self._actualBest],
                                self._fit[self._actualBest])

            if self._verbose:
                if self._statistic is None:
                    print(self._t, ": ", self._fit.max(),
                          self._fit.min(), self._fit.std())

            if self._t > 5:
                if np.allclose(self._oldBest[1], self._actualBest[1]):
                    self._countEpidemic += 1
                else:
                    self._countEpidemic = 0

            # verifiy epidemic
            if self._epidemic:
                if self._countEpidemic > 5:
                    print("epidemic")
                    self._countNumberOfEpidemicActivate += 1

                    # find the two bests menbers of population
                    id_fit = np.argpartition(self._fit, 2)
                    choose = [i for i in id_fit[:2]]

                    # save the two bests members of orginal population
                    old_population = []
                    old_population_fit = []

                    for i in choose:
                        old_population.append(self._population[i])
                        old_population_fit.append(self._fit[i])

                    # generate new polulation and calc fit
                    self._population = np.array(ProcessingPool(ncpus=cpu_count()).map(
                        self._individual, range(self._sizeOfPopulation)))

                    self._fit = np.array(ProcessingPool(ncpus=cpu_count()).map(
                        self._objective, self._population))

                    # restore the two bests members
                    # of the original population
                    for idx, j in enumerate(choose):
                        self._population[j] = old_population[idx]
                        self._fit[j] = old_population_fit[idx]

                    self._countEpidemic = 0

            # test criter of convergegion
            #if t > minimalGenerationNumber:
            #    if np.abs((self._actualBest.fun - self._oldBest.fun)/self._actualBest.fun) < error:
            #        return actualBest
