import threading
import tkinter as tk
import random
import math
import time

class Firefly(threading.Thread):
    def __init__(self, canvas, x, y, size):
        threading.Thread.__init__(self)
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.neighbors = []
        self.phase = random.uniform(0, 2 * math.pi)
        self.period = 1.0
        self.rect = canvas.create_rectangle(x, y, x + size, y + size, fill="black")

    def run(self):
        while True:
            self.update_phase()
            self.update_state()
            time.sleep(0.1)

    def update_phase(self):
        coupling_strength = 0.1
        neighbor_phases = [neighbor.phase for neighbor in self.neighbors]
        mean_phase = sum(neighbor_phases) / len(neighbor_phases)
        self.phase += coupling_strength * math.sin(mean_phase - self.phase)
        self.phase = (self.phase + 2 * math.pi) % (2 * math.pi)

    def update_state(self):
        if math.sin(self.phase) > 0:
            self.canvas.itemconfig(self.rect, fill="yellow")
        else:
            self.canvas.itemconfig(self.rect, fill="black")

class FireflySimulation:
    def __init__(self, root, rows, cols, size):
        self.canvas = tk.Canvas(root, width=cols * size, height=rows * size)
        self.canvas.pack()
        self.fireflies = []
        for i in range(rows):
            row = []
            for j in range(cols):
                firefly = Firefly(self.canvas, j * size, i * size, size)
                row.append(firefly)
            self.fireflies.append(row)
        
        for i in range(rows):
            for j in range(cols):
                self.fireflies[i][j].neighbors = self.get_neighbors(i, j, rows, cols)
                self.fireflies[i][j].start()

    def get_neighbors(self, i, j, rows, cols):
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = (i + di) % rows, (j + dj) % cols
                neighbors.append(self.fireflies[ni][nj])
        return neighbors

if __name__ == "__main__":
    root = tk.Tk()
    simulation = FireflySimulation(root, 10, 10, 20)
    root.mainloop()