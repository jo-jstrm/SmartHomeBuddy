// import * as grpc from "@grpc/grpc-js";
import { ChannelCredentials, ServiceError } from "@grpc/grpc-js";
import { config } from "../../config"
import { HeartbeatRequest, HeartbeatResponse } from "../proto/heartbeat_pb";
import { HeartbeatClient } from "../proto/heartbeat_grpc_pb";

export function callHeartbeatService(): Promise<any> {
  const client = new HeartbeatClient(
    config.grpc.server_url,
    ChannelCredentials.createInsecure()
  );
  const heartbeatRequest = new HeartbeatRequest();
  return new Promise<boolean>((accept, reject) => {
    client.getHeartbeat(
      heartbeatRequest,
      (err: ServiceError | null, response: HeartbeatResponse | undefined) => {
        if (response) console.log("Response: ", response.toString());
        if (err) console.log("Error: ", err.toString());
        if (!err) {
          console.log(
            "Device identifier's heartbeat server is healthy.\n"
          );
          accept(true);
        } else {
          console.log(
            "Received an error from device identifier's heartbeat service.\n",
            err
          );
          reject(false);
        }
      }
    );
  });
}
