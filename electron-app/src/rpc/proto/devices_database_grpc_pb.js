// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var devices_database_pb = require('./devices_database_pb.js');

function serialize_SmartHomeBuddy_IdentifyRequest(arg) {
  if (!(arg instanceof devices_database_pb.IdentifyRequest)) {
    throw new Error('Expected argument of type SmartHomeBuddy.IdentifyRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_IdentifyRequest(buffer_arg) {
  return devices_database_pb.IdentifyRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_SmartHomeBuddy_IdentifyResponse(arg) {
  if (!(arg instanceof devices_database_pb.IdentifyResponse)) {
    throw new Error('Expected argument of type SmartHomeBuddy.IdentifyResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_IdentifyResponse(buffer_arg) {
  return devices_database_pb.IdentifyResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var DevicesDatabaseService = exports.DevicesDatabaseService = {
  identifyDevices: {
    path: '/SmartHomeBuddy.DevicesDatabase/IdentifyDevices',
    requestStream: false,
    responseStream: false,
    requestType: devices_database_pb.IdentifyRequest,
    responseType: devices_database_pb.IdentifyResponse,
    requestSerialize: serialize_SmartHomeBuddy_IdentifyRequest,
    requestDeserialize: deserialize_SmartHomeBuddy_IdentifyRequest,
    responseSerialize: serialize_SmartHomeBuddy_IdentifyResponse,
    responseDeserialize: deserialize_SmartHomeBuddy_IdentifyResponse,
  },
};

exports.DevicesDatabaseClient = grpc.makeGenericClientConstructor(DevicesDatabaseService);
