import tkinter as tk
from tkinter import messagebox
from skijump import ski_

def start_simulator():
    try:
        # Retrieve user input values
        mass = float(mass_entry.get())
        height_inrun = float(height_inrun_entry.get())
        height_ramp = float(height_ramp_entry.get())
        length_ramp = float(length_ramp_entry.get())
        deg_inrun = float(deg_inrun_entry.get())
        deg_slope = float(deg_slope_entry.get())

        # Call the ski() function to start the simulation
        ski_(mass, height_inrun, height_ramp, length_ramp, deg_inrun, deg_slope)

    except ValueError:
        # Display an error message if the user enters invalid input
        messagebox.showerror("Error", "Invalid input. Please enter numerical values.")
        
window = tk.Tk()
window.title("Ski Jump Simulator")

# Labels
labels = [
    "Mass (kg):", "Height of Inrun (m):", "Height of Ramp (m):",
    "Length of Ramp (m):", "Degree of Inrun:", "Degree of Slope:"
]

for i, label_text in enumerate(labels):
    label = tk.Label(window, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=5)

# Entry fields
mass_entry = tk.Entry(window)
mass_entry.grid(row=0, column=1, padx=10, pady=5)

height_inrun_entry = tk.Entry(window)
height_inrun_entry.grid(row=1, column=1, padx=10, pady=5)

height_ramp_entry = tk.Entry(window)
height_ramp_entry.grid(row=2, column=1, padx=10, pady=5)

length_ramp_entry = tk.Entry(window)
length_ramp_entry.grid(row=3, column=1, padx=10, pady=5)

deg_inrun_entry = tk.Entry(window)
deg_inrun_entry.grid(row=4, column=1, padx=10, pady=5)

deg_slope_entry = tk.Entry(window)
deg_slope_entry.grid(row=5, column=1, padx=10, pady=5)

start_button = tk.Button(window, text="Start", command=start_simulator)
start_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()