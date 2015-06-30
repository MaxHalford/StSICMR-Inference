import random as rand
import numpy as np
from copy import deepcopy

def integral(X, Y):
    ''' Calculate distance from step function to abscissa line. '''
    rectangle = lambda x0, x1, y: (x1 - x0) * y / x0
    integral = [rectangle(X[i], X[i+1], Y[i]) for i in range(len(X)-1)]
    return np.array(integral)


class Individual:

    def __init__(self, Model, maxTime, maxIslands, switches):
        ''' Generate a model. '''
        # Maximal time allowed
        self.maxTime = maxTime
        # Number of islands
        self.n = np.random.random_integers(2, maxIslands)
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
        ''' Evaluate how close two vectors are. '''
        # Update the model
        self.model.update(self.n, self.T, self.M)
        # Compute the differences
        modelLamdbas = [self.model.lambda_s(t) for t in times]
        differences = np.array(lambdas) - np.array(modelLamdbas)
        # The fitness is the sum of the squared differences
        self.fitness = np.sum(np.square(differences))

    def evaluate_integral(self, times, referenceIntegral):
        ''' Evaluate how close two functions are. '''
        # Update the model
        self.model.update(self.n, self.T, self.M)
        # Get the new lambdas
        lambdas = [self.model.lambda_s(t) for t in times]
        # Compute the model integral
        modelIntegral = integral(times, lambdas)
        # The fitness is the difference between both
        self.fitness = np.sum((modelIntegral - referenceIntegral) ** 2)

    def mutate(self, rate):
        '''
        Randomly mutate islands, times, migrations rates or both. The
        mutation rates can be manually specified here. The general idea
        is that a big mutation rate will make the algorithm converge
        faster whereas a small mutation rate will make it converge
        better and more precisely.
        '''
        threshold = rand.random()
        if threshold < 0.33:
            self.mutate_T(rate)
        elif threshold < 0.66:
            self.mutate_M(rate)
        elif threshold < 0.88:
            self.mutate_T_M(rate)
        else:
            self.mutate_n(1)

    def mutate_T(self, variance):
        ''' Mutate times. '''
        # The first time is always 0
        if len(self.T) >= 2:
            # Choose how many times to mutate
            sampleSize = rand.randint(1, len(self.T) - 1)
            # Choose a sample of the chosen size
            sample = rand.sample(range(1, len(self.T)), sampleSize)
            # For each time
            for i in sample:
                # Mutate it
                t = self.T[i]
                self.T[i] = rand.normalvariate(t, variance)
                # Do it again as long as it is not valid
                while not 0 < self.T[i] < self.maxTime:
                    self.T[i] = rand.normalvariate(t, variance)
                # Sort them in ascending order
                self.T.sort()

    def mutate_M(self, variance):
        ''' Mutate migration rates. '''
        # The first time is always 0
        sampleSize = rand.randint(1, len(self.M))
        # Choose how many migration rates to mutate
        sample = rand.sample(range(len(self.M)), sampleSize)
        # For each migration rate
        for i in sample:
            # Mutate it
            m = self.M[i]
            self.M[i] = rand.normalvariate(m, variance)
            # Do it again as long as it is not valid
            while not 0 < self.M[i]:
                self.M[i] = rand.normalvariate(m, variance)

    def mutate_T_M(self, variance):
        ''' Mutate couples (time, rate). Same ideas as before. '''
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
        ''' Mutate number of islands. '''
        n = self.n
        # Mutate n
        self.n = n + np.random.choice((-variance, variance))
        # Verify that n is greater or equal to 2.
        while not self.n >= 2:
            self.n = n + np.random.choice((-variance, variance))


class Population:

    def __init__(self, Model, times, lambdas, maxIslands, switches,
                 size, repetitions, rate, method='least_squares'):
        ''' List of models for a given number of islands. '''
        # Timeframe to study
        self.times = np.array(times)
        # PSMC distribution to fit
        self.lambdas = np.array(lambdas)
        # Calculate integral for comparing
        self.integral = integral(self.times, self.lambdas)
        # Number of switches
        self.switches = switches
        # Mutation rate
        self.rate = rate
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

    def sort(self, index):
        ''' Sort in ascending order (smallest to highest fitness). '''
        self.individuals[index].sort(key=lambda indi: indi.fitness)

    def evaluate(self, index):
        ''' Evaluate all the individuals. '''
        for indi in self.individuals[index]:
            if self.method == 'least_squares':
                indi.evaluate_least_squares(self.times, self.lambdas)
            elif self.method == 'integral':
                indi.evaluate_integral(self.times, self.integral)
        self.sort(index)

    def tournament(self, size, tournamentSize, index):
        ''' Tournament selection, the parameters are not so crucial. '''
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

    def enhance(self, generations):
        ''' Mutate the population. '''
        for i in range(len(self.individuals)):
            for g in range(generations):
                newIndividuals = []
                for individual in self.tournament(20, 10, i):
                    # Create a copy of the individual
                    newIndividuals.append(deepcopy(individual))
                    # Enhance
                    for _ in range(5):
                        newIndividual = deepcopy(individual)
                        newIndividual.mutate(self.rate)
                        newIndividuals.append(newIndividual)
                # Renew to population
                self.individuals[i] = newIndividuals
                # Reevaluate the new models
                self.evaluate(i)
                # Check if there is a new best individual
                if self.individuals[i][0].fitness < self.best.fitness:
                    self.best = deepcopy(self.individuals[i][0])
                print ('Repetition {0} - Generation {1} done.'.format(i+1, g+1))
