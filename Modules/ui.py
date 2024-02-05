"""
Author: Jose Renteria

README: Abstracted Tkinter App Class to render functional ui components for EasyA interface. 

notes: still need to actually generate graphs as frames or images
"""

import tkinter as tk
from tkinter import ttk
from Modules.GenerateGraph import *
from sys import platform as sys_pf


if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


filters = {"Department", "Level", "Class"}
class_levels = [100, 200, 300, 400, 500, 600]
aprec_yes = {"Percent A's": True, "Percent D/F's": False}
courses = ["BI", "CH", "CIS", "GEOG", "HPHY", "MATH", "PHYS", "PSY"]

class App(tk.Tk):
    def __init__(self, title):
        super().__init__(title)
        # Inherit from tk.Tk
        self.title(title)
        self.geometry('1200x700')
        self.resizable(False, False)

        # Side Frame Parent element
        
        self.menu = SideFrame(self, callback=self.update_graph)
        self.graphs = GraphFrame(self)
        self.clear = tk.Button(self.menu, text="Clear", command=lambda: self.on_clear())
        self.clear.place(x= 130, y = 670, relheight=0.03, relwidth=0.2)
        self.mainloop()
        
    def on_clear(self):
        self.destroy()
        return App("Easy A")


    def update_graph(self, filter, ctr):
        self.graphs.update_graph(filter, ctr)

        

