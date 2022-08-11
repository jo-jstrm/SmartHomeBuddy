import click
import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from loguru import logger

import shbdeviceidentifier.app as app
from .proto import heartbeat_pb2_grpc, heartbeat_pb2
from .proto import pcap_database_pb2_grpc, pcap_database_pb2


class HeartbeatService(heartbeat_pb2_grpc.HeartbeatServicer):
    def GetHeartbeat(self, request: heartbeat_pb2.HeartbeatRequest, context) -> heartbeat_pb2.HeartbeatResponse:
        logger.info("Python Server got a heartbeat request.")
        return heartbeat_pb2.HeartbeatResponse(alive=True)


class PcapDatabaseService(pcap_database_pb2_grpc.PcapDatabaseServicer):
    def LoadPcapIntoDatabase(
        self, request: pcap_database_pb2.DbLoadRequest, context
    ) -> pcap_database_pb2.DbLoadResponse:
        logger.info(f"GRPC Server received a request {type(request)} for the Pcap database.")
        app.read(file_path=request.file_path, file_type=request.file_type)
        logger.success("Read packet file and wrote contents to database.")
        return pcap_database_pb2.DbLoadResponse(is_done=True)


def run_rpc_server() -> None:
    port = 8090
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    heartbeat_pb2_grpc.add_HeartbeatServicer_to_server(HeartbeatService(), server)
    pcap_database_pb2_grpc.add_PcapDatabaseServicer_to_server(PcapDatabaseService(), server())
    SERVICE_NAMES = (
        pcap_database_pb2.DESCRIPTOR.services_by_name["PcapDatabase"].full_name,
        heartbeat_pb2.DESCRIPTOR.services_by_name["Heartbeat"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    logger.success("RPC server started. Press Ctrl+C to stop.")
    logger.debug(f"Server listening on port {port}.")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
