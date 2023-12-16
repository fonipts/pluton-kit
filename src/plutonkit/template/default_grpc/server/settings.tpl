from proto import test_pb2_grpc
from service.test_server import TestServicer

ROUTES = [{
    "server":test_pb2_grpc.add_TestServicer_to_server,
    "service":TestServicer
}]


