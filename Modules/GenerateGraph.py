from Modules.ManipGradeData import applyFilter, read_average_grades
from Modules.StyledGraph import StyledGraph

def GenerateGraph(filter):
    """
    filter in this format (TERM_DESC is optional): {
        'TERM_DESC': year[1].get(),
        'COURSE_CODE': f'{course[1].get()}{txt[1].get()}',
        'regular_instructors': checkbox[1].get()
    }
    """
    # read data from file
    averages = read_average_grades("Data/average_grades.txt")

    # apply filter to data
    filtered_data = applyFilter(averages, filter)

    # print(filtered_data)

    # manipulate labels, if applicable
    # if the keys used below aren't included in a specific filter, they default to True, False respectively
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