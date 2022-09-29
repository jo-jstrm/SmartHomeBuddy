// package: SmartHomeBuddy
// file: devices_database.proto

import * as jspb from "google-protobuf";

export class ClassifyRequest extends jspb.Message {
  getClassifierModel(): string;
  setClassifierModel(value: string): void;

  getMeasurement(): string;
  setMeasurement(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ClassifyRequest.AsObject;
  static toObject(includeInstance: boolean, msg: ClassifyRequest): ClassifyRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: ClassifyRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ClassifyRequest;
  static deserializeBinaryFromReader(message: ClassifyRequest, reader: jspb.BinaryReader): ClassifyRequest;
}

export namespace ClassifyRequest {
  export type AsObject = {
    classifierModel: string,
    measurement: string,
  }
}

export class ClassifyResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ClassifyResponse.AsObject;
  static toObject(includeInstance: boolean, msg: ClassifyResponse): ClassifyResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: ClassifyResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ClassifyResponse;
  static deserializeBinaryFromReader(message: ClassifyResponse, reader: jspb.BinaryReader): ClassifyResponse;
}

export namespace ClassifyResponse {
  export type AsObject = {
    success: boolean,
  }
}

