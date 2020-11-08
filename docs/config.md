# Config

## Build Setup

You need **python 3** and **pip** installed on your machine.

```sh
# install a local environment
$ pip install pipenv
# install all packages
$ pipenv install
# start the project
$ pipenv run start
# start in dev mode
$ pipenv run dev
# start the map editor
$ pipenv run map_editor
```

## Docs

To start the docs locally, you need [nodejs](https://nodejs.org).

```sh
# install dependencies
npm install
# start the docs in dev mode
npm docs:dev
# build the docs
npm docs:build
```

## Tools

### Virtual Environnement

To be sure that everyone have the same packages and working environnement, we will use [`pipenv`](https://pipenv.pypa.io/en/latest/). This tool is very useful to install and lock packages and to run script

```sh
# install package
$ pipenv install [package]
# run a script
$ pipenv run <cmd>
```

### VS Code

[VS Code](https://code.visualstudio.com/) is recommended for this project.

To improve the way the code is written, there is some recommendations, about extensions, in the `.vscode` folder.

### Linter and formatter

To lint our code, we will use [`pylint`](https://pylint.org/). Using it with VS Code is very interesting because [`pylint`](https://pylint.org/) will be able to tell use what we can do to improve our file in the file your working !

To automatically format our code, we will use [`autopep8`](https://pypi.org/project/autopep8/). This is a super useful tool to be sure that everybody have the sames editor rules and to prevent some unwanted changes.

```sh
# check the code
$ pipenv run lint <file_name_to_check>
# format the code
$ pipenv run lint_fix
```
