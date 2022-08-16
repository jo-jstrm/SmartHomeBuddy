// GENERATED CODE -- DO NOT EDIT!

// package: SmartHomeBuddy
// file: devices_database.proto

import * as devices_database_pb from "./devices_database_pb";
import * as grpc from "@grpc/grpc-js";

interface IDevicesDatabaseService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
  classifyDevices: grpc.MethodDefinition<devices_database_pb.ClassifyRequest, devices_database_pb.ClassifyResponse>;
}

export const DevicesDatabaseService: IDevicesDatabaseService;

export interface IDevicesDatabaseServer extends grpc.UntypedServiceImplementation {
  classifyDevices: grpc.handleUnaryCall<devices_database_pb.ClassifyRequest, devices_database_pb.ClassifyResponse>;
}

export class DevicesDatabaseClient extends grpc.Client {
  constructor(address: string, credentials: grpc.ChannelCredentials, options?: object);
  classifyDevices(argument: devices_database_pb.ClassifyRequest, callback: grpc.requestCallback<devices_database_pb.ClassifyResponse>): grpc.ClientUnaryCall;
  classifyDevices(argument: devices_database_pb.ClassifyRequest, metadataOrOptions: grpc.Metadata | grpc.CallOptions | null, callback: grpc.requestCallback<devices_database_pb.ClassifyResponse>): grpc.ClientUnaryCall;
  classifyDevices(argument: devices_database_pb.ClassifyRequest, metadata: grpc.Metadata | null, options: grpc.CallOptions | null, callback: grpc.requestCallback<devices_database_pb.ClassifyResponse>): grpc.ClientUnaryCall;
}
