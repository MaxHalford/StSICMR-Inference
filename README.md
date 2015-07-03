![StSICMR](http://i.imgur.com/MtvTjvh.png)

## Symmetrical Island Model with Changes in Migration Rates - Inference

The Symmetrical Island Model with Changes in Migration Rates (StSICMR) is a model developped by [Oliver Mazet](http://fr.viadeo.com/fr/profile/olivier.mazet1) and [Lounès Chikhi](https://www.wikiwand.com/en/Loun%C3%A8s_Chikhi) with their research team.

This repository supposes that you are familiar with the [PSMC algorithm](http://www.nature.com/nature/journal/v475/n7357/full/nature10231.html) developped by [Richard Durbin](https://www.wikiwand.com/en/Richard_M._Durbin) and [Heng Li](https://www.wikiwand.com/en/Heng_Li).

The method tries to fit the model to a PSMC timeline produced with [Heng Li's algorithm](https://github.com/lh3/psmc). It starts by extracting the times and the lambda values of the last iteration from a ``.psmc`` file. Then it normalizes the lambda value so that they start at 1 (because the model is normalized to begin at 1 also). For the fitting part it uses a [genetic algorithm](http://www.wikiwand.com/en/Genetic_algorithm) using [tournament selection](https://www.wikiwand.com/en/Tournament_selection). The implementation is done in Python 3.4 and is designed to be comprehensible and easy to edit. I wrote a [tutorial on genetic algorithms](http://maxhalford.com/resources/notebooks/genetic-algorithms.html) to explain how I code genetic algorithms with Python.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Examples](#example)
- [Output](#output)
- [Architecture](#architecture)
- [Contact](#contact)
- [License](#license)

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

If you want to be safe and not mess with your Python environment you can create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) by doing the following steps.

**1. Clone the repository**

```sh
git clone https://github.com/MaxHalford/StSICMR-Inference
cd StSICMR-Inference
```
	
**2. Create and activate a virtual environment**

```sh
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
```
	
**3. Install requirements**

```sh
pip3 install -r requirements.txt
```

This creates a sandboxed Python where you can do as you please without fear of screwing up your setup. The only thing required is to have Python 3.x installed in order to run ``virtualenv env``. To deactivate the virtual environment type ``deactivate``. To activate it type ``source venv/bin/activate``, if you don't the default Python interpreter will be used. You can delete the ``StSICMR-Inference`` folder and it will be as if nothing ever happened.

### 3. Anaconda

This is probably the easiest way if you don't have Python installed. Simply [download Anaconda](http://continuum.io/downloads) for your platform (you can choose between Python 2 or 3). Anaconda includes all the modules necessary so there is nothing else to do.

## Usage

### Infer

The main script is called ``infer`` and guesses the parameters for a given PSMC timeline.

| Argument | Name        | Description                                                  | Default    |
|----------|-------------|--------------------------------------------------------------|------------|
| -v       | Version     | Get the version of the script.                               |            |
| -n       | Islands     | Maximal number of islands for the first generation.          | 100        |
| -s       | Switches    | Number of switches for the model.                            | 0          |
| -p       | Size        | Initial generation size.                                     | 1000       |
| -r       | Repetitions | Number of times to repeat the process.                       | 1          |
| -g       | Generations | Number of iterations for each population.                    | 100        |
| -u       | Rate        | Rate at which the parameters mutate.                         | 1          |
| -m       | Method      | Method for evaluating the fits.                              | 'integral' |
| -k       | Keep        | Set to True to save the inference as a plot and a JSON file. | 'False'    |
| -o       | Outfile     | Override name of output files.                               |            |

The initial number of islands (``-n``) is not important as the algorithm usually finds the right number of islands straight away. The higher the initial population size (``-p``) is the more of the search space will be covered at first. For repeating the process you can use the repetitions arguments (``-r``) and the best model will be saved. The genetic algorithm implementation stops after a fixed number of generations (``g``). The mutation rate (``u``) is important; if it is high the algorithm will not get stuck, at the cost of precision. There are two methods (``m``) for measuring the distance between two curves:

- the least squares on the vectors which doesn't take into account the abscissa (``'least_squares'``).
- the least squares on the functions which does take into account the abscissa (``'integral'``).

If the keep argument (``-k``) is set to ``'True'`` then the best model will be saved as a PNG file for the chart and a JSON file for the parameters with default names. You can also use the outfile argument (``-o``) for overriding the name given to the saved files.

### Manual

The other script called ``manual`` is for visualizing a model with user-defined parameters.

| Argument | Name            |
|----------|-----------------|
| -n       | Islands         |
| -T       | Switch times    |
| -M       | Migration rates |
| -k       | Keep            |
| -o       | Override        |

### Taming the genetic algorithm

- Increasing the generation size can have an impact, the longer the algorithm runs the lower the chance that the algorithm won't improve the model.
- If the algorithm seems to fail you can try to increase the mutation rate. Often is the case this will enable it to find a better area. However a high mutation rate removes precision from the algorithm.
- *Trying again* isn't a bad idea when using genetic algorithms.
- The initial population size can be important, the higher it is and the more of the search space will be explored at first.
The genetic algorithm uses [tournament selection](https://www.wikiwand.com/en/Tournament_selection) for choosing which individuals will breed new individuals. You can configure the parameters of the tournament in the ``lib/inference/tournamentOptions.json`` file:
	- ``"rounds"`` is the number of individuals that will breed new individuals.
	- ``"roundSize"`` is the size of each tournament.
	- ``"offspring"`` is the quantity of individuals the chosen individuals will breed.
	There are offspring x rounds number of new individuals. The way the tournament works is that the best out of a random 		sample of individuals is chosen. This means that big tournaments are favorable to strong individuals and small 			tournaments allow weaker individuals to go through (which isn't necessarily a bad thing, 					[simulated annealing](http://www.wikiwand.com/en/Simulated_annealing) does the same thing).

## Examples

The following commands use PSMC files provided by [Willy Rodriguez](https://github.com/willyrv).

### First example - 0 switches

```sh
python convert examples/example1.psmc
python infer.py examples/example1.csv -n 100 -s 0 -p 1000 -r 1 -g 25 -u 1 -m least_squares -k True
```

![Example 1](examples/example1_0_switch.png)

### Second example - 3 switches

```sh
python convert examples/example2.psmc
python infer.py examples/example2.csv -n 100 -s 3 -p 1000 -r 1 -g 100 -u 5 -m integral -k True -o examples/example2_3_switch
```

![Example 2](examples/example2_3_switch.png)

### Third example - Manual

You can also try to fit the model to the PSMC curve yourself. Make sure to give the same number of times (T) and migration rates (M). Don't forget that the first time is always ``0``.

```sh
python convert examples/example3.psmc
python manual.py examples/example3.csv -n 12 -T 0 3 8 20 -M 3 4 3 7 -k True
```

![Example 3](examples/example3_manual.png)

## Output

Changing the chart outputs is really easy. The ``lib/chartOptions.json``file is made for easily doing so. The default settings produce the charts you see in the [Examples](#examples) section. Most of the parameters are not too hard to understand. I would recommend reading the documentation from [matplotlib](http://matplotlib.org/contents.html) if you want to do something complicated.

## Architecture

    StSICMR-Inference
    ├───┐ examples
    │   ├─── example1.csv
    │   ├─── example1.psmc
    │   ├─── example1_0_switch.json
    │   ├─── example1_0_switch.png
    │   ├─── example2.csv
    │   ├─── example2.psmc
    │   ├─── example2_3_switch.json
    │   ├─── example2_3_switch.png
    │   ├─── example3.csv
    │   ├─── example3.psmc
    │   ├─── example3_manual.json
    │   └─── example3_manual.png
    ├───┐ lib
    │   ├───┐ cython
    │   │   ├─── compile.sh
    │   │   ├─── cythonized.c
    │   │   ├─── cythonized.pyx
    │   │   └─── setup.py
    │   ├───┐ inference
    │   │   ├─── __init.py__
    │   │   ├─── distance.py
    │   │   ├─── genalg.py
    │   │   └─── tournamentOptions.json
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
    └─── requirements.txt

The two main scripts (``infer`` and ``manual``) are in the top-level of the directory. In the ``lib`` folder is where the heavy-lifting is being done:

- ``model.py`` contains the StSCMIR class where the mathematics are done. 
- ``psmcfit.py`` is for opening and parsing a ``.psmc`` file.
- ``genalg.py`` tries to find good parameters for the model to fit a PSMC timeline.
- ``plotting.py`` plots a model and a PSMC timeline on the same chart.

One of the flaws of genetic algorithms is their computational cost. The ``cython`` folder aims at speeding up some of the mathematics done in the ``model.py`` script (for example eigenvalues and diagonalization). For the moment I haven't done much work here (I want to learn how to do good C code) but I will be in the future. If ever you want to add some C code you can use [cprofilev](https://github.com/ymichael/cprofilev) to check what functions are taking the most time. Once you have added code to ``cythonized.pyx`` you can compile it to C code with ``compile.sh`` script, it's as easy as that.

## Contact

If you have questions about the mathematics please send a mail to <willyrv@gmail.com>.

If you have questions about the genetic algorithm and/or the code please send a mail to <maxhalford25@gmail.com>.

## License

See the [LICENSE file](LICENSE).
