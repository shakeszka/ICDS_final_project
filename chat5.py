import tkinter as tk
from tkinter import ttk

import customtkinter

# root window
root = tk.Tk()
root.geometry(f"{1100}x{580}")
root.title('Login')
root.resizable(0, 0)

# Define a function to create placeholder frames for visual structure
def create_widget(parent, row, column, rowspan=1, columnspan=1, corner_radius=10, border_color='white', border_width=1, width=0, height=0, pady=(20, 0), padx=(0, 20)):
    frame = customtkinter.CTkFrame(master=parent, corner_radius=corner_radius, border_color=border_color, border_width=border_width, width=width, height=height)
    frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew", pady=pady, padx=padx)
    return frame

def create_label(parent, row, column, rowspan=1, columnspan=1, border_color='white', border_width=1, width=0, height=0, pady=(20, 0), padx=(0, 20)):
    label = customtkinter.CTkLabel(master=parent, corner_radius=10, border_color=border_color, border_width=border_width, width=width, height=height)
    label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew", pady=pady, padx=padx)
    return label
        
def create_button(parent, row, column, rowspan=1, columnspan=1, border_color='white', border_width=1, width=0, height=0, pady=(20, 0), padx=(0, 20)):
    button = customtkinter.CTkButton(master=parent, corner_radius=10, border_color=border_color, border_width=border_width, width=width, height=height)
    button.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew", pady=pady, padx=padx)
    return button

# Configure grid rows and columns
rows = [4, 2, 1] # the weight of the rows
columns = [1, 2, 6] # the weight of the columns
for r in range(len(rows)):
    root.rowconfigure(r, weight=rows[r])
for c in range(len(columns)):
    root.columnconfigure(c, weight=columns[c])

# Create placeholder frames for the layout
# sidebar
sidebar = create_widget(root, 0, 0, rowspan=3, pady=0, corner_radius=0)


# middle
create_widget(root, 0, 1)
create_widget(root, 1, 1)
create_widget(root, 2, 1, pady=(20, 20))

# main
create_widget(root, 0, 2)
create_widget(root, 1, 2)
create_widget(root, 2, 2, pady=(20, 20))

root.mainloop()