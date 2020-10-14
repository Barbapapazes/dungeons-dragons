# Dungeons and Dragons

> A 3A students project for INSA's python courses

## Build Setup

You need **python 3** and **pip** installed on your machine.

```sh
# install pipenv
pip install pipenv
# install all packages
pipenv install
# start the project
pipenv run start
# start in dev mode
pipenv run dev
```

## Docs

## Tools

### Virtual Environnement

To be sure that everyone have the same packages and working environnement, we will use `pipenv`. This tool is very useful to install and lock packages and to run script

```sh
# install package
pipenv install [package]
# run a script
pipenv run <cmd>
```

### VS Code

VS Code is recommended for this project.

To improve the way the code is written, there is some recommendations, about extensions, in the `.vscode` folder.

### Linter and formatter

To lint our code, we will use `pylint`. Using it with VS Code is very interesting because `pylint` will be able to tell use what we can do to improve our file in the file your working !

To automatically format our code, we will use `autopep8`. This is a super useful tool to be sure that everybody have the sames editor rules and to prevent some unwanted changes.

```sh
# check the code
pipenv run lint
# format the code
pipenv run lint_fix
```
