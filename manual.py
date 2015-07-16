import argparse
import pandas as pd
from lib import model
from lib import plotting
from lib import tools

parser = argparse.ArgumentParser()

# Version
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 1.1')
# PSMC file
parser.add_argument('file', type=str,
                      help='Pathname of directory to analyze.')
# Normalization
parser.add_argument('-l', action='store', dest='normalize', type=bool,
                    help='Normalize the PSMC data so that the first lambda is 1.')

# Islands
parser.add_argument('-n', action='store',
                    dest='islands', type=int, help='Number of islands.')
# Times
parser.add_argument('-T', nargs='+', dest='times',
                    help='Times of migration rate changes.', type=float)
# Rates
parser.add_argument('-M', nargs='+', dest='rates',
                    help='Migration rates.', type=float)
# Sizes
parser.add_argument('-C', nargs='+', dest='sizes',
                    help='Population sizes.', type=float)
# Plot and JSON
parser.add_argument('-k', action='store', dest='keep', type=bool,
                    default=False,
                    help="""Set to True to save the fit as a plot and a
                            JSON file.""")
# Outfile
parser.add_argument('-o', action='store', dest='outfile', type=str,
                    help='Override name of output files.')
parameters = parser.parse_args()

# PSMC
data = pd.read_csv(parameters.file)
data.columns = ('times', 'lambdas')
# Extract the times and the lambdas and remove initial decreases
times, lambdas = tools.search_increase(list(data['times']),
                                       list(data['lambdas']))

# Verify the user input
assert len(parameters.times) == len(parameters.rates), 'There has to be as many times as there are rates.'

# Normalize the vectors
if parameters.normalize is True:   
    l0 = 1 / lambdas[0]
    times = [t * l0 for t in times]
    lambdas = [l * l0 for l in lambdas]

# Build the model
m = model.StSICMR(parameters.islands, parameters.times, parameters.rates, parameters.sizes)

# Plot
if parameters.keep is True:
    if parameters.outfile is None:
        path = parameters.file.split('/')
        file = path[-1].split('.')[0]
        path = '/'.join(path[:-1])
        fileName = '{0}/{1}_manual'.format(path, file)
    else:
        fileName = parameters.outfile
    m.save(fileName)
    plotting.plotModel(m, times, lambdas, logScale=True,
                       save='{0}.png'.format(fileName))
else:
    plotting.plotModel(m, times, lambdas, logScale=True)
