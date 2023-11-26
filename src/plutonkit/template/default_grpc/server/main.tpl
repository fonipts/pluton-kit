import sys

sys.path.insert(0,'./proto')
from proto import test_pb2_grpc
import test_pb2
import logging
import grpc
from concurrent import futures



class TestServicer(test_pb2_grpc.TestServicer):
    def __init__(self):
        pass
    def health(self,request, context):
        return test_pb2.HealthResponse(title="title")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_TestServicer_to_server(
        TestServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
 
