import numpy as np

################
### Integral ###
################

def integral(X, Y):
    ''' Calculate distance from step function to abscissa line. '''
    rectangle = lambda x0, x1, y: (x1 - x0) * y / x0
    integral = [rectangle(X[i], X[i+1], Y[i]) for i in range(len(X)-1)]
    return np.array(integral)

def evaluate_integral(model, times, referenceIntegral):
    ''' Evaluate how close two functions are. '''
    # Get the new lambdas
    lambdas = [model.lambda_s(t) for t in times]
    # Compute the model integral
    modelIntegral = integral(times, lambdas)
    # The fitness is the difference between both
    return np.sum((modelIntegral - referenceIntegral) ** 2)

###############################
### Least Squares, not used ###
###############################

def evaluate_least_squares(model, times, lambdas):
    ''' Evaluate how close two vectors are. '''
    # Compute the differences
    modelLamdbas = [model.lambda_s(t) for t in times]
    differences = np.array(lambdas) - np.array(modelLamdbas)
    # The fitness is the sum of the squared differences
    return np.sum(np.square(differences))