// package: SmartHomeBuddy
// file: devices_database.proto

import * as jspb from "google-protobuf";

export class IdentifyRequest extends jspb.Message {
  getClassifierModel(): string;
  setClassifierModel(value: string): void;

  getMeasurement(): string;
  setMeasurement(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): IdentifyRequest.AsObject;
  static toObject(includeInstance: boolean, msg: IdentifyRequest): IdentifyRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: IdentifyRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): IdentifyRequest;
  static deserializeBinaryFromReader(message: IdentifyRequest, reader: jspb.BinaryReader): IdentifyRequest;
}

export namespace IdentifyRequest {
  export type AsObject = {
    classifierModel: string,
    measurement: string,
  }
}

export class IdentifyResponse extends jspb.Message {
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): IdentifyResponse.AsObject;
  static toObject(includeInstance: boolean, msg: IdentifyResponse): IdentifyResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: IdentifyResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): IdentifyResponse;
  static deserializeBinaryFromReader(message: IdentifyResponse, reader: jspb.BinaryReader): IdentifyResponse;
}

export namespace IdentifyResponse {
  export type AsObject = {
  }
}

