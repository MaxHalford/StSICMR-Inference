# Verifying the installation
try:
    import matplotlib
except ImportError:
    print('matplotlib is not installed')
try:
    import pandas
except ImportError:
    print('pandas is not installed')
try:
    import numpy
except ImportError:
    print('numpy is not installed')

# Verifying the model
try:
    from lib import model
    m = model.StSICMR(3, [0, 10, 20], [10, 1, 10], [1, 1, 1])
except:
    print('The model module is not working.')

# Verifying the plotting
try:
    from lib import plotting
    plotting.plotModel(m, times=[0.1, 0.2, 0.3], logScale=True, show=False)
except:
    print('The plotting module is not working.')

# Verifying the genetic algorithm
try:
    from lib.inference import genalg
    pop = genalg.Population(model.StSICMR, [0.1, 0.2, 0.3], [1, 2, 1],
                            switches=1,
                            sizeChange=False,
                            repetitions=1,
                            method='least_squares')
    pop.enhance(10, repeat=False)
except:
    print('The genetic algorithm module is not working.')

print ('All the tests were successful!')