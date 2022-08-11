// GENERATED CODE -- DO NOT EDIT!

// package: 
// file: pcap_database.proto

import * as pcap_database_pb from "./pcap_database_pb";
import * as grpc from "@grpc/grpc-js";

interface IPcapDatabaseService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
  loadPcapIntoDatabase: grpc.MethodDefinition<pcap_database_pb.DbLoadRequest, pcap_database_pb.DbLoadResponse>;
}

export const PcapDatabaseService: IPcapDatabaseService;

export interface IPcapDatabaseServer extends grpc.UntypedServiceImplementation {
  loadPcapIntoDatabase: grpc.handleUnaryCall<pcap_database_pb.DbLoadRequest, pcap_database_pb.DbLoadResponse>;
}

export class PcapDatabaseClient extends grpc.Client {
  constructor(address: string, credentials: grpc.ChannelCredentials, options?: object);
  loadPcapIntoDatabase(argument: pcap_database_pb.DbLoadRequest, callback: grpc.requestCallback<pcap_database_pb.DbLoadResponse>): grpc.ClientUnaryCall;
  loadPcapIntoDatabase(argument: pcap_database_pb.DbLoadRequest, metadataOrOptions: grpc.Metadata | grpc.CallOptions | null, callback: grpc.requestCallback<pcap_database_pb.DbLoadResponse>): grpc.ClientUnaryCall;
  loadPcapIntoDatabase(argument: pcap_database_pb.DbLoadRequest, metadata: grpc.Metadata | null, options: grpc.CallOptions | null, callback: grpc.requestCallback<pcap_database_pb.DbLoadResponse>): grpc.ClientUnaryCall;
}
