import grpc
from concurrent import futures
from .proto.heartbeat_pb2_grpc import HeartbeatServicer, add_HeartbeatServicer_to_server


def run_rpc_server() -> None:
    port = 8090
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HeartbeatServicer_to_server(HeartbeatServicer(), server)
    logging.info(f"Server listening on port {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
