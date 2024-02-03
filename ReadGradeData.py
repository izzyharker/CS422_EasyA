"""
Author: Izzy Harker, Carter Young
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

    def filter_by_majors(self, majors_to_keep):
        """Filters data to include only specified majors

            Args:
            majors_to_keep (list)

            Returns:
            Filtered class data
        """
        filtered_data = {}
        for key in self.data:
            if any(key.startswith(major) for major in majors_to_keep):
                filtered_data[key] = self.data[key]
        return filtered_data

    def save_data_to_file(self, data, filename):
        """
        Saves data to a file

        Args:
            data (dict): data to be saved
            filename(str): where we are saving

        """
        with open(filename, 'w') as file:
            for key, value in data.items():
                file.write(f'"{key}": [\n')
                for section in value:
                    file.write('    {\n')
                    for inner_key, inner_value in section.items():
                        file.write(f'        "{inner_key}": "{inner_value}",\n')
                    file.write('    },\n')
                file.write('],\n')

    def remove_elements(self, elements_to_remove):
        """ Removes unnecessary data fields from the grade data

        Args:
        elements_to_remove (list): list of keys from each entry
        """
        for key in self.data:
            for section in self.data[key]:
                for element in elements_to_remove:
                    section.pop(element, None)  # Removes element if it is present

    def store_aprec_as_percent(self):
        """ Converts 'aprec' values from numeric strings to percentage strings for graphing ease. """
        for key in self.data:
            for section in self.data[key]:
                if 'aprec' in section:
                    # Just add %
                    section['aprec'] = f"{section['aprec']}%"

    def calculate_failprec(self):
        """ Calculates 'failprec' as sum of 'dprec' and 'fprec' for each section. """
        for key in self.data:
            for section in self.data[key]:
                dprec = float(section.get('dprec', '0'))  # Convert to float, default to 0 if not there
                fprec = float(section.get('fprec', '0'))  # Convert to float, default to 0 if not present
                section['failprec'] = f"{dprec + fprec:.2f}%"

    def reformat_name(self):
        """ This function reformats the instructor name to be the same as the web scrape. """
        for key in self.data:
            for section in self.data[key]:
                if 'instructor' in section:
                    name_parts = section['instructor'].split(', ')
                    if len(name_parts) == 2:
                        last_name, first_middle_name = name_parts
                        section['instructor'] = f"{first_middle_name} {last_name}"


def read_and_normalize_faculty_names(filename):
    """ This function reads the names from the web scrape and resolves discrepancies. """
    faculty_names = set()
    # Read in faculty_names.txt
    with open(filename, 'r') as file:
        for line in file:
            # Normalize name by converting to lowercase
            normalized_name = line.strip().lower()
            # Split name into parts
            parts = normalized_name.split()
            # Extract only first and last name
            if len(parts) >= 2:
                first_name, last_name = parts[0], parts[-1]
                faculty_names.add((first_name, last_name))
    return faculty_names


def include_faculty_status(data, faculty_names):
    """ This function integrates faculty identification into the work flow by comparing loaded data to scrape. """
    for key in data:
        for section in data[key]:
            # Our key is instructor name
            if 'instructor' in section:
                # Normalize and split name as before
                normalized_name = section['instructor'].lower().split(', ')
                # Case: instructor doesn't have a middle name
                if len(normalized_name) == 2:
                    last_name, first_middle_name = normalized_name
                # Case: instructor does have a middle name
                else:
                    name_parts = section['instructor'].split()
                    first_name, last_name = name_parts[0].lower(), name_parts[-1].lower()

                first_name = first_middle_name.split() if ',' in section['instructor'] else first_name
                # Check against faculty status and assign
                # 1 for regular faculty, 0 otw
                section['faculty_status'] = 1 if (first_name, last_name) in faculty_names else 0


def calculate_avg(data):
    """ Calculate the average of key fields per class and per instructor. """
    averages = {}
    for course, sections in data.items():  # Filter on course
        for section in sections:
            instructor = section.get('instructor', 'Unknown Instructor')  # Filter on instructor and course

            # Safely get 'aprec' and 'failprec'
            aprec = float(section.get('aprec', '0').rstrip('%'))  # Removing % and converting to float
            failprec = float(section.get('failprec', '0').rstrip('%'))  # Removing % and converting to float

            # Init counts
            if (course, instructor) not in averages:
                # Default to 0 if not there
                averages[(course, instructor)] = {'aprec_sum': 0, 'failprec_sum': 0, 'count': 0}

            averages[(course, instructor)]['aprec_sum'] += aprec  # Count aprec per course per instructor
            averages[(course, instructor)]['failprec_sum'] += failprec  # Count failprec per course per instructor
            averages[(course, instructor)]['count'] += 1  # Store num times instructor teaches class

    # Calculate averages
    for key in averages:
        aprec_avg = averages[key]['aprec_sum'] / averages[key]['count']  # Calculate aprec avg per class/instructor
        failprec_avg = averages[key]['failprec_sum'] / averages[key]['count']  # Calculate %D/F avg per class/instructor
        averages[key] = {  # These are our values per class per instructor
             'aprec_avg': aprec_avg,
             'failprec_avg': failprec_avg,
             'teaching_count': averages[key]['count'],
        }

    # Ensure we have regular faculty labels
    attach_faculty_status(data, averages)

    return averages


def attach_faculty_status(original_data, averages):
    """ Attaches faculty status to each instructor's averages. """
    for course, sections in original_data.items():
        for section in sections:
            instructor = section.get('instructor', 'Unknown Instructor')
            faculty_status = section.get('faculty_status', 0)  # Def to 0
            # Update matching record in averages with faculty status
            if (course, instructor) in averages:
                averages[(course, instructor)]['faculty_status'] = faculty_status


def save_averages_to_file(averages, filename):
    """ Save averages to text file """
    with open(filename, 'w') as file:
        for (course, instructor), scores in averages.items():
            line = f"Course: {course}, Instructor: {instructor}, Taught Count: {scores['teaching_count']}, Aprec Avg: {scores['aprec_avg']:.2f}%, Failprec Avg: {scores['failprec_avg']:.2f}%, Faculty Status: {scores['faculty_status']}\n"
            file.write(line)


# Define elements to remove
elements_to_remove = ["crn", "bprec", "cprec", "dprec", "fprec"]

# Define majors to keep
majors_to_keep = ["BI", "CH", "CIS", "HPHY", "MATH", "NEU", "PHYS", "PSY"]

# Load data
grade_data_container = readGradeData("gradedata.txt")

# Call aprec -> %
grade_data_container.store_aprec_as_percent()

# Call calc_failprec
grade_data_container.calculate_failprec()

# Remove superfluous elements
grade_data_container.remove_elements(elements_to_remove)

# Reformat instructor names
grade_data_container.reformat_name()

# Filter out non-natural science majors
filtered_grade_data = grade_data_container.filter_by_majors(majors_to_keep)

faculty_names = read_and_normalize_faculty_names('faculty_names.txt')

include_faculty_status(filtered_grade_data, faculty_names)

# Calc avg
average_scores = calculate_avg(filtered_grade_data)

# Output filtered data
grade_data_container.save_data_to_file(filtered_grade_data, "filtered_gradedata.txt")

# Output average data
save_averages_to_file(average_scores, "average_grades.txt")

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