import grpc
import example_pb2
import example_pb2_grpc

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = example_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(example_pb2.HelloRequest(name="Alice"))
        print(f"Server response: {response.message}")

if __name__ == "__main__":
    run()