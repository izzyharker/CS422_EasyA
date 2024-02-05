# Web scraper for Easy A project, CS422 Winter 2024,  by Sequoia A.

import requests
from bs4 import BeautifulSoup


def write_to_txt(faculty_names, file_name):
    """
    Writes a list of faculty names to a text file.

    Parameters:
    - faculty_names: List of strings, each representing a faculty name.
    - file_name: String, the name of the file to write the names into.

    Each name is written to the file on a new line with UTF-8 encoding.
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for name in faculty_names:
            file.write(f"{name}\n")



def format_names(elements):
    """
    Formats names extracted from BeautifulSoup, elements within <p> tags.

    Parameters:
    - elements: Iterable of BeautifulSoup elements to be processed.

    Returns a list of formatted names, skipping non-faculty text and formatting according to 'lname, fname'.
    """
    formated_list = []
    for element in elements:
        # remove extra (not faculty names) text within <p> tags
        if element.name == 'p' and 'The date in parentheses' in element.get_text():
            continue
        # inspected a faculty name to see they are nested within the html elements,
        # '<p class="facultylist">'
        # returns an empty list if class="facultylist" is not found
        if element.name == 'p' and 'facultylist' in element.get('class', []):
            # the text inside the p tag and facultylist class
            # which we cut off at the comma, in order to remove unnecessary text
            # this is based on 'name, role' format of 2014-2015 catalog
            full_name = element.get_text().split(',')[0].strip()
            # split the name into a list, separated by whitespace
            #name_parts = full_name.split()
            # check if the name consists of at least first and last names
            #if len(name_parts) >= 2:
                # format as 'lname, fname', -1 is the last item in the list
                # then rejoin the parts, placing the last name, and remaining names in order
            #    formatted_name = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
            #else:
                # if only one part is present, use it as is
             #   formatted_name = full_name
            formated_list.append(full_name)
    return formated_list



def scrape_faculty_names(base_url, department=''):
    """
    Scrapes faculty names from a given department webpage.

    Parameters:
    - base_url: String, the base URL of the faculty directory.
    - department: String, the specific department path to append to the base URL.

    Returns a list of faculty names if successful; otherwise, returns an empty list.
    """
    # construct the full URL by appending the department to the base URL
    full_url = base_url + department
    response = requests.get(full_url)
    # if there is an unsuccessful http request
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []
    # parse html, turn it into a nested data structure
    soup = BeautifulSoup(response.text, 'html.parser')


    # return a list of tag objects, i.e., <p> tags in the HTML where faculty names are listed, or any other tag
    # from bs4 documentation:
    # "If you pass in a list, Beautiful Soup will allow a string match against any item in that list."
    elements = soup.find_all(['p', 'h3'])


    faculty_names = format_names(elements)


    return faculty_names


base_url = 'https://web.archive.org/web/20141028184934/http://catalog.uoregon.edu/arts_sciences/'

# list of department urls of the natural sciences
dept_list = ['biology/', 'chemistry/', 'computerandinfoscience/', 'generalscience/', 'geologicalsciences/',
             'humanphysiology/', 'mathematics/', 'neuroscience/', 'physics/', 'psychology/']

faculty_names = []

# begin scraping each department

for dept in dept_list:
    print(dept)
    faculty_names.append(dept)
    faculty_names += scrape_faculty_names(base_url, dept)


print(faculty_names)

write_to_txt(faculty_names, 'faculty_names.txt')