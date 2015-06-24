# Symmetrical Island Model with Changes in Migration Rates - Inference

## Introduction

## Requirements

All of the code has been tested on Python 3.4 and Ubuntu 14.04. This should work fine on a different OS, however I would highly recommend using Python 3.x.

The following module versions were used, that said older and newer versions have a good chance of working too. If you do not have them installed you can simply ``cd`` to the first level of the repository (where ``requirements.txt`` is located) and type ``pip3 install -r requirements.txt``. If you don't have ``pip`` installed then you can install the modules manually, this should be easy on any platform as all of them are extremely popular modules. 

	- Cython == 0.22.1
	- matplotlib == 1.4.3
	- numpy == 1.9.2
	- scipy == 0.15.1

### Virtual environment

If you want to be safe and not mess with you Python environment you can create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) by doing the following steps.

1. Clone the repository:

	git clone https://github.com/MaxHalford/StSICMR-Inference
	cd StSICMR-Inference

2. Create and activate a virtual environment:

	virtualenv env
	source env/bin/activate

3. Install requirements:

	pip install -r requirements.txt

## Architecture

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

## Examples

``python3 infer -f examples/example1.psmc -i 100 -s 0 -p 1000 -r 1 -g 25 -m least_squares -k True``

![Example 1](examples/example1_0_switch.png)

``python3 infer -f examples/example2.psmc -i 100 -s 4 -p 1000 -r 1 -g 100 -m integral -k True``

![Example 2](examples/example2_3_switch.png)

## Advice

## Remarks

[cprofilev](https://github.com/ymichael/cprofilev)

## Contact

**``willyrv@gmail.com``**

**``maxhalford25@gmail.com``**
