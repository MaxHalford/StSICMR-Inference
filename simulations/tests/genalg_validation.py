import sys
sys.path.append('../lib/')
from model import StSICMR
from plotting import plotInference
from inference import genalg
import json
import numpy as np


def generate_times(tMax, steps=64):
    #~ psmc_t_vector = 0.1 * np.array([np.exp(np.true_divide(i *
                                    #~ np.log(1 + steps * tMax), 10)) - 1
                                    #~ for i in range(1, steps+1)])
    psmc_t_vector = np.linspace(0, tMax, steps)
    return psmc_t_vector


def generate_scenarii():
    ''' Build a battery of tests as a JSON files. '''
    switches = [2, 4, 8]
    maxTimes = [1, 10, 50, 100]
    islands = [2, 5, 10, 50, 100]
    scenarii = {}
    # Define different typologies of migration rates
    migrationRates = {2: [[1, 10, 1],
                          [10, 1, 10]],
                      4: [[1, 10, 1, 10, 1],
                          [10, 1, 10, 1, 10],
                          [1, 5, 10, 5, 1],
                          [10, 5, 1, 5, 10]],
                      8: [[1, 10, 1, 10, 1, 10, 1, 10, 1],
                          [10, 1, 10, 1, 10, 1, 10, 1, 10],
                          [1, 5, 3, 10, 15, 10, 3, 5, 1],
                          [15, 10, 3, 5, 1, 5, 3, 10, 15],
                          [1, 10, 1, 10, 1, 10, 5, 3, 1],
                          [1, 3, 5, 10, 1, 10, 5, 10, 1]]}
    # Generate the scenarii
    counter = 1
    for s in switches:
        for t in maxTimes:
            for n in islands:
                for m in migrationRates[s]:
                        scenarii[counter] = {'switches': s,
                                             'maxTime': t,
                                             'true_n': n,
                                             'true_M': m}
                        counter += 1
    # Save it a s a .json file
    with open('scenarii.json', 'w') as outfile:
        json.dump(scenarii, outfile)


def generate_T2s():
    scenarii = json.loads(open('scenarii.json').read())
    for key, info in scenarii.items():
        # Define the switch points
        times = np.linspace(0, info['maxTime'], info['switches'] + 1,
                            endpoint=False)
        # Build the theoretical model
        model = StSICMR(info['true_n'], times, info['true_M'])
        # Choose points in which to evaluate the model
        steps = generate_times(info['maxTime'])
        scenarii[key]['times'] = list(steps)
        scenarii[key]['lambdas'] = [model.lambda_s(s) for s in steps]
        scenarii[key]['true_T'] = list(times)
    # Save it a s a .json file
    with open('scenarii.json', 'w') as outfile:
        json.dump(scenarii, outfile)

generate_scenarii()
generate_T2s()
scenarii = json.loads(open('scenarii.json').read())

for number, parameters in scenarii.items():
    n = parameters['true_n']
    s = parameters['switches']
    times = np.array(parameters['times'])
    lambdas = np.array(parameters['lambdas'])
    individuals = genalg.Population(StSICMR, times, lambdas,
                                    maxIslands=120, switches=s,
                                    size=1000, repetitions=5)
    individuals.enhance(120)
    scenarii[number]['obtained_T'] = list(individuals.best.model.T_list)
    scenarii[number]['obtained_M'] = list(individuals.best.model.M_list)
    plotInference(model=individuals.best.model, times=times,
                  lambdas=lambdas, true_n=scenarii[number]['true_n'],
                  true_T=scenarii[number]['true_T'],
                  true_M=scenarii[number]['true_M'],
                  logScale=False,
                  save='genalg_results/{0}'.format(number),
                  show=False)

with open('scenarii.json', 'w') as outfile:
    json.dump(scenarii, outfile)
