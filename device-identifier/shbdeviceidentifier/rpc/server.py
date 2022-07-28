from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger

from .proto import heartbeat_pb2_grpc, heartbeat_pb2


class HeartbeatService(heartbeat_pb2_grpc.HeartbeatServicer):
    def GetHeartbeat(self, request, context) -> heartbeat_pb2.HeartbeatResponse:
        logger.info("Python Server got a heartbeat request.")
        response = heartbeat_pb2.HeartbeatResponse(alive=True)
        return response


def run_rpc_server() -> None:
    port = 8090
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    heartbeat_pb2_grpc.add_HeartbeatServicer_to_server(HeartbeatService(), server)
    SERVICE_NAMES = (
        heartbeat_pb2.DESCRIPTOR.services_by_name["Heartbeat"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    logger.info(f"Server listening on port {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
