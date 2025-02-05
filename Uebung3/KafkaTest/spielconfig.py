import tkinter as tk
from tkinter import messagebox
import json

# Einfache Feld-Typen
FIELD_TYPES = ["Start", "Normal", "Schikane", "Ziel"]


def move_up():
    idx = listbox.curselection()
    if not idx:
        return
    index = idx[0]
    if index > 0:
        fields[index], fields[index - 1] = fields[index - 1], fields[index]
        update_listbox()
        listbox.selection_set(index - 1)


def move_down():
    idx = listbox.curselection()
    if not idx:
        return
    index = idx[0]
    if index < len(fields) - 1:
        fields[index], fields[index + 1] = fields[index + 1], fields[index]
        update_listbox()
        listbox.selection_set(index + 1)


def add_field():
    field_type = field_type_var.get()
    fields.append(field_type)
    update_listbox()


def remove_field():
    idx = listbox.curselection()
    if not idx:
        return
    index = idx[0]
    fields.pop(index)
    update_listbox()


def update_listbox():
    listbox.delete(0, tk.END)
    for f in fields:
        listbox.insert(tk.END, f)


def save_and_close():
    # Speichere das Feld-Layout als JSON
    config = {"board_fields": fields}
    with open("ave_cesar_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    root.destroy()


root = tk.Tk()
root.title("Ave Caesar - Spielbrett konfigurieren")

fields = []

# Dropdown zum Feldtyp wählen
field_type_var = tk.StringVar(value=FIELD_TYPES[0])
tk.Label(root, text="Feldtyp:").grid(row=0, column=0, padx=5, pady=5)
type_menu = tk.OptionMenu(root, field_type_var, *FIELD_TYPES)
type_menu.grid(row=0, column=1, padx=5, pady=5)

# Buttons zum Hinzufügen/Entfernen/Reihenfolge ändern
add_btn = tk.Button(root, text="Feld hinzufügen", command=add_field)
add_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

remove_btn = tk.Button(root, text="Feld entfernen", command=remove_field)
remove_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

up_btn = tk.Button(root, text="▲", command=move_up)
up_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

down_btn = tk.Button(root, text="▼", command=move_down)
down_btn.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Listbox zum Anzeigen der Reihenfolge
listbox = tk.Listbox(root, height=8, width=25)
listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Speichern-und-Schließen-Button
save_btn = tk.Button(root, text="Speichern und Schließen", command=save_and_close)
save_btn.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
