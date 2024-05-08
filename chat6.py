import tkinter as tk
from tkinter import ttk

import customtkinter

# root window
root = tk.Tk()
root.geometry(f"{1100}x{580}")
root.title('Login')
root.resizable(0, 0)

# Define a function to create placeholder frames for visual structure
def create_placeholder(parent, row, column, rowspan=1, columnspan=1):
    frame = customtkinter.CTkFrame(master=parent, width=100, height=100, corner_radius=10)
    frame.grid(row=row, column=column, padx=10, pady=10, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
    return frame

# Configure grid rows and columns
rows = [1, 1, 1, 2, 2]
columns = [1, 1, 3]
for r in range(len(rows)):
    root.rowconfigure(r, weight=rows[r])
for c in range(len(columns)):
    root.columnconfigure(c, weight=columns[c])

# Create placeholder frames for the layout
create_placeholder(root, 0, 0)
create_placeholder(root, 1, 0)
create_placeholder(root, 2, 0)
create_placeholder(root, 3, 0, rowspan=2)

create_placeholder(root, 0, 1, columnspan=2)
create_placeholder(root, 1, 1)
create_placeholder(root, 2, 1, columnspan=2)
create_placeholder(root, 3, 1)
create_placeholder(root, 4, 1)

create_placeholder(root, 1, 2)
create_placeholder(root, 3, 2)
create_placeholder(root, 4, 2)

root.mainloop()