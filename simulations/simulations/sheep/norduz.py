import sys
sys.path.append('../../lib/')
from inference import genalg
import model
import plotting
import psmcfit

data = psmcfit.get_psmc_history('Norduz.psmc')

times, lambdas = psmcfit.search_increase(data['times'], data['lambdas'])

l0 = 1 / lambdas[0]

times *= l0
lambdas *= l0

#~ # Build a group of models
pop = genalg.Population(model.StSICMR, times, lambdas,
                        maxIslands=100, switches=4,
                        size=1000, repetitions=4)
# Enhance them all
pop.enhance(1000)
# Plot the best one
plotting.plotModel(pop.best.model, times, lambdas, logScale=True)
