"""
Author: Izzy Harker
Date: 1/14/24
Description: Contains class definition and methods for generating a stylized graph displaying grade data.
"""
import matplotlib.pyplot as plt

class StyledGraph():
    image_out_folder = "./media/"

    def __init__(self, filename = "temp"):
        # styling parameters
        self.style = None
        self.size = (8, 6)

        self.out_file = filename
        self.filetype = "png"
        self.dpi = 300

        self.title = "Test"

    def graph(self, data: list[float], teachers: list[str]):
        """
        Generates a bar plot for the given data and saves it to the media folder as a png

        (For now)   data should be a list of percentages
                    teachers should be a list of teachers, corresponding to data
        """
        #set up figure and axes
        fig = plt.figure(figsize=self.size)
        ax = plt.axes()

        # plot data
        ax.bar(teachers, data, color=plt.get_cmap("Set2").colors, width = 0.6)

        # formatting graph
        ax.set_title(self.title, fontweight = "bold", pad=12.0)

        ax.spines["left"].set_linewidth(2)
        ax.spines["bottom"].set_linewidth(2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        ax.set_yticklabels(ax.get_yticklabels(), weight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), weight='bold')
        ax.tick_params(axis='both', width = 2, length = 6)

        ax.set_ylabel("%A's given", {"weight": "bold"})
        ax.set_ylim(bottom = 0, top = 100)
        ax.set_yticks(ticks=range(0, 101, 20))

        ax.grid(False)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout(pad = 4)

        # save
        fig.savefig(fname=StyledGraph.image_out_folder + self.out_file + "." + self.filetype, dpi=self.dpi, format=self.filetype)

        # plt.show()


# in-file testing for styling purposes
test_data = [40, 22, 37, 91, 56]
test_teachers = ["Wills", "Childs", "Hornof", "Erickson", "Li"]

graph = StyledGraph()
graph.graph(test_data, test_teachers)
