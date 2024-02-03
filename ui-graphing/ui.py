"""
Author: Jose Renteria

README: Abstracted Tkinter functions to render consistent ui components for EasyA interface. 

notes: still need to actually generate graphs as frames or images
"""

import tkinter as tk
from tkinter import *

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#026773", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

# Function to generate a graph
def gen_graph(data, title, xlabel, ylabel):
    fig, ax1 = plt.subplots()
    ax1.bar(data.keys(), data.values())
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    # plt.show()
    return fig

# Create a window and add charts
def gen_root():
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry('1200x700')
    root.resizable()
    return root
# Side frame

def gen_side_frame(root, width, height, color):
    side_frame = tk.Frame(root, width=width, height=height, bg=color)
    side_frame.pack(side="right", fill="y")
    return side_frame

def gen_label(root, text, color, text_color, font_size):
    label = tk.Label(root, text=text, bg=color, fg=text_color, font=35)
    label.pack(pady=20, padx=100)
    return label


# Year DropDown
def gen_dropdown(root:object, frame:object, set:str, options:list) -> object:
    dropdown_var = tk.StringVar(root)
    dropdown_var.set(set)
    year_dropdown = tk.OptionMenu(frame, dropdown_var, *options)
    dropdown_var.set(year_dropdown)
    year_dropdown.pack(side="top", fill="none",pady=20)
    return year_dropdown, dropdown_var

def gen_text_input(root, frame):
    # Text input
    input_var = tk.StringVar(root)
    entry = tk.Entry(frame, textvariable = input_var)
    input_var.set(entry)
    entry.pack(side="top", fill="none")
    return entry, input_var


def gen_button(frame, text, command):
    # Submit button
    button = tk.Button(frame, text=text, command=command)
    button.pack(side="top", fill="y", pady=20)
    return button

def send_obj(year, course, txt, checkbox):
    obj = {
        'TERM_DESC': year[1].get(),
        'COURSE_CODE': f'{course[1].get()}{txt[1].get()}',
        'regular_instructors': checkbox[1].get()
    }
    print(obj)
    return obj

def gen_frame(root, w, h):
    charts_frame = tk.Frame(root, width=w, height=h)
    charts_frame.pack(fill="x")
    return charts_frame

def gen_canvas(fig, root, side):
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=side, fill="x")
    return canvas

def gen_checkbox(root):
    checkvar = IntVar()
    check1 = Checkbutton(root, variable = checkvar, onvalue = 1, offvalue = 0, height =1, width = 2, highlightcolor='green', background='#024959')
    check1.pack(fill = 'none')
    return check1, checkvar