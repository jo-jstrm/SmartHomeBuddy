// package: 
// file: pcap_database.proto

import * as jspb from "google-protobuf";

export class DbLoadRequest extends jspb.Message {
  getFilePath(): string;
  setFilePath(value: string): void;

  getFileType(): string;
  setFileType(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DbLoadRequest.AsObject;
  static toObject(includeInstance: boolean, msg: DbLoadRequest): DbLoadRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: DbLoadRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DbLoadRequest;
  static deserializeBinaryFromReader(message: DbLoadRequest, reader: jspb.BinaryReader): DbLoadRequest;
}

export namespace DbLoadRequest {
  export type AsObject = {
    filePath: string,
    fileType: string,
  }
}

export class DbLoadResponse extends jspb.Message {
  getIsDone(): boolean;
  setIsDone(value: boolean): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DbLoadResponse.AsObject;
  static toObject(includeInstance: boolean, msg: DbLoadResponse): DbLoadResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: DbLoadResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DbLoadResponse;
  static deserializeBinaryFromReader(message: DbLoadResponse, reader: jspb.BinaryReader): DbLoadResponse;
}

export namespace DbLoadResponse {
  export type AsObject = {
    isDone: boolean,
  }
}

