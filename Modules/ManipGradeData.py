"""
Author: Carter Young, Izzy Harker
Date Updated: 2/3/24
Description: Reads in average_grades.txt and filters them according to the project description:
1. Department level:
    Function: User specifies a natural science department, and the average_grades.txt is filtered to show %As,
    %Ds/Fs, and total # of times the course was taught for every course.
    Input: average_grades.txt, Department
    Output: dept_{dept name}.txt
2. Class level:
    Function: User specifies a natural science course, and the average_grades.txt is filtered to show %As, %Ds/%Fs,
    and total # of times the course was taught per instructor for the course.
    Input: average_grades.txt, Course
    Output: class_{class name}.txt
3. Level level:
    Function: User specifies a natural science department, and the average_grades.txt is filtered to show %As, %Ds/%Fs,
    and total # of times the course was taught for every course of a specified level.
    Input: average_grades.txt, Department, Level
    Output: level_{department}_{level}.txt
"""

def read_average_grades(filename):
    """ Read in average_grades.txt """
    data = {}  # Set data to empty
    with open(filename, 'r') as file:  # Read data
        for line in file:  # Iterate
            # Split line according to format
            if line.startswith('Course'):
                parts = line.split(',')
                course = parts[0].split(':')[1].strip()
                taught_count = int(parts[2].split(':')[1].strip())
                aprec_avg = float(parts[3].split(':')[1].strip().rstrip('%').strip())
                failprec_avg = float(parts[4].split(':')[1].strip().rstrip('%').strip())

                # Error case: course not in data
                # All fields default to 0
                if course not in data:
                    data[course] = {
                        'total_taught_count': 0,
                        'aprec_avg': 0,
                        'failprec_avg': 0,
                        'count': 0
                    }

                # Treat 'taught_count' as sum
                # Treat 'aprec_avg' as avg
                # Treat 'failprec_avg' as avg
                # +1 Index for counting
                data[course]['total_taught_count'] += taught_count
                data[course]['aprec_avg'] += aprec_avg
                data[course]['failprec_avg'] += failprec_avg
                data[course]['count'] += 1

    for course in data:
        data[course]['aprec_avg'] /= data[course]['count']
        data[course]['failprec_avg'] /= data[course]['count']
        del data[course]['count']  # Remove index

    # Return average data
    return data


def filter_by_course(data, course):
    """ Filters average_data.txt by course. """
    filtered_data = {}  # Sets data to empty
    # Iterate
    for entry in data:
        # Split line according to format
        if entry.startswith('Course: ' + course):
            parts = entry.split(',')
            instructor = parts[1].split(': ')[1].strip()
            taught_count = int(parts[2].split(': ')[1].strip())
            aprec_avg = float(parts[3].split(': ')[1].strip().rstrip('%').strip())
            failprec_avg = float(parts[4].split(': ')[1].strip().rstrip('%').strip())
            faculty_status = int(parts[5].split(': ')[1].strip())

            # Error case: If instructor is not present...
            if instructor not in filtered_data:
                # Default to 0
                filtered_data[instructor] = {'Total Classes': 0, 'Aprec Sum': 0, 'Failprec Sum': 0, 'Faculty Status': 0}

            # Iterate
            filtered_data[instructor]['Total Classes'] += taught_count
            filtered_data[instructor]['Aprec Sum'] += aprec_avg * taught_count
            filtered_data[instructor]['Failprec Sum'] += failprec_avg * taught_count
            filtered_data[instructor]['Faculty Status'] = faculty_status

    # Average out the aprec_avg and failprec_avg
    for instructor in filtered_data:
        total_taught = filtered_data[instructor]['Total Classes']
        faculty_status = filtered_data[instructor]['Faculty Status']
        filtered_data[instructor]['Aprec Avg'] = filtered_data[instructor]['Aprec Sum'] / total_taught if total_taught > 0 else 0
        filtered_data[instructor]['Failprec Avg'] = filtered_data[instructor]['Failprec Sum'] / total_taught if total_taught > 0 else 0

    # Return
    return filtered_data


