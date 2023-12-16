import sys

import collections

import grpc
sys.path.insert(0,'../server/proto')
import test_pb2_grpc
import test_pb2
import logging
import grpc

class _ClientCallDetails(
        collections.namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    pass

class AuthenticationInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, interceptor_function):
        self._fn = interceptor_function

    def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, iter((request,)), False, False)
        response = continuation(new_details, next(new_request_iterator))
        return postprocess(response) if postprocess else response

def add_authentication(header, value):
    def intercept_call(client_call_details, request_iterator, request_streaming,
                       response_streaming):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append((
            header,
            value,
        ))
        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)
        return client_call_details, request_iterator, None

    return AuthenticationInterceptor(intercept_call)

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
