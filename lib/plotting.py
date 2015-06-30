import matplotlib.pyplot as plt
import numpy as np

plt.style.use('fivethirtyeight')

def plotModel(model, times, lambdas, logScale=False,
              save=None, show=True):
    ''' Plot a model in green and a determined lambda function in red. '''
    plt.clf()
    plt.grid(color='white', linestyle='solid')
    # Evaluate the model at the given time steps
    lambda_s = [model.lambda_s(t) for t in times]
    # Plot the model in red
    plt.step(times, lambda_s, label='PSMC Lambda', linewidth=3,
             where='post', color='red', alpha=0.5)
    # Plot the lambda function in green
    plt.step(times, lambdas, label='Model Lambda', linewidth=3,
             where='post', color='green', alpha=0.5)
    # Compute the squared error
    squared_error = np.sum(((lambdas[i] - lambda_s[i]) ** 2
                          for i in range(len(lambdas))))
    plt.title('Least squares: ' + str(squared_error))
    # Add the migration rate time changes as vertical lines
    for t in model.T[1:]:
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
                     np.round(model.T, 2),
                     np.round(model.M, 2))
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