def filter_by_department(data, department, level=None):
    """ Filters average_data.txt by department and, if selected, level."""
    filtered_data = {}  # Sets data to empty
    # Iterate
    for entry in data:
        # Split line according to format
        if entry.startswith('Course:'):
            parts = entry.split(',')
            course_with_code = parts[0].split(':')[1].strip()
            # Split dept and level appropriately
            course_dept = ''.join(filter(str.isalpha, course_with_code))  # Dept portion are alphabetical
            course_level = ''.join(filter(str.isdigit, course_with_code)) # Dept portion are numerical

            # Checks on two conditions
            # If level is none, consider all levels in department
            # If level is not none, consider only those courses which start with the specified digit
            if course_dept == department and (level is None or course_level.startswith(level)):
                instructor = parts[1].split(': ')[1].strip()
                taught_count = int(parts[2].split(': ')[1].strip())
                aprec_avg = float(parts[3].split(':')[1].strip().rstrip('%').strip())
                failprec_avg = float(parts[4].split(':')[1].strip().rstrip('%').strip())
                faculty_status = int(parts[5].split(': ')[1].strip())

                # Error case: course is not included in filtered_data...
                if instructor not in filtered_data:
                    # Default to 0
                    filtered_data[instructor] = {'Total Classes': 0, 'Aprec Sum': 0, 'Failprec Sum': 0, 'Faculty Status': 0}

                filtered_data[instructor]['Total Classes'] += taught_count
                filtered_data[instructor]['Aprec Sum'] += aprec_avg * taught_count
                filtered_data[instructor]['Failprec Sum'] += failprec_avg * taught_count
                filtered_data[instructor]['Faculty Status'] = faculty_status
                #filtered_data[instructor]['Classes'].append(course_with_code)

    # Iterate through instructors
    for instructor in filtered_data:
        total_taught = filtered_data[instructor]['Total Classes']
        faculty_status = filtered_data[instructor]['Faculty Status']
        filtered_data[instructor]['Aprec Avg'] = filtered_data[instructor]['Aprec Sum'] / total_taught if total_taught > 0 else 0
        filtered_data[instructor]['Failprec Avg'] = filtered_data[instructor]['Failprec Sum'] / total_taught if total_taught > 0 else 0
        del filtered_data[instructor]['Aprec Sum'], filtered_data[instructor]['Failprec Sum']

    # Return
    return filtered_data


"""
Need additional function which shows all courses in a specified department's specified level
"""
def filter_by_department_classes(data, department, level):
    """ Filters average_data.txt by department and, if selected, level."""
    print("calling filter_by_department_classes")
    filtered_data = {}  # Sets data to empty
    # Iterate
    for entry in data:
        # Split line according to format
        if entry.startswith('Course:'):
            parts = entry.split(',')
            course_with_code = parts[0].split(':')[1].strip()
            # Split dept and level appropriately
            course_dept = ''.join(filter(str.isalpha, course_with_code))  # Dept portion are alphabetical
            course_level = ''.join(filter(str.isdigit, course_with_code)) # Dept portion are numerical

            # Checks on two conditions
            # If level is none, consider all levels in department
            # If level is not none, consider only those courses which start with the specified digit
            if course_dept == department and (level is None or course_level.startswith(level)):
                # instructor = parts[1].split(': ')[1].strip()
                taught_count = int(parts[2].split(': ')[1].strip())
                aprec_avg = float(parts[3].split(':')[1].strip().rstrip('%').strip())
                failprec_avg = float(parts[4].split(':')[1].strip().rstrip('%').strip())
                # faculty_status = int(parts[5].split(': ')[1].strip())

                # Error case: course is not included in filtered_data...
                if course_level not in filtered_data:
                    # Default to 0
                    filtered_data[course_level] = {'Total Classes': 0, 'Aprec Sum': 0, 'Failprec Sum': 0, 'Faculty Status': 0}

                filtered_data[course_level]['Aprec Sum'] += aprec_avg
                filtered_data[course_level]['Failprec Sum'] += failprec_avg
                filtered_data[course_level]["Total Classes"] += taught_count
                #filtered_data[instructor]['Classes'].append(course_with_code)

    # Iterate through instructors
    for course in filtered_data:
        total_taught = filtered_data[course]['Total Classes']
        filtered_data[course]['Aprec Avg'] = filtered_data[course]['Aprec Sum'] / total_taught if total_taught > 0 else 0
        filtered_data[course]['Failprec Avg'] = filtered_data[course]['Failprec Sum'] / total_taught if total_taught > 0 else 0
        del filtered_data[course]['Aprec Sum'], filtered_data[course]['Failprec Sum']

    # Return
    return filtered_data


