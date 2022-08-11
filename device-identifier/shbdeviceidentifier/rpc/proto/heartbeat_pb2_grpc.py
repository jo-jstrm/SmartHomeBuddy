# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from shbdeviceidentifier.rpc.proto import heartbeat_pb2 as shbdeviceidentifier_dot_rpc_dot_proto_dot_heartbeat__pb2


class HeartbeatStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetHeartbeat = channel.unary_unary(
        '/Heartbeat/GetHeartbeat',
        request_serializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_heartbeat__pb2.HeartbeatRequest.SerializeToString,
        response_deserializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_heartbeat__pb2.HeartbeatResponse.FromString,
        )


class HeartbeatServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetHeartbeat(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_HeartbeatServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetHeartbeat': grpc.unary_unary_rpc_method_handler(
          servicer.GetHeartbeat,
          request_deserializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_heartbeat__pb2.HeartbeatRequest.FromString,
          response_serializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_heartbeat__pb2.HeartbeatResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Heartbeat', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
