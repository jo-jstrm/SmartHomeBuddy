// GENERATED CODE -- DO NOT EDIT!

// package: SmartHomeBuddy
// file: devices_database.proto

import * as devices_database_pb from "./devices_database_pb";
import * as grpc from "@grpc/grpc-js";

interface IDevicesDatabaseService
  extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
  identifyDevices: grpc.MethodDefinition<
    devices_database_pb.IdentifyRequest,
    devices_database_pb.IdentifyResponse
  >;
}

export const DevicesDatabaseService: IDevicesDatabaseService;

export interface IDevicesDatabaseServer
  extends grpc.UntypedServiceImplementation {
  identifyDevices: grpc.handleUnaryCall<
    devices_database_pb.IdentifyRequest,
    devices_database_pb.IdentifyResponse
  >;
}

export class DevicesDatabaseClient extends grpc.Client {
  constructor(
    address: string,
    credentials: grpc.ChannelCredentials,
    options?: object
  );
  identifyDevices(
    argument: devices_database_pb.IdentifyRequest,
    callback: grpc.requestCallback<devices_database_pb.IdentifyResponse>
  ): grpc.ClientUnaryCall;
  identifyDevices(
    argument: devices_database_pb.IdentifyRequest,
    metadataOrOptions: grpc.Metadata | grpc.CallOptions | null,
    callback: grpc.requestCallback<devices_database_pb.IdentifyResponse>
  ): grpc.ClientUnaryCall;
  identifyDevices(
    argument: devices_database_pb.IdentifyRequest,
    metadata: grpc.Metadata | null,
    options: grpc.CallOptions | null,
    callback: grpc.requestCallback<devices_database_pb.IdentifyResponse>
  ): grpc.ClientUnaryCall;
}
