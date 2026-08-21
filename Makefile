MAIN = main.py

VENV = .venv

PYTHON3 = python3

PAHT_PYTHON3 = $(VENV)/bin/python3

env:
	if [ ! -d "$(VENV)" ]; then $(PYTHON3) -m venv $(VENV); fi

run: env
	$(VENV)/bin/python3 $(MAIN)

clean:
	rm -rf $(VENV)

install: env
	$(VENV)/bin/pip	install -r requirements.txt