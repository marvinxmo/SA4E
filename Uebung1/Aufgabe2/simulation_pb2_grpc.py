# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import simulation_pb2 as simulation__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in simulation_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ObserverServiceStub(object):
    """Observer service for registration and status updates
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Register = channel.unary_unary(
                '/firefly.ObserverService/Register',
                request_serializer=simulation__pb2.RegistrationRequest.SerializeToString,
                response_deserializer=simulation__pb2.RegistrationResponse.FromString,
                _registered_method=True)
        self.UpdateStatus = channel.unary_unary(
                '/firefly.ObserverService/UpdateStatus',
                request_serializer=simulation__pb2.StatusUpdate.SerializeToString,
                response_deserializer=simulation__pb2.Empty.FromString,
                _registered_method=True)


class ObserverServiceServicer(object):
    """Observer service for registration and status updates
    """

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ObserverServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=simulation__pb2.RegistrationRequest.FromString,
                    response_serializer=simulation__pb2.RegistrationResponse.SerializeToString,
            ),
            'UpdateStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateStatus,
                    request_deserializer=simulation__pb2.StatusUpdate.FromString,
                    response_serializer=simulation__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'firefly.ObserverService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('firefly.ObserverService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ObserverService(object):
    """Observer service for registration and status updates
    """

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/firefly.ObserverService/Register',
            simulation__pb2.RegistrationRequest.SerializeToString,
            simulation__pb2.RegistrationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/firefly.ObserverService/UpdateStatus',
            simulation__pb2.StatusUpdate.SerializeToString,
            simulation__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class FireflyServiceStub(object):
    """Firefly service for neighbor communication
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ReportFlashInterval = channel.unary_unary(
                '/firefly.FireflyService/ReportFlashInterval',
                request_serializer=simulation__pb2.FlashIntervalRequest.SerializeToString,
                response_deserializer=simulation__pb2.Empty.FromString,
                _registered_method=True)
        self.UpdateNeighbors = channel.unary_unary(
                '/firefly.FireflyService/UpdateNeighbors',
                request_serializer=simulation__pb2.NeighborUpdate.SerializeToString,
                response_deserializer=simulation__pb2.Empty.FromString,
                _registered_method=True)


class FireflyServiceServicer(object):
    """Firefly service for neighbor communication
    """

    def ReportFlashInterval(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateNeighbors(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FireflyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ReportFlashInterval': grpc.unary_unary_rpc_method_handler(
                    servicer.ReportFlashInterval,
                    request_deserializer=simulation__pb2.FlashIntervalRequest.FromString,
                    response_serializer=simulation__pb2.Empty.SerializeToString,
            ),
            'UpdateNeighbors': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateNeighbors,
                    request_deserializer=simulation__pb2.NeighborUpdate.FromString,
                    response_serializer=simulation__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'firefly.FireflyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('firefly.FireflyService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class FireflyService(object):
    """Firefly service for neighbor communication
    """

    @staticmethod
    def ReportFlashInterval(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/firefly.FireflyService/ReportFlashInterval',
            simulation__pb2.FlashIntervalRequest.SerializeToString,
            simulation__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateNeighbors(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/firefly.FireflyService/UpdateNeighbors',
            simulation__pb2.NeighborUpdate.SerializeToString,
            simulation__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)