# observer.py
import tkinter as tk
import grpc
from concurrent import futures
import fireflies_pb2
import fireflies_pb2_grpc
import random
import threading

class FireflyObserver(fireflies_pb2_grpc.FireflyObserverServicer):
    def __init__(self):
        # GUI Setup
        self.root = tk.Tk()
        self.root.title("Firefly Observer")
        
        # Control Frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Add Firefly", command=self.spawn_firefly).pack(side=tk.LEFT, padx=5)
        
        # Canvas for fireflies
        self.canvas_size = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        
        # Firefly management
        self.fireflies = {}  # id -> state
        self.adjustment_rate = 0.1
        
        # Start gRPC server with status check
        try:
            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            fireflies_pb2_grpc.add_FireflyObserverServicer_to_server(self, self.server)
            port = 50051
            self.server.add_insecure_port(f'[::]:{port}')
            self.server.start()
            print(f"Server started successfully on port {port}")
        except Exception as e:
            print(f"Failed to start server: {e}")
            raise

    def ReportState(self, request, context):
        self.fireflies[request.id] = request
        avg_interval = self.calculate_average_interval()
        adjustment = self.adjustment_rate * (avg_interval - request.flash_interval)
        return fireflies_pb2.SynchronizationResponse(adjustment=adjustment)
    
    def calculate_average_interval(self):
        
        # In case there are no fireflies, return 1.0
        if not self.fireflies:
            return 1.0
        
        
        return sum(f.flash_interval for f in self.fireflies.values()) / len(self.fireflies)
    
    def spawn_firefly(self):
        import subprocess
        subprocess.Popen(['python', 'firefly.py'])
    

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    observer = FireflyObserver()
    observer.run()