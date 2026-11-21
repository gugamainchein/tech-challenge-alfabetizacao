PY ?= python
export PYTHONPATH := src

.PHONY: install test lint batch silver gold produce consume

install:
	$(PY) -m pip install -r requirements-dev.txt

test:
	$(PY) -m pytest

lint:
	$(PY) -m ruff check src tests

batch:
	$(PY) -m pipeline.run batch

silver:
	$(PY) -m pipeline.run silver

gold:
	$(PY) -m pipeline.run gold

produce:
	$(PY) -m pipeline.run produce --n 500

consume:
	$(PY) -m pipeline.run consume
