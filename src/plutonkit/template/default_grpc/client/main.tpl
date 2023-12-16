import sys
sys.path.insert(0,'../server/proto')
import test_pb2_grpc
import test_pb2
import logging
import grpc

def health(stub):
   feature = stub.health(test_pb2.HealthRequest(title="title"))
   print(feature)
def run():
   # NOTE(gRPC Python Team): .close() is possible on a channel and should be
   # used in circumstances in which the with statement does not fit the needs
   # of the code.
   with grpc.insecure_channel("localhost:50051") as channel:
      stub = test_pb2_grpc.TestStub(channel)
      print("-------------- health --------------")
      health(stub)



if __name__ == "__main__":
   logging.basicConfig()
   run()
