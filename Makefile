SHELL := /bin/bash
PY_DIR := device-identifier
VENV_DIR := .venv/bin/activate
INFLUXDB_DIR := InfluxData/influxdb
INFLUXDB_CLIENT_DIR := InfluxData/influxdb-client

start-dev: start-influxdb-dev start-device-identifier-dev start-electron-dev

start-electron-dev:
	cd electron-app && \
		npm start

start-device-identifier-dev:
	cd $(PY_DIR) && \
		source $(VENV_DIR) && \
		python -m pip install --upgrade pip && \
		python -m pip install -r requirements.txt
		python -m pip install -e .
		shbdeviceidentifier start\
		& # Run in the background

start-influxdb-dev:
	cd $(INFLUXDB_DIR) && \
		./influxd \
		& # Run in the background

setup-influxdb:
	cd $(INFLUXDB_CLIENT_DIR) && \
		./influx setup --username admin --password SHBadmin --org SmartHomeBuddy --bucket network-traffic --force && \
		./influx auth list --json --user admin > .\admin_auth.json

dist-device-identifier:
	 cd device-identifier && \
	 	pyinstaller cli.py &&