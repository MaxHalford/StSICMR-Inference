## Symmetrical Island Model with Changes in Migration Rates - Inference

The Symmetrical Island Model with Changes in Migration Rates (StSICMR) is a model developped by [Oliver Mazet](http://fr.viadeo.com/fr/profile/olivier.mazet1) and [Lounès Chikhi](https://www.wikiwand.com/en/Loun%C3%A8s_Chikhi) with their research team.

This repository supposes that you are familiar with the [PSMC algorithm](http://www.nature.com/nature/journal/v475/n7357/full/nature10231.html) developped by [Richard Durbin](https://www.wikiwand.com/en/Richard_M._Durbin) and [Heng Li](https://www.wikiwand.com/en/Heng_Li).

The method tries to fit the model to a PSMC timeline produced with [Heng Li's algorithm](https://github.com/lh3/psmc). It starts by extracting the times and the lambda values of the last iteration from a ``.psmc`` file. Then it normalizes the lambda value so that they start at 1 (because the model is normalized to begin at 1 also). For the fitting part it uses a [genetic algorithm](http://www.wikiwand.com/en/Genetic_algorithm) using [tournament selection](https://www.wikiwand.com/en/Tournament_selection). The implementation is done in Python 3.4 and is designed to be comprehensible and easy to edit. I wrote a [tutorial on genetic algorithms](http://maxhalford.com/resources/notebooks/genetic-algorithms.html) to explain how I code genetic algorithms with Python.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Examples](#examples)
- [Output](#output)
- [Architecture](#architecture)
- [Contact](#contact)
- [License](#license)
- [Issues](#issues)
- [Updates](#updates)

## Setup

All of the code has been tested with both Python 2 and Python 3. People have successfully used it on Ubuntu, Mac OS and Windows. You can either use your current Python installation, a virtual environment or the [Anaconda distribution](https://store.continuum.io/cshop/anaconda/).

### 1. Normal

The following module versions were used, that said older and newer versions have a good chance of working too.
	
    - matplotlib == 1.4.3
    - pandas == 0.16.2
    - Cython == 0.22.1
    - numpy == 1.9.2

If you do not have them installed type

```sh
cd StSICMR-Inference
pip3 install -r requirements.txt
```
	
If you don't have ``pip`` installed then you can install the modules manually, this should be easy on any platform as all of them are extremely popular modules.

### 2. With a virtual environment

If you want to be safe and not mess with your Python environment you use a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) included in the repository.

```sh
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

This uses a sandboxed Python where you can do as you please without fear of screwing up your setup. To deactivate the virtual environment type ``deactivate``. To activate it type ``source venv/bin/activate``, or else the default Python interpreter will be used. You can delete the ``StSICMR-Inference`` folder and it will be as if nothing ever happened.

### 3. Anaconda

This is probably the easiest way if you don't have Python installed. Simply [download Anaconda](http://continuum.io/downloads) for your platform (you can choose between Python 2 or 3). Anaconda includes all the modules necessary so there is nothing else to do.

## Usage

### Convert

The algorithm requires a CSV file. Most of the time these are to be extracted from PSMC files. The ``convert.py``script can do this, as can be seen in the [Examples](#examples) section. You can use any CSV file, the first column will be considered as the time vector and the second one as the PSMC vector.

### Infer

The main script is called ``infer.py`` and guesses the parameters for a given PSMC timeline.

| Argument | Name        | Description                                                  | Default    |
|----------|-------------|--------------------------------------------------------------|------------|
| -v       | Version     | Get the version of the script.                               |            |
| -n       | Islands     | Maximal number of islands for the first generation.          | 100        |
| -s       | Switches    | Number of switches for the model.                            | 0          |
| -c       | Size        | Allow the islands to change size.                            | False      |
| -r       | Repetitions | Number of times to repeat the process.                       | 1          |
| -g       | Generations | Number of iterations for each population.                    | 100        |
| -m       | Method      | Method for evaluating the fits.                              | 'integral' |
| -k       | Keep        | Set to True to save the inference as a plot and a JSON file. | 'False'    |
| -o       | Outfile     | Override name of output files.                               |            |

The initial number of islands (``-n``) is not important as the algorithm usually finds the right number of islands straight away. The higher the initial population size (``-p``) is the more of the search space will be covered at first. If you don't want to allow the islands to change sizes then don't include the initial maximal island size argument (``-c``), if you want to set it to ``True``. For repeating the process you can use the repetitions arguments (``-r``) and the best model will be saved. The genetic algorithm implementation stops after a fixed number of generations (``-g``). The mutation rate (``-u``) is important; if it is high the algorithm will not get stuck, at the cost of precision. There are two methods (``-m``) for measuring the distance between two curves:

- the least squares on the vectors which doesn't take into account the abscissa (``'least_squares'``).
- the least squares on the functions which does take into account the abscissa (``'integral'``).

If the keep argument (``-k``) is set to ``True`` then the best model will be saved as a PNG file for the chart and a JSON file for the parameters with default names. You can also use the outfile argument (``-o``) for overriding the name given to the saved files.

At every repetition the console will prompt you if you desire to continue (``y``) or to go to the next repetition (``n``). If you do then it will ask you for how many generations you wish to continue.

### Manual

The other script called ``manual.py`` is for visualizing a model with user-defined parameters.

| Argument | Name            |
|----------|-----------------|
| -l       | Normalization   |
| -n       | Islands         |
| -T       | Switch times    |
| -M       | Migration rates |
| -C       | Population sizes|
| -k       | Keep            |
| -o       | Override        |

### Taming the genetic algorithm

- Increasing the generation size can have an impact, the longer the algorithm runs the lower the chance that the algorithm won't improve the model.
- If the algorithm seems to fail you can try to increase the mutation rate. Often is the case this will enable it to find a better area. However a high mutation rate removes precision from the algorithm.
- *Trying again* isn't a bad idea when using genetic algorithms.
- The initial population size can be important, the higher it is and the more of the search space will be explored at first
- The genetic algorithm uses [tournament selection](https://www.wikiwand.com/en/Tournament_selection) for choosing which individuals will breed new individuals. You can configure the parameters of the tournament and the mutation amplitudes applied to the parameters in the ``lib/inference/genalgOptions.json`` file:
	- ``"rounds"`` is the number of individuals that will breed new individuals.
	- ``"roundSize"`` is the size of each tournament.
	- ``"offspring"`` is the quantity of individuals the chosen individuals will breed.
	There are offspring x rounds number of new individuals. The way the tournament works is that the best out of a random 		sample of individuals is chosen. This means that big tournaments are favorable to strong individuals and small 			tournaments allow weaker individuals to go through (which isn't necessarily a bad thing, 					[simulated annealing](http://www.wikiwand.com/en/Simulated_annealing) does the same thing).
- It also has to be said that including the island size parameter (``-c``) requires the algorithm to run for much more generations because the search space becomes much bigger.
- If you think you have a better way of measuring the distance between two curves you can add it to the ``distance.py`` script and modify the ``evaluate()`` procedure in the ``genalg.py`` script.
- A recurring problem was that sometimes the times as which the migration rates changes were so close it was like having only one. The ``genalgOptions.json`` now has a ``timeGapPercentage`` parameter. This obliges times to be split by at least a percetenge of the last time. For example if the last time is 120 and the parameter is set to 18 then times will have to be spread out by at least 120 * 18 / 100 = 21.6.

## Examples

The following commands use PSMC files provided by [Willy Rodriguez](https://github.com/willyrv).

### First example - 0 switches

```sh
python convert.py data/example1.psmc
python infer.py data/example1.csv -s 0 -g 25 -r 1 -m least_squares -k True
```

![First example](http://i.imgur.com/dAjLVEo.png)

### Second example - 3 switches

```sh
python convert.py data/example2.psmc
python infer.py data/example2.csv -s 3 -g 100 -m integral -k True -o data/example2_3_switch
```

![Second example](http://i.imgur.com/kxyBi7l.png)

### Third example - Islands can change size

You can also try to fit the model to the PSMC curve yourself. Make sure to give the same number of times (T) and migration rates (M). Don't forget that the first time is always ``0``.

```sh
python convert.py data/example3.psmc
python infer.py data/example3.csv -s 3 -c True -g 100 -m least_squares -k True -o data/example3_island_size_change
```

![Third example](http://i.imgur.com/6H4m7IL.png)

### Fourth example - Manual

You can also try to fit the model to the PSMC curve yourself. Make sure to give the same number of times (T) and migration rates (M). Don't forget that the first time is always ``0``.

```sh
python convert.py data/example4.psmc
python manual.py data/example4.csv -n 12 -T 0 3 8 20 -M 3 4 3 7 -C 1 1 1 1 -k True
```

![Fourth example](http://i.imgur.com/O7kLV5J.png)

## Output

Changing the chart outputs is really easy. The ``lib/chartOptions.json``file is made for easily doing so. The default settings produce the charts you see in the [Examples](#examples) section. Most of the parameters are not too hard to understand. I would recommend reading the documentation from [matplotlib](http://matplotlib.org/contents.html) if you want to do something complicated.

## Architecture

    StSICMR-Inference
    ├───┐ data
    │   └─── ...
    ├───┐ lib
    │   ├───┐ inference
    │   │   ├─── __init__.py
    │   │   ├─── distance.py
    │   │   ├─── genalg.py
    │   │   └─── genalgOptions.json
    │   ├─── __init__.py
    │   ├─── chartOptions.json
    │   ├─── model.py
    │   ├─── plotting.py
    │   └─── tools.py
    ├─── convert.py
    ├─── infer.py
    ├─── LICENSE
    ├─── manual.py
    ├─── README.md
    ├─── requirements.txt
    └─── utests.py

The two main scripts (``infer.py`` and ``manual.py``) are in the top-level of the directory. In the ``lib`` folder is where the heavy-lifting is being done:

- ``model.py`` contains the StSCMIR class where the mathematics are done. 
- ``tools.py`` is for opening and parsing a ``.psmc`` file.
- ``genalg.py`` tries to find good parameters for the model to fit a PSMC timeline.
- ``plotting.py`` plots a model and a PSMC timeline on the same chart.

The reason why ``lib`` contains the ``inference`` folder is if ever there will be another method of infering the parameters, it doesn't necessarily have to be a genetic algorithm. However the distance measures between the target curve and the model curve will always be the same, hence the ``distance.py`` script that can easily be reused with other methods.

## Contact

If you have questions about the mathematics please send a mail to <willyrv@gmail.com>.

If you have questions about the genetic algorithm and/or the code please send a mail to <maxhalford25@gmail.com>.

I wrote an [internship report](http://maxhalford.com/data/internships/L3_Internship_Max_Halford.pdf) related to this software in 2015 for my third year at university.

## License

See the [LICENSE file](LICENSE).

## Issues

Please click on the "Issues" button or use the email adresses, we'll be glad to help.
