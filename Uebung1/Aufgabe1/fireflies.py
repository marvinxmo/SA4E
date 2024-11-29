import math
import tkinter as tk
import threading
import random
import time

# Parameter der Simulation
GRID_SIZE = 10      # Größe des Torus (10x10)
FLASH_DURATION = 0.2    # Dauer des Aufleuchtens in Sekunden
ADJUSTMENT_RATE = 0.4   # Einflussfaktor auf die Frequenz-Anpassung
TIME_STEP = 1   # Zeitschritt für die Simulation

class Firefly:
    def __init__(self, x, y, canvas, grid):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.grid = grid
        self.nb = []
        self.is_lit = False
        # Zufällige Anfangsfrequenz:Zyklus
        self.flash_interval = random.uniform(0, 2 * math.pi)  # Zykluslänge in Sekunden
        
        self.next_flash_time = time.time() + random.uniform(0, 2000)/1000 # Zeitpunkt des nächsten Aufleuchtens
        self.rect = canvas.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill="black")

    def get_neighbors(self):
        # Torus-artige Nachbarschaftsbestimmung
        return self.nb

    def update_flash_interval(self):
        # Mittlere Frequenz der Nachbarn berechnen und allmählich anpassen
        neighbor_intervals = [neighbor.flash_interval for neighbor in self.get_neighbors()]
        average_interval = sum(neighbor_intervals) / len(neighbor_intervals)
        # Anpassung der eigenen Frequenz an die der Nachbarn
        self.flash_interval += ADJUSTMENT_RATE * (average_interval - self.flash_interval)

    def update_next_flash(self):
        # Mittlere Frequenz der Nachbarn berechnen und allmählich anpassen
        neighbor_intervals = [neighbor.next_flash_time for neighbor in self.get_neighbors()]
        average_interval = sum(neighbor_intervals) / len(neighbor_intervals)
        # Anpassung der eigenen Frequenz an die der Nachbarn
        self.next_flash_time += ADJUSTMENT_RATE * (average_interval - self.next_flash_time)
 
    def flash(self):
        # Glühwürmchen leuchtet für die Dauer der flash_duration
        if (self.x == 0 and self.y == 0) or (self.x == 0 and self.y == 1):
            print(f"Firefly ({self.x}, {self.y}) at {time.time():.2f}. Flash interval: {self.flash_interval:.2f} seconds.")
        
        self.is_lit = True
        self.canvas.itemconfig(self.rect, fill="red")
        time.sleep(FLASH_DURATION)
        self.is_lit = False
        self.canvas.itemconfig(self.rect, fill="black")


    def flash2(self):
        # Glühwürmchen leuchtet für die Dauer der flash_duration

        self.is_lit = True
        self.canvas.itemconfig(self.rect, fill="red")
        time.sleep(FLASH_DURATION)
        self.is_lit = False
        self.canvas.itemconfig(self.rect, fill="black")

        self.update_next_flash()



    def run(self):
        while True:
            # # Aktuelle Zeit abrufen
            # current_time = time.time()

            # # Prüfen, ob das Glühwürmchen aufleuchten soll
            # if current_time >= self.next_flash_time:
                # Glühwürmchen aufleuchten lassen
            if time.time() >= self.next_flash_time:
                self.flash2()

      

                #self.next_flash_time = current_time + self.flash_interval

class FireflySimulation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Synchronisierte Glühwürmchen-Simulation")
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE * 20, height=GRID_SIZE * 20)
        self.canvas.pack()

        # Erstellen der Glühwürmchen in einer Torus-Struktur
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                firefly = Firefly(x, y, self.canvas, self.grid)
                self.grid[x][y] = firefly
        

        # Nachbarn der Glühwürmchen festlegen
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                self.grid[x][y].nb = [
                self.grid[(x - 1) % GRID_SIZE][y],
                self.grid[(x + 1) % GRID_SIZE][y],
                self.grid[x][(y - 1) % GRID_SIZE],
                self.grid[x][(y + 1) % GRID_SIZE]
                ]


        # Starten aller Threads für die Glühwürmchen
        self.threads = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                thread = threading.Thread(target=self.grid[x][y].run)
                thread.daemon = True  # Threads beenden sich automatisch, wenn das Hauptprogramm beendet wird
                self.threads.append(thread)
                thread.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulation = FireflySimulation()
    simulation.run()
