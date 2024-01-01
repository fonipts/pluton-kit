import sys

APPS = [
    './proto',
    './service',
    './utils'
]
for value in APPS:
    sys.path.append(value)

import logging
import grpc
from concurrent import futures
from utils.interceptor import AuthenticationInterceptor

from settings import ROUTES


authenticator = AuthenticationInterceptor(
        'authorization',
        '42',
        grpc.StatusCode.UNAUTHENTICATED,
        'Access denied!'
    )
       
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=(authenticator,))

    for value in ROUTES:
        value['server'](value['service'](),server)

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
