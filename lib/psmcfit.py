# -*- coding: utf-8 -*-
"""
Created on Wed May  6 09:27:01 2015

@author: willy, max
"""

import matplotlib.pyplot as plt
import numpy as np
from bisect import bisect_right


def plot_psmc_history(N_ref, t_k, lambda_k, generation_time=25):
    # Plot the history infered by psmc
    fig = plt.figure()
    ax = fig.add_subplot(111)

    X = 2 * N_ref * generation_time * np.array(t_k)
    Y = N_ref * np.array(lambda_k)

    ax.step(X, Y, '-g', where='post')
    ax.set_xscale('log')

    plt.show()


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


def avg_psmc_history(directory, mut_rate=2.5e-8, bin_size=100):
    return 'to do'


def evaluate_noscaled_psmc_history(t_k, lambda_k, t):
    i = max(bisect_right(t_k, t) - 1, 0)
    return lambda_k[i]


def evaluate_scaled_psmc_history():
    pass


def evaluate_normalized_psmc_hist(N_ref, t_k, lambda_k, plot=False):
    normalized_sizes = np.true_divide(np.array(lambda_k), lambda_k[0])
    normalized_times = np.true_divide(2*np.array(t_k), lambda_k[0])
    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.step(normalized_times, normalized_sizes, '-g', where='post')
        ax.set_xscale('log')
    return (normalized_times, normalized_sizes)


def plot_psmchist(psmc_filename, t_vector=False, mut_rate=2.5e-8,
                  generation_time=25, bin_size=100):
    # Get the psmc infered history
    (N_ref, t_k, lambda_k) = get_psmc_history(psmc_filename, mut_rate,
                                                bin_size)

    if t_vector:
        psmc_time = 2 * N_ref * generation_time * t_vector
        temp_lambda = [evaluate_noscaled_psmc_history(t_k, lambda_k, i) for i
                        in t_vector]
        psmc_lambda = N_ref * np.array(temp_lambda)
    else:
        psmc_time = 2 * N_ref * generation_time * np.array(t_k)
        psmc_lambda = N_ref * np.array(lambda_k)

    # Now we plot
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.step(psmc_time, psmc_lambda, '-g', where='post')
    ax.set_xscale('log')
    plt.show()








