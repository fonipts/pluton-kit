from proto import test_pb2_grpc
from proto import test_pb2

class TestServicer(test_pb2_grpc.TestServicer):
    def __init__(self):
        pass
    def health(self,request, context):
        return test_pb2.HealthResponse(title="title")
