# 2do.py

## Introduction
This is a simple project I've been working on to create a simple to-do program that runs in the terminal, without a GUI. The main purpose of this was to get used to creating and managing an SQL Database, and to get refreshed with performing pandas.DataFrame operations.

## Usage
First, make sure your pyton environment has the following libraries installed:
- pandas
- python-dateutil
- sqlite3
If you do not have any of these, you can install them easily using pip.

To use this program, open a terminal and navigate to the folder where the program is located. Then, simply run the program with your local python directory. The program will create a new local SQL database in the same location. Commands are input either by inputting the first letter of the command, or the whole command. The following commands are implemented: 

- Help: Displays a list of all commmands.
- New: Creates a new task in the database.
- Edit: Edit the details of a task after providing it's ID number. 
    - At the moment, updating the following task elements are possible: name, due_date, priority, and completed. Please note that you have to input these as they are written.
- Complete: Mark a task as complete after providing it's ID number.
- Save: Save any new or edited tasks to the SQL database. 
    - If you do not call this, any changes and additions made in this session will not be loaded the next time the program is run.
    - ***In future development***, this is planned to be performed automatically every 5 minutes
- Quit: Exit the program.
    - NOTE: This does not save the database. That must be done manually before quitting, though it might be implemented in the future.

## Future Development Goals and Ideas:
- Implement python library rich in order to have a better terminal output.
- Implement graphs and statistics for completed statistics.
- Implement Auto-Saving.
- Implement Creating and Completing tasks from the command line
    - Syntax would be something like "python3 todo.py -c (id number)" for completing a task and "python3 todo.py -n "task name", MM/DD/YY HH:MM, (prioritylevel)" to make a new task.
        - It would try to perform these, and if errors occur then it'd leave the corresponding value blank (besides the task name)
- Rename python file to "2do.py" instead of "todo.py"
- Allow for filters to the main view (Filter out completed tasks, Filter out tasks that aren't completed, sort by priority, sort by date, ect.)
- Be able to search all tasks by name to decide on which to complete and edit, rather than having to input the ID number.
    - The main issue I can forsee is dealing with duplicate tasks, as it'd need to return multiple tasks and then ask the user to pick one.
