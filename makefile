SHELL := $(SHELL) -e  # ensure return codes within line continuations are honored
REPO_NAME = $(shell basename $(CURDIR))
PYTHON_VERSION := 3.6.5
.DEFAULT_GOAL := all

PYENV_ROOT := $(shell pyenv root)

clean: deactivate_pyenv
	rm -f .python_dependencies

pyenv: ${PYENV_ROOT}/versions/${REPO_NAME}/activate
	pyenv local ${REPO_NAME}

${PYENV_ROOT}/versions/${REPO_NAME}/activate:
	pyenv install -s ${PYTHON_VERSION}
	[ -e ${PYENV_ROOT}/versions/${REPO_NAME} ] && echo "Skipping pyenv creation" || pyenv virtualenv ${PYTHON_VERSION} ${REPO_NAME}
	touch ${PYENV_ROOT}/versions/${REPO_NAME}/activate

deactivate_pyenv:
	pyenv uninstall --force ${REPO_NAME}
	rm -f .python-version

python_dependencies: pyenv .python_dependencies

.python_dependencies: requirements.txt
	pip install -r requirements.txt
	pip install -r test_requirements.txt
	touch .python_dependencies

dependencies: python_dependencies

all: dependencies

.PHONY: clean pyenv deactivate_pyenv python_dependencies dependencies all
