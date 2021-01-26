# Dungeons and Dragons

> A 3A students project for INSA's python courses

## Build Setup

You need **python 3.9** and **pip** installed on your machine.

```sh
# install pipenv
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

### Env

As you can see, there is a `.env.local` file. To enable feature like production mode or online mode, you have to create a copy of it and call it `.env`.

For production:

```txt
PYTHON_ENV=production
```

For online game (only add this key to play online, otherwise, remove it):

```txt
SERVER_IP=178.79.177.210 (this IP is the remote server)
```

## Docs

Read the docs [here](https://barbapapazes.github.io/dungeons-dragons/).

To start the docs locally, you need [nodejs](https://nodejs.org).

```sh
# install dependencies
npm i
# start the docs in dev mode
npm docs:dev
# build the docs in production mode
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
