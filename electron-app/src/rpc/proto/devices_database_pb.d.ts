// package: SmartHomeBuddy
// file: devices_database.proto

import * as jspb from "google-protobuf";

export class ClassifyRequest extends jspb.Message {
  getParam(): string;
  setParam(value: string): void;

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
    param: string,
  }
}

export class ClassifyResponse extends jspb.Message {
  getIsDone(): boolean;
  setIsDone(value: boolean): void;

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
    isDone: boolean,
  }
}

export class DevicesRequest extends jspb.Message {
  getParam(): string;
  setParam(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DevicesRequest.AsObject;
  static toObject(includeInstance: boolean, msg: DevicesRequest): DevicesRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: DevicesRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DevicesRequest;
  static deserializeBinaryFromReader(message: DevicesRequest, reader: jspb.BinaryReader): DevicesRequest;
}

export namespace DevicesRequest {
  export type AsObject = {
    param: string,
  }
}

export class Device extends jspb.Message {
  getName(): string;
  setName(value: string): void;

  getMacAddress(): string;
  setMacAddress(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Device.AsObject;
  static toObject(includeInstance: boolean, msg: Device): Device.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Device, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Device;
  static deserializeBinaryFromReader(message: Device, reader: jspb.BinaryReader): Device;
}

export namespace Device {
  export type AsObject = {
    name: string,
    macAddress: string,
  }
}

export class Devices extends jspb.Message {
  clearDevicesList(): void;
  getDevicesList(): Array<Device>;
  setDevicesList(value: Array<Device>): void;
  addDevices(value?: Device, index?: number): Device;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Devices.AsObject;
  static toObject(includeInstance: boolean, msg: Devices): Devices.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Devices, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Devices;
  static deserializeBinaryFromReader(message: Devices, reader: jspb.BinaryReader): Devices;
}

export namespace Devices {
  export type AsObject = {
    devicesList: Array<Device.AsObject>,
  }
}

