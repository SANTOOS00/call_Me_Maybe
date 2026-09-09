UV = uv

PYTHON := $(UV) run python

PROJECT := src

FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

PATH_FLAKE8 = $(UV) run flake8

PATH_MYPY = $(UV) run mypy

OUTPUT_DEF = data/output/function_calls.json

INPUT_DEF = data/input/function_calling_tests.json

FUNCTIONS_DEFINITION_DEF = data/input/functions_definition.json

install:
	@$(UV) sync --all-packages
	@echo "venv environment has been created"

run: install
	$(PYTHON) -m $(PROJECT) --functions_definition \
	$(FUNCTIONS_DEFINITION_DEF) --output $(OUTPUT_DEF) \
	--input $(INPUT_DEF)

clean:
	rm -rf .venv .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint: install
	@$(PATH_FLAKE8) $(PROJECT)
	@$(PATH_MYPY) $(PROJECT) $(FLAGS)

lint-strict: install
	@$(PATH_FLAKE8) $(PROJECT)
	@$(PATH_MYPY) $(PROJECT) --strict

test_project = test_project

run_test:
	@$(PYTHON) -m $(test_project) --functions_definition \
	$(FUNCTIONS_DEFINITION_DEF) --output $(OUTPUT_DEF) \
	--input $(INPUT_DEF)
