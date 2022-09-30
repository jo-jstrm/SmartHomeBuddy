from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger

import shbdeviceidentifier.commands as commands
from .proto import devices_database_pb2_grpc, devices_database_pb2
from .proto import heartbeat_pb2_grpc, heartbeat_pb2
from .proto import read_pb2_grpc, read_pb2
from ..db import Database


class DeviceDatabaseService(devices_database_pb2_grpc.DevicesDatabaseServicer):
    def IdentifyDevices(
        self, request: devices_database_pb2.IdentifyRequest, context
    ) -> devices_database_pb2.IdentifyResponse:
        logger.debug(
            f"GRPC Server received a IdentifyDevices request: measurement = {request.measurement}, model = {request.classifier_model}"
        )
        res = commands.identify_devices(Database(), request.measurement, request.classifier_model)
        logger.debug("Processed IdentifyDevices request.")
        return devices_database_pb2.IdentifyResponse()


class HeartbeatService(heartbeat_pb2_grpc.HeartbeatServicer):
    def GetHeartbeat(self, request: heartbeat_pb2.HeartbeatRequest, context) -> heartbeat_pb2.HeartbeatResponse:
        logger.debug("GRPC Server received a heartbeat request.")
        return heartbeat_pb2.HeartbeatResponse(alive=True)


class ReadService(read_pb2_grpc.ReadServiceServicer):
    def Read(self, request: read_pb2.ReadRequest, context) -> read_pb2.ReadResponse:
        logger.debug(f"GRPC Server received a read request.")
        file_type = request.capture_file_path.split(".")[-1]
        logger.debug(f"Capture file path: {request.capture_file_path}")
        commands.read(Database(), request.capture_file_path, file_type, measurement=request.measurement)
        logger.debug("Processed read request.")
        return read_pb2.ReadResponse()


def start_rpc_server():
    port = 8090
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    devices_database_pb2_grpc.add_DevicesDatabaseServicer_to_server(DeviceDatabaseService(), server)
    heartbeat_pb2_grpc.add_HeartbeatServicer_to_server(HeartbeatService(), server)
    read_pb2_grpc.add_ReadServiceServicer_to_server(ReadService(), server)
    service_names = (
        devices_database_pb2.DESCRIPTOR.services_by_name["DevicesDatabase"].full_name,
        heartbeat_pb2.DESCRIPTOR.services_by_name["Heartbeat"].full_name,
        read_pb2.DESCRIPTOR.services_by_name["ReadService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    logger.success("RPC server started. Press Ctrl+C to stop.")
    logger.debug(f"Server listening on port {port}.")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
