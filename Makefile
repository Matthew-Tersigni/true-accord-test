PYTHON_MODULES := src
PYTHONPATH := .
VENV := .venv
PYTEST := env PYTHONPATH=$(PYTHONPATH) PYTEST=1 $(VENV)/bin/py.test tests/*.py -s --cov=$(PYTHON_MODULES) --cov-report=term-missing --cov-fail-under=98
PYLINT := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pylint --disable=I0011 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
PYCODESTYLE := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pycodestyle --repeat --ignore=E202,E501,E402
PYTHON := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/python
PIP := $(VENV)/bin/pip

DEFAULT_PYTHON := /usr/bin/python3
VIRTUALENV := /usr/local/bin/virtualenv

REQUIREMENTS := -r requirements.dev

default: check-style

venv:
		test -d $(VENV) || $(VIRTUALENV) -p $(DEFAULT_PYTHON) -q $(VENV)
requirements:
		@if [ -d wheelhouse ]; then \
			$(PIP) install -q --no-index --find-links=wheelhouse $(REQUIREMENTS); \
        else \
			$(PIP) install -q $(REQUIREMENTS); \
        fi
bootstrap: venv requirements

check-style: bootstrap
		$(PYCODESTYLE) $(PYTHON_MODULES)
		$(PYLINT) -E $(PYTHON_MODULES)
pylint-full: check-style
		$(PYLINT) $(PYTHON_MODULES)
test: check-style
		$(PYTEST)
check:
		$(PYTEST)

.PHONY: default venv requirements bootstrap check-style pylint-full test check