// GENERATED CODE -- DO NOT EDIT!

"use strict";
var grpc = require("@grpc/grpc-js");
var heartbeat_pb = require("./heartbeat_pb.js");

function serialize_SmartHomeBuddy_HeartbeatRequest(arg) {
  if (!(arg instanceof heartbeat_pb.HeartbeatRequest)) {
    throw new Error(
      "Expected argument of type SmartHomeBuddy.HeartbeatRequest"
    );
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_HeartbeatRequest(buffer_arg) {
  return heartbeat_pb.HeartbeatRequest.deserializeBinary(
    new Uint8Array(buffer_arg)
  );
}

function serialize_SmartHomeBuddy_HeartbeatResponse(arg) {
  if (!(arg instanceof heartbeat_pb.HeartbeatResponse)) {
    throw new Error(
      "Expected argument of type SmartHomeBuddy.HeartbeatResponse"
    );
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_HeartbeatResponse(buffer_arg) {
  return heartbeat_pb.HeartbeatResponse.deserializeBinary(
    new Uint8Array(buffer_arg)
  );
}

var HeartbeatService = (exports.HeartbeatService = {
  getHeartbeat: {
    path: "/SmartHomeBuddy.Heartbeat/GetHeartbeat",
    requestStream: false,
    responseStream: false,
    requestType: heartbeat_pb.HeartbeatRequest,
    responseType: heartbeat_pb.HeartbeatResponse,
    requestSerialize: serialize_SmartHomeBuddy_HeartbeatRequest,
    requestDeserialize: deserialize_SmartHomeBuddy_HeartbeatRequest,
    responseSerialize: serialize_SmartHomeBuddy_HeartbeatResponse,
    responseDeserialize: deserialize_SmartHomeBuddy_HeartbeatResponse,
  },
});

exports.HeartbeatClient = grpc.makeGenericClientConstructor(HeartbeatService);
