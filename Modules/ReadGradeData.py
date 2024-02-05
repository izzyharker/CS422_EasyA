"""
Author: Izzy Harker, Carter Young
Date Updated: 2/3/24
Description: Contains a class which loads data from the gradedata.txt file into a dictionary and processes it for filtering.

Notes: 
- breaks on keyword "function" keyword in addition to EOF to indicate end of data
- works with the original gradedata.js file or any similarly formatted json-esque file.
"""

class readGradeData():
    # static class elements
    # Define elements to remove
    elements_to_remove = ["crn", "bprec", "cprec", "dprec", "fprec"]

    # Define majors to keep
    majors_to_keep = ["BI", "CH", "CIS", "GEOG", "HPHY", "MATH", "NEUR", "PHYS", "PSY"]

    def __init__(self, filepath):
        """
        Defines filepath and initializes data. Calls read_data
        """
        self.filepath = filepath

        self.data = {}

        self.read_data()

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

            # if no : found and we are between class codes, setup the new class in the dict
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
            # otherwise, we have a data entry for the current class
            elif len(current_line_data) == 2:
                # if we find a new class code and don't currently have a class code, setup the new class
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

    def filter_by_majors(self, majors_to_keep):
        """Filters data to include only specified majors

            Args:
            majors_to_keep (list)

            Returns:
            Filtered class data
        """
        # initialize empty dict
        filtered_data = {}
        
        # iterate over the complete data set
        for key in self.data:
            # if the key is contained in the list of majors, added it to the filtered_data 
            if any(key.startswith(major) for major in majors_to_keep):
                filtered_data[key] = self.data[key]
        # set self.data to be equal to filtered_data
        self.data = filtered_data

    def save_data_to_file(self, data, filename):
        """
        Saves data to a file. [deprecated]

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
        # iterate over the keys 
        for key in self.data:
            for section in self.data[key]:
                # convert the values to % form
                if 'aprec' in section:
                    # Just add %
                    section['aprec'] = f"{section['aprec']}%"

    def calculate_failprec(self):
        """ Calculates 'failprec' as sum of 'dprec' and 'fprec' for each section. """
        # iterate over the keys
        for key in self.data:
            for section in self.data[key]:
                # combine and convert the fail percentage (D/F) to %
                dprec = float(section.get('dprec', '0'))  # Convert to float, default to 0 if not there
                fprec = float(section.get('fprec', '0'))  # Convert to float, default to 0 if not present
                section['failprec'] = f"{dprec + fprec:.2f}%"

    def reformat_name(self):
        """ This function reformats the instructor name to be the same as the web scrape. """
        for key in self.data:
            for section in self.data[key]:
                if 'instructor' in section:
                    # reformat the instructor name to match the web scrape
                    name_parts = section['instructor'].split(', ')
                    if len(name_parts) == 2:
                        last_name, first_middle_name = name_parts
                        section['instructor'] = f"{first_middle_name} {last_name}"


    def include_faculty_status(self, faculty_names):
        """ This function integrates faculty identification into the work flow by comparing loaded data to scrape. Directly edits the self.data object
        
        Args:
            faculty_names (list[tuple]): contains (first name, last name) of the faculty, taken from the web scrape

        Returns:
            None
        """
        # iterate over the keys
        for key in self.data:
            for section in self.data[key]:
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
                    # 1 for regular faculty, 0 otherwise
                    section['faculty_status'] = 1 if (first_name, last_name) in faculty_names else 0

    def attach_faculty_status(self, averages):
        """ Attaches faculty status to each instructor's averages. 
        
        Args:
            averages (dict): dict containing the averaged data values per course and instructor    

        Returns: 
            None
        """
        # iterate over the courses/sections in self.data
        for course, sections in self.data.items():
            for section in sections:
                # check if the instructor exists
                instructor = section.get('instructor', 'Unknown Instructor')

                # default faculty status to 0 if it doesn't already exist
                faculty_status = section.get('faculty_status', 0)  # Def to 0
                # Update matching record in averages with faculty status
                if (course, instructor) in averages:
                    averages[(course, instructor)]['faculty_status'] = faculty_status

    def calculate_avg(self):
        """ Calculate the average of key fields per class and per instructor. """
        averages = {}
        for course, sections in self.data.items():  # Filter on course
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
        self.attach_faculty_status(averages)

        return averages
    
def convert_data_to_common_format(averages: dict):
    """Converts data to format used by filtering methods. This is the same as the format output to the average_grades.txt file
    
    Args:
        averages (dict): contains the average grade data.

    Returns:
        data (list): Reformatted version of averages
    """
    
    # initialize to empty list
    data = []

    # iterate over the information in averages and save each as a line
    for (course, instructor), scores in averages.items():
        line = f"Course: {course}, Instructor: {instructor}, Taught Count: {scores['teaching_count']}, Aprec Avg: {scores['aprec_avg']:.2f}%, Failprec Avg: {scores['failprec_avg']:.2f}%, Faculty Status: {scores['faculty_status']}"
        
        # append each line to the data
        data.append(line)

    # return the reformatted data object
    return data

def save_averages_to_file(averages, filename):
    """ Save averages to text file """
    with open(filename, 'w+') as file:
        for (course, instructor), scores in averages.items():
            line = f"Course: {course}, Instructor: {instructor}, Taught Count: {scores['teaching_count']}, Aprec Avg: {scores['aprec_avg']:.2f}%, Failprec Avg: {scores['failprec_avg']:.2f}%, Faculty Status: {scores['faculty_status']}\n"
            file.write(line)

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

def loadData(filename: str):
    """
    Given a filename, loads the data from the filename into a dictionary. Performs preliminary processing to average the grades, remove unnecessary elements, and cross-check instructor data. Writes the final data to a Data/average_grades.txt for later use.

    Args: 
        filename (str): the name of the data file. If the file cannot be found in a relative repository, this should be the absolute local path to the data file.
    """
    # load data
    try:
        grade_data_container = readGradeData(filename)
    except FileNotFoundError:
        print("Grade file not found. exiting...")
        exit()

    # convert values to correct percentages
    grade_data_container.store_aprec_as_percent()
    grade_data_container.calculate_failprec()

    # remove superfluous elements
    grade_data_container.remove_elements(readGradeData.elements_to_remove)

    # reformat instructor names
    grade_data_container.reformat_name()

    # filter non-natural science majors
    grade_data_container.filter_by_majors(readGradeData.majors_to_keep)

    # cross-examine faculty names with the scrape results
    faculty_names = read_and_normalize_faculty_names("Data/faculty_names.txt")

    # add faculty status to each instructor
    grade_data_container.include_faculty_status(faculty_names)

    # calculate average scores
    average_scores = grade_data_container.calculate_avg()

    # save average grades to a file for later filtering
    save_averages_to_file(average_scores, "Data/average_grades.txt")