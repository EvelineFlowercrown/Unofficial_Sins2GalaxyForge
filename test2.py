import pygame
import tkinter as tk
from tkinter import ttk

pygame.init()

# Set up Pygame screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up Tkinter root window
root = tk.Tk()
root.withdraw()

def show_dialog():
    # Create a Tkinter toplevel window for the dialog
    dialog = tk.Toplevel(root)

    # Add widgets to the dialog
    label = ttk.Label(dialog, text="Choose a planet type to add:")
    label.pack()

    planet_types = ["gas_giant_planet", "random_home_ice_volcanic_planet", "random_moon_planet", "random_fair_planet", "random_poor_planet", "random_rich_planet", "random_asteroid_line_cluster", "player_home_planet", "random_asteroid"]
    planet_type_var = tk.StringVar(value=planet_types[0])
    planet_type_dropdown = ttk.Combobox(dialog, textvariable=planet_type_var, values=planet_types)
    planet_type_dropdown.pack()

    def on_cancel():
        dialog.destroy()

    def on_add_planet():
        planet_type = planet_type_var.get()
        print(f"Chosen planet type: {planet_type}")
        print(f"Position of double click: {pygame.mouse.get_pos()}")
        dialog.destroy()

    cancel_button = ttk.Button(dialog, text="Cancel", command=on_cancel)
    add_planet_button = ttk.Button(dialog, text="Add planet", command=on_add_planet)
    cancel_button.pack(side="left")
    add_planet_button.pack(side="right")

    # Run the Tkinter event loop until the dialog is closed
    dialog.mainloop()

show_dialog()

# Pygame event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
