UV = uv

PYTHON := $(UV) run python

PROJECT := src

FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

PATH_FLAKE8 = $(UV) run flake8

ARGS_DEF = --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json


PATH_MYPY = $(UV) run mypy

install: 
	@$(UV) sync --all-packages
	@echo "venv environment has been created"

run: install
	$(PYTHON) -m $(PROJECT) $(AEGS_DEF)


clean:
	rm -rf .venv .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +


lint: install
	@$(PATH_FLAKE8) $(PROJECT)
	@$(PATH_MYPY) $(PROJECT) $(FLAGS)

lint-strict: install
	@$(PATH_FLAKE8) $(PROJECT)
	@$(PATH_MYPY) $(PROJECT) --strict

