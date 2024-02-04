"""
Author: Jose Renteria

README: Abstracted Tkinter App Class to render functional ui components for EasyA interface. 

notes: still need to actually generate graphs as frames or images
"""

import tkinter as tk
from tkinter import ttk
from data import avgs, aprec_yes, years, courses, class_levels, filters, class_data
from StyledGraph import *
from sys import platform as sys_pf

if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class App(tk.Tk):
    def __init__(self, title):
        super().__init__(title)
        # Inherit from tk.Tk
        self.title(title)
        self.geometry('1200x700')
        self.resizable(False, False)
        # Side Frame Parent element
        self.menu = SideFrame(self)

        # Graph Frame Parent Element
        # 1 2
        # 3 4
        self.graphs = GraphFrame(self)
        g1 = tk.Frame(self.graphs, background='red')
        g1.place(x=0, y= 0, relheight=1, relwidth=1)
        self.fig1 = self.gen_graph(class_data)
        self.c1 = self.gen_canvas(g1, self.fig1[0],0,0)

        g2 = tk.Frame(self.graphs, background='green')
        g2.place(x=420, y= 0, relheight=1, relwidth=1)
        self.fig2 = self.gen_graph(class_data)
        self.c2 = self.gen_canvas(g2, self.fig2[0], 0,0)

        g3 = tk.Frame(self.graphs, background='yellow')
        g3.place(x=0, y= 350, relheight=1, relwidth=1)
        self.fig3 = self.gen_graph(class_data)
        self.c3 = self.gen_canvas(g3, self.fig3[0], 0,0)

        g4 = tk.Frame(self.graphs, background='purple')
        g4.place(x=420, y= 350, relheight=1, relwidth=1)
        self.fig4 = self.gen_graph(class_data)
        self.c4 = self.gen_canvas(g4, self.fig4[0], 0,0)


        # Select Term DropDown Menu
        self.term_label = self.Label(self.menu, "Select Term", "White", 25).place(x=20, y = 0, relwidth = 0.4, relheight = 0.07)
        self.term_dd = self.DropDown(self.menu, "Select Term", years)
        self.term_dd[0].place(x=25, y = 45, relwidth = 0.35, relheight = 0.1)

        # Department DropDown Menu
        self.dept_label = self.Label(self.menu, "Select Dept", "White", 25).place(x=20, y = 125, relwidth = 0.4, relheight = 0.06)
        self.dept_dd = self.DropDown(self.menu, "Select Dept", courses)
        self.dept_dd[0].place(x=25, y = 165, relwidth = 0.35, relheight = 0.1)

        # Filtering Option DropDown Menu
        self.filter_by = self.Label(self.menu, "Filter by:", "White", 25).place(x=170, y = 0, relwidth = 0.4, relheight = 0.07)
        self.filter_dd = self.DropDown(self.menu, "Select Filter", filters )
        self.filter_dd[0].place(x=180, y = 45, relwidth = 0.35, relheight = 0.1)
        self.trace_var = self.filter_dd[1].trace_add('write', self.on_selection)
        # Select Dropdown Menu
        self.select_label = self.Label(self.menu, "Class Level", "White", 25).place(x=170, y = 125, relwidth = 0.4, relheight = 0.06)
        self.select_dd = self.DropDown(self.menu, "Select Level", class_levels)
        self.select_dd[0].config(state='disabled')
        self.select_dd[0].place(x=180, y = 165, relwidth = 0.35, relheight = 0.1)

        # Input box for classes
        self.entry_label = self.Label(self.menu, "Enter Class Code:", "White", 25).place(x=70, y = 250, relwidth = 0.4, relheight = 0.07)
        self.class_entry = self.EntryBox(self, self.menu)
        self.class_entry[0].config(state='disabled')
        self.class_entry[0].place(x=215, y = 260, relwidth = 0.15, relheight = 0.04)
        
        # Easy A vs Just Pass
        self.avpass_dd = self.DropDown(self.menu, "Percent A's",aprec_yes)
        self.avpass_dd[0].place(x=25, y = 310, relwidth = 0.35, relheight = 0.1)

        # Number of Graphs
        self.num_graphs = self.DropDown(self.menu, "No. of Graphs", [1,2,3,4])
        self.num_graphs[0].place(x=180, y = 310, relwidth = 0.35, relheight = 0.1)

        # Checkbox for regular faculty
        self.cbox_label = self.Label(self.menu, f'Regular Faculty\n(Default: All Instructors)', "White", 25)
        self.cbox_label.place(x=10, y = 410,  relheight = 0.07)
        self.cbox = self.CheckBox(self.menu)
        self.cbox[0].place(x=75, y = 450, relwidth = 0.1, relheight = 0.05)

        # Checkbox for class count
        self.class_count_label = self.Label(self.menu, "Include Class Count", "White", 25)
        self.class_count_label.place(x=175, y = 420, relwidth = 0.55, relheight = 0.07)
        self.count_cbox = self.CheckBox(self.menu)
        self.count_cbox[0].place(x=255, y = 450, relwidth = 0.1, relheight = 0.05)

       # Submit Button 
        self.button = tk.Button(self.menu, text="Submit", command=lambda: self.on_submit())
        self.button.place(x = 135, y = 530, relwidth = 0.2, relheight = 0.05)

        self.mainloop()
    def Label(self, parent, text, color, font):
        # Abstracted Tkinter Label
        return tk.Label(parent, text = text, bg = '#024959', fg = color, font = font)
    
    def DropDown(self, parent, set, options):
        # Abstracted Tkinter Dropdown menu
        self.var = tk.StringVar(parent)
        self.var.set("")
        self.dd = tk.OptionMenu(parent, self.var, *options) 
        self.var.set(self.var.get() if self.var.get() else set)
        return self.dd, self.var

    def CheckBox(self, parent):
        # Tkinter Checkbox
        self.checked = tk.IntVar()
        self.checkbox = tk.Checkbutton(parent, variable = self.checked, onvalue = True, offvalue = False, height = 1, width = 2, highlightcolor = 'gray', background = '#024959') 
        return self.checkbox, self.checked
    
    def EntryBox(self, master, parent):
        # Tkinter user Input Text Entry Box
        self.entry_var = tk.StringVar(master)
        self.entry = tk.Entry(parent, textvariable=self.entry_var)
        self.entry_var.set(self.entry_var.get() if self.entry_var.get() else "ex: 422")
        return self.entry, self.entry_var
    
    def gen_canvas(self, parent, fig, x, y):
        # Generates a canvas to house the graph
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().place(x=x, y=y, relheight=0.5, relwidth=0.5)
        return canvas 
    
    def gen_graph(self, data):
        fig, ax1 = plt.subplots()
        ax1.bar(data.keys(), data.values())
        return fig, ax1
    
    def on_submit(self):        
        # generates and sends a filter object w/ options to be used by
        # the matplotlib backend for graphing
        filter = {
            'TYPE': self.filter_dd[1].get(),
            'DEPT': self.dept_dd[1].get(),
            'REG_INSTR': self.cbox[1].get(),
            'TERM_DESC': self.term_dd[1].get(),
            'APREC_YES': aprec_yes[self.avpass_dd[1].get()],
            'COURSE': self.class_entry[1].get(),
            'SHOW_INSTR_CLASSES_TAUGHT': self.count_cbox[1].get(),
            'SHOW_INSTR': True,
            'LEVEL': self.select_dd[1].get(),
            'NUM_GRAPHS': self.num_graphs[1].get(),
        }
        # return GenerateGraph(averages, filter)

        # as of now just generates random graph for each
        # quadrant in graph frame. Need to be able to call GenerateGraph,
        # and render the number of graphs specified by the filter
        canvases = [self.c1, self.c2, self.c3, self.c4]
        axes = [self.fig1[1], self.fig2[1], self.fig3[1], self.fig4[1]]
        for ax in axes:
            ax.clear()
            x = np.random.randint(0,10,10)
            y = np.random.randint(0,10,10)
            ax.bar(x, y)    
        for canvas in canvases:
            canvas.draw()
        return filter


    def on_selection(self, index, var, mode):
        # Conditional option selection based on
        # Filter option chosen
        # Certain options become disabled if you don't filter by them
        var = self.filter_dd[1].get()
        if var == "Level":
            self.select_dd[0].config(state='normal')
            self.class_entry[0].config(state='disabled')

        elif var == "Class":
            self.class_entry[0].config(state='normal')
            self.select_dd[0].config(state='disabled')
            
            self.class_entry[0].config(state='normal')
            self.class_entry[1].set("")

        elif var == "Department":
            self.select_dd[0].config(state='disabled')
            self.class_entry[0].config(state='disabled')
        else: 
            self.select_dd[0].config(state='disabled')
            self.class_entry[0].config(state='disabled')
        

class SideFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, background = '#024959').pack(expand = True, fill = 'both')
        self.place(x=0, y = 0, relwidth = 0.3, relheight = 1)

class GraphFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, background = '#bbe7f2').pack(expand = True, fill = 'both')
        self.place(x=360, y = 0, relwidth = 0.7, relheight = 1)
