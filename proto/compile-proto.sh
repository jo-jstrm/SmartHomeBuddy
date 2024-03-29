#!/bin/bash

# Prerequisites:
# Install node stuff with `cd electron-app && npm install`
# Install protobuf-compiler
# Install grpcio-tools in your python venv.

# All relative to electron-app/, because we always start at SmartHomeBuddy/proto
export PY_SRC_DIR="shbdeviceidentifier/rpc/proto"
export PY_DST_DIR="../device-identifier/$PY_SRC_DIR"
export TS_SRC_DIR="../proto/$PY_SRC_DIR"
export TS_DST_DIR="src/rpc/proto"
export VENV_DIR="../device-identifier/.venv/bin/activate"
export TS_CD_PATH="../electron-app"

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
echo "Generating Python scripts..."
source $VENV_DIR
# The Python auto-generation is a bit quirky regarding the auto generated import statements.
# See https://github.com/grpc/grpc/issues/9575 for details.
python3 -m grpc_tools.protoc \
              --python_out=. \
              --grpc_python_out=. \
              --proto_path . \
              $PY_SRC_DIR/*.proto
mv $PY_SRC_DIR/*.py $PY_DST_DIR
# Must cd to electron-app due to node packages
cd $TS_CD_PATH || exit 1
echo "Generating Javascript and corresponding Typescript Interfaces..."
npx grpc_tools_node_protoc \
      --proto_path=$TS_SRC_DIR \
      --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
      --plugin=protoc-gen-grpc=./node_modules/.bin/grpc_tools_node_protoc_plugin \
      --js_out=import_style=commonjs:$TS_DST_DIR \
      --ts_out=service=grpc-node,mode=grpc-js:$TS_DST_DIR \
      --grpc_out=grpc_js:$TS_DST_DIR \
      "$TS_SRC_DIR"/*.proto