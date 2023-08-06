# Mammut-Py

## Installation

Use pip to install the package:
```
pip install mammut-py
```

## Development

The following tools are used in this project:
- [Poetry](https://python-poetry.org/) is used as package manager.
- [Nox](https://nox.thea.codes/) is used as automation tool, mainly for testing.
- [Black](https://black.readthedocs.io/) is the mandatory formatter tool.
- [PyEnv](https://github.com/pyenv/pyenv/wiki) is recommended as a tool to handle multiple python versions in your machine.

The library is intended to be compatible with python ~3.6.9, ~3.7.4 and ~3.8.2. But the primary version to support is ~3.8.2.

The general structure of the project is trying to follow the recommendations
in [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).
The main difference lies in the source code itself which is not constraint to data science code.
