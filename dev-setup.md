# Local Development Setup

## electron-app
```bash
cd electron-app && \
npm install && \
npm start
```

## device-identifier
First, you need to download influxdb and place the executable in `InfluxData/influxdb`.
Next, set up your virtual environment:
```bash
cd device-identifier && \
python3.8 -m venv .venv && \
source .venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt && \
pip install -e . && \
```

Now you can use the deviceidentifier, e.g. `shbdeviceidentifier -d start`.

## Requirements
All OSs
- Python 3.8 including distutils
- Packages from `device-identifier/requirements.txt`
- node with npm
- optional: 
  - make
  - protoc: if you want to compile the proto files, e.g., after you made changes or added grpc services
    - Download from Github for newest version

## Build from source
Having done the steps under [electron-app](#electron-app) and [device-identifier](#device-identifier), you can build the application from source.
```bash
cd device-identifier && \
source .venv/bin/activate && \
pip install pyinstaller && \
pyinstaller device_identifier_server.py &&\
cd ../electron-app && \
npm run make
```

## GRPC
- Add new `proto` files to `proto/shbdeviceidentifier/rpc/proto`. You can compile and place them in the correct folders automagically using `proto/compile_proto.sh`. Really, just use the script.
- You can test the running server from the command line usind [grpcurl](https://github.com/fullstorydev/grpcurl): `./grpcurl --plaintext localhost:8090 list`
- RPC example: `./grpcurl -v -d '{"file_path": "/home/jo/git/SmartHomeBuddy/device-identifier/shbdeviceidentifier/pcaps/dummy.pcap", "file_type": "pcap"}' -plaintext localhost:8090 SmartHomeBuddy.PcapDatabase/LoadPcapIntoDatabase`

## Additional Info
- If you want to check if you have orphaned python processes running, run `pgrep -f 'shbdeviceidentifier start'`. To kill them, use `pkill`instead of `pgrep`.