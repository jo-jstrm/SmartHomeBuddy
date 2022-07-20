// package:
// file: heartbeat.proto

/* tslint:disable */
/* eslint-disable */

import * as grpc from "grpc";
import * as heartbeat_pb from "./heartbeat_pb";

interface IHeartbeatService
  extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
  getHeartbeat: IHeartbeatService_IGetHeartbeat;
}

interface IHeartbeatService_IGetHeartbeat
  extends grpc.MethodDefinition<
    heartbeat_pb.HeartbeatRequest,
    heartbeat_pb.HeartbeatResponse
  > {
  path: "/Heartbeat/GetHeartbeat";
  requestStream: false;
  responseStream: false;
  requestSerialize: grpc.serialize<heartbeat_pb.HeartbeatRequest>;
  requestDeserialize: grpc.deserialize<heartbeat_pb.HeartbeatRequest>;
  responseSerialize: grpc.serialize<heartbeat_pb.HeartbeatResponse>;
  responseDeserialize: grpc.deserialize<heartbeat_pb.HeartbeatResponse>;
}

export const HeartbeatService: IHeartbeatService;

export interface IHeartbeatServer {
  getHeartbeat: grpc.handleUnaryCall<
    heartbeat_pb.HeartbeatRequest,
    heartbeat_pb.HeartbeatResponse
  >;
}

export interface IHeartbeatClient {
  getHeartbeat(
    request: heartbeat_pb.HeartbeatRequest,
    callback: (
      error: grpc.ServiceError | null,
      response: heartbeat_pb.HeartbeatResponse
    ) => void
  ): grpc.ClientUnaryCall;
  getHeartbeat(
    request: heartbeat_pb.HeartbeatRequest,
    metadata: grpc.Metadata,
    callback: (
      error: grpc.ServiceError | null,
      response: heartbeat_pb.HeartbeatResponse
    ) => void
  ): grpc.ClientUnaryCall;
  getHeartbeat(
    request: heartbeat_pb.HeartbeatRequest,
    metadata: grpc.Metadata,
    options: Partial<grpc.CallOptions>,
    callback: (
      error: grpc.ServiceError | null,
      response: heartbeat_pb.HeartbeatResponse
    ) => void
  ): grpc.ClientUnaryCall;
}

export class HeartbeatClient extends grpc.Client implements IHeartbeatClient {
  constructor(
    address: string,
    credentials: grpc.ChannelCredentials,
    options?: object
  );
  public getHeartbeat(
    request: heartbeat_pb.HeartbeatRequest,
    callback: (
      error: grpc.ServiceError | null,
      response: heartbeat_pb.HeartbeatResponse
    ) => void
  ): grpc.ClientUnaryCall;
  public getHeartbeat(
    request: heartbeat_pb.HeartbeatRequest,
    metadata: grpc.Metadata,
    callback: (
      error: grpc.ServiceError | null,
      response: heartbeat_pb.HeartbeatResponse
    ) => void
  ): grpc.ClientUnaryCall;
  public getHeartbeat(
    request: heartbeat_pb.HeartbeatRequest,
    metadata: grpc.Metadata,
    options: Partial<grpc.CallOptions>,
    callback: (
      error: grpc.ServiceError | null,
      response: heartbeat_pb.HeartbeatResponse
    ) => void
  ): grpc.ClientUnaryCall;
}
