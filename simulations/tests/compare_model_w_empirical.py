# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:59:05 2015

@author: willy, max
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../lib/')
from model import StSICMR
from testmodel import simulate_T2_ms, create_ms_command_T2
from testmodel import compute_empirical_hist

# Parameters to test

n = 10 # Number of islands
T_list = [0, 5.7, 55, 90] # Times for the changes of migration rates
M_list = [0.55, 4, 0.55, 0.8] # Migration rates

n_obs = 100000 # Number of observations (simulated values of T2)
sampling = 'same'

T_max = 120
n_tw = 64
psmc_t_vector = 0.1*np.array([np.exp(np.true_divide(i*np.log(1+10*T_max),
                                                    n_tw))-1
                             for i in range(1, n_tw+1)])
print (psmc_t_vector)
#t_vector = psmc_t_vector
t_vector = np.arange(0, 50, 0.1)

N_ref = 1000
path2ms = '../bin'

if __name__ == "__main__":
    model = StSICMR(n, T_list, M_list)
    T_list_ms = np.true_divide(np.array(T_list), 2)
    cmd = create_ms_command_T2(n_obs, n, T_list_ms, M_list, sampling)
    obs_T2 = simulate_T2_ms(cmd, path2ms)
    (x, empirical_lambda) = compute_empirical_hist(obs_T2, t_vector, N_ref,
                                                     path2ms)
    theoretical_lambda = [model.lambda_s(t) for t in t_vector]

    times = 2 * N_ref * np.array(x)
    empirical_sizes = N_ref * np.array(empirical_lambda)
    theoretical_sizes = N_ref * np.array(theoretical_lambda)

    # Now we plot
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.step(times, empirical_sizes, '-r', where='post', label='empirical')
    ax.step(times, theoretical_sizes, '-b', where='post', label='theoretical')
    ax.set_xlim(1e3, 2*N_ref*t_vector[-1])
    ax.set_ylim(0, 1e5)
    ax.set_xscale('log')
    print (empirical_lambda[0])
    print (theoretical_lambda[0])
    plt.legend()
    plt.show()
