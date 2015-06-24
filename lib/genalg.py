# -*- coding: utf-8 -*-
"""
Created on Wed May  6 09:27:01 2015

@author: willy, max
"""

import random as rand
import numpy as np
from copy import deepcopy
import json

def integral(X, Y):
    ''' Calculate distance from step function to abscissa line. '''
    rectangle = lambda x0, x1, y: (x1 - x0) * y / x0
    integral = [rectangle(X[i], X[i+1], Y[i]) for i in range(len(X)-1)]
    return np.array(integral)


class Individual:

    ''' Model. '''

    def __init__(self, Model, maxTime, maxIslands, switches):
        # Maximal time allowed
        self.maxTime = maxTime
        # Number of islands
        self.n = np.random.random_integers(2, maxIslands)
        #self.n = maxIslands
        # Times of flow rate changes
        self.T = [0] + sorted([rand.uniform(0, self.maxTime)
                              for _ in range(switches)])
        # Flow rates
        self.M = [rand.uniform(0, 30) for _ in range(switches + 1)]
        # Create model
        self.model = Model(self.n, self.T, self.M)
        # Fitness
        self.fitness = None

    def evaluate_least_squares(self, times, lambdas):
        # Update the model
        self.model.update(self.n, self.T, self.M)
        # Compute the differences
        modelLamdbas = [self.model.lambda_s(t) for t in times]
        differences = np.array(lambdas) - np.array(modelLamdbas)
        # The fitness is the sum of the squared differences
        self.fitness = np.sum(np.square(differences))

    def evaluate_integral(self, times, referenceIntegral):
        # Update the model
        self.model.update(self.n, self.T, self.M)
        # Get the new lambdas
        lambdas = [self.model.lambda_s(t) for t in times]
        # Compute the model integral
        modelIntegral = integral(times, lambdas)
        # The fitness is the difference between both
        self.fitness = np.sum((modelIntegral - referenceIntegral) ** 2)

    def mutate(self, rate=30):
        threshold = rand.random()
        if threshold < 0.33:
            self.mutate_T(rate)
        elif threshold < 0.66:
            self.mutate_M(rate)
        elif threshold < 0.88:
            self.mutate_T_M(rate)
        else:
            self.mutate_n(1)
            #self.mutate_T_M(rate)

    def mutate_T(self, variance):
        if len(self.T) >= 2:
            sampleSize = rand.randint(1, len(self.T) - 1)
            sample = rand.sample(range(1, len(self.T)), sampleSize)
            for i in sample:
                t = self.T[i]
                self.T[i] = rand.normalvariate(t, variance)
                while not 0 < self.T[i] < self.maxTime:
                    self.T[i] = rand.normalvariate(t, variance)
                self.T.sort()

    def mutate_M(self, variance):
        sampleSize = rand.randint(1, len(self.M))
        sample = rand.sample(range(len(self.M)), sampleSize)
        for i in sample:
            m = self.M[i]
            self.M[i] = rand.normalvariate(m, variance)
            while not 0 < self.M[i]:
                self.M[i] = rand.normalvariate(m, variance)

    def mutate_T_M(self, variance):
        if len(self.T) >= 2:
            sampleSize = rand.randint(1, len(self.T)-1)
            sample = rand.sample(range(1, len(self.T)), sampleSize)
            for i in sample:
                t = self.T[i]
                self.T[i] = rand.normalvariate(t, variance)
                while not 0 < self.T[i] < self.maxTime:
                    self.T[i] = rand.normalvariate(t, variance)
                self.T.sort()
                m = self.M[i]
                self.M[i] = rand.normalvariate(m, variance)
                while not self.M[i] > 0:
                    self.M[i] = rand.normalvariate(m, variance)

    def mutate_n(self, variance):
        n = self.n
        self.n = n + np.random.choice((-variance, variance))
        while not self.n >= 2:
            self.n = n + np.random.choice((-variance, variance))

    # Save the DNA of the individual (the parameters)
    def save(self, path):
        # Create a dictionary
        DNA = {'n': self.n,
               'T': list(self.T),
               'M': list(self.M),
               'method': {'name': 'Genetic Algorithm',
                          'fitness': self.fitness
                          }
               }
        # Save it a s a .json file
        with open(path + '.json', 'w') as outfile:
            json.dump(DNA, outfile)
        # Tell the user the inference has been saved
        print ('Inference saved to {0}'.format(path))


class Population:

    ''' List of models for a given number of islands. '''

    def __init__(self, Model, times, lambdas, maxIslands, switches,
                 size=1000, repetitions=1, method='least_squares'):
        # Timeframe to study
        self.times = np.array(times)
        # PSMC distribution to fit
        self.lambdas = np.array(lambdas)
        # Calculate integral for comparing
        self.integral = integral(self.times, self.lambdas)
        # Number of switches
        self.switches = switches
        # Fitness method
        self.method = method
        # Create initial random individuals
        self.individuals = [[Individual(Model, self.times[-1],
                             maxIslands, self.switches)
                            for _ in range(size)]
                            for _ in range(repetitions)]
        # Evaluate them
        for i in range(repetitions):
            self.evaluate(i)
        # Store the best model
        self.best = np.random.choice(self.individuals[0])
        self.best.fitness = np.inf

    # Sort in ascending order (smallest to highest fitness)
    def sort(self, index):
        self.individuals[index].sort(key=lambda indi: indi.fitness)

    # Evaluate all the individuals
    def evaluate(self, index):
        for indi in self.individuals[index]:
            if self.method == 'least_squares':
                indi.evaluate_least_squares(self.times, self.lambdas)
            elif self.method == 'integral':
                indi.evaluate_integral(self.times, self.integral)
        self.sort(index)

    # Elitism
    def elite(self, size, index):
        return self.individuals[index][:size]

    # Tournament selection
    def tournament(self, size, tournamentSize, index):
        newIndividuals = []
        for _ in range(size):
            # Choose random participants for the tournament
            participants = rand.sample(self.individuals[index],
                                       tournamentSize)
            # Sort them by fitness
            participants.sort(key=lambda indi: indi.fitness)
            # Append the best to the new list
            newIndividuals.append(participants[0])
        return newIndividuals

    # Linear rank based roulette selection
    def rankedRoulette(self, size):
        return 'to do'

    # Mutate the population
    def enhance(self, generations):
        for i in range(len(self.individuals)):
            for _ in range(generations):
                newIndividuals = []
                for individual in self.tournament(20, 10, i):
                    # Create a copy of the individual
                    newIndividuals.append(deepcopy(individual))
                    # Enhance
                    for _ in range(5):
                        newIndividual = deepcopy(individual)
                        newIndividual.mutate()
                        newIndividuals.append(newIndividual)
                # Renew to population
                self.individuals[i] = newIndividuals
                # Reevaluate the new models
                self.evaluate(i)
                # Check if there is a new best individual
                if self.individuals[i][0].fitness < self.best.fitness:
                    self.best = deepcopy(self.individuals[i][0])
