# Local Development Setup


## electron-app
- `make electronapp` or `cd electron-app && npm install && npm start`

## device-identifier
- `make deviceidentifier` or `cd device-identifier && source .venv/bin/activate && python -m shbdeviceidentifier`

## Requirements
All OSs
- Python 3.8 including distutils
- Packages from `device-identifier/requirements.txt`
- node with npm
- optional: 
  - make
  - protoc: if you want to compile the proto files
    - Download from Github for newest version

Linux: None

Windows
- pypiwin32 for pyinstaller: `pip install pypiwin32`

## Additional Info
- If you have orphaned python processes running, run `kill $(pgrep -f 'python -m shbdeviceidentifier')`