import grpc

from . import config
from .proto import read_pb2_grpc, read_pb2


class ReadUpdateClient:
    def __init__(self):
        self.host = "localhost"
        self.port = config.PYTHON_SERVER_PORT
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.stub = read_pb2_grpc.ReadServiceStub(self.channel)

    def send_update(self, progress: int):
        """Send a progress update to the server.

        Parameters
        ----------
        update : int
            Progress in percent.
        """
        update_msg = read_pb2.UpdatedReadStatusMsg(value=progress)
        self.stub.UpdateReadStatus(update_msg)
