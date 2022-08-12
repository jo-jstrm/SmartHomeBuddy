import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from loguru import logger

import shbdeviceidentifier.commands as commands
from ..utilities.ml_utilities import classify_devices
from ..db import Database
from .proto import devices_database_pb2_grpc, devices_database_pb2
from .proto import heartbeat_pb2_grpc, heartbeat_pb2
from .proto import pcap_database_pb2_grpc, pcap_database_pb2


class DeviceDatabaseService(devices_database_pb2_grpc.DevicesDatabaseServicer):
    def ClassifyDevices(
        self, request: devices_database_pb2.ClassifyRequest, context
    ) -> devices_database_pb2.ClassifyResponse:
        logger.debug("GRPC Server received a ClassifyDevices request.")
        classify_devices(Database())
        logger.debug("Processed ClassifyDevices request.")
        return devices_database_pb2.ClassifyResponse()


class HeartbeatService(heartbeat_pb2_grpc.HeartbeatServicer):
    def GetHeartbeat(self, request: heartbeat_pb2.HeartbeatRequest, context) -> heartbeat_pb2.HeartbeatResponse:
        logger.debug("GRPC Server received a heartbeat request.")
        return heartbeat_pb2.HeartbeatResponse(alive=True)


class PcapDatabaseService(pcap_database_pb2_grpc.PcapDatabaseServicer):
    def LoadPcapIntoDatabase(
        self, request: pcap_database_pb2.DbLoadRequest, context
    ) -> pcap_database_pb2.DbLoadResponse:
        logger.debug(f"GRPC Server received a {type(request)} for the Pcap database.")
        commands.read(Database(), request.file_path, request.file_type)
        logger.debug("Processed LoadPcapIntoDatabase request.")
        return pcap_database_pb2.DbLoadResponse(is_done=True)


def run_rpc_server():
    port = 8090
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    devices_database_pb2_grpc.add_DevicesDatabaseServicer_to_server(DeviceDatabaseService(), server)
    heartbeat_pb2_grpc.add_HeartbeatServicer_to_server(HeartbeatService(), server)
    pcap_database_pb2_grpc.add_PcapDatabaseServicer_to_server(PcapDatabaseService(), server)
    service_names = (
        devices_database_pb2.DESCRIPTOR.services_by_name["DevicesDatabase"].full_name,
        pcap_database_pb2.DESCRIPTOR.services_by_name["PcapDatabase"].full_name,
        heartbeat_pb2.DESCRIPTOR.services_by_name["Heartbeat"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    logger.success("RPC server started. Press Ctrl+C to stop.")
    logger.debug(f"Server listening on port {port}.")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
