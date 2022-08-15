// GENERATED CODE -- DO NOT EDIT!

"use strict";
var grpc = require("@grpc/grpc-js");
var devices_database_pb = require("./devices_database_pb.js");

function serialize_SmartHomeBuddy_ClassifyRequest(arg) {
  if (!(arg instanceof devices_database_pb.ClassifyRequest)) {
    throw new Error("Expected argument of type SmartHomeBuddy.ClassifyRequest");
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_ClassifyRequest(buffer_arg) {
  return devices_database_pb.ClassifyRequest.deserializeBinary(
    new Uint8Array(buffer_arg)
  );
}

function serialize_SmartHomeBuddy_ClassifyResponse(arg) {
  if (!(arg instanceof devices_database_pb.ClassifyResponse)) {
    throw new Error(
      "Expected argument of type SmartHomeBuddy.ClassifyResponse"
    );
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_ClassifyResponse(buffer_arg) {
  return devices_database_pb.ClassifyResponse.deserializeBinary(
    new Uint8Array(buffer_arg)
  );
}

function serialize_SmartHomeBuddy_Devices(arg) {
  if (!(arg instanceof devices_database_pb.Devices)) {
    throw new Error("Expected argument of type SmartHomeBuddy.Devices");
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_Devices(buffer_arg) {
  return devices_database_pb.Devices.deserializeBinary(
    new Uint8Array(buffer_arg)
  );
}

function serialize_SmartHomeBuddy_DevicesRequest(arg) {
  if (!(arg instanceof devices_database_pb.DevicesRequest)) {
    throw new Error("Expected argument of type SmartHomeBuddy.DevicesRequest");
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SmartHomeBuddy_DevicesRequest(buffer_arg) {
  return devices_database_pb.DevicesRequest.deserializeBinary(
    new Uint8Array(buffer_arg)
  );
}

var DevicesDatabaseService = (exports.DevicesDatabaseService = {
  classifyDevices: {
    path: "/SmartHomeBuddy.DevicesDatabase/ClassifyDevices",
    requestStream: false,
    responseStream: false,
    requestType: devices_database_pb.ClassifyRequest,
    responseType: devices_database_pb.ClassifyResponse,
    requestSerialize: serialize_SmartHomeBuddy_ClassifyRequest,
    requestDeserialize: deserialize_SmartHomeBuddy_ClassifyRequest,
    responseSerialize: serialize_SmartHomeBuddy_ClassifyResponse,
    responseDeserialize: deserialize_SmartHomeBuddy_ClassifyResponse,
  },
  getAllDevices: {
    path: "/SmartHomeBuddy.DevicesDatabase/GetAllDevices",
    requestStream: false,
    responseStream: false,
    requestType: devices_database_pb.DevicesRequest,
    responseType: devices_database_pb.Devices,
    requestSerialize: serialize_SmartHomeBuddy_DevicesRequest,
    requestDeserialize: deserialize_SmartHomeBuddy_DevicesRequest,
    responseSerialize: serialize_SmartHomeBuddy_Devices,
    responseDeserialize: deserialize_SmartHomeBuddy_Devices,
  },
});

exports.DevicesDatabaseClient = grpc.makeGenericClientConstructor(
  DevicesDatabaseService
);
