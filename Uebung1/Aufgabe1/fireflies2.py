import threading
import tkinter as tk
import random
import math
import time

# Parameter der Simulation
GRID_SIZE = 10      # Größe des Torus (10x10)
FLASH_DURATION = 0.2    # Dauer des Aufleuchtens in Sekunden
ADJUSTMENT_RATE = 0.1   # Einflussfaktor auf die Frequenz-Anpassung
TIME_STEP = 0.2   # Zeitschritt für die Simulation

class Firefly:
    def __init__(self, x, y, canvas, grid):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.grid = grid
        self.nb = []
        self.is_lit = False
        # Zufällige Anfangsphase
        self.phase = random.uniform(0, 2 * math.pi)
        self.rect = canvas.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill="black")

    def get_neighbors(self):
        # Torus-artige Nachbarschaftsbestimmung
        return self.nb

    def update_phase(self):
        # Mittlere Phase der Nachbarn berechnen und allmählich anpassen
        neighbor_phases = [neighbor.phase for neighbor in self.get_neighbors()]
        average_phase = sum(neighbor_phases) / len(neighbor_phases)
        # Anpassung der eigenen Phase an die der Nachbarn
        self.phase += ADJUSTMENT_RATE * math.sin(average_phase - self.phase)
        self.phase = (self.phase + 2 * math.pi) % (2 * math.pi)

    def flash(self):
        # Glühwürmchen leuchtet für die Dauer der flash_duration
        self.is_lit = True
        self.canvas.itemconfig(self.rect, fill="red")
        time.sleep(FLASH_DURATION)
        self.is_lit = False
        self.canvas.itemconfig(self.rect, fill="black")

        if (self.x == 0 and self.y == 0) or (self.x == 0 and self.y == 1):
            print(f"Firefly ({self.x}, {self.y}) phase: {self.phase:.2f} radians")

    def run(self):
        while True:
            self.update_phase()
            if math.sin(self.phase) > 0:
                self.flash()
            time.sleep(TIME_STEP)

class FireflySimulation:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE * 20, height=GRID_SIZE * 20)
        self.canvas.pack()
        self.fireflies = []
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                firefly = Firefly(i, j, self.canvas, self.fireflies)
                row.append(firefly)
            self.fireflies.append(row)
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.fireflies[i][j].nb = self.get_neighbors(i, j, GRID_SIZE, GRID_SIZE)
        
        self.threads = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                thread = threading.Thread(target=self.fireflies[i][j].run)
                thread.daemon = True
                self.threads.append(thread)
                thread.start()

    def get_neighbors(self, i, j, rows, cols):
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = (i + di) % rows, (j + dj) % cols
                neighbors.append(self.fireflies[ni][nj])
        return neighbors

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulation = FireflySimulation()
    simulation.run()