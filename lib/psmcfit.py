import numpy as np


def get_psmc_history(filename, mut_rate=2.5e-8, bin_size=100):
    # Returns the history infered by psmc in a tuple (N_ref, t_k, lambda_k)
    a = open(filename, 'r')
    text = a.read()
    a.close()

    # getting the time windows and the lambda values
    last_block = text.split('//\n')[-2]
    last_block = last_block.split('\n')
    time_windows = []
    estimated_lambdas = []
    for line in last_block:
        if line[:2] == 'RS':
            time_windows.append(float(line.split('\t')[2]))
            estimated_lambdas.append(float(line.split('\t')[3]))


    # getting the estimations of theta and N0
    result = text.split('PA\t') # The 'PA' lines contain the estimated lambda values
    result = result[-1].split('\n')[0]
    result = result.split(' ')
    theta = float(result[1])
    N_ref = theta/(4*mut_rate)/bin_size

    return {'nRef': N_ref, 'times': np.array(time_windows[1:]),
            'lambdas': np.array(estimated_lambdas[1:])}


def search_increase(times, lambdas):
    i = 0
    if lambdas[1] <= lambdas[0]:
        i = 1
        while lambdas[i] > lambdas[i+1]:
            i += 1
    return (times[i:], lambdas[i:])








