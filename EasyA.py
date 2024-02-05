from Modules.ReadGradeData import loadData
from Modules.UI_loop import UI
from Modules.GenerateGraph import GenerateGraph

def main():
    start_mode = input("Start program? (type 'y' to start, 'u' to update data, 'n' to exit): ")

    if start_mode == 'y':
        # load data
        file_path_to_data = open("Data/PathToDataFile", "r")
        path_to_data = file_path_to_data.readline()
        path_to_data.strip()
        file_path_to_data.close()

        try: 
            loadData(path_to_data)
        except FileNotFoundError:
            # if file not found, exit
            print("ERROR: Data file not found")
            return

        UI()
        # filt = {"TYPE": "level", "DEPT": "MATH", "COURSE": "400", "REG_INSTR": 0, "APREC_YES": True, "SHOW_INSTR": True, "SHOW_INSTR_CLASSES_TAUGHT": False}

        # fig = GenerateGraph(filt)

        # fig.savefig(fname="test.png", dpi=300, format="png")

    elif start_mode == 'u':
        new_path = input("Please enter the filepath to the new data: ")

        file_path_to_data = open("Data/PathToDataFile", "w")

        if new_path == "reset":
            file_path_to_data.write("Data/gradedata.js")
        else:
            file_path_to_data.write(new_path)
        file_path_to_data.close()

    return 0


if __name__ == "__main__":
    main()