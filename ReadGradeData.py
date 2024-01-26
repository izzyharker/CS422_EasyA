"""
Author: Izzy Harker
Date: 1/21/24
Description: Contains a class which reads data from the gradedata.txt file into a dictionary

Notes: 
- now works with original gradedata.js file
- breaks on keyword "function" keyword to indicate end of data (or EOF)
"""

class readGradeData():
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}

        self.read_data()

    def get_data(self):
        return self.data

    def read_data(self):
        # open file and read lines
        raw_data = open(self.filepath, "r")
        raw_data_lines = raw_data.readlines()

        raw_data.close()

        # set current key and index to default values
        current_key = ""
        crn_index = 0

        # iterate through lines of file
        for raw_line in raw_data_lines:
            # strip newline and , chars
            current_line = raw_line.strip().strip(",\n")

            # check if we've reached the end of the data
            if "function" in current_line:
                break

            # split line by : and remove spaces, whitespace
            current_line_data = []
            for token in current_line.split(":"):
                current_line_data.append(token.replace("'", "").strip())

            # if no : found and we are between class codes
            if len(current_line_data) == 1:
                if current_key != "":
                    for char in current_line_data[0]:
                        if char == "[":
                            self.data[current_key] = []
                        elif char == "{" and current_key != "":
                            self.data[current_key].append({})
                            crn_index += 1
                        elif char == "]":
                            current_key = ""
            # otherwise, we have a data entry!
            elif len(current_line_data) == 2:
                # if we find a new class code, process it
                if current_key == "":
                    current_key = current_line_data[0]
                    crn_index = 0
                    for char in current_line_data[1]:
                        if char == "[":
                            self.data[current_key] = []
                        elif char == "{":
                            self.data[current_key].append({})
                            crn_index += 1
                        elif char == "]":
                            current_key = ""
                # otherwise enter data into current class code
                else:
                    self.data[current_key][crn_index - 1][current_line_data[0]] = current_line_data[1]

    def reformatForTermPrio(self):
        """
        Reformats data dictionary to have term as the top level
        
        Returns:
            Reformatted dictionary
        """
        reformatted_data = {}
        for classid, sections in self.data.items():
            for section in sections:
                term = section["TERM_DESC"]
                section.pop("TERM_DESC")
                if term not in reformatted_data.keys():
                    reformatted_data[term] = {}
                
                reformatted_data[term][classid] = section
        
        return reformatted_data
                

# Testing code for the class
    
grade_data_container = readGradeData("./media/gradedata.js")
grade_data = grade_data_container.get_data()

print(grade_data_container.data["CIS415"])
print()
print(grade_data["CIS415"])
print()
print(grade_data["MATH261"])

reformatted_data = grade_data_container.reformatForTermPrio()

print()
print(reformatted_data["Spring 2014"]["CIS415"])
print()