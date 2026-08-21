MAIN = main.py

VENV = venv

PYTHON3 = python3

PAHT_PYTHON3 = .$(VENV)/bin/python3

env:
	if [ ! -d "$(VENV)" ]; then uv $(VENV); fi

install: env
	uv pip install -r requirements.txt

run: install
	.$(VENV)/bin/python3 $(MAIN)

clean:
	rm -rf $(VENV) __pycache__
