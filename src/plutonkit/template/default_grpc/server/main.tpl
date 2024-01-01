import sys

APPS = [
    './proto',
    './service',
    './utils'
]
for value in APPS:
    sys.path.append(value)

from settings import ROUTES
import logging
import grpc
from concurrent import futures


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    for value in ROUTES:
        value['server'](value['service'](),server)

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
