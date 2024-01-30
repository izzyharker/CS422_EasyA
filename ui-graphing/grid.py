import tkinter as tk
from tkinter import *

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from data import class_data


plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#026773", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

# Chart 1: Bar chart of sales data
fig1, ax1 = plt.subplots()
ax1.bar(class_data.keys(), class_data.values())
ax1.set_title("% Of Grades Given")
ax1.set_xlabel("Fall 2020")
ax1.set_ylabel("% A's")
# plt.show()

# Chart 2: Horizontal bar chart of inventory data
fig2, ax2 = plt.subplots()
ax2.bar(class_data.keys(), class_data.values())
ax2.set_title("% Of Grades Given")
ax2.set_xlabel("Winter 2021")
ax2.set_ylabel("% A's")
# plt.show()

# Chart 3: Pie chart of product data
fig3, ax3 = plt.subplots()
ax3.bar(class_data.keys(), class_data.values())
ax3.set_title("% Of Grades Given")
ax3.set_xlabel("Spring 2021")
ax3.set_ylabel("% A's")
# plt.show()

# Chart 4: Line chart of sales by year
fig4, ax4 = plt.subplots()
ax4.bar(class_data.keys(), class_data.values())
ax4.set_title("% Of Grades Given")
ax4.set_xlabel("Fall 2022")
ax4.set_ylabel("% A's")
# plt.show()


# Create a window and add charts
root = tk.Tk()
root.title("Dashboard")
root.geometry('1200x700')
root.resizable()

side_frame = tk.Frame(root, width="300", height='700', bg="#024959")
side_frame.pack(side="right", fill="y")

label = tk.Label(side_frame, text="Easy A", bg="#024959", fg="#FFF", font=35)
label.pack(pady=20, padx=100)

class_code_label = tk.Label(side_frame, text="Select Year", bg="#024959", fg="#FFF", font=35)
class_code_label.pack(pady=20, padx=100)





# Year DropDown
year_dropdown_var = tk.StringVar(root)
year_dropdown_var.set("No year selected")
years = ['2013', '2014', '2015', '2016']
year_dropdown = tk.OptionMenu(side_frame, year_dropdown_var, *years)
year_dropdown_var.set(year_dropdown)
year_dropdown.pack(side="top", fill="none")

class_code_label = tk.Label(side_frame, text="Select Class Code", bg="#024959", fg="#FFF", font=35)
class_code_label.pack(pady=20, padx=100)

# Class Code DropDown
class_dropdown_var = tk.StringVar(root)
class_dropdown_var.set("No Class Code Selected")
class_codes = ["ANTH", "ART", "BIO", "CHEM", "CS", "ECON", "PHYS"]
class_dropdown = tk.OptionMenu(side_frame, class_dropdown_var, *class_codes)
class_dropdown_var.set(class_dropdown)
class_dropdown.pack(side="top", fill="none")

# Text input
class_num_var = tk.StringVar(root)
class_num = tk.Entry(side_frame, textvariable = class_num_var)
class_num_var.set(class_num)
class_num_label = tk.Label(side_frame, text = "Enter Course Number: ", bg="#024959", fg="#FFF", font=35)
class_num_label.pack(pady=20, padx=10)
class_num.pack(side="top", fill="none")




# Chart grid
charts_frame = tk.Frame(root, width="900", height='700')
charts_frame.pack(side="left", fill="x")

upper_frame = tk.Frame(charts_frame, width="900", height='350')
upper_frame.pack(fill="both", expand=True)

canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="x")

canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="right", fill="x")


lower_frame = tk.Frame(charts_frame, width="900", height="350")

canvas3 = FigureCanvasTkAgg(fig3, lower_frame)
canvas3.draw()
canvas3.get_tk_widget().pack(side="left", fill="x")

lower_frame.pack(fill="both", expand=True)

canvas4 = FigureCanvasTkAgg(fig4, lower_frame)
canvas4.draw()
canvas4.get_tk_widget().pack(side="right", fill="x")

# Function for the button to retrieve user inputs
def get_val():
    vals = { 
        "Year": year_dropdown_var.get(),
        "Class_Code": class_dropdown_var.get(),
        "Course_Number": class_num_var.get()
    }
    print(vals)
    return vals

# Submit button
button = tk.Button(side_frame, text='Submit', command=lambda: (get_val()))
button.pack(side="top", fill="none", pady=20)


root.mainloop()
