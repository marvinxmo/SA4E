import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc

class GreeterServicer(example_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # The actual implementation of the service method
        return example_pb2.HelloReply(message=f"Hello, {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50051")  # Bind to port 50051
    server.start()
    print("Server is running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()