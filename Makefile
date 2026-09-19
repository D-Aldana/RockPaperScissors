PYTHON ?= python3.11
VENV := game/.venv

.PHONY: dev install redis game frontend

# Ctrl-C stops everything
dev:
	@$(MAKE) -j3 redis game frontend

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r game/requirements.txt
	cd react-app && npm install

# Skip if Redis is already running (e.g. via brew services)
redis:
	@redis-cli ping >/dev/null 2>&1 || redis-server

# Model paths are relative to game/src
game:
	cd game/src && ../.venv/bin/python rock_paper_scissors.py

frontend:
	cd react-app && npm start
