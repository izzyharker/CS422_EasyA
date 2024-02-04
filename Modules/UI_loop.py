"""
Author: Jose Renteria

README: Main container for all UI components that get generated. Components are rendered in hierarchical order. 

notes: If you want to see the functions, see ui.py
"""

from Modules.data import class_data, years, courses
from Modules.ui import *
from Modules.GenerateGraph import GenerateGraph

def UI(*averages):

    app = App("Easy A")
    return app

if __name__ == '__main__':
    UI()