"""
Author: Izzy Harker
Date Updated: 2/3/24
Description: Contains class definition and methods for generating a stylized graph displaying grade data.
"""
import matplotlib.pyplot as plt

class StyledGraph():

    def __init__(self, title: str = ""):
        """
        Defines default styling parameters, including filetype and size.

        Args:
            title (str): the title of the output graph. If not passed, the graph has no title. 
        """
        self.style = None
        self.size = (8, 6)

        self.filetype = "png"
        self.dpi = 300

        self.title = title

    def graph(self, data: list[tuple], aprec=True):
        """
        Generates a bar plot for the given data and saves it to the media folder as a png

        Args: 
            data (list[tuple]): list of tuples (y, x). The x-value is shown on the x-axis, and the y-value represents the height of the bar.
            aprec (bool): defaults to True, defines the y-axis label. If True, the label is "% A's Given", and if False, the label is "% D/F's Given". 

        Returns:
            fig (matplotlib.pyplot.fig): the graph generated from the data.
        """
        #set up figure and axes
        fig = plt.figure(figsize=self.size)
        ax = plt.axes()

        # pull the x, y from the given data into separate lists
        grades = [item[0] for item in data]
        x_labels = [item[1] for item in data]

        # plot data
        ax.bar(x_labels, grades, color=plt.get_cmap("Set2").colors)

        # apply formatting to graph - this is donw for easier comprehension of the data
        # set graph title
        ax.set_title(self.title, fontweight = "bold", pad=12.0)

        # remove the top and right borders of the graph
        ax.spines["left"].set_linewidth(2)
        ax.spines["bottom"].set_linewidth(2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # set tick labels to bold and increase tick size on both axes
        ax.set_yticklabels(ax.get_yticklabels(), weight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), weight='bold')
        ax.tick_params(axis='both', width = 2, length = 6)

        # set label of y-axis based on given arg
        if aprec:
            ylabel = "% A's Given"
        else:
            ylabel = "% D/F's Given"
        ax.set_ylabel(ylabel, {"weight": "bold"})

        # set y limits to correspond to percentages
        ax.set_ylim(bottom = 0, top = 100)

        # define well-spaced ticks on y-axis
        ax.set_yticks(ticks=range(0, 101, 20))

        # remove grid from graph
        ax.grid(False)

        # rotate x-labels (instructor names, typically) to be more horizontal
        plt.xticks(rotation=45, ha="right")

        # reformat for better visibility
        plt.tight_layout(pad = 2)

        # return graph
        return fig
