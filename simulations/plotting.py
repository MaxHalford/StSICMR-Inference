import matplotlib.pyplot as plt
import numpy as np

plt.style.use('fivethirtyeight')

def plotModel(model, times, lambdas=None, logScale=False,
              save=None, show=True):
    ''' Plot a model in green and a determined lambda function in red. '''
    plt.clf()
    plt.grid(color='white', linestyle='solid')
    # Evaluate the model at the given time steps
    lambda_s = [model.lambda_s(t) for t in times]
    # Plot the model in red
    plt.step(times, lambda_s, label='Obtained', linewidth=3,
             where='post', color='red', alpha=0.5)
    # Plot the lambda function in green
    if lambdas is not None:
        plt.step(times, lambdas, label='Model', linewidth=3,
                 where='post', color='green', alpha=0.5)
        # Compute the squared error
        squared_error = np.sum(((lambdas[i] - lambda_s[i]) ** 2
                          for i in range(len(lambdas))))
        plt.title('Least squares: ' + str(squared_error))
    # Add the migration rate time changes as vertical lines
    for t in model.T_list[1:]:
        plt.axvline(t, linestyle='--', color='gray', alpha=0.5)
    # Set x scale to logarithmic
    if logScale is True:
        plt.xscale('log')
    # Annotate the graph
    plt.suptitle('Structured model inference of lambda function',
                 fontsize=14, fontweight='bold')
    plt.legend(loc=4)
    plt.xlabel('Time going backwards')
    plt.ylabel('Lambda')
    # Add model information to the top-left corner
    information = '''
    n: {0}
    T: {1} 
    M: {2}'''.format(model.n,
                     np.round(model.T_list, 2),
                     np.round(model.M_list, 2))
    plt.annotate(information, xy=(0, 1), xycoords='axes fraction',
                 fontsize=13, ha='left', va='top', xytext=(5, -5),
                 textcoords='offset points')
    # Save the figure
    if save is not None:
        figure = plt.gcf()
        figure.set_size_inches(20, 14)
        plt.savefig(save, dpi=100)
    if show is True:
        plt.show()


def plotInference(model, times, lambdas, true_n, true_T, true_M,
                  logScale=False, save=None, show=False):
    ''' Plot an inference of the parameters in a structured model. '''
    plt.clf()
    # Evaluate the model at the given time steps
    lambda_s = [model.lambda_s(t) for t in times]
    # Compute the squared error
    squared_error = np.sum(((lambdas[i] - lambda_s[i]) ** 2
                          for i in range(len(lambdas))))
    # Plot the model in red
    plt.step(times, lambda_s, label='Obtained', linewidth=3,
             where='post', color='red', alpha=0.5)
    # Plot the lambda function in green
    plt.step(times, lambdas, label='Model', linewidth=3,
             where='post', color='green', alpha=0.5)
    # Add the migration rate time changes as vertical lines
    for t in zip(model.T_list[1:], true_T[1:]):
        plt.axvline(t[0], linestyle='--', color='red', alpha=0.7)
        plt.axvline(t[1], linestyle='--', color='green', alpha=0.7)
    # Set x scale to logarithmic time
    if logScale is True:
        plt.xscale('log')
    # Annotate the graph
    plt.suptitle('Genetic Algorithm VS Model',
                 fontsize=14, fontweight='bold')
    plt.title('Least squares: {0}'.format(squared_error))
    plt.legend(loc=4)
    plt.xlabel('Time going backwards')
    plt.ylabel('Lambda')
    # Add comparison legend in the top-left corner
    information = '''
    True n: {0}
    Obtained n: {1}
    True T: {2}
    Obtained T: {3}
    True M: {4}
    Obtained M: {5}'''.format(true_n,
                              model.n,
                              np.round(list(true_T), 2),
                              np.round(list(model.T_list), 2),
                              np.round(list(true_M), 2),
                              np.round(list(model.M_list), 2))
    plt.annotate(information, xy=(0, 1), xycoords='axes fraction',
                 fontsize=13, ha='left', va='top', xytext=(5, -5),
                 textcoords='offset points')
    # Save the figure
    if save is not None:
        figure = plt.gcf()
        figure.set_size_inches(20, 14)
        plt.savefig(save, dpi=100)
    if show is True:
        plt.show()
