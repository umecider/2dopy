from backend import usrInput, initialize, updateSQL
import pandas as pd
from tabulate import tabulate
import time
import argparse
import sys
from cml import parseArgs

### GLOBAL STATIC VARS - hopefully to be parsed through a config file ###
SHOW_COMPLETED = True
AUTOSAVE_DELAY = 20

### FUNCTIONS ###
def mainView(df):
    '''
    Main overview of the program. In end result, should display a table of tasks to complete, along with other statistics to be decided (total tasks completed/completed in a week, completed task streak?, ect.)
    Make sure overdue tasks are in their own category at the top.
    

    '''
    #this conditional will need to be updated at a later point in time.
    if len(df) == 0:
        print("There are no tasks at the moment. Why not add one? :)")
    else:
        displayTasks = pd.DataFrame(df.sort_values(["due_date", "priority"], ascending=[True, False]))
        displayTasks.drop(columns = ["changed", "new", "completion_date"], inplace = True)
        displayTasks.set_index("id", inplace=True)
        colReorder = ["name", "priority", "due_date", "complete"]
        displayTasks = displayTasks[colReorder]
        if(SHOW_COMPLETED == False):
            #drop rows based on condition: https://stackoverflow.com/questions/13851535/how-to-delete-rows-from-a-pandas-dataframe-based-on-a-conditional-expression
            displayTasks.drop(displayTasks[displayTasks["complete"] == 1].index, inplace=True)
            displayTasks.drop(columns = ["complete"], inplace = True)
            print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date"], tablefmt = "rounded_grid", numalign="center"))
        elif(SHOW_COMPLETED == True):
            print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date", "Completed?"], tablefmt = "rounded_grid", numalign="center"))
    #need to figure out how to actually get the main view to look cool
    print("Please type the command you would like to perform, and press enter.")
    print("(Type 'help' for a list of commands!)")
    #run input function
    #TO DO: update this function to refresh everything only once in awhile
    return usrInput(df)

def checkTime(delay, lastRun, df) -> float:
    currentTime = time.time()
    if(currentTime - lastRun >= delay):
        updatedFlag = updateSQL(df)
        if(updatedFlag == True):
            print("Your changes have been automatically saved.")
        return currentTime
    else:
        return lastRun

def populateDF() -> pd.DataFrame:
    df = initialize()
    #implementing new column variable to cut down on how many rows the program will update
    #0 = not changed 1 = changed
    #only update changed values in database
    df["changed"] = 0
    #Implementing column variable to also flag when I need to use a different function to update the database.
    #0 = not new, 1 = new
    #if new need to add a row rather than update it.
    df["new"] = 0
    return df


### ARGPARSE ###
#https://docs.python.org/3/library/argparse.html
""" arguments to implement
        "New: Create a new task.",
            "Edit: Edit details of a task.",
            "Complete: Mark a task as complete.",
100% Done.            Show Table
handled by python.           "Help: Display this message.",
"""
parser = argparse.ArgumentParser(description="Simple to-do list, from the comfort of your terminal! \nIf you want to use the Terminal UI, please run the file again, without any flags. :)")
parser.add_argument("--new","-n", nargs = 1, metavar="Title", help = "Create new task. Can be combined with --date and --priority.")
parser.add_argument("--date","-d",nargs=1, help = "Add date to a task in the format MM/DD/YY. Used in conjunction with --new") #can probably also use this with edit
parser.add_argument("--priority","-p",nargs=1, type=int, help="Add a priority level to a task, on a level from 1-5. Used in conjunction with --new")#can also probably be used with edit
parser.add_argument("--show","-s", action="store_true", help = "Display the table of tasks to be completed. Will run after any other flags have been passed. Pass --all to show all tasks.")
parser.add_argument("--all", "-a", action="store_true", help = "Show all tasks. Used in conjunction with --show")
args = parser.parse_args()


#argparse - figure out if no flags called
#https://stackoverflow.com/questions/10698468/argparse-check-if-any-arguments-have-been-passed


### Main loop - runs when no args ###
if not len(sys.argv) > 1:
    pandaDF = populateDF()
    continueFlag = True
    lastUpdate = time.time()
    while(continueFlag == True):
        continueFlag = mainView(pandaDF)
        #print("checking time")
        if(continueFlag!=False):
            lastUpdate = checkTime(AUTOSAVE_DELAY, lastUpdate, pandaDF)
### Dealing with commandline arguments
else:
    cmlDF = populateDF()
    parseArgs(args, cmlDF)