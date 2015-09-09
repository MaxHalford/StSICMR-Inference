import sys
sys.path.append('../lib/')
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
liDurbin_tk = np.array([0.011, 0.0178, 0.026, 0.0354, 0.0466, 0.0598, 0.075,
                        0.093, 0.1142, 0.139, 0.168, 0.202, 0.242, 0.2888,
                        0.3436, 0.408, 0.4836, 0.572, 0.6758, 0.7976, 0.9402,
                        1.1076, 1.304, 1.5342, 1.804, 2.1206])

liDurbin_lk = np.array([0.0244, 0.0489, 0.0607, 0.1072, 0.2093, 0.363, 0.5041,
                        0.587, 0.6343, 0.6138, 0.5292, 0.4409, 0.3749, 0.3313,
                        0.3066, 0.2952, 0.2915, 0.295, 0.3103, 0.3458, 0.4109,
                        0.5048, 0.5996, 0.644, 0.6178, 0.5345])

# Now we divide the lambda vector and the times vector by lambda[0]
l0 = 1 / liDurbin_lk[0]
liDurbin_tk *= l0
liDurbin_lk *= l0

#########################
### Genetic Algorithm ###
#########################

## Build a group of models
#pop = genalg.Population(model.StSICMR, liDurbin_tk, liDurbin_lk,
#                        maxIslands=20, switches=3,
#                        size=1000, repetitions=1)
## Enhance them all
#pop.enhance(200)
## Plot the best one
#plotting.plotModel(pop.best.model, liDurbin_tk, liDurbin_lk,
#                   logScale=True)

################
### Boxplots ###
################

switches = range(2, 7)
islands = range(2, 31)
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

for s in switches:
    data = pd.read_csv('errors/li_durbin_errors_{0}.csv'.format(s))
    traces = []
    for n in islands:
        traces.append(Box(y=list(data[str(n)]), name=n))
    traces = Data(traces)
    layout = Layout(
        title='{0} switches errors'.format(s),
        xaxis=XAxis(
            title='Islands'
            ),
        yaxis=YAxis(
            title='Squared error'
        )
    )
    fig = Figure(data=traces, layout=layout)
    plot_url = py.plot(fig, filename='{0} switches'.format(s))

#########################
### Time distribution ###
#########################

file = 'individuals/{0}_switches/{1}_islands.json'

islands = 12

for s in switches:
    individual = json.loads(open(file.format(s, islands)).read())
    m = model.StSICMR(individual['n'], individual['T'], individual['M'])
    plotting.plotModel(m, liDurbin_tk, liDurbin_lk, logScale=True,
                       save=str(s), show=False)
