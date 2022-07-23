// import * as grpc from "@grpc/grpc-js";
import {ChannelCredentials, ServiceError} from "@grpc/grpc-js";
import {HeartbeatRequest, HeartbeatResponse} from "./proto/heartbeat_pb";
import {HeartbeatClient} from "./proto/heartbeat_grpc_pb";

export function callHeartbeatServer(): Promise<any> {
    const client = new HeartbeatClient(
        "localhost:8090",
        ChannelCredentials.createInsecure()
    );
    const heartbeatRequest = new HeartbeatRequest();
    heartbeatRequest.setCount(1);
    return new Promise<boolean>((accept, reject) => {
        client.getHeartbeat(heartbeatRequest, (err: ServiceError | null, response: HeartbeatResponse | undefined) => {
                if (response) console.log("Response: ", response.toString())
                if (err) console.log("Error: ", err.toString())
                if (!err) {
                    console.log("Device identifier's heartbeat server is healthy.\n", err);
                    accept(true);
                } else {
                    console.log("Received an error from device identifier's heartbeat server.\n", err);
                    reject(false);
                }
            }
        );
    });
}