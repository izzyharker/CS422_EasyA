from Modules.ReadGradeData import loadData
from Modules.UI_loop import UI
from Modules.StyledGraph import GenerateGraph

def main():
    # load data
    averages = loadData("Data/gradedata.js")

    # start UI loop
    # UI(averages)
    filt = {"TYPE": "level", "DEPT": "MATH", "COURSE": "400", "REG_INSTR": 0, "APREC_YES": True, "SHOW_INSTR": True, "SHOW_INSTR_CLASSES_TAUGHT": False}

    fig = GenerateGraph(averages, filt)

    fig.savefig(fname="test.png", dpi=300, format="png")

    return 0


if __name__ == "__main__":
    main()