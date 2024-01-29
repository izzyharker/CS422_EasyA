# web scraper WIP for Easy A project, by Sequoia
import requests
from bs4 import BeautifulSoup
import csv
import time


def write_to_csv(faculty_names, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        # write names to the csv, replaces any existing files
        # do we want to add more info besides names?
        writer = csv.writer(file)
        for name in faculty_names:
            writer.writerow([name])  # each name is written to a new row

# TODO: Add this parameter if we want to filter names besides the core staff
# , stop_at_headers=['Emeriti', 'Courtesy', 'Special Staff']
def scrape_faculty_names(base_url, department=''):
    # construct the full URL by appending the department to the base URL
    full_url = base_url + department
    response = requests.get(full_url)
    # if there is an unsuccessful http request
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []
    # parse html, turn it into an object, a nested data structure in particular
    soup = BeautifulSoup(response.text, 'html.parser')

    faculty_names = []

    # return a list of tag objects, i.e., <p> tags in the HTML where faculty names are listed, <h3> to cutoff emeriti
    elements = soup.find_all(['p', 'h3'])

    for element in elements:
        if element.name == 'p' and 'facultylist' in element.get('class', []):
            full_name = element.get_text().split(',')[0].strip()
            # split the name
            name_parts = full_name.split()
            # check if the name consists of at least first and last names
            if len(name_parts) >= 2:
                # format as 'lname, fname'
                formatted_name = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
            else:
                # if only one part is present, use it as is
                formatted_name = full_name
            faculty_names.append(formatted_name)

    return faculty_names


base_url = 'https://web.archive.org/web/20141028184934/http://catalog.uoregon.edu/arts_sciences/'
# scraping the natural sciences
dept_list = ['biology/', 'chemistry/', 'computerandinfoscience/', 'generalscience/', 'geologicalsciences/',
             'humanphysiology/', 'mathematics/', 'neuroscience/', 'physics/', 'psychology/']
faculty_names = []

for dept in dept_list:
    print(dept)
    faculty_names.append(dept)
    faculty_names += scrape_faculty_names(base_url, dept)
    time.sleep(2)

print(faculty_names)

write_to_csv(faculty_names, 'faculty_names.csv')
