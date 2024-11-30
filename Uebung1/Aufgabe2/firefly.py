# firefly.py
import grpc
import tkinter as tk
import random
import time
import threading
import fireflies_pb2
import fireflies_pb2_grpc

class Firefly:
    def __init__(self):

        self.id = random.randint(1000, 9999)
        self.flash_interval = random.uniform(0.5, 1.5)
        self.flash_duration = 0.2
        self.is_lit = False
        
        # # GUI setup
        # self.root = tk.Tk()
        # self.root.title(f"Firefly {self.id}")
        
        # # Display flash interval
        # self.interval_label = tk.Label(self.root, text=f"Interval: {self.flash_interval:.3f}")
        # self.interval_label.pack()
        
        # self.canvas = tk.Canvas(self.root, width=100, height=100)
        # self.canvas.pack()
        # self.rect = self.canvas.create_rectangle(10, 10, 90, 90, fill="black")
        
        # gRPC channel
        self.setup_grpc_channel()
        self.run()
        
        # Start firefly behavior
        # self.thread = threading.Thread(target=self.run, daemon=True)
        # self.thread.start()

    def setup_grpc_channel(self):
        
        time.sleep(10)  # Wait for observer create other fireflies and start server
        MAX_RETRY = 5
        retry = 0
        while retry < MAX_RETRY:
            try:
                self.channel = grpc.insecure_channel('localhost:50051')
                # Try a dummy call to check connection
                grpc.channel_ready_future(self.channel).result(timeout=5)
                self.stub = fireflies_pb2_grpc.FireflyObserverStub(self.channel)
                print(f"Successfully connected to observer")
                return
            except grpc.FutureTimeoutError:
                retry += 1
                print(f"Connection attempt {retry} failed, retrying...")
                time.sleep(1)
        raise Exception("Could not connect to observer after maximum retries")

    # def flash(self):
    #     self.is_lit = True
    #     self.canvas.itemconfig(self.rect, fill="yellow")
    #     self.root.after(200, self.unflash)

    # def unflash(self):
    #     self.is_lit = False
    #     self.canvas.itemconfig(self.rect, fill="black")

    def run(self):
        while True:
            try:
                # Report state and get adjustment
                response = self.stub.ReportState(
                    fireflies_pb2.FireflyState(
                        id=self.id,
                        flash_interval=self.flash_interval,
                        is_lit=self.is_lit
                    )
                )
                
                # Adjust flash interval
                self.flash_interval += response.adjustment
                #self.interval_label.config(text=f"Interval: {self.flash_interval:.3f}")
                
                # Flash
                #self.root.after(0, self.flash)
                time.sleep(self.flash_interval)
                
            except grpc.RpcError as e:
                status_code = e.code()
                print(f"RPC failed: {status_code} - {e.details()}")
                time.sleep(1)

    # def start(self):
    #     self.root.mainloop()

if __name__ == "__main__":
    firefly = Firefly()
    #firefly.start()