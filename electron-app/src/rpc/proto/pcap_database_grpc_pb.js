// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var pcap_database_pb = require('./pcap_database_pb.js');

function serialize_DbLoadRequest(arg) {
  if (!(arg instanceof pcap_database_pb.DbLoadRequest)) {
    throw new Error('Expected argument of type DbLoadRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_DbLoadRequest(buffer_arg) {
  return pcap_database_pb.DbLoadRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_DbLoadResponse(arg) {
  if (!(arg instanceof pcap_database_pb.DbLoadResponse)) {
    throw new Error('Expected argument of type DbLoadResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_DbLoadResponse(buffer_arg) {
  return pcap_database_pb.DbLoadResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var PcapDatabaseService = exports.PcapDatabaseService = {
  loadPcapIntoDatabase: {
    path: '/PcapDatabase/LoadPcapIntoDatabase',
    requestStream: false,
    responseStream: false,
    requestType: pcap_database_pb.DbLoadRequest,
    responseType: pcap_database_pb.DbLoadResponse,
    requestSerialize: serialize_DbLoadRequest,
    requestDeserialize: deserialize_DbLoadRequest,
    responseSerialize: serialize_DbLoadResponse,
    responseDeserialize: deserialize_DbLoadResponse,
  },
};

exports.PcapDatabaseClient = grpc.makeGenericClientConstructor(PcapDatabaseService);
