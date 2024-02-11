# Climate-Change-Adaptation-Lower-Saxony

## Introduction

## Whats contained in this repository
- `data` contains all the inputs used to run the model and generate the plots.
- `data/adaptation_speed.xlsx` in particular contains tweakable parameters that allow the configuration of adaptation measures.
- `run_model` the main module that runs the model parameters and and generates the plots

## How to run the models

### Setup
The environment can be setup using pip or pipenv. Make sure your environment is using python 3.9. This application and its dependancies were not tested for any other python version.

pip: `pip install -r requirements.txt`

pipenv: `pipenv sync`

### Run
`python run_model.py`

Or, alternatively, you can provide an integer argument to run this application with multiprocessing and speed it up:

`python run_model.py 8`

Either method will create a `plots` directory that is then populated with the plots also referenced in the accompanying publication.