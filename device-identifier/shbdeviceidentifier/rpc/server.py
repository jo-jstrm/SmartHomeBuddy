import grpc
from concurrent import futures
from .proto.heartbeat_pb2_grpc import HeartbeatServicer, add_HeartbeatServicer_to_server


def run_rpc_server() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HeartbeatServicer_to_server(HeartbeatServicer(), server)
    server.add_insecure_port("[::]:8090")
    server.start()
    server.wait_for_termination()
