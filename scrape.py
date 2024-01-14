# web scraper WIP for Easy A project, by Sequoia
# not sure if we should add more files to gitignore - any opinions?

import requests
from bs4 import BeautifulSoup

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
    # select method finds all <p> elements with the class 'facultylist' - inspected the html of the page to find this
    # return a list of tag objects, i.e., <p> tags in the HTML where faculty names are listed
    faculty_elements = soup.select('p.facultylist')

    # extracting only the names from each element
    # debugging is still in order to ensure we only grab names
    faculty_names = [element.get_text().split(',')[0].strip() for element in faculty_elements]
    return faculty_names


# base URL for Wayback Machine archive
base_url = 'https://web.archive.org/web/20141028184934/http://catalog.uoregon.edu/arts_sciences/'

# e.g., scraping the mathematics department
faculty_names_math = scrape_faculty_names(base_url, 'mathematics/')
print(faculty_names_math)
