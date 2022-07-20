import logging

import rpc.proto.heartbeat_pb2_grpc as heartbeat_pb2_grpc
from rpc.proto.heartbeat_pb2 import HeartbeatResponse


class HeartbeatServicer(heartbeat_pb2_grpc.HeartbeatServicer):
    def GetHeartbeat(self, request, context) -> None:
        logging.info("Python Server got a heartbeat request.")
        response = HeartbeatResponse()
        response.alive = True
        return response
