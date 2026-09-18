.PHONY: install run debug clean lint lint-strict

UV := uv
PYTHON := $(UV) run python
SRC := src

install:
	$(UV) sync --package

run:
	$(UV) run python -m $(SRC)

clean:
	rm -rf __pycache__ .mypy_cache
	rm -rf .venv *.egg-info
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +

lint:
	$(UV) run $(UV_FLAGS) flake8 $(SRC)
	$(UV) run $(UV_FLAGS) mypy $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV) run $(UV_FLAGS) mypy $(SRC)
	$(UV) run $(UV_FLAGS) flake8 $(SRC)

