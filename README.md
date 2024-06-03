# 2do.py

## Introduction
This is a simple project I've been working on to create a simple to-do program that runs in the terminal, without a GUI. The main purpose of this was to get used to creating and managing an SQL Database, and to get refreshed with performing pandas.DataFrame operations.

## Usage
First, make sure your pyton environment has the following libraries installed:
- pandas
- python-dateutil
- sqlite3
- tabulate

If you do not have any of these, you can install them easily using pip ("python -m pip install [name]")

To use this program, open a terminal and navigate to the folder where the program is located. Then, simply run the program with your local python directory. The program will create a new local SQL database in the same location. Commands are input either by inputting the first letter of the command, or the whole command. The following commands are implemented: 

- Help: Displays a list of all commmands.
- New: Creates a new task in the database.
- Edit: Edit the details of a task after providing it's ID number. 
    - At the moment, updating the following task elements are possible: name, due_date, priority, and completed. Please note that you have to input these as they are written.
- Complete: Mark a task as complete after providing it's ID number.
- Save: Save any new or edited tasks to the SQL database. 
    - If you do not call this, any changes and additions made in this session will not be loaded the next time the program is run.
    - This is automatically done in 20 second intervals. *Currently planned to be cusomizable through a config file*
- Remove: Delete a task from the database, after providing it's ID number.
    - Note: ***There is currently NO UNDO for this.*** Be careful.
- Quit: Exit the program.
    - NOTE: This **will save your changes**.

If you'd like to perform these actions in the command line, the python file now accepts arguments! Try -h to get a general help message. Here are a few example actions:
- Create a task: python3 2do.py -n -t Task Name Here -d 010124 -p 4 (Creates a task named "Task Name Here", which is due at Jan 1st, 2024 with a priority level of 4.)
- Edit a task: python3 2do.py -e -i 15 -t Fix Typo -c (Edits the task at ID 15, changing the title to "Fix Typo" and inverts the completion status.)
- Complete a task: python3 2do.py -c -i 15 -s -a(Marks the task at ID 15 as completed. Sets the completed date to the time the command was sent. After, shows all tasks.)
- Remove task: python3 2do.py -r -id 15 (Removes the task at ID 15)
- Show current to-do list: 2do.py -s (Shows a list of tasks that have not been completed. Add the -a modifier to show all tasks.)
- *NEW!* You can batch complete and batch remove tasks! Just pass multiple numbers to the ID modifier (eg: -c -i 15 16 18 or -r -i 1 2 3)

## Future Development Goals and Ideas:
- Implement python library textualize in order to greate a Terminal GUI.
- Implement graphs and statistics for completed statistics.
- Implement Settings Adjustment (database location, auto save duration.)
- Allow for filters to the main view (Filter out completed tasks, Filter out tasks that aren't completed, sort by priority, sort by date, ect.)
- Be able to search all tasks by name to decide on which to complete and edit, rather than having to input the ID number.
    - The main issue I can forsee is dealing with duplicate tasks, as it'd need to return multiple tasks and then ask the user to pick one.
- ~~Implement Auto-Saving.~~ Done! Set to 20 seconds at the moment.
- ~~Implement Creating and Completing tasks from the command line~~ Done! Will need to do a write up, but in general -h will give the information needed to start!
- ~~Rename python file to "2do.py" instead of "todo.py"~~ Done!

