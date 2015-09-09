import sys
sys.path.append('../../lib/')
from inference import genalg
import model
import plotting
import numpy as np
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
import json
from copy import deepcopy

# We take the ms command from the Supplementary Material multiplied by 2
t_list = np.array([3e-4, 4e-4, 5e-4, 6e-4, 7e-4, 8e-4, 9e-4, 1e-3,
                   1.2e-3, 1.3e-3, 1.5e-3, 1.8e-3, 2e-3, 2.5e-3,
                   2.8e-3, 3e-3, 3.5e-3, 4e-3, 4.5e-3, 5e-3,
                   6e-3, 7e-3, 8e-3, 9e-3, 1e-2, 1.3e-2, 1.7e-2,
                   2e-2, 2.3e-2, 2.6e-2, 2.8e-2, 3e-2, 3.5e-2,
                   4e-2, 5e-2, 6e-2]) * 500

l_list = np.array([0.1, 0.11, 0.112, 0.14, 0.2, 0.21, 0.39, 0.4,
                   0.6, 0.62, 0.9, 1.1, 1.3, 1.4, 1.5, 1.48, 1.42,
                   1.3, 1.25, 1.1, 0.95, 0.8, 0.7, 0.6, 0.57, 0.59,
                   0.72, 0.74, 1, 1.1, 1.2, 1.4, 1.5, 1.3, 1.28, 1.27])

# Now we divide the lambda vector and the times vector by lambda[0]
l0 = 1 / l_list[0]
t_list *= l0
l_list *= l0

#########################
### Genetic Algorithm ###
#########################

# Build a group of models
pop = genalg.Population(model.StSICMR, t_list, l_list,
                        maxIslands=100, switches=3,
                        size=1000, repetitions=5)
# Enhance them all
pop.enhance(200)
# Plot the best one
plotting.plotModel(pop.best.model, t_list, l_list,
                   logScale=True)

################
### Boxplots ###
################

#switches = range(2, 7)
#islands = range(2, 31)
#for s in switches:
#    data = pd.DataFrame()
#    for n in islands:
#        errors = []
#        minError = np.inf
#        bestIndi = None
#        for _ in range(20):
#            pop = genalg.Population(model.StSICMR, liDurbin_tk, liDurbin_lk,
#                                    maxIslands=n, switches=s,
#                                    size=1000, repetitions=1)
#            pop.enhance(100)
#            if pop.best.fitness < minError:
#                bestIndi = deepcopy(pop.best)
#                minError = pop.best.fitness
#            errors.append(pop.best.fitness)
#        data[n] = errors
#        bestIndi.save('individuals/{0}_switches/{1}_islands'.format(s, n))
#    data.to_csv('errors/li_durbin_errors_{0}.csv'.format(s))

#for s in switches:
#    data = pd.read_csv('errors/li_durbin_errors_{0}.csv'.format(s))
#    traces = []
#    for n in islands:
#        traces.append(Box(y=list(data[str(n)]), name=n))
#    traces = Data(traces)
#    layout = Layout(
#        title='{0} switches errors'.format(s),
#        xaxis=XAxis(
#            title='Islands'
#            ),
#        yaxis=YAxis(
#            title='Squared error'
#        )
#    )
#    fig = Figure(data=traces, layout=layout)
#    plot_url = py.plot(fig, filename='{0} switches'.format(s))

#########################
### Time distribution ###
#########################

#file = 'individuals/{0}_switches/{1}_islands.json'
#
#islands = 12
#
#for s in switches:
#    individual = json.loads(open(file.format(s, islands)).read())
#    m = model.StSICMR(individual['n'], individual['T'], individual['M'])
#    plotting.plotModel(m, liDurbin_tk, liDurbin_lk, logScale=True,
#                       save=str(s), show=False)
