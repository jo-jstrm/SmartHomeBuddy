import { ChannelCredentials, ServiceError } from "@grpc/grpc-js";
import {
  IdentifyRequest,
  IdentifyResponse,
} from "../proto/devices_database_pb";
import { config } from "../../config";
import { DevicesDatabaseClient } from "../proto/devices_database_grpc_pb";

export function callIdentifyDevices(classifierModel: string, measurement: string): Promise<boolean> {
  const client = new DevicesDatabaseClient(
    config.grpc.server_url,
    ChannelCredentials.createInsecure()
  );
  const identifyRequest = new IdentifyRequest();
  identifyRequest.setClassifierModel(classifierModel);
  identifyRequest.setMeasurement(measurement);
  return new Promise<boolean>((accept, reject) => {
    client.identifyDevices(
      identifyRequest,
      (err: ServiceError | null, response: IdentifyResponse | undefined) => {
        if (response) console.log("Response: ", response.toString());
        if (err) console.log("Error: ", err.toString());
        if (!err) {
          console.log("Device identification done.\n");
          accept(true);
        } else {
          console.log(
            "Received an error from device identifier's DeviceDatabase service.\n",
            err
          );
          reject(false);
        }
      }
    );
  });
}
