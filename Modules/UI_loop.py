"""
Author: Jose Renteria

README: Main container for all UI components that get generated. Components are rendered in hierarchical order. 

notes: If you want to see the functions, see ui.py
"""

from data import class_data, years, courses
from ui import *
from StyledGraph import GenerateGraph


def UI(*averages):

    app = App("Easy A")
    return app

if __name__ == '__main__':
    UI()