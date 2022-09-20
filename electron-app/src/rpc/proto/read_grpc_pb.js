// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var read_pb = require('./read_pb.js');

function serialize_SmartHomeBuddy_ReadRequest(arg) {
  if (!(arg instanceof read_pb.ReadRequest)) {
    throw new Error('Expected argument of type SmartHomeBuddy.ReadRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_ReadRequest(buffer_arg) {
  return read_pb.ReadRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_SmartHomeBuddy_ReadResponse(arg) {
  if (!(arg instanceof read_pb.ReadResponse)) {
    throw new Error('Expected argument of type SmartHomeBuddy.ReadResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_ReadResponse(buffer_arg) {
  return read_pb.ReadResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_SmartHomeBuddy_UpdateReadStatusRequest(arg) {
  if (!(arg instanceof read_pb.UpdateReadStatusRequest)) {
    throw new Error('Expected argument of type SmartHomeBuddy.UpdateReadStatusRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_UpdateReadStatusRequest(buffer_arg) {
  return read_pb.UpdateReadStatusRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_SmartHomeBuddy_UpdateReadStatusResponse(arg) {
  if (!(arg instanceof read_pb.UpdateReadStatusResponse)) {
    throw new Error('Expected argument of type SmartHomeBuddy.UpdateReadStatusResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_UpdateReadStatusResponse(buffer_arg) {
  return read_pb.UpdateReadStatusResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var ReadServiceService = exports.ReadServiceService = {
  read: {
    path: '/SmartHomeBuddy.ReadService/Read',
    requestStream: false,
    responseStream: false,
    requestType: read_pb.ReadRequest,
    responseType: read_pb.ReadResponse,
    requestSerialize: serialize_SmartHomeBuddy_ReadRequest,
    requestDeserialize: deserialize_SmartHomeBuddy_ReadRequest,
    responseSerialize: serialize_SmartHomeBuddy_ReadResponse,
    responseDeserialize: deserialize_SmartHomeBuddy_ReadResponse,
  },
  updateReadStatus: {
    path: '/SmartHomeBuddy.ReadService/UpdateReadStatus',
    requestStream: false,
    responseStream: false,
    requestType: read_pb.UpdateReadStatusRequest,
    responseType: read_pb.UpdateReadStatusResponse,
    requestSerialize: serialize_SmartHomeBuddy_UpdateReadStatusRequest,
    requestDeserialize: deserialize_SmartHomeBuddy_UpdateReadStatusRequest,
    responseSerialize: serialize_SmartHomeBuddy_UpdateReadStatusResponse,
    responseDeserialize: deserialize_SmartHomeBuddy_UpdateReadStatusResponse,
  },
};

exports.ReadServiceClient = grpc.makeGenericClientConstructor(ReadServiceService);
