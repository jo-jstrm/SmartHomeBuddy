SHELL := /bin/bash
PY_DIR := device-identifier
VENV_DIR := .venv/bin/activate

start:
	cd $(PY_DIR) && \
		source $(VENV_DIR) && \
		python -m shbdeviceidentifier \
		& # Run in the background
	cd electron-app && \
		npm start

electron:
	cd electron-app && \
		npm start

deviceidentifier:
	cd device-identifier && \
		python -m shbdeviceidentifier