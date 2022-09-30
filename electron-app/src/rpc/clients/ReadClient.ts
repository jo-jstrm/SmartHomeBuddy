import { ChannelCredentials, ServiceError } from "@grpc/grpc-js";
import { ReadRequest, ReadResponse } from "../proto/read_pb";
import { config } from "../../config";
import { ReadServiceClient } from "../proto/read_grpc_pb";

export function callRead(path: string, measurement: string): Promise<boolean> {
  console.log("callRead called.");
  const client = new ReadServiceClient(
    config.grpc.server_url,
    ChannelCredentials.createInsecure()
  );
  let readRequest = new ReadRequest();
  readRequest.setCaptureFilePath(path);
  readRequest.setMeasurement(measurement);
  return new Promise<boolean>((accept, reject) => {
    client.read(
      readRequest,
      (err: ServiceError | null, response: ReadResponse | undefined) => {
        if (response) console.log("Read: server responded.");
        if (err) console.log("Error: ", err.toString());
        if (!err) {
          console.log("Read successful.\n");
          accept(true);
        } else {
          console.log(
            "Read not successful. Received an error from device identifier's ReadService.\n",
            err
          );
          reject(false);
        }
      }
    );
  });
}
