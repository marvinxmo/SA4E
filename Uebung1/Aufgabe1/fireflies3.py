import math
import threading
import tkinter as tk
import random
import time

# Parameter der Simulation
GRID_SIZE = 10      # Größe des Torus (10x10)
FLASH_DURATION = 0.4    # Dauer des Aufleuchtens in Sekunden
ADJUSTMENT_RATE = 1   # Einflussfaktor auf die Frequenz-Anpassung
TIME_STEP = 0.1  # Zeitschritt für die Simulation

class Firefly:
    def __init__(self, x, y, canvas, grid):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.grid = grid
        self.nb = []
        self.is_lit = False
        # Zufällige Anfangszeit für das nächste Aufleuchten
        self.next_flash_time = time.time() + random.uniform(0, 2 * math.pi)
        self.rect = canvas.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill="black")

    def get_neighbors(self):
        # Torus-artige Nachbarschaftsbestimmung
        return self.nb

    def update_next_flash_time(self):
        # Mittlere nächste Aufleuchtzeit der Nachbarn berechnen und allmählich anpassen
        neighbor_flash_times = [neighbor.next_flash_time for neighbor in self.get_neighbors()]
        average_flash_time = sum(neighbor_flash_times) / len(neighbor_flash_times)
        # Anpassung der eigenen nächsten Aufleuchtzeit an die der Nachbarn
        self.next_flash_time += ADJUSTMENT_RATE * (average_flash_time - self.next_flash_time)

    def flash(self):
        # Glühwürmchen leuchtet für die Dauer der flash_duration
        self.is_lit = True
        self.canvas.itemconfig(self.rect, fill="red")
        time.sleep(FLASH_DURATION)
        self.is_lit = False
        self.canvas.itemconfig(self.rect, fill="black")

        print(f"Firefly ({self.x}, {self.y}) next flash time: {self.next_flash_time}")

    def run(self):
        while True:
            current_time = time.time()
            if current_time >= self.next_flash_time:
                self.flash()
                self.update_next_flash_time()
                #self.next_flash_time = current_time + (2 * math.pi)  # Set the next flash time to a fixed interval
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