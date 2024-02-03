"""
Author: Jose Renteria

README: Main container for all UI components that get generated. Components are rendered in hierarchical order. 

notes: If you want to see the functions, see ui.py
"""

# from data import class_data, years, courses
from Modules.ui import *
from Modules.StyledGraph import GenerateGraph


def UI(averages):
    years = ['Fall 2013', 'Fall 2014', 'Winter 2015', 'Spring 2016']

    # Generate Root TK Window
    root = gen_root()
    # Side Frame, will be used as a root for other components
    side_frame = gen_side_frame(root, 300, 700, '#024959')
    side_frame_label = gen_label(side_frame, "Easy A", "#024959", "#FFF", 35)
    # Year selection label and drop down menu
    class_code_label = gen_label(side_frame, "Select Term", "#024959", "#FFF", 35)
    year_menu = gen_dropdown(root, side_frame, "No Year Selected", years)
    # Class selection label and drop down menu
    class_code_label = gen_label(side_frame, "Select Class Code","#024959", "#FFF", 35)
    class_menu = gen_text_input(root, side_frame)
    key = class_menu[1].get()
    # Label and text box for user input
    user_input_label = gen_label(side_frame, "Enter Course Number", "#024959", "#FFF", 35)
    user_input = gen_text_input(root, side_frame)
     # Run the main loop
    graph_frame = gen_frame(root, 900, 900)
    # upper_frame = gen_frame(graph_frame, 900, 350)
    
    # fig1 = gen_graph(class_data, "Fall 2023", "", "Percent Grade Given")
    # # c1 = gen_canvas(fig1, upper_frame, 'left')
    # fig2 = gen_graph(class_data, "Fall 2023", "", "Percent Grade Given")
    # # c2 = gen_canvas(fig2, upper_frame, 'right')
    # # lower_frame = gen_frame(graph_frame, 900, 350)
    # fig3 = gen_graph(class_data, "Fall 2023", "", "Percent Grade Given")
    # # c3 = gen_canvas(fig3, lower_frame, 'left')
    # fig4 = gen_graph(class_data, "Fall 2023", "", "Percent Grade Given")
    # # c4 = gen_canvas(fig4, lower_frame, 'right')
    # instructor_label = gen_label(side_frame, 'Regular Faculty', "#024959", "#FFF", 35)

    check_instructors = gen_checkbox(side_frame)

    # Submit button
    
    submit_button = gen_button(side_frame, "Submit", lambda: GenerateGraph(averages, send_obj(year_menu, class_menu, user_input, check_instructors)))

    root.mainloop()