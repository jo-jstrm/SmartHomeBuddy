SHELL := /bin/bash
PY_DIR := device-identifier
VENV_DIR := .venv/bin/activate
INFLUXDB_DIR := InfluxData/influxdb
INFLUXDB_CLIENT_DIR := InfluxData/influxdb-client

start-local: start-influxdb-local start-device-identifier-local	start-electron-local

start-electron-local:
	cd electron-app && \
		npm start

start-device-identifier-local:
	cd $(PY_DIR) && \
		source $(VENV_DIR) && \
		python -m shbdeviceidentifier \
		& # Run in the background

start-influxdb-local:
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