def display_instructor_data(data, course):
    # Displays data for course filter
    print(f"Data for Course: {course}")
    # Iterates on instructions
    for instructor, info in data.items():
        # Data being displayed
        print(f"\tInstructor: {instructor}, Total Taught Count: {info['Total Classes']}, Aprec Avg: {info['Aprec Avg']}%, Failprec Avg: {info['Failprec Avg']}%, Faculty Status: {info['Faculty Status']}")


def display_data(data):
    # Displays data for non-course filter
    for instructor, info in data.items():
        print(f"Instructor: {instructor}, Total Taught Count: {info['Total Classes']}, Aprec Avg: {info['Aprec Avg']}%, Failprec Avg: {info['Failprec Avg']}%, Faculty Status: {info['Faculty Status']}")


def write_to_file(filename, data):
    """ This function converts filter output to .txt for easy graph manipulation. """
    with open(filename, 'w') as file:
        for instructor, info in data.items():
            file.write(f"Instructor: {instructor}, Total Classes: {info['Total Classes']}, ")
            file.write(f"Aprec Avg: {info['Aprec Avg']}%, Failprec Avg: {info['Failprec Avg']}%, Faculty Status: {info['Faculty Status']}\n")

def applyFilter(average_grades, filter_options: dict):
    # department, class, level
    filter_type = filter_options["TYPE"]

    # dept, course code
    # if course code is single-digit, then filter by level
    department = filter_options["DEPT"].upper()

    # set faculty_only True or False
    if filter_options["REG_INSTR"] == 0:
        faculty_only = False
    else:
        faculty_only = True

    # iterate through sort types
    # filter by department
    if filter_type == "department":
        filter_data = filter_by_department(average_grades, department)

    # filter by class
    # if COURSE field is empty for some reason, this filters by department instead
    elif filter_type == "class":
        try:
            course = filter_options["COURSE"]
        except KeyError:
            print("ERROR: Course data not found. Filtering by department...")
            filter_data = filter_by_department(average_grades, department)
        filter_data = filter_by_course(average_grades, course)

    # filter by level
    elif filter_type == "level":
        try:
            course = filter_options["COURSE"]
            if filter_options["SHOW_INSTR"]:
                # if true, filter by instructor
                filter_data = filter_by_department(average_grades, department, course[0])
            else:
                # else filter by class options
                filter_data = filter_by_department_classes(average_grades, department, course[0])
        except KeyError:
            # if unspecified, default behavior is to show instructor names
            filter_data = filter_by_department(average_grades, department, course[0])

    # if filtering by faculty only, delete non-faculty instructors
    if faculty_only:
        for instr, info in filter_data.items():
            if info["Faculty Status"] == 0:
                filter_data.pop(instr)
            else:
                filter_data[instr].pop("Faculty Status")

    # returns the filtered data, possible cut down to faculty only.
    return filter_data
    

def main():
    """
    main function for testing the filter functions and levels. [deprecated]
    """
    filename = "average_grades.txt"
    with open(filename, 'r') as file:
        average_grades = file.readlines()

    # 1st choice: What do we want to filter by?
    choice = input("Do you want to query by department, level, or class? Enter 'department', 'level' or 'class: ").lower()
    # Department level filter and save to file
    if choice == 'department':
        department = input("Enter a department (e.g., 'BI'): ")
        department_data = filter_by_department(average_grades, department)
        # print(department_data)
        output_filename = f"dept_{department}.txt"
        write_to_file(output_filename, department_data)
        print(f"Results for department filter saved to {output_filename}")

    # Class level filter and save to file
    elif choice == 'class':
        class_code = input("Enter a class code (e.g., 'BI121'): ")
        class_data = filter_by_course(average_grades, class_code)
        output_filename = f"class_{class_code}.txt"
        write_to_file(output_filename, class_data)
        print(f"Results for class filter saved to {output_filename}")

    # Level filter and save to file
    elif choice == 'level':
        department = input("Enter a department (e.g., 'BI'): ")
        level = input("Enter the course level (e.g., '1' for 100-level courses): ")
        level_data = filter_by_department(average_grades, department, level)
        output_filename = f"level_{department}{level}.txt"
        write_to_file(output_filename, level_data)
        print(f"Results for level filter saved to {output_filename}")

    # Error
    else:
        print("Invalid.")


# if __name__ == "__main__":
#     main()
