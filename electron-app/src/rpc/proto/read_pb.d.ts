// package: SmartHomeBuddy
// file: read.proto

import * as jspb from "google-protobuf";

export class ReadRequest extends jspb.Message {
  getCaptureFilePath(): string;
  setCaptureFilePath(value: string): void;

  getMeasurement(): string;
  setMeasurement(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ReadRequest.AsObject;
  static toObject(includeInstance: boolean, msg: ReadRequest): ReadRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: ReadRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ReadRequest;
  static deserializeBinaryFromReader(message: ReadRequest, reader: jspb.BinaryReader): ReadRequest;
}

export namespace ReadRequest {
  export type AsObject = {
    captureFilePath: string,
    measurement: string,
  }
}

export class ReadResponse extends jspb.Message {
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ReadResponse.AsObject;
  static toObject(includeInstance: boolean, msg: ReadResponse): ReadResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: ReadResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ReadResponse;
  static deserializeBinaryFromReader(message: ReadResponse, reader: jspb.BinaryReader): ReadResponse;
}

export namespace ReadResponse {
  export type AsObject = {
  }
}

export class UpdateReadStatusRequest extends jspb.Message {
  getProgress(): number;
  setProgress(value: number): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): UpdateReadStatusRequest.AsObject;
  static toObject(includeInstance: boolean, msg: UpdateReadStatusRequest): UpdateReadStatusRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: UpdateReadStatusRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): UpdateReadStatusRequest;
  static deserializeBinaryFromReader(message: UpdateReadStatusRequest, reader: jspb.BinaryReader): UpdateReadStatusRequest;
}

export namespace UpdateReadStatusRequest {
  export type AsObject = {
    progress: number,
  }
}

export class UpdateReadStatusResponse extends jspb.Message {
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): UpdateReadStatusResponse.AsObject;
  static toObject(includeInstance: boolean, msg: UpdateReadStatusResponse): UpdateReadStatusResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: UpdateReadStatusResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): UpdateReadStatusResponse;
  static deserializeBinaryFromReader(message: UpdateReadStatusResponse, reader: jspb.BinaryReader): UpdateReadStatusResponse;
}

export namespace UpdateReadStatusResponse {
  export type AsObject = {
  }
}

