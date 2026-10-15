PYTHON = python3
CONFIG = config.txt

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install flake8 mypy mazegen-1.0.0-py3-none-any.whl

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint: install
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict
