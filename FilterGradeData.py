"""
Author(s): Izzy Harker
Date: 1/14/24
Description: Contains class definition and methods to read, filter, and format data from data file.
"""
from StyledGraph import StyledGraph
from ReadGradeData import readGradeData

class DataFilter():
    def __init__(self, show_number_of_classes: bool = False):
        # metadata for graphing
        self.title = ""
        self.show_number_of_classes_in_label = show_number_of_classes
        
        # formatted data (end result) - this is passed to StyledGraph function
        self.percentages = []
        self.xaxis_labels = []

    def configureAxisLabels(self):
        pass

    def readAndProcessData(self):
        """
        Read and process the data from the data file. This will depend a bit on what format the data is in to begin with.
        """
        pass

    def filterData(self):
        """
        Filter the data
        """
        pass

    def generateGraph(self):
        graph = StyledGraph()
        graph.graph()