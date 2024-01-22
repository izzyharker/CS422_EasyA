"""
Author: Izzy Harker
Date: 1/21/24
Description: Contains a class which reads data from the gradedata.txt file into a dictionary

Notes: 
- gradedata.txt is the same as gradedata.js, I just deleted the function at the end for my sanity
- this should work with any similar files, as long as they maintain json-like formatting. specifically, 
    as long as attributes are in the form [key]:[val] and on the same line, it should be fine
- i had other notes but i am forgetting them. anyway
"""

class readGradeData():
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}

        self.read_data()

    def get_data(self):
        return self.data

    def read_data(self):
        raw_data = open(self.filepath, "r")
        raw_data_lines = raw_data.readlines()

        raw_data.close()

        current_key = ""
        crn_index = 0

        for raw_line in raw_data_lines:
            current_line = raw_line.strip().strip(",\n")

            current_line_data = []
            for token in current_line.split(":"):
                current_line_data.append(token.replace("'", "").strip())

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
            elif len(current_line_data) == 2:
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
                else:
                    self.data[current_key][crn_index - 1][current_line_data[0]] = current_line_data[1]

    def reformatForTermPrio(self):
        reformatted_data = {}
        for classid, sections in self.data.items():
            for section in sections:
                term = section["TERM_DESC"]
                section.pop("TERM_DESC")
                if term not in reformatted_data.keys():
                    reformatted_data[term] = {}
                
                reformatted_data[term][classid] = section
        
        return reformatted_data
                

"""
Testing code for the class

grade_data_container = readGradeData("gradedata.txt")
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
"""