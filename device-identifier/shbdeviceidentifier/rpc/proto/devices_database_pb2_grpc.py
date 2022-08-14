# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from shbdeviceidentifier.rpc.proto import devices_database_pb2 as shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2


class DevicesDatabaseStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ClassifyDevices = channel.unary_unary(
        '/SmartHomeBuddy.DevicesDatabase/ClassifyDevices',
        request_serializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.ClassifyRequest.SerializeToString,
        response_deserializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.ClassifyResponse.FromString,
        )
    self.GetAllDevices = channel.unary_unary(
        '/SmartHomeBuddy.DevicesDatabase/GetAllDevices',
        request_serializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.DevicesRequest.SerializeToString,
        response_deserializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.Devices.FromString,
        )


class DevicesDatabaseServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ClassifyDevices(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetAllDevices(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DevicesDatabaseServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ClassifyDevices': grpc.unary_unary_rpc_method_handler(
          servicer.ClassifyDevices,
          request_deserializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.ClassifyRequest.FromString,
          response_serializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.ClassifyResponse.SerializeToString,
      ),
      'GetAllDevices': grpc.unary_unary_rpc_method_handler(
          servicer.GetAllDevices,
          request_deserializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.DevicesRequest.FromString,
          response_serializer=shbdeviceidentifier_dot_rpc_dot_proto_dot_devices__database__pb2.Devices.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'SmartHomeBuddy.DevicesDatabase', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
