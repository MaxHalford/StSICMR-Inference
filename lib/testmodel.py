# -*- coding: utf-8 -*-
"""
Created on Mon May  4 23:56:41 2015

@author: willy, max
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import kstest

# The objective of this package is to test the theoretical functions by
# comparison with the empirical function obtained from simulations with
# ms

def create_ms_command_T2(n_obs, n_islands, T_list, M_list, sampling='same'):
    if sampling == 'same': # same island
        sampling_pattern = '-I {n} 2{s} {M}'.format(n = n_islands, 
                                                    s = (n_islands-1)*' 0', 
                                                    M = M_list[0])
    else:
        sampling_pattern = '-I {n} 1 1{s} {M}'.format(n = n_islands, 
                                                    s = (n_islands-2)*' 0', 
                                                    M = M_list[0])
    command = 'ms 2 {} -T -L {}'.format(n_obs, sampling_pattern)
    demog_events_list = ['-eM {time} {new_rate}'.format(time=t, new_rate=m) for
                    (t,m) in list(zip(T_list, M_list))[1:]]
    demog_events = ' '.join(demog_events_list)
    return '{} {}'.format(command, demog_events)
    
def simulate_T2_ms(command, path2ms='./'):
    cmd_output = os.popen(os.path.join(path2ms, command)).read()
    output_list = cmd_output.split('time:\t')
    obs_T2 = [float(t.split('\t')[0]) for t in output_list[1:]]
    return obs_T2    
    
def compare_cdf_g(model, n_obs=10000, case='T2s',
                  t_vector=np.arange(0, 100, 0.1), path2ms='./'):
    # Do a graphical comparison by plotting the theoretical cdf and the 
    # empirical pdf
    T_list_ms = np.true_divide(model.T_list,2)
    M_list = model.M_list
    if case == 'T2s':
        cmd = create_ms_command_T2(n_obs, model.n, T_list_ms, M_list, 'same')
        theor_cdf = model.cdf_T2s
    elif case == 'T2d':
        cmd = create_ms_command_T2(n_obs, model.n, T_list_ms, M_list, 'disctint')
        theor_cdf = model.cdf_T2d
    else:
        return 1
    
    obs = simulate_T2_ms(cmd, path2ms)
    obs = np.array(obs) * 2
    
    delta = t_vector[-1] - t_vector[-2]
    bins = t_vector
    
    f_obs = np.histogram(obs, bins=bins)[0]
    cum_f_obs = [0] + list(f_obs.cumsum())
    F_obs = np.true_divide(np.array(cum_f_obs), n_obs)
    F_theory = [theor_cdf(t) for t in bins]    
    
    # Now we plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(bins, F_obs, '-r', label = 'Empirical cdf')
    ax.plot(bins, F_theory, '-b', label = 'Theoretical cdf')
    
    plt.legend()
    plt.show()
    
def compare_cdf_KS(model, n_obs=10000, case='T2s', test_repetitions=100, 
                   print_pvalues=False, alpha=0.05, path2ms='./'):
    # Compares the values simulated by ms with the theoretical distribution
    # by usin the Kolmogorov-Smirnov test
    T_list_ms = np.true_divide(model.T_list,2)
    M_list = model.M_list
    if case == 'T2s':
        cmd = create_ms_command_T2(n_obs, model.n, T_list_ms, M_list, 'same')
        theor_cdf = model.cdf_T2s
    elif case == 'T2d':
        cmd = create_ms_command_T2(n_obs, model.n, T_list_ms, M_list, 'distinct')
        theor_cdf = model.cdf_T2d
    else:
        return 1
        
    # create the theoretical function (it must be a callable) for the KS
    theoretical = lambda x : np.array([theor_cdf(i) for i in x])
    
    # Simulate and do the test
    number_of_rejects = 0
    pvalues = []
    for i in range(test_repetitions):
        obs = simulate_T2_ms(cmd, path2ms)
        obs = np.array(obs) * 2
        ks_result = kstest(obs, theoretical)
        if ks_result[1]<alpha: number_of_rejects+=1
        pvalues.append(ks_result[1])
    if print_pvalues: print(pvalues)
    print('{0} tests out of {1} rejected the null hypothesis.'.format(number_of_rejects, test_repetitions))
    
def compute_empirical_hist(obs_T2, t_vector, N_ref=1, path2ms='./'):
    # Compute the emirical lambda from simulated T2 values comming from ms

    # Given that the obs_T2 come from ms, we have to multiply them by 2
    # in order to rescale to our model
    obs_T2 = 2 * np.array(obs_T2)
    # obs_T2 = np.true_divide(np.array(obs_T2), 2)
    # obs_T2 = np.array(obs_T2)
    x = np.array(t_vector)
    x[-1] = max(x[-1], max(obs_T2))
    
    # First we compute the empirical cdf (denoted Fx)
    counts, ignored_values = np.histogram(obs_T2, bins = x)
    Fx = counts.cumsum()
    Fx = np.array([0] + list(Fx))
        
    # Now we compute the pdf (denoted fx)
    # We will compute the derivative f(x[i]) as 
    # ( F(x[i]+dx/2) - F(x[i]-dx/2) ) / dx

    dx = x[1:]-x[:-1]    
    x_vector_left = x[1:] - np.true_divide(dx,2)
    x_vector_right = x[1:] + np.true_divide(dx,2)
    x_vector_left = np.array([0,0] + list(x_vector_left))
    x_vector_right = np.array([0, t_vector[0]+dx[0]] + list(x_vector_right))
    dx = np.array([dx[0]*2]+list(dx))

    counts_l, ignored_values = np.histogram(obs_T2, bins = x_vector_left)
    counts_r, ignored_values = np.histogram(obs_T2, bins = x_vector_right)
    Fx_l = counts_l.cumsum()
    Fx_r = counts_r.cumsum()
    
    fx = np.true_divide(Fx_r - Fx_l, dx)
    fx[0] = 2*fx[0]
    
    # Computes the empirical lambda
    empirical_lambda = np.true_divide(len(obs_T2)-Fx, fx)
    
    return (x, empirical_lambda)
                    