class SideFrame(ttk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.frame = tk.Frame(self, background='#024959')
        self.frame.pack(expand = True, fill = 'both')
        self.callback = callback
        self.place(x=0, y = 0, relwidth = 0.3, relheight = 1)
        self.menu = self
        self.buttonCtr = 1
        self.height = 165
        self.shift = 0
        self.quadshift = 0
        self.quadx = 420
        self.quady = 350
        self.filters = self.GenFilter(self.shift, self.buttonCtr)
        self.i = 1


    def on_press_increment(self):
        self.buttonCtr += 1
        if(self.buttonCtr <= 4):
            self.i += 1
            self.shift += (self.height)
            print(self.buttonCtr, self.shift)
            return self.GenFilter(self.shift, self.i)
        elif(self.buttonCtr >= 4):
            self.buttonCtr = 4
            print(self.buttonCtr, self.shift)

            return None
        
    
    def on_press_decrement(self, i):
        if(1 <= self.i <= 4):
            self.i -= 1
        elif(self.i == 0):
            self.i = 1
        print(self.i)
        return self.i

    def GenFilter(self, shift, i):
        # Department DropDown Menu
        # self.dept_label = self.menu.Label(self.menu, "Select Dept", "White", 25, 25 , 0 + shift)
        self.dept_dd = self.menu.DropDown(self.menu, "Select Dept", courses, 25, 45 + shift)
        # Filtering Option DropDown Menu
        # self.filter_by = self.menu.Label(self.menu, "Filter by:", "White", 25, 25, 60 + shift)
        self.filter_dd = self.menu.DropDown(self.menu, "Select Filter", filters, 25, 10 + shift)
        self.trace_var = self.filter_dd[1].trace_add('write', self.on_selection)
        # Select Dropdown Menu
        # self.select_label = self.menu.Label(self.menu, "Class Level", "White", 25, 25, 120 + shift)
        #self.select_dd = self.menu.DropDown(self.menu, "Select Level", class_levels, 25, 80 + shift)
        # self.select_dd[0].config(state='disabled')
        # Input box for classes
        self.entry_label = self.menu.Label(self.menu, "Level/Class #: ", "White", 150, 150, 40 + shift)
        self.class_entry = self.menu.EntryBox(self, self.menu, 270, 47 + shift)
        self.class_entry[0].config(state='disabled')
        # Easy A vs Just Pass
        self.avpass_dd = self.menu.DropDown(self.menu, "Percent A's",aprec_yes, 180, 10 + shift)

        # Checkbox for regular faculty
        self.cbox_label = self.menu.Label(self.menu, f'Regular Faculty Only: ', "White", 25, 150, 105 + shift)
        self.cbox = self.CheckBox(self.menu, 295, 108 + shift )

        # Checkbox for class count
        self.class_count_label = self.menu.Label(self.menu, "Count: ", "White", 25, 110, 73 + shift)
        self.count_cbox = self.CheckBox(self.menu, 200, 76 + shift)

        # Checkbox for show classes
        self.class_or_instr_label = self.menu.Label(self.menu, "By Class: ", "White", 25, 220, 75 + shift)
        self.show_classes_cbox = self.CheckBox(self.menu, 320, 78 + shift)

       # Add Graph Button 
        self.button = tk.Button(self.menu, text="Add Graph", command=lambda: self.on_press_increment())
        self.button.place(x = 25, y = 85 + shift, relwidth = 0.3, relheight = 0.03 )
        self.button.config(bg = '#024959')
        
        self.indexbutton = tk.Button(self.menu, text=i, command=lambda: print(i))
        self.indexbutton.place(x = 335, y = 5 + shift, relwidth = 0.05, relheight = 0.03 )

        self.submit_button = tk.Button(self.menu, text="Submit", command=lambda: self.on_submit(self.filter_dd, self.avpass_dd, self.dept_dd, self.cbox, self.class_entry, self.count_cbox, self.show_classes_cbox))

        self.submit_button.place(x = 25, y = 115 + shift, relwidth = 0.3, relheight = 0.03, )
        self.separator = tk.Label(self, background='#001a30').place(x=0, y=155 + shift, relwidth = 1, relheight = 0.001)
        return self.dept_dd, self.filter_dd, self.trace_var, self.entry_label, self.class_entry, self.avpass_dd, self.cbox_label, self.cbox, self.class_count_label, self.count_cbox, self.button, self.indexbutton, self.submit_button, self.separator

    def Label(self, parent, text, color, font, x, y):
        # Abstracted Tkinter Label
        return tk.Label(parent, text = text, bg = '#024959', fg = color, font = font).place(x=x, y=y, relwidth = 0.4, relheight = 0.06 )
    
    def DropDown(self, parent, set, options, x, y):
        # Abstracted Tkinter Dropdown menu
        self.var = tk.StringVar(parent)
        self.var.set("")
        self.dd = tk.OptionMenu(parent, self.var, *options)
        self.var.set(self.var.get() if self.var.get() else set)
        self.dd.place(x=x, y=y, relwidth = 0.3, relheight=0.05)
        self.dd.config(bg = '#024959')

        return self.dd, self.var

    def CheckBox(self, parent, x, y):
        # Tkinter Checkbox
        self.checked = tk.IntVar()
        self.CB = tk.Checkbutton(parent, variable = self.checked, onvalue = True, offvalue = False, height = 1, width = 2, highlightcolor = 'gray', background = '#024959') 
        self.CB.config(bg = '#024959') 
        self.CB.place(x=x, y = y, relwidth = 0.1, relheight = 0.05)
        return self.CB, self.checked
    
    def EntryBox(self, master, parent, x, y):
        # Tkinter user Input Text Entry Box
        self.entry_var = tk.StringVar(master)
        self.entry = tk.Entry(parent, textvariable=self.entry_var)
        self.entry_var.set(self.entry_var.get() if self.entry_var.get() else "ex: 422")
        self.entry.place(x=x, y = y, relwidth = 0.15, relheight = 0.04)
        return self.entry, self.entry_var
    
    def on_submit(self, filter_dd, avpass_dd, dept_dd, cbox, class_entry, count_cbox, show_classes_cbox):        
        # generates and sends a filter object w/ options to be used by
        # the matplotlib backend for graphing
        filter = {
            'TYPE': filter_dd[1].get(),
            'DEPT': dept_dd[1].get(),
            'REG_INSTR': cbox[1].get(),
            'APREC_YES': aprec_yes[self.avpass_dd[1].get()],
            'COURSE': class_entry[1].get(),
            'SHOW_INSTR_CLASSES_TAUGHT': count_cbox[1].get(),
            'SHOW_INSTR': show_classes_cbox[1].get(),        }

        # as of now just generates random graph for each
        # quadrant in graph frame. Need to be able to call GenerateGraph,
        # and render the number of graphs specified by the filter
        #axes = [self.fig1[1], self.fig2[1], self.fig3[1], self.fig4[1]]
        #for ax in axes:
        #    ax.clear()
        #    ax.bar(x, y)    
        return self.callback(filter, self.i)

    
    def on_selection(self, index, var, mode):
        # Conditional option selection based on
        # Filter option chosen
        # Certain options become disabled if you don't filter by them
        var = self.filter_dd[1].get()
        if var == "Level":
            #self.select_dd[0].config(state='normal')
            self.class_entry[0].config(state='normal')
            self.class_entry[1].set("")

        elif var == "Class":
            # self.class_entry[0].config(state='normal')
            #self.select_dd[0].config(state='disabled')
            
            self.class_entry[0].config(state='normal')
            self.class_entry[1].set("")

        elif var == "Department":
            # self.select_dd[0].config(state='disabled')
            self.class_entry[0].config(state='disabled')
        else: 
            # self.select_dd[0].config(state='disabled')
            self.class_entry[0].config(state='disabled')

class GraphFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, background = '#bbe7f2').pack(expand = True, fill = 'both')
        self.place(x=360, y = 0, relwidth = 0.7, relheight = 1)
        # Graph Frame Parent Element
        # 1 2
        # 3 4
        self.current_quadrant = 0
        g1 = tk.Frame(self, background='#8ebcd4')
        g1.place(x=0, y= 0, relheight=1, relwidth=1)
        #self.fig1 = self.gen_graph(class_data)
        #self.c1 = self.gen_canvas(g1, self.fig1[0],0,0)

        g2 = tk.Frame(self, background='#7ca8bf')
        g2.place(x=420, y= 0, relheight=1, relwidth=1)
        #self.fig2 = self.gen_graph(class_data)
        #self.c2 = self.gen_canvas(g2, self.fig2[0], 0,0)

        g3 = tk.Frame(self, background='#6590a6')
        g3.place(x=0, y= 350, relheight=1, relwidth=1)
        #self.fig3 = self.gen_graph(class_data)
        #self.c3 = self.gen_canvas(g3, self.fig3[0], 0,0)

        g4 = tk.Frame(self, background='#54798c')
        g4.place(x=420, y= 350, relheight=1, relwidth=1)
        #self.fig4 = self.gen_graph(class_data)
        #self.c4 = self.gen_canvas(g4, self.fig4[0], 0,0)
    
    def gen_canvas(self, parent, fig, x, y):
        # Generates a canvas to house the graph
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().place(x=x, y=y, relheight=0.5, relwidth=0.5)
        return canvas 
    
    def update_graph(self, filter, ctr):
        if ctr == 1:
            canvas = self.gen_canvas(self, GenerateGraph(filter), 0, 0)   
        elif ctr == 2:
            canvas = self.gen_canvas(self, GenerateGraph(filter), 420, 0)   
        elif ctr == 3:
            canvas = self.gen_canvas(self, GenerateGraph(filter), 0, 350)  
        elif ctr >= 4:
            canvas =  self.gen_canvas(self, GenerateGraph(filter), 420, 350) 

        if canvas:
            return canvas.draw()
        else:
            None
    def gen_graph(self, data):
        fig, ax1 = plt.subplots()
        ax1.bar(data.keys(), data.values())
        return fig, ax1