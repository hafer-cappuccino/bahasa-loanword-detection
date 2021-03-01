# bahasa-loanwords-detection

This project can be set up either with [`docker`](https://docker.com) or
[`poetry`](https://python-poetry.org).

## Quickstart

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
| `analysis` | Outputs into the terminal the classification reports and confusion matrices of each language model. |
