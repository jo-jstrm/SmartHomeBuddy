#!/bin/bash
# All relative to electron-app/, because we always start at SmartHomeBuddy/proto
export PY_SRC_DIR=shbdeviceidentifier/rpc/proto
export PY_DST_DIR=../device-identifier/$PY_SRC_DIR
export TS_SRC_DIR=../proto/$PY_SRC_DIR
export TS_DST_DIR=src/proto
export VENV_DIR=../device-identifier/.venv/bin/activate
export TS_CD_PATH=../electron-app

# Make the script work from within the most common dirs
if [ $(basename "$(pwd)") = "SmartHomeBuddy" ]; then
  export PY_CD_PATH=proto
elif [ $(basename "$(pwd)") = "proto" ]; then
  export PY_CD_PATH=.
elif [ $(basename "$(pwd)") = "device-identifier" ] || [ $(basename "$(pwd)") = "electron-app" ]; then
  export PY_CD_PATH=../proto
else
  echo "Please only execute this script from the project folder."
  exit 1
fi

cd $PY_CD_PATH || exit 1
# Install protoc with `sudo apt install protobuf-compiler`.
# Install grpcio-tools in your python venv.
echo "Generating Python scripts..."
source $VENV_DIR
# The Python auto-generation is a bit quirky regarding the auto generated import statements.
# See https://github.com/grpc/grpc/issues/9575 for details.
python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. $PY_SRC_DIR/*.proto
mv $PY_SRC_DIR/*.py $PY_DST_DIR
echo "Generating Typescript scripts..."
cd $TS_CD_PATH || exit 1
# Must cd to electron-app due to node packages
# Install with `cd electron-app && npm install`
npx protoc --ts_out $TS_DST_DIR --proto_path $TS_SRC_DIR $TS_SRC_DIR/*.proto