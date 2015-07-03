import argparse
import pandas as pd
from lib.inference import genalg
from lib import model
from lib import plotting
from lib import tools

parser = argparse.ArgumentParser()

# Version
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 1.0')
# CSV file
parser.add_argument('file', type=str,
                    help='Pathname of directory to analyze.')
# Islands
parser.add_argument('-n', action='store', dest='islands', type=int,
                    default=100,
                    help="""Maximal number of islands for the first
                            generation.""")
# Switches
parser.add_argument('-s', action='store', dest='switches', type=int,
                    default=0,
                    help='Number of switches for the model.')
# Size
parser.add_argument('-p', action='store', dest='size', type=int,
                    default=1000,
                    help='Initial generation size.')
# Repetitions
parser.add_argument('-r', action='store', dest='repetitions', type=int,
                    default=1,
                    help='Number of times to repeat the process.')
# Generations
parser.add_argument('-g', action='store', dest='generations', type=int,
                    default=100,
                    help='Number of iterations for each population.')

# Mutation
parser.add_argument('-u', action='store', dest='rate', type=int,
                    default=1,
                    help='Rate at which the parameters mutate.')

# Method
parser.add_argument('-m', action='store', dest='method', type=str,
                    default='integral',
                    help='Method for evaluating the fits.')
# Plot and JSON
parser.add_argument('-k', action='store', dest='keep', type=str,
                    default='False',
                    help="""Set to True to save the inference as a plot
                            and a JSON file.""")
# Outfile
parser.add_argument('-o', action='store', dest='outfile', type=str,
                    help='Override name of output files.')

parameters = parser.parse_args()

# Extract the times and the lambdas and remove initial decreases
data = pd.read_csv(parameters.file)
data.columns = ('times', 'lambdas')
# Extract the times and the lambdas and remove initial decreases
times, lambdas = tools.search_increase(list(data['times']),
                                       list(data['lambdas']))
# Normalize the vectors
l0 = 1 / lambdas[0]
times = [t * l0 for t in times]
lambdas = [l * l0 for l in lambdas]
# Build a genetic algorithm
pop = genalg.Population(model.StSICMR, times, lambdas,
                        maxIslands=parameters.islands,
                        switches=parameters.switches,
                        size=parameters.size,
                        repetitions=parameters.repetitions,
                        rate=parameters.rate,
                        method=parameters.method)
# Enhance them all
pop.enhance(parameters.generations)
# Plot the best one
if parameters.keep == 'True':
    if parameters.outfile is None:
        path = parameters.file.split('/')
        file = path[-1].split('.')[0]
        path = '/'.join(path[:-1])
        fileName = '{0}/{1}_{2}_switch'.format(path, file, parameters.switches)
    else:
        fileName = parameters.outfile
    plotting.plotModel(pop.best.model, times, lambdas, logScale=True,
                       save='{0}.png'.format(fileName))
    pop.best.model.save(fileName)
else:
    plotting.plotModel(pop.best.model, times, lambdas, logScale=True)
