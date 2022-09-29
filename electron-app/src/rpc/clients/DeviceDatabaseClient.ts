import { ChannelCredentials, ServiceError } from "@grpc/grpc-js";
import {
  ClassifyRequest,
  ClassifyResponse,
} from "../proto/devices_database_pb";
import { config } from "../../config";
import { DevicesDatabaseClient } from "../proto/devices_database_grpc_pb";

export function callClassifyDevices(classifierModel: string, measurement: string): Promise<boolean> {
  const client = new DevicesDatabaseClient(
    config.grpc.server_url,
    ChannelCredentials.createInsecure()
  );
  const classifyRequest = new ClassifyRequest();
  classifyRequest.setClassifierModel(classifierModel);
  classifyRequest.setMeasurement(measurement);
  return new Promise<boolean>((accept, reject) => {
    client.classifyDevices(
      classifyRequest,
      (err: ServiceError | null, response: ClassifyResponse | undefined) => {
        if (response) console.log("Response: ", response.toString());
        if (err) console.log("Error: ", err.toString());
        if (!err) {
          console.log("Device classification done.\n");
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
