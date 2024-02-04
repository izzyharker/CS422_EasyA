"""
Author: Izzy Harker
Date Updated: 2/3/24
Description: Contains class definition and methods for generating a stylized graph displaying grade data.
"""
import matplotlib.pyplot as plt
from Modules.ManipGradeData import applyFilter

class StyledGraph():
    image_out_folder = "./media/"

    def __init__(self, title = "", filename = "temp"):
        # styling parameters
        self.style = None
        self.size = (8, 6)

        self.out_file = filename
        self.filetype = "png"
        self.dpi = 300

        self.title = title

    def graph(self, data: list[tuple], aprec=True):
        """
        Generates a bar plot for the given data and saves it to the media folder as a png

        (For now)   data is a list of tuples, [(value, x-label), ..]
        """
        #set up figure and axes
        fig = plt.figure(figsize=self.size)
        ax = plt.axes()

        grades = [item[0] for item in data]
        x_labels = [item[1] for item in data]

        # plot data
        ax.bar(x_labels, grades, color=plt.get_cmap("Set2").colors)

        # formatting graph
        ax.set_title(self.title, fontweight = "bold", pad=12.0)

        ax.spines["left"].set_linewidth(2)
        ax.spines["bottom"].set_linewidth(2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        ax.set_yticklabels(ax.get_yticklabels(), weight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), weight='bold')
        ax.tick_params(axis='both', width = 2, length = 6)

        if aprec:
            ylabel = "% A's Given"
        else:
            ylabel = "% D/F's Given"
        ax.set_ylabel(ylabel, {"weight": "bold"})

        ax.set_ylim(bottom = 0, top = 100)
        ax.set_yticks(ticks=range(0, 101, 20))

        ax.grid(False)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout(pad = 4)

        # save
        # fig.savefig(fname=StyledGraph.image_out_folder + self.out_file + "." + self.filetype, dpi=self.dpi, format=self.filetype)
        return fig
        # plt.show()

def GenerateGraph(averages, filter):
    """
    filter in this format (TERM_DESC is optional): {
        'TERM_DESC': year[1].get(),
        'COURSE_CODE': f'{course[1].get()}{txt[1].get()}',
        'regular_instructors': checkbox[1].get()
    }
    """
    # apply filter to data
    filtered_data = applyFilter(averages, filter)

    # print(filtered_data)

    # manipulate labels, if applicable
    try:
        if filter["SHOW_INSTR"]:
            try:
                if filter["SHOW_INSTR_CLASSES_TAUGHT"]:
                    filtered_data = {label + " (" + str(info["Total Classes"]) + ")": info for label, info in filtered_data.items()}
            except KeyError:
                pass
    except KeyError:
        pass

    # format graph title depending on filter type
    if filter["TYPE"] == 'department':
        title = "All " + filter["DEPT"] + " Classes"
    elif filter["TYPE"] == 'level':
        title = f"All {filter['DEPT']} {filter['COURSE'][0]}00-level"
    elif filter["TYPE"] == 'course':
        title = f"{filter['DEPT']} {filter['COURSE']}"
    else:
        title = ""

    # isolate the parts of data that we want
    if filter["APREC_YES"]:
        # if true, graph aprec
        data = sorted([(info["Aprec Avg"], label) for label, info in filtered_data.items()], reverse=True)
    else:
        # graph failprec
        data = sorted([(info["Failprec Avg"], label) for label, info in filtered_data.items()], reverse=True)

    # if there are too many data entries, including all of them will be too much for the graph, so only show top 10
    if len(data) > 12:
        data = data[:12]

    graph = StyledGraph(title = title)

    fig = graph.graph(data, filter["APREC_YES"])
    return fig
