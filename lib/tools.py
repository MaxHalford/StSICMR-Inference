import pandas as pd

def psmc_to_csv(filename, mutationRate=2.5e-8, binSize=100):
    ''' Convert the last iteration of the PSMC to a CSV file. '''
    with open(filename) as f:
        data = f.read()
    # Get the last block
    lastBlock = [line.split('\t') for line in data.split('//')[-2].splitlines()
                 if line.startswith('RS')]
    # Only keep the times and the lambda values
    data = pd.DataFrame(lastBlock)[[2, 3]]
    data.columns = ('times', 'lambdas')
    # Save them to a CSV file
    path = '/'.join(filename.split('/')[:-1])
    name = filename.split('/')[-1].split('.')[-2]
    data.to_csv('{0}/{1}.csv'.format(path, name), index=False)
    print ('{} has been converted to CSV.'.format(filename))

def search_increase(times, lambdas):
    '''
    Some PSMC outputs start by decreasing going back in time,
    this is obviously a change in population size and isn't
    what the model is trying to show.
    '''
    i = 0
    if lambdas[1] <= lambdas[0]:
        i = 1
        while lambdas[i] > lambdas[i+1]:
            i += 1
    return (times[i:], lambdas[i:])








