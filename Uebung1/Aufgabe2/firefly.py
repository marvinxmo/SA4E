import grpc
import time
import random
from concurrent import futures
import simulation_pb2
import simulation_pb2_grpc

class FireflyService(simulation_pb2_grpc.FireflyServiceServicer):
    def __init__(self, firefly):
        self.firefly = firefly
        
    def ReportFlashInterval(self, request, context):
        self.firefly.handle_neighbor_interval(request.id, request.flash_interval)
        return simulation_pb2.Empty()
    
    def UpdateNeighbors(self, request, context):
        """Handle neighbor updates from observer"""
        try:
            self.firefly.update_neighbors(request.neighbors)
            return simulation_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to update neighbors: {str(e)}")
            return simulation_pb2.Empty()

class Firefly:
    def __init__(self):
        self.flash_interval = random.uniform(2, 5)
        self.flash_duration = 0.2
        self.adjustment_rate = 0.1
        self.is_lit = False
        self.neighbors = {}  # id -> stub
        self.neighbor_intervals = {}  # id -> interval


        
        # Start server
        self.port = self.find_free_port()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        simulation_pb2_grpc.add_FireflyServiceServicer_to_server(
            FireflyService(self), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        
        # Register with observer
        self.register_with_observer()
        
    def register_with_observer(self):
        channel = grpc.insecure_channel('localhost:50051')
        stub = simulation_pb2_grpc.ObserverServiceStub(channel)
        
        response = stub.Register(simulation_pb2.RegistrationRequest(
            host='localhost',
            port=self.port
        ))
        
        self.id = response.id
        self.observer_start_time = response.start_time
        print(f"Registered with observer as {self.id}")
        
        # Connect to neighbors
        for neighbor in response.neighbors:
            channel = grpc.insecure_channel(f'{neighbor.host}:{neighbor.port}')
            self.neighbors[neighbor.id] = simulation_pb2_grpc.FireflyServiceStub(channel)
    
    def update_neighbors(self, neighbors):

        """Update neighbor connections when receiving new neighbor information"""
        # Clear old connections
        self.neighbors.clear()
        self.neighbor_intervals.clear()
        
        # Create new connections
        for neighbor in neighbors:
            try:
                channel = grpc.insecure_channel(f'{neighbor.host}:{neighbor.port}')
                self.neighbors[neighbor.id] = simulation_pb2_grpc.FireflyServiceStub(channel)
                print(f"Connected to neighbor {neighbor.id}")
            except Exception as e:
                print(f"Failed to connect to neighbor {neighbor.id}: {e}")

    def handle_neighbor_interval(self, neighbor_id, interval):
        """Handle incoming interval update from neighbor"""
        self.neighbor_intervals[neighbor_id] = interval
        self.update_flash_interval()
    
    def update_flash_interval(self):
        """Update own flash interval based on neighbors"""
        if self.neighbor_intervals:
            avg_interval = sum(self.neighbor_intervals.values()) / len(self.neighbor_intervals)
            self.flash_interval += self.adjustment_rate * (avg_interval - self.flash_interval)
            #print(f"Updated interval to {self.flash_interval:.3f} based on {len(self.neighbor_intervals)} neighbors")
    
    def run(self):
        observer_channel = grpc.insecure_channel('localhost:50051')
        observer_stub = simulation_pb2_grpc.ObserverServiceStub(observer_channel)
        
        while True:
            try:
                # Flash
                self.is_lit = True
                observer_stub.UpdateStatus(simulation_pb2.StatusUpdate(
                    id=self.id,
                    flash_interval=self.flash_interval,
                    is_lit=True
                ))
                
                time.sleep(self.flash_duration)
                
                # Turn off
                self.is_lit = False
                observer_stub.UpdateStatus(simulation_pb2.StatusUpdate(
                    id=self.id,
                    flash_interval=self.flash_interval,
                    is_lit=False
                ))

                # Notify neighbors
                for neighbor_id, stub in list(self.neighbors.items()):
                    try:
                        stub.ReportFlashInterval(simulation_pb2.FlashIntervalRequest(
                            id=self.id,
                            flash_interval=self.flash_interval
                        ))
                    except grpc.RpcError:
                        print(f"Failed to communicate with neighbor {neighbor_id}")
                        del self.neighbors[neighbor_id]
                        del self.neighbor_intervals[neighbor_id]                
                
                
                # Berechne absolute Zeit seit Start
                current_time = time.time()
                elapsed_time = current_time - self.observer_start_time

                # Berechne nächsten Blinkzeitpunkt
                current_phase = elapsed_time % self.flash_interval
                next_flash_delay = self.flash_interval - current_phase

                # Passe flash_interval basierend auf Nachbarn an
                if self.neighbor_intervals:
                    avg_interval = sum(self.neighbor_intervals.values()) / len(self.neighbor_intervals)
                    adjustment = (avg_interval - self.flash_interval) * 0.1  # 10% Anpassungsrate
                    self.flash_interval += adjustment

                # Präzises Warten bis zum nächsten Blinken
                time.sleep(next_flash_delay)


            except grpc.RpcError as e:
                print(f"Connection to observer lost: {e}")
                time.sleep(1)  # Wait before retry
    
    @staticmethod
    def find_free_port():
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port

if __name__ == "__main__":
    firefly = Firefly()
    firefly.run()