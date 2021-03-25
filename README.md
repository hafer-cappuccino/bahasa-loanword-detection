# Loanwords Detection in Bahasa Indonesia 

## Project description

This repository contains materials on the project dedicated to Loanwords Detection in Bahasa Indonesia. We carried out this mini research as our final project for the Master’s course *Advanced Natural Language Processing* at the University of Potsdam. 

The whole framework of the project was mainly inspired by the study of [Miller et al. on Borrowings Detection in Monolingual Wordlists](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0242709). Following their practice, we also considered words as their [phonetic representations](https://github.com/hafer-cappuccino/bahasa-loanword-detection/blob/main/notebooks/data/phonemes.ipynb) and took phonemes as features for the models. However, unlike the authors who studied loanwords in all the languages represented in [WOLD](https://wold.clld.org), we only focused on the Bahasa Indonesian language.

We implemented three following **models**:
-	[The Bag of Sounds](https://github.com/hafer-cappuccino/bahasa-loanword-detection/blob/main/src/models/svm.py) 
-	[Markov Model](https://github.com/hafer-cappuccino/bahasa-loanword-detection/blob/main/src/models/markov.py) with interpolated Kneser-Ney smoothing
-	[GRU-based Neural Network](https://github.com/hafer-cappuccino/bahasa-loanword-detection/tree/main/src/models/gru). For this model, also find the python [notebook](https://github.com/hafer-cappuccino/bahasa-loanword-detection/tree/main/notebooks/model/GRU-NN-overview.ipynb) with detailed explanations and code. 

The **results** were in line with those of Miller et al. BoS predictably resulted in lower performance since it processed phonemes as an unordered set of phonemes: **f1-score** of **0.48**. MM and GRU-NN that considered the phonemic sequences in a word, led to **f1-score** of **0.62** and **0.64** respectively on the testing set. 



## Quickstart

This project can be set up either with [`docker`](https://docker.com) or
[`poetry`](https://python-poetry.org).

### Docker

Before a docker container can be run, the image must be built first:

```sh
$ make build
```

To run the docker container:

```sh
$ make shell
```

This runs an interactive bash shell. Then from within the docker container's bash shell, you can run the following to see the model evaluations:

``` sh
$ make analysis
```

### Poetry

First, install the project dependencies with Poetry:

```sh
$ poetry install
```

Once the dependencies are installed, you can activate the virtualenv that Poetry
generated with `poetry shell`.

From within the virtualenv, a Jupyter lab can be served: `jupyter lab` and the project's CLI script available:

```
$ python src/cli/cli.py --help
```

## Make Directives

**These directives only work outside of docker containers except `analysis`.**

A [Makefile](Makefile) has been included in this project for convenience. To use
the Makefile rules, simply run `make <rule>` with `<rule>` substituted with any
of the rules in the table below. 

| rule | description |
| --------| ----------- |
| `build` | Build a docker image. |
| `run` | Runs a docker container with the built image. This starts a Jupyter server.|
| `stop` | Stops the docker container. |
| `csv` | Writes the list of Indonesian word forms to a CSV file. Requires a running docker container. |
| `shell` | Runs an interactive bash shell of a docker container. |
| `analysis` | Outputs into the terminal the classification reports and confusion matrices of each language model. Requires to be in an activated virtualenv with `poetry shell` or in a running docker container (with `make shell`).|
