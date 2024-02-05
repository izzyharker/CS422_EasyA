from Modules.ManipGradeData import applyFilter, read_average_grades
from Modules.StyledGraph import StyledGraph

def GenerateGraph(filter):
    """
    Accepts a filter and produces a graph.

    Args: 
        filter (dict): Contains the filter parameters

    Returns:
        fig (matplotlib.pyplot.fig): Graph
    """
    # normalize filter type to lowercase
    filter["TYPE"] = filter["TYPE"].lower()
    # print(filter)

    # change instructor filter to bool
    if filter["SHOW_INSTR"] == 1:
        filter["SHOW_INSTR"] = False
    else:
        filter["SHOW_INSTR"] = True

    # read data from file
    average_grades_file = open("Data/average_grades.txt")
    averages = average_grades_file.readlines()

    average_grades_file.close()

    # print(averages)

    # apply filter to data
    filtered_data = applyFilter(averages, filter)

    # print(filtered_data)

    # manipulate labels, if applicable
    # if the keys used below aren't included in a specific filter, they default to True, False respectively
    try:
        if filter["SHOW_INSTR"]:
            try:
                if filter["SHOW_INSTR_CLASSES_TAUGHT"]:
                    filtered_data = {label.split(' ')[0] + " " + label.split(' ')[-1] + " (" + str(info["Total Classes"]) + ")": info for label, info in filtered_data.items()}
                else:
                    filtered_data = {label.split(' ')[0] + " " + label.split(' ')[-1]: info for label, info in filtered_data.items()}
            except KeyError:
                filtered_data = {label.split(' ')[0] + " " + label.split(' ')[-1]: info for label, info in filtered_data.items()}
                pass
    except KeyError:
        pass

    # format graph title depending on filter type
    if filter["TYPE"] == 'department':
        title = "All " + filter["DEPT"] + " Classes"
    elif filter["TYPE"] == 'level':
        title = f"All {filter['DEPT']} {filter['COURSE'][0]}00-level"
    elif filter["TYPE"] == 'class':
        title = f"{filter['DEPT']} {filter['COURSE']}"
    else:
        title = ""

    # isolate the %A, %D/F depending on the filter status, and reorganize the data for graphing
    # this also sorts the data in descending order
    if filter["APREC_YES"]:
        # if true, graph aprec
        data = sorted([(info["Aprec Avg"], label) for label, info in filtered_data.items()], reverse=True)
    else:
        # graph failprec
        data = sorted([(info["Failprec Avg"], label) for label, info in filtered_data.items()], reverse=True)

    # if there are too many data entries, including all of them will make them appear too small, so only show top 12
    if len(data) > 12:
        data = data[:12]

    # create a graph object with the appropriate title
    graph = StyledGraph(title = title)

    # generate the graph
    fig = graph.graph(data, filter["APREC_YES"])

    # return the fig
    return fig