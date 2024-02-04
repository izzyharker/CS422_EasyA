# EasyA
CS 422, Winter 2024, Group Project 1. Written by Izzy Harker, Carter Young, Jose Renteria, and Sequoia Anichini.

## Installation
### Requirements
This program runs on Python 3.9>=. If you do not have python installed on your machine, please do that first.

### Dependencies
Required libraries can all be installed using `pip`. The required libraries are: `matplotlib, requests, tkinter, requests, bs4 (BeautifulSoup)`. 

### Usage
To run this program, either download the files or `git clone` the repository. Once you `cd` into the main directory, run the program on the command line by running 
```
python EasyA.py
```

You will be prompted to enter 'y', 'u', or 'n'. Entering 'y' will start the program. 

## Admin
This program also contains functionality for the admin to "upload" new data. To use this function, run 
```
python EasyA.py
```

Enter 'u' when prompted the first time. You will then be prompted to enter the path to the new data file. This will replace the old data and the new data will be used the next time the program is started.

## Notes
If new data is entered and the filepath is invalid, or the file is not found, then the program will abort. 

If you would like to reset the program to use the old data file, run the program to update data (see "System Admin") and when prompted to enter a path to the data file, enter `reset` instead.

# Frontend information for Jose
## Filtering dictionary structure
Filtering takes a dictionary with the following key/value pairs.
required:

TYPE: department, level, course

DEPT: valid department code

REG_INSTR: 0 if False, 1 if True

APREC_YES: True/False

optional/situational

COURSE: 3-digit course code

SHOW_INSTR_CLASSES_TAUGHT: True/False

SHOW_INSTR: True/False

### Additional information
TYPE, DEPT, REG_INSTR, APREC_YES are always used in the filtering and correspond to buttons

COURSE is used with filtering by class and by level, but not by overall department

SHOW_INSTR_CLASSES_TAUGHT adds the number of classes an instructor teaches to the x-axis label of the graph

SHOW_INSTR is only used with filtering by level, if true then the graph sorts by instructor, otherwise the program filters by specific class.

If necessary you can modify these, but this minimal necessary information as far as I can tell in terms of what is needed by the filter to produce all the graphs that we need to produce. I'm happy to explain more if you need.

## Frontend connections
Right now, I have the graphing function return the fig - if it's easier to have it write to an image file let me know and I can change it. I'll leave the rest of the frontend up to you, I changed your main.py file -> UI_loop.py and put it in Modules/. 

Let me know if any of that is confusing or if you want me to change anything.

-Izzy


## Overview of the scrape.py Module
Our web scraper is scrape.py by Sequoia A. It automatically extracts faculty names from the UO course catalog page.
It leverages the requests library to fetch webpages and BeautifulSoup from bs4 for parsing HTML content.

### Key Features
Scraping Faculty Names: It fetches webpages from the Wayback -> UO course catalog URL, appended with department paths, to make the list of faculty names.

Formatting Names: Names are formatted in a "lastname, firstname" convention, which is best suited for data resolution needs.

File Output: Formatted names are written into faculty_names.txt, replacing the previous file, with each execution.

### Usage
Initial Setup: Requires installation of Python3, requests and bs4 python libraries.

Execution: Users can specify the base URL of the faculty directory and a list of departmental paths to scrape faculty names.
To run, execute in an IDE that's compatible with Python, or type 'python scrape.py' in a terminal

Output: The script outputs a text file named faculty_names.txt, containing the formatted names of faculty members, organized by department.