## Functional Requirements
- The user should be able to view data in the following manner
### (a) **Within a single graph, broke out by *instructor* for:**
- a single class (Math 111)
- A single department (Math)
- All classes of a particular level within a department (such as Math 100-level courses, from 100-600 range)
    Figure 2 ![figure2.png](figure2.png)
### (b) **All classes of a particular level within a department**
- This would help students, for example to choose which electives to take. Figure 3 shows an example 
            - ![figure3.png](figure3.png)
### (c) **All instructors vs Regular Faculty**
- For all graphs, there should be two options as follows:
- "All instructors" (the default)
- "Regular faculty" which are the faculty listed within departments in the 2014/15 UO course catalog https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/
### **(d) Easy A's versus Just Pass**
- For all graphs, there should be two options, as follows. The selection should be indicated on the Y-axis label:
    - (1) "Percent A's" or "%A's" (default)
    - (2) "Percent D's pr F's" (%D's/F's)
### ** (e) An option to show the class count**
- Ideally, your system will have an option to show the number of classes represented in each bar in the bar graph. Figure 4 shows an example
            - ![figure4.png](figure4.png)
### Side by side viewing
- the system should support some sort of side by side viewing of graphs, such as to show figure 3 (Math 400 level classes) alongside a separate, similar graph for all CS 400 level classes
### Graph formatting
- Graphs should be easy to use and easy to read as those shown in figures 1-4. For example, bar graphs should be narrow, clearly visible, easy to compare, and ordered to support the user's task, which will usually be from highest to lowest, or lowest to highest.
### Fully populated initial system
- The system that is delivered should not require any admin steps to convert or prepare data for the system other than (optionally) setting up a database (if the system uses it). But, for example, there should not be any web scraping or data conversion required for the initial use of the system
### The Administrator Adding New Data 
With regards of the use-case of a system administrator updating the system with that new data: 
1.  You should provide a program that permits an administrator (such as the instructor) to replace all of the data in the system (all grade data, and all instructor data) using the “gradedata.js” file that was provided to you (or a .csv or other single file that you created from the gradedata.js file), and by scraping the instructor names from the “way back machine”. Replacing the data should be quick and easy (such as, able to be accomplished by an administrator unfamiliar with the system in less than five minutes). 
2.  The data file (that the system administrator will use to load the new grade data) can be in a file format of your choice, such as the original “gradedata.js” file that is provided to you for this project, or a CSV file. If it is a format of your choice, you would ideally provide an appropriately-formatted file that contains all of the data in “gradedata.js”. 
3.  A “scraper” for extracting the faculty names from the “way back machine” data at  
https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/ 
would ideally be provided. You can use the python library BeautifulSoup to help with this. 
4.  When replacing the system data, ideally, discrepancies between names found in 
“gradedata.js” and the names found in the scraped instructor data would be easy to resolve using the administrator tools, to ensure that the data in your tables is clean, consistent and accurate. (Optionally, as the two sources of data are brought into alignment, the tools could generate statistics such as lists of names from both data sources that have yet to find a match, so you can see how your data resolving process needs to be further improved.) 
5.  Any software tools that you create for the administrator to load data can be separate 
standalone applications, not integrated with the main program used by students. These can be command-line tools (without a graphical user interface). Instructions for their use should of course be provided. (Optional: Some sort of statistics could be provided when loading the new data, such as how many classes or instructors were added, and any naming discrepancies that were resolved.) 
6.  The new data should overwrite the old data.