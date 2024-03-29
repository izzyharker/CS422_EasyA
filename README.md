# EasyA
CS 422, Winter 2024, Group Project 1. Written by Izzy Harker, Carter Young, Jose Renteria, and Sequoia Anichini.

## Installation
### Requirements
This program runs on Python 3.9>=. If you do not have python installed on your machine, please do that first.

### Dependencies
Dependencies can all be installed using `pip`. The required dependencies are: `matplotlib, requests, tkinter, requests, bs4 (BeautifulSoup)`. These should all be updated to the latest version to ensure proper functionality.

## Usage
### Running the program
`gradedata.js` is included in the git repository under the `Data/` directory, as well as `faculty_names.txt` and `PathToDataFile`. All three of these files are necessary for proper execution of the program. 

If `faculty_names.txt` is missing, please run 
```
python scrape.py
```
and ensure the resulting file is placed in the `Data/` directory. This is vital for cross-referencing the ground truth of  instructors with the given data.

`gradedata.js` should contain the grade data that you would like to filter and examing using the program.

`PathToDataFile` should be one line, and that line should match the local path to the data file. This can be a relative path from the directory that `EasyA.py` is contained in, or can be a absolute path. 

To run this program, either download the files or `git clone` the repository. Once you `cd` into the main directory, run the program on the command line by running 
```
python EasyA.py
```

You will be prompted to enter 'y', 'u', or 'n'. Entering 'y' will start the program. 

### Admin
This program also contains functionality for the admin to "upload" new data. To use this function, run 
```
python EasyA.py
```

Enter 'u' when prompted the first time. You will then be prompted to enter the path to the new data file. This will replace the old data by writing a new path into `PathToDataFile`, and the new data will be used the next time the program is started.

## Notes
If new data is entered and the filepath is invalid, or the file is not found, then the program will abort. 

If you would like to reset the program to use the old data file, run the program to update data (see "System Admin") and when prompted to enter a path to the data file, enter the keyword `reset`.

## Program files
The primary file is `EasyA.py`, which contains the main function and control flow for the program. 

## Directories
### Modules/
The modules are all contained in the `Modules/` directory. 

`scrape.py` contains functions to scrape faculty names from the Wayback machine and format them appropriately. On execution, this file produces `faculty_names.txt`, which contains a list of formatted faculty names by department. This file is used when loading data in order to cross-reference teacher names and check which are faculty and which aren't.

`ReadGradeData.py` contains functions for reading data from the initial `gradedata.js` file (or specified alternative data file) and processing it to have all the necessary data for filtering in the correct formats. In practice, this is output as `average_grades`. This file also contains the top-level function `loadData`, which reads data from a file, compares it against the faculty names produced by `scrape.py`, and produces an object containing all relevant data. There is included support for saving the loaded data to a file, but this functionality is not utilized in our product in order to avoid writing miscellaneous files.

`ManipGradeData.py` contains methods for filtering the average_grades data produced by the `loadData` function in `ReadGradeData.py`, as well as the top-level filtering function `applyFilter`, which takes the average grade data alongside a specific filter and applies the appropriate filtering method to return the correct set of data. There are also functions included to save filtered data to a file if desired, but these methods are not used in the final product in order to avoid file bloat.

`StyledGraph.py` contains the graphing class `StyledGraph` for producing formatted bar charts, as well as the top-level graphing function `GenerateGraph`. This function is called from the frontent and takes average_grades alongside a filter, calling the filtering module to get filtered data and using the filtered data to graph using a `StyledGraph` object. The `Matplotlib.pyplot.fig` produced by the `StyledGraph.graph` function is returned to the frontend so that it can be drawn on screen. 

`ui.py` is the module for rendering all functional components of the user interface. It contains three classes, `App`, `SideFrame`, and `GraphFrame`. App is where all of the components are called and placed according to how they will show up on the interface. The main application is split into two frames, one for the menu options and one for the actual graphing display grid. This is why it is split up into `SideFrame`, and `GraphFrame`. These frames are utilized to act as 'parents' or root components of the subcomponents housed within them, in order to more efficiently utilize relative positioning as well as an overall consistent layout.

`UI_loop.py` is the main container for all UI components rendered from the `ui.py` module. It simply runs the main loop by calling a function that invokes the application by calling `App()` and returning it. Think of this is the controller for the components that show up.

### Data/
The `Data/` directory should contain three files on start. These are `gradedata.js`, `PathToGradeData`, and `faculty_names.txt`. These are all used by the `loadData` function in order to locate, read, and process the raw data. 

# Overview of the scrape.py Module
Our web scraper is scrape.py by Sequoia A. It automatically extracts faculty names from the UO course catalog page.
It leverages the requests library to fetch webpages and BeautifulSoup from bs4 for parsing HTML content.

## Key Features
Scraping Faculty Names: It fetches webpages from the Wayback -> UO course catalog URL, appended with department paths, to make the list of faculty names.

Formatting Names: Names are formatted in a "lastname, firstname" convention, which is best suited for data resolution needs.

File Output: Formatted names are written into faculty_names.txt, replacing the previous file, with each execution.

## Usage
Initial Setup: Requires installation of Python3, requests and bs4 python libraries.

Execution: Users can specify the base URL of the faculty directory and a list of departmental paths to scrape faculty names.
To run, execute in an IDE that's compatible with Python, or type 'python scrape.py' in a terminal

Output: The script outputs a text file named faculty_names.txt, containing the formatted names of faculty members, organized by department.