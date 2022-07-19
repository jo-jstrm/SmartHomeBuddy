#!/bin/bash
# All relative to electron-app/
export SRC_DIR=../proto
export TS_DST_DIR=./src/proto
export PY_DST_DIR=../device-identifier/smarthomebuddy/proto

if [ $(basename "$(pwd)") = "SmartHomeBuddy" ]; then
  export CD_DIR=electron-app
elif [ $(basename "$(pwd)") = "electron-app" ]; then
  export CD_DIR=.
elif [ $(basename "$(pwd)") = "device-identifier" ] || [ $(basename "$(pwd)") = "proto" ]; then
  export CD_DIR=../electron-app
else
  echo "Please only execute this script from the project folder."
  exit 1
fi

cd $CD_DIR
# Install with `sudo apt install protobuf-compiler`
protoc -I=$SRC_DIR --python_out=$PY_DST_DIR $SRC_DIR/heartbeat.proto
# Must cd to electron-app due to node packages
# Install with `cd electron-app && npm install`
npx protoc --ts_out $TS_DST_DIR --proto_path $SRC_DIR $SRC_DIR/heartbeat.proto