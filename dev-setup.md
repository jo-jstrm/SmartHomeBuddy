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
- GRPC
  - You can test the running server from the command line usind [grpcurl](https://github.com/fullstorydev/grpcurl): `./grpcurl --plaintext localhost:8090 list`
  - RPC example: `./grpcurl -v -d '{"file_path": "/home/jo/git/SmartHomeBuddy/device-identifier/shbdeviceidentifier/pcaps/dummy.pcap", "file_type": "pcap"}' -plaintext localhost:8090 SmartHomeBuddy.PcapDatabase/LoadPcapIntoDatabase`