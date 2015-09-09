import sys
sys.path.append('../lib/')

import model
import testmodel

# Number of islands
n = 10
# Flow rate changes
T_list = [0, 2, 3]
# Flow rates
M_list = [1, 5, 1]
# Create a model
model = model.StSICMR(n, T_list, M_list)
# Validate it graphically
testmodel.compare_cdf_g(model, path2ms='../bin/')
# Validate it with a KS-test
testmodel.compare_cdf_KS(model, path2ms='../bin/')
