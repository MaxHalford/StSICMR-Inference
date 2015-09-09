import os
import numpy as np

def sameIsland(n, T, M):
    # Generate the command
    command = '../bin/ms 2 100000 -T -L -I ' + str(n) + ' 2 ' + \
              '0 ' * (n-1) + str(M[0])
    # If there is more than one flow rate
    if len(T) > 1:
        # Add them to the end of the command
        for flowRate in list(zip(T, M))[1:]:
            command += ' -eM ' + str(0.5 * flowRate[0]) + ' ' + str(flowRate[1])
    # Capture its output
    shellOutput = os.popen(command + " | grep 'time' | cut -f 2")
    # Remove carriage returns and convert to float
    cleaned = [float(cell) for cell in shellOutput.read().splitlines()]
    # Multiply by 2 because of the time scale in MS
    T2s = np.true_divide(cleaned, 0.5)
    return T2s

def differentIslands(n, T, M):
    # Generate the command
    command = '../bin/ms 2 100000 -T -L -I ' + str(n) + ' 1 1 ' + \
              '0 ' * (n-2) + str(M[0])
    # If there is more than one flow rate
    if len(T) > 1:
        # Add them to the end of the command
        for flowRate in list(zip(T, M))[1:]:
            command += ' -eM ' + str(0.5 * flowRate[0]) + ' ' + str(flowRate[1])
    # Capture its output
    shellOutput = os.popen(command + " | grep 'time' | cut -f 2")
    # Remove carriage returns and convert to float
    cleaned = [float(cell) for cell in shellOutput.read().splitlines()]
    # Multiply by 2 because of the time scale in MS
    T2s = np.true_divide(cleaned, 0.5)
    return T2s
