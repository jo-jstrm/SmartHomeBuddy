// GENERATED CODE -- DO NOT EDIT!

// package:
// file: heartbeat.proto

import * as heartbeat_pb from "./heartbeat_pb";
import * as grpc from "@grpc/grpc-js";

interface IHeartbeatService
  extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
  getHeartbeat: grpc.MethodDefinition<
    heartbeat_pb.HeartbeatRequest,
    heartbeat_pb.HeartbeatResponse
  >;
}

export const HeartbeatService: IHeartbeatService;

export interface IHeartbeatServer extends grpc.UntypedServiceImplementation {
  getHeartbeat: grpc.handleUnaryCall<
    heartbeat_pb.HeartbeatRequest,
    heartbeat_pb.HeartbeatResponse
  >;
}

export class HeartbeatClient extends grpc.Client {
  constructor(
    address: string,
    credentials: grpc.ChannelCredentials,
    options?: object
  );
  getHeartbeat(
    argument: heartbeat_pb.HeartbeatRequest,
    callback: grpc.requestCallback<heartbeat_pb.HeartbeatResponse>
  ): grpc.ClientUnaryCall;
  getHeartbeat(
    argument: heartbeat_pb.HeartbeatRequest,
    metadataOrOptions: grpc.Metadata | grpc.CallOptions | null,
    callback: grpc.requestCallback<heartbeat_pb.HeartbeatResponse>
  ): grpc.ClientUnaryCall;
  getHeartbeat(
    argument: heartbeat_pb.HeartbeatRequest,
    metadata: grpc.Metadata | null,
    options: grpc.CallOptions | null,
    callback: grpc.requestCallback<heartbeat_pb.HeartbeatResponse>
  ): grpc.ClientUnaryCall;
}
