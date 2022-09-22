// GENERATED CODE -- DO NOT EDIT!

// package: SmartHomeBuddy
// file: read.proto

import * as read_pb from "./read_pb";
import * as grpc from "@grpc/grpc-js";

interface IReadServiceService
  extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
  read: grpc.MethodDefinition<read_pb.ReadRequest, read_pb.ReadResponse>;
  updateReadStatus: grpc.MethodDefinition<
    read_pb.UpdateReadStatusRequest,
    read_pb.UpdateReadStatusResponse
  >;
}

export const ReadServiceService: IReadServiceService;

export interface IReadServiceServer extends grpc.UntypedServiceImplementation {
  read: grpc.handleUnaryCall<read_pb.ReadRequest, read_pb.ReadResponse>;
  updateReadStatus: grpc.handleUnaryCall<
    read_pb.UpdateReadStatusRequest,
    read_pb.UpdateReadStatusResponse
  >;
}

export class ReadServiceClient extends grpc.Client {
  constructor(
    address: string,
    credentials: grpc.ChannelCredentials,
    options?: object
  );
  read(
    argument: read_pb.ReadRequest,
    callback: grpc.requestCallback<read_pb.ReadResponse>
  ): grpc.ClientUnaryCall;
  read(
    argument: read_pb.ReadRequest,
    metadataOrOptions: grpc.Metadata | grpc.CallOptions | null,
    callback: grpc.requestCallback<read_pb.ReadResponse>
  ): grpc.ClientUnaryCall;
  read(
    argument: read_pb.ReadRequest,
    metadata: grpc.Metadata | null,
    options: grpc.CallOptions | null,
    callback: grpc.requestCallback<read_pb.ReadResponse>
  ): grpc.ClientUnaryCall;
  updateReadStatus(
    argument: read_pb.UpdateReadStatusRequest,
    callback: grpc.requestCallback<read_pb.UpdateReadStatusResponse>
  ): grpc.ClientUnaryCall;
  updateReadStatus(
    argument: read_pb.UpdateReadStatusRequest,
    metadataOrOptions: grpc.Metadata | grpc.CallOptions | null,
    callback: grpc.requestCallback<read_pb.UpdateReadStatusResponse>
  ): grpc.ClientUnaryCall;
  updateReadStatus(
    argument: read_pb.UpdateReadStatusRequest,
    metadata: grpc.Metadata | null,
    options: grpc.CallOptions | null,
    callback: grpc.requestCallback<read_pb.UpdateReadStatusResponse>
  ): grpc.ClientUnaryCall;
}
