import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from data import class_data, inventory_data, product_data, sales_year_data, inventory_month_data


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
root.state('zoomed')

side_frame = tk.Frame(root, bg="#024959")
side_frame.pack(side="right", fill="y")

label = tk.Label(side_frame, text="Easy A", bg="#024959", fg="#FFF", font=35)
label.pack(pady=20, padx=100)

label2 = tk.Label(side_frame, text="Select Year", bg="#024959", fg="#FFF", font=35)
label2.pack(pady=20, padx=100)



def get_val():
    print(dropdown_var.get())


# DropDown
dropdown_var = tk.StringVar()
dropdown_var.set("No year selected")
years = ['2013', '2014', '2015', '2016']
dropdown = tk.OptionMenu(side_frame, dropdown_var, *years)
dropdown.pack(side="top", fill="none")

button = tk.Button(side_frame, text='Submit', command=get_val)
button.pack(side="bottom", fill="none")

charts_frame = tk.Frame(root)
charts_frame.pack()

upper_frame = tk.Frame(charts_frame)
upper_frame.pack(fill="both", expand=True)

canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)


lower_frame = tk.Frame(charts_frame)

canvas3 = FigureCanvasTkAgg(fig3, lower_frame)
canvas3.draw()
canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)

lower_frame.pack(fill="both", expand=True)

canvas4 = FigureCanvasTkAgg(fig4, lower_frame)
canvas4.draw()
canvas4.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()