# observer.py
import time
import tkinter as tk
import grpc
from concurrent import futures
import fireflies_pb2
import fireflies_pb2_grpc
import random
import threading
import subprocess


class FireflyObserver(fireflies_pb2_grpc.FireflyObserverServicer):
    def __init__(self):
        # GUI Setup
        self.root = tk.Tk()
        self.root.title("Firefly Observer")
        
        # Canvas for fireflies
        self.canvas_size = 600
        self.grid_size = 5  # 5x5 grid
        self.square_size = self.canvas_size // self.grid_size
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        
        # Firefly management
        self.fireflies = {}  # id -> state
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.adjustment_rate = 0.1
        self.next_row = 0
        self.next_col = 0

        self.initialize_fireflies()
        
        # Start gRPC server
        try:
            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            fireflies_pb2_grpc.add_FireflyObserverServicer_to_server(self, self.server)
            port = 50051
            self.server.add_insecure_port(f'[::]:{port}')
            self.server.start()
            print(f"Server started successfully on port {port}")
            
            # Initialize all fireflies after server is ready
            #self.initialize_fireflies()
            
        except Exception as e:
            print(f"Failed to start server: {e}")
            raise
    
    
    def get_next_position(self):

        """Get next available grid position"""
        if self.next_row >= self.grid_size:
            return None, None
            
        row, col = self.next_row, self.next_col
        self.next_col += 1
        if self.next_col >= self.grid_size:
            self.next_col = 0
            self.next_row += 1
        return row, col


    def initialize_fireflies(self):
        """Create all 25 fireflies on startup"""
        NUM_FIREFLIES = self.grid_size ** 2
        for _ in range(NUM_FIREFLIES):
            threading.Thread(
                target=lambda: subprocess.Popen(['python', 'firefly.py']),
                daemon=True
            ).start()
            print("Spawned firefly")


            time.sleep(0.3)  # Small delay between spawns to prevent connection issues


    def create_firefly_visual(self, firefly_id, flash_interval):
        row, col = self.get_next_position()
        if row is None:
            print("Grid is full!")
            return None
            
        x = col * self.square_size
        y = row * self.square_size
        
        rect = self.canvas.create_rectangle(
            x + 5, y + 5,
            x + self.square_size - 5, y + self.square_size - 5,
            fill="black"
        )
        
        text = self.canvas.create_text(
            x + self.square_size/2,
            y + self.square_size/2,
            text=f"{flash_interval:.3f}",
            fill="white"
        )
        
        self.grid[row][col] = firefly_id
        return {"rect": rect, "text": text}
    
    # def flash_firefly(self, firefly_id):
    #     # Set the color to yellow
    #     self.canvas.itemconfig(
    #         self.fireflies[firefly_id]["visuals"]["rect"],
    #         fill="yellow"
    #     )
    #     # Schedule to revert to black after 200ms
    #     self.root.after(200, lambda: self.canvas.itemconfig(
    #         self.fireflies[firefly_id]["visuals"]["rect"],
    #         fill="black"
    #     ))



    def ReportState(self, request, context):
        if request.id not in self.fireflies:
            # New firefly - create visual
            visuals = self.create_firefly_visual(request.id, request.flash_interval)
            if visuals:
                self.fireflies[request.id] = {
                    "state": request,
                    "visuals": visuals
                }
        else:
            # Update existing firefly
            self.fireflies[request.id]["state"] = request
            self.canvas.itemconfig(
                self.fireflies[request.id]["visuals"]["text"],
                text=f"{request.flash_interval:.3f}"
            )

            # Set the color to yellow
            self.canvas.itemconfig(
                self.fireflies[request.id]["visuals"]["rect"],
                fill="yellow"
            )

            time.sleep(0.2)
            # Schedule to revert to black after 200ms
            self.canvas.itemconfig(
                self.fireflies[request.id]["visuals"]["rect"],
                fill="black"
            )

        avg_interval = self.calculate_average_interval()
        adjustment = self.adjustment_rate * (avg_interval - request.flash_interval)
        return fireflies_pb2.SynchronizationResponse(adjustment=adjustment)
    
    def calculate_average_interval(self):
        if not self.fireflies:
            return 1.0
        return sum(f["state"].flash_interval for f in self.fireflies.values()) / len(self.fireflies)
    
    def spawn_firefly(self):
        subprocess.Popen(['python', 'firefly.py'])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    observer = FireflyObserver()
    observer.run()