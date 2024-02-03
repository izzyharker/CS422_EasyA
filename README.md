# CS422_EasyA
First group project for CS 422 (EasyA).
Test
test2

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