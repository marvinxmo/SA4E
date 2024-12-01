import math
import tkinter as tk
import threading
import random
import time



class Firefly:

    # Add shared start time as class variable
    start_time = None
    sync_event = threading.Event()

    def __init__(self, x, y, canvas, grid, square_size, flash_duration, adjustment_rate, color, show_phase):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.grid = grid
        self.nb = []
        self.is_lit = False
        self.show_phase = show_phase
        self.flash_duration = flash_duration
        self.adjustment_rate = adjustment_rate
        self.color = color
        
        # Zufällige Anfangsfrequenz
        self.flash_interval = random.uniform(500, 1500)/1000  # Zykluslänge in Sekunden
        
        # Square dimensions
        self.square_size = square_size
        self.font_size = int(self.square_size * 0.25)  # Font size 25% of square size
        
        self.rect = canvas.create_rectangle(
            x * self.square_size, 
            y * self.square_size, 
            (x + 1) * self.square_size, 
            (y + 1) * self.square_size, 
            fill=color
        )

        if show_phase:
            self.text = canvas.create_text(
                x * self.square_size + self.square_size/2,  # Center X 
                y * self.square_size + self.square_size/2,  # Center Y
                text=str(round(self.flash_interval, 4)),
                fill="white",
                font=("Arial", self.font_size)  # Set font size
            )


    def update_flash_interval(self):
        # Mittlere Frequenz der Nachbarn berechnen und allmählich anpassen
        neighbor_intervals = [neighbor.flash_interval for neighbor in self.nb]
        average_interval = sum(neighbor_intervals) / len(neighbor_intervals)
        # Anpassung der eigenen Frequenz an die der Nachbarn
        self.flash_interval += self.adjustment_rate* (average_interval - self.flash_interval)

        if self.show_phase:
            # Update text with new font configuration
            self.canvas.itemconfig(
                self.text, 
                text=str(round(self.flash_interval, 4)),
                font=("Arial", self.font_size)
            )

    def flash(self):

        # Glühwürmchen leuchtet für die Dauer der flash_duration        
        self.is_lit = True
        self.canvas.itemconfig(self.rect, fill=self.color)
        time.sleep(self.flash_duration)
        self.is_lit = False
        self.canvas.itemconfig(self.rect, fill="black")

    def run(self):

        # Wait for all fireflies to be ready
        Firefly.sync_event.wait()

        while True:
            # Calculate time since start
            current_time = time.time() - Firefly.start_time
            # Wait until next interval
            # Calculate next_flash as follows:
            # 1. Determine how many flash intervals have passed since start (integer division)
            # 2. Add 1 for the next flash interval
            # 3. Multiply by the flash interval to get the next flash time
            next_flash = ((current_time // self.flash_interval) + 1) * self.flash_interval
            time.sleep(max(0, next_flash - (time.time() - Firefly.start_time)))

            self.flash()
            self.update_flash_interval()

class FireflySimulation:
    
    def __init__(self, n_rows, n_columns, square_size, flash_duration, adjustment_rate, color, show_phase):
        
        self.root = tk.Tk()
        self.root.title("Synchronisierte Glühwürmchen-Simulation")
        self.canvas = tk.Canvas(self.root, width=n_rows * square_size, height=n_columns * square_size)
        self.canvas.pack()

        # Erstellen der Glühwürmchen in einer Torus-Struktur
        self.grid = [[None for _ in range(n_columns)] for _ in range(n_rows)]

        for x in range(n_rows):
            for y in range(n_columns):
                firefly = Firefly(x, y, self.canvas, self.grid, square_size, flash_duration, adjustment_rate, color, show_phase)
                self.grid[x][y] = firefly
        

        # Nachbarn der Glühwürmchen festlegen
        for x in range(n_rows):
            for y in range(n_columns):
                self.grid[x][y].nb = [
                self.grid[(x - 1) % n_rows][y],
                self.grid[(x + 1) % n_rows][y],
                self.grid[x][(y - 1) % n_columns],
                self.grid[x][(y + 1) % n_columns]
                ]

        # Set shared start time just before starting threads
        Firefly.start_time = time.time()

        # Starten aller Threads für die Glühwürmchen
        self.threads = []
        for x in range(n_rows):
            for y in range(n_columns):
                thread = threading.Thread(target=self.grid[x][y].run)
                thread.daemon = True  # Threads beenden sich automatisch, wenn das Hauptprogramm beendet wird
                self.threads.append(thread)
                thread.start()

        # Signal all fireflies to start
        Firefly.sync_event.set()

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":

    def get_input(prompt, default, cast_func):
        while True:
            user_input = input(prompt)
            if user_input == "":
                return default
            try:
                return cast_func(user_input)
            except ValueError:
                print(f"Invalid input. Please enter a valid value.")

    def is_valid_color(color):
        try:
            root = tk.Tk()
            root.withdraw()
            root.winfo_rgb(color)
            root.destroy()
            return True
        except tk.TclError:
            return False

    def get_color_input(prompt, default):
        while True:
            user_input = input(prompt).lower()
            if user_input == "":
                return default
            if is_valid_color(user_input):
                return user_input
            else:
                print("Invalid input. Please enter a valid color name.")

    N_ROWS = get_input("Enter number of rows (default 15): ", 15, int)
    N_COLUMNS = get_input("Enter number of columns (default 15): ", 15, int)
    SQUARE_SIZE = get_input("Enter square edge length (default 30): ", 30, int)
    FLASH_DURATION = get_input("Enter flash duration in seconds (default 0.2): ", 0.2, float)
    ADJUSTMENT_RATE = get_input("Enter adjustment rate (default 0.5): ", 0.5, float)
    COLOR = get_color_input("Enter flash color (default 'red'): ", "red")
    SHOW_PHASE = get_input("Show phase difference (default False): ", False, bool)

    simulation = FireflySimulation(N_ROWS, N_COLUMNS, SQUARE_SIZE, FLASH_DURATION, ADJUSTMENT_RATE, COLOR, SHOW_PHASE)
    simulation.run()
