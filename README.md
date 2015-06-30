![StSICMR](http://i.imgur.com/MtvTjvh.png)

## Symmetrical Island Model with Changes in Migration Rates - Inference

The Symmentrical Island Model with Changes in Migration Rates (StSICMR) is a model developped by [Oliver Mazet](http://fr.viadeo.com/fr/profile/olivier.mazet1) and [Lounès Chikhi](https://www.wikiwand.com/en/Loun%C3%A8s_Chikhi) with their research team.

This repository supposes that you are familiar with the [PSMC algorithm](http://www.nature.com/nature/journal/v475/n7357/full/nature10231.html) developped by [Richard Durbin](https://www.wikiwand.com/en/Richard_M._Durbin) and [Heng Li](https://www.wikiwand.com/en/Heng_Li).

The method tries to fit the model to a PSMC history produced with [Heng Li's algorithm](https://github.com/lh3/psmc). It starts by extracting the times and the lambda values of the last iteration from ``.psmc`` file. Then it normalizes the lambda value so that they start at 1 (because the model is normalized to begin at 1 also).

## Setup

All of the code has been tested on Python 3.4 and Ubuntu 14.04. This should work fine on a different OS, however Python 3.x is highly recommended.

### Normal

The following module versions were used, that said older and newer versions have a good chance of working too.
	
	- Cython == 0.22.1
	- matplotlib == 1.4.3
	- numpy == 1.9.2
	- scipy == 0.15.1

If you do not have them installed type

```sh
cd /StSICMR-Inference
pip3 install -r requirements.txt
```
	
If you don't have ``pip`` installed then you can install the modules manually, this should be easy on any platform as all of them are extremely popular modules. 

In order to compile some Python code into C code you also have to type

```sh
cd /lib/cython/
./compile.sh
```

### With a virtual environment

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

**4. Compile Python code to C code**

```sh
cd lib/cython
./compile.sh
```

This creates a sandboxed Python where you can do as you please without fear of screwing up your setup. The only thing required is to have Python 3.x installed in order to run ``virtualenv env``. To deactivate the virtual environment type ``deactivate``. To activate it type ``source venv/bin/activate``, if you don't the default Python interpreter will be used. You can delete the ``StSICMR-Inference`` folder and it will be as if nothing ever happened.

## Usage

### Command line arguments

The main script is called ``infer`` and is written in Python 3.

| Argument | Name        | Description                                                  |
|----------|-------------|--------------------------------------------------------------|
| -v       | Version     | Get the version of the script.                               |
| -n       | Islands     | Maximal number of islands for the first generation.          |
| -s       | Switches    | Number of switches for the model.                            |
| -p       | Size        | Initial generation size.                                     |
| -r       | Repetitions | Number of times to repeat the process.                       |
| -g       | Generations | Number of iterations for each population.                    |
| -u       | Rate        | Rate at which the parameters mutate.                         |
| -m       | Method      | Method for evaluating the fits.                              |
| -k       | Keep        | Set to True to save the inference as a plot and a JSON file. |
| -o       | Outfile     | Override name of output files.                               |

### Examples

The following commands use PSMC files provided by [Willy Rodriguez](https://github.com/willyrv).

#### First example

```sh
./infer examples/example1.psmc -n 100 -s 0 -p 1000 -r 1 -g 25 -u 1 -m least_squares -k True
```

![Example 1](examples/example1_0_switch.png)

#### Second example

```sh
./infer examples/example2.psmc -n 100 -s 3 -p 1000 -r 1 -g 100 -u 5 -m integral -k True -o examples/example2_3_switch
```

![Example 2](examples/example2_3_switch.png)

### Manual

You can also try to fit the model to the PSMC curve yourself. Make sure to give the same number of times (T) and migration rates (M). Don't forget that the first time is always ``0``.

```sh
./manual examples/example3.psmc -n 12 -T 0 3 8 20 -M 3 4 3 7 -k True
```

![Example 3](examples/example3_manual.png)

### Advice

If the algorithm seems to fail

## Architecture & explanation

    StSICMR-Inference/
        -results/
        -lib/
            -cython/
                -build/
                    -temp.linux-x86_64-3.4/
                        -cythonized.o
                -profile.sh
                -compile.sh
                -setup.py
                -cythonized.pyx
                -cythonized.c
            -__pycache__/
            -__init__.py
            -cythonized.so
            -plotting.py
            -model.py
            -psmcfit.py
            -genalg.py
        -README.md
        -infer
        -requirements.txt
        -LICENSE
        -example.psmc
        -architecture.md

[cprofilev](https://github.com/ymichael/cprofilev)

## Contact

If you have questions about the mathematics please send a mail to <willyrv@gmail.com>.

If you have questions about the genetic algorithm and/or the code please send a mail to <maxhalford25@gmail.com>.

## License

See the [LICENSE file](LICENSE).