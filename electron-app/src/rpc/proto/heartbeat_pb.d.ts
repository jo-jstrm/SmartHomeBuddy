// package:
// file: heartbeat.proto

import * as jspb from "google-protobuf";

export class HeartbeatRequest extends jspb.Message {
  getCount(): number;
  setCount(value: number): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): HeartbeatRequest.AsObject;
  static toObject(
    includeInstance: boolean,
    msg: HeartbeatRequest
  ): HeartbeatRequest.AsObject;
  static extensions: { [key: number]: jspb.ExtensionFieldInfo<jspb.Message> };
  static extensionsBinary: {
    [key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>;
  };
  static serializeBinaryToWriter(
    message: HeartbeatRequest,
    writer: jspb.BinaryWriter
  ): void;
  static deserializeBinary(bytes: Uint8Array): HeartbeatRequest;
  static deserializeBinaryFromReader(
    message: HeartbeatRequest,
    reader: jspb.BinaryReader
  ): HeartbeatRequest;
}

export namespace HeartbeatRequest {
  export type AsObject = {
    count: number;
  };
}

export class HeartbeatResponse extends jspb.Message {
  getAlive(): boolean;
  setAlive(value: boolean): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): HeartbeatResponse.AsObject;
  static toObject(
    includeInstance: boolean,
    msg: HeartbeatResponse
  ): HeartbeatResponse.AsObject;
  static extensions: { [key: number]: jspb.ExtensionFieldInfo<jspb.Message> };
  static extensionsBinary: {
    [key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>;
  };
  static serializeBinaryToWriter(
    message: HeartbeatResponse,
    writer: jspb.BinaryWriter
  ): void;
  static deserializeBinary(bytes: Uint8Array): HeartbeatResponse;
  static deserializeBinaryFromReader(
    message: HeartbeatResponse,
    reader: jspb.BinaryReader
  ): HeartbeatResponse;
}

export namespace HeartbeatResponse {
  export type AsObject = {
    alive: boolean;
  };
}
