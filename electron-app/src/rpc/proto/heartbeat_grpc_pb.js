// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var heartbeat_pb = require('./heartbeat_pb.js');

function serialize_HeartbeatRequest(arg) {
  if (!(arg instanceof heartbeat_pb.HeartbeatRequest)) {
    throw new Error('Expected argument of type HeartbeatRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_HeartbeatRequest(buffer_arg) {
  return heartbeat_pb.HeartbeatRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_HeartbeatResponse(arg) {
  if (!(arg instanceof heartbeat_pb.HeartbeatResponse)) {
    throw new Error('Expected argument of type HeartbeatResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_HeartbeatResponse(buffer_arg) {
  return heartbeat_pb.HeartbeatResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var HeartbeatService = exports.HeartbeatService = {
  getHeartbeat: {
    path: '/Heartbeat/GetHeartbeat',
    requestStream: false,
    responseStream: false,
    requestType: heartbeat_pb.HeartbeatRequest,
    responseType: heartbeat_pb.HeartbeatResponse,
    requestSerialize: serialize_HeartbeatRequest,
    requestDeserialize: deserialize_HeartbeatRequest,
    responseSerialize: serialize_HeartbeatResponse,
    responseDeserialize: deserialize_HeartbeatResponse,
  },
};

exports.HeartbeatClient = grpc.makeGenericClientConstructor(HeartbeatService);
