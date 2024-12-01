import time
import grpc
import tkinter as tk
from concurrent import futures
import simulation_pb2
import simulation_pb2_grpc
import random
import subprocess


class ObserverService(simulation_pb2_grpc.ObserverServiceServicer):
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Firefly Observer")

        self.start_time = time.time()

        # Add control frame for button
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        
        # Add spawn button
        spawn_button = tk.Button(
            control_frame, 
            text="Spawn Firefly", 
            command=self.spawn_firefly
        )
        spawn_button.pack()

        self.canvas_size = 600
        self.grid_size = 5
        self.square_size = self.canvas_size // self.grid_size
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        
        self.fireflies = {}  # id -> {info, visual}
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]  # Store firefly IDs in grid
        self.next_id = 1

        self.fireflies_subprocesses = []





    def spawn_firefly(self):
        """Spawn a new firefly process"""

        firefly_script_path = __file__.replace('observer.py', 'firefly.py')
        if self.next_id <= self.grid_size * self.grid_size:

            p = subprocess.Popen(['python', firefly_script_path])
            self.fireflies_subprocesses.append(p)
            print(f"Spawning new firefly...")
        else:
            print("Grid is full!")
    
    
    def get_position_for_id(self, firefly_id):
        """Calculate grid position from ID"""
        id_adjusted = firefly_id - 1  # Convert to 0-based
        row = id_adjusted // self.grid_size
        col = id_adjusted % self.grid_size
        return row, col
    
    def get_torus_neighbors(self, row, col):
        """Get neighbor IDs in torus topology"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dx, dy in directions:
            neighbor_row = (row + dx) % self.grid_size
            neighbor_col = (col + dy) % self.grid_size
            if self.grid[neighbor_row][neighbor_col] is not None:
                neighbors.append({
                    "id": self.grid[neighbor_row][neighbor_col],
                    "host": self.fireflies[self.grid[neighbor_row][neighbor_col]]["host"],
                    "port": self.fireflies[self.grid[neighbor_row][neighbor_col]]["port"]
                })
        return neighbors
    
    def update_neighbors(self, firefly_id):
        """Update neighbors for all affected fireflies"""
        row, col = self.get_position_for_id(firefly_id)
        
        # Update neighbors for the new firefly
        neighbors = self.get_torus_neighbors(row, col)
        neighbor_messages = [
            simulation_pb2.Neighbor(
                id=n["id"],
                host=n["host"],
                port=n["port"]
            ) for n in neighbors
        ]
        
        # Update neighbors for surrounding fireflies
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            neighbor_row = (row + dx) % self.grid_size
            neighbor_col = (col + dy) % self.grid_size
            neighbor_id = self.grid[neighbor_row][neighbor_col]
            if neighbor_id is not None:
                self.notify_firefly_of_neighbors(neighbor_id)

        return neighbor_messages
    def update_neighbor_display(self, firefly_id):
        """Update the neighbor text display for a given firefly"""
        if firefly_id not in self.fireflies:
            return
            
        row, col = self.get_position_for_id(firefly_id)
        neighbors = self.get_torus_neighbors(row, col)
        neighbor_ids = [str(neighbor["id"]) for neighbor in neighbors]
        neighbor_text = "N: " + ",".join(neighbor_ids) if neighbor_ids else "N: -"
        
        self.canvas.itemconfig(
            self.fireflies[firefly_id]["visuals"]["neighbors_text"],
            text=neighbor_text
        )

    def notify_firefly_of_neighbors(self, firefly_id):
        """Notify a firefly of its updated neighbors"""
        if firefly_id in self.fireflies:
            row, col = self.get_position_for_id(firefly_id)
            neighbors = self.get_torus_neighbors(row, col)
            try:
                channel = grpc.insecure_channel(f'{self.fireflies[firefly_id]["host"]}:{self.fireflies[firefly_id]["port"]}')
                stub = simulation_pb2_grpc.FireflyServiceStub(channel)
                stub.UpdateNeighbors(simulation_pb2.NeighborUpdate(
                    neighbors=[simulation_pb2.Neighbor(
                        id=n["id"],
                        host=n["host"],
                        port=n["port"]
                    ) for n in neighbors]
                ))
            except grpc.RpcError as e:
                print(f"Failed to update neighbors for firefly {firefly_id}: {e}")

    def Register(self, request, context):
        firefly_id = self.next_id
        self.next_id += 1

        # Get position in grid
        row, col = self.get_position_for_id(firefly_id)   
        self.grid[row][col] = firefly_id


        # Create visual representation
        visuals = self.create_firefly_visual(firefly_id)
        
        # Store firefly information
        self.fireflies[firefly_id] = {
            "host": request.host,
            "port": request.port,
            "visuals": visuals,
            "position": (row, col)
        }

        # Update neighbor displays for new firefly and its neighbors
        self.update_neighbor_display(firefly_id)
        
        # Update displays for surrounding fireflies
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor_row = (row + dx) % self.grid_size
            neighbor_col = (col + dy) % self.grid_size
            if self.grid[neighbor_row][neighbor_col]:
                self.update_neighbor_display(self.grid[neighbor_row][neighbor_col])
        

        
        # Get neighbors
        neighbors_messages = self.update_neighbors(firefly_id)
        
        return simulation_pb2.RegistrationResponse(
            id=firefly_id,
            start_time= self.start_time,
            neighbors=neighbors_messages
        )
        
    def UpdateStatus(self, request, context):
        if request.id in self.fireflies:
            firefly = self.fireflies[request.id]
            # Update visual
            if request.is_lit:
                self.canvas.itemconfig(firefly["visuals"]["rect"], fill="red")
            else:
                self.canvas.itemconfig(firefly["visuals"]["rect"], fill="black")
            
            # Update interval display
            self.canvas.itemconfig(
                firefly["visuals"]["text"],
                text=f"{request.flash_interval:.3f}"
            )
        return simulation_pb2.Empty()
        
    def create_firefly_visual(self, firefly_id):
        row = (firefly_id - 1) // self.grid_size
        col = (firefly_id - 1) % self.grid_size
        
        x = col * self.square_size
        y = row * self.square_size
        
        rect = self.canvas.create_rectangle(
            x + 5, y + 5,
            x + self.square_size - 5, y + self.square_size - 5,
            fill="black"
        )

        # Create text displays
        id_text = self.canvas.create_text(
            x + self.square_size/2,
            y + self.square_size/4,
            text=f"ID: {firefly_id}",
            fill="white",
            font=("Arial", 10)
        )
        
        interval_text = self.canvas.create_text(
            x + self.square_size/2,
            y + self.square_size/2,
            text="0.000",
            fill="white",
            font=("Arial", 10)
        )

        neighbors_text = self.canvas.create_text(
            x + self.square_size/2,
            y + 3*self.square_size/4,
            text="N: -",
            fill="white",
            font=("Arial", 10)
        )

        
        return {
            "rect": rect,
            "id_text": id_text,
            "text": interval_text,
            "neighbors_text": neighbors_text
        }
        
    def get_neighbors(self, firefly_id):
        neighbors = []
        row = (firefly_id - 1) // self.grid_size
        col = (firefly_id - 1) % self.grid_size
        
        # Calculate neighbor positions (up, down, left, right)
        neighbor_positions = [
            ((row - 1) % self.grid_size, col),
            ((row + 1) % self.grid_size, col),
            (row, (col - 1) % self.grid_size),
            (row, (col + 1) % self.grid_size)
        ]
        
        for n_row, n_col in neighbor_positions:
            n_id = n_row * self.grid_size + n_col + 1
            if n_id in self.fireflies:
                neighbors.append(simulation_pb2.Neighbor(
                    id=n_id,
                    host=self.fireflies[n_id]["host"],
                    port=self.fireflies[n_id]["port"]
                ))
        
        return neighbors

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        simulation_pb2_grpc.add_ObserverServiceServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("Observer server started on port 50051")
        self.root.mainloop()

if __name__ == "__main__":
    observer = ObserverService()
    observer.run()

    # End all fireflies processes
    for p in observer.fireflies_subprocesses:
        p.kill()

    

    

    
