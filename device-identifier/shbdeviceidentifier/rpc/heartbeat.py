import logging

from rpc.proto.heartbeat_pb2_grpc import HeartbeatServicer


class HeartbeatServicer(HeartbeatServicer):
    def send_heartbeat(self, request, context) -> None:
        logging.info("Python Server got a response.")
