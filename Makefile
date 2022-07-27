SHELL := /bin/bash
PY_DIR := device-identifier
VENV_DIR := .venv/bin/activate

start-local:
	cd $(PY_DIR) && \
		source $(VENV_DIR) && \
		python -m shbdeviceidentifier \
		& # Run in the background
	cd electron-app && \
		npm start

start-electron-local:
	cd electron-app && \
		npm start

start-device-identifier-local:
	cd $(PY_DIR) && \
		source $(VENV_DIR) && \
		python -m shbdeviceidentifier \

dist-device-identifier:
	 cd device-identifier && \
	 	pyinstaller cli.py &&