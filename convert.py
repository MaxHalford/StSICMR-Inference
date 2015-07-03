from lib import tools
import argparse

parser = argparse.ArgumentParser()

# The user inputs the PSMC file to convert
parser.add_argument('file', type=str, help='PSMC file to convert to CSV file.')
parameters = parser.parse_args()
# Convert the PSMC file to CSV
tools.psmc_to_csv(parameters.file)