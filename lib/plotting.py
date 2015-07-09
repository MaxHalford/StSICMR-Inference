import matplotlib.pyplot as plt
import numpy as np
import json

with open('lib/chartOptions.json') as chartOptions:    
    chart = json.load(chartOptions)

if chart['style'] != 'None':
    plt.style.use(chart['style'])

def plotModel(model, times, lambdas, logScale=False,
              save=None, show=True):
    ''' Plot a target and an inference. '''
    plt.clf()
    plt.grid(color=chart['grid']['color'],
             linestyle=chart['grid']['lineStyle'])
    # Evaluate the model at the given time steps
    lambda_s = [model.lambda_s(t) for t in times]
    # Plot the target
    target = chart['target']
    if target['style'] == 'step': 
        plt.step(times, lambdas, label=target['label'],
                 linewidth=target['width'], color=target['color'],
                 alpha=target['alpha'], where='post')
    elif target['style'] == 'smooth':
        plt.plot(times, lambdas, label=target['label'],
                linewidth=target['width'], color=target['color'],
                alpha=target['alpha'])
    # Plot the inference
    inference = chart['inference']
    if inference['style'] == 'step': 
        plt.step(times, lambda_s, label=inference['label'],
                 linewidth=inference['width'], color=inference['color'],
                 alpha=inference['alpha'], where='post')
    elif inference['style'] == 'smooth':
        plt.plot(times, lambda_s, label=inference['label'],
                linewidth=inference['width'], color=inference['color'],
                alpha=inference['alpha'])
    # Add the migration rate time changes as vertical lines
    if chart['migrations']['show'] == 'True':
        for t in model.T[1:]:
            plt.axvline(t, linestyle=chart['migrations']['style'],
                        color=chart['migrations']['color'],
                        alpha=chart['migrations']['alpha'])
    # Set x scale to logarithmic
    if logScale is True:
        plt.xscale('log')
    # Annotate the graph
    plt.suptitle(chart['title']['text'], fontsize=chart['title']['size'],
                 fontweight=chart['title']['weight'])
    plt.legend(loc=4)
    plt.xlabel(chart['xLabel'])
    plt.ylabel(chart['yLabel'])
    # Add model information to the top-left corner
    information = '''
    n: {0}
    T: {1} 
    M: {2}
    C: {3}'''.format(model.n,
                     np.round(model.T, 2),
                     np.round(model.M, 2),
                     np.round(model.C, 2))
    plt.annotate(information, xy=(0, 1), xycoords='axes fraction',
                 fontsize=13, ha='left', va='top', xytext=(5, -5),
                 textcoords='offset points')
    # Save the figure
    if save is not None:
        figure = plt.gcf()
        figure.set_size_inches(chart['quality']['sizeInches'])
        plt.savefig(save, dpi=chart['quality']['dpi'])
    if show is True:
        plt.show()
