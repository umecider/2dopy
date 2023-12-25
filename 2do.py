from backend import usrInput, initialize, updateSQL
import pandas as pd
from tabulate import tabulate
import time
#import argparse
#import sys

### GLOBAL STATIC VARS - hopefully to be parsed through a config file ###
SHOW_COMPLETED = False
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


pandaDF = populateDF()
continueFlag = True
lastUpdate = time.time()

while(continueFlag == True):
    continueFlag = mainView(pandaDF)
    #print("checking time")
    lastUpdate = checkTime(AUTOSAVE_DELAY, lastUpdate, pandaDF)

# ### ARGPARSE ###
# #https://docs.python.org/3/library/argparse.html
# """ arguments to implement
#         "New: Create a new task.",
#             "Edit: Edit details of a task.",
#             "Complete: Mark a task as complete.",
# 100% Done.            Show Table
# handled by python.           "Help: Display this message.",
# """
# parser = argparse.ArgumentParser(description="Simple to-do list, from the comfort of your terminal! \nIf you want to use the Terminal UI, please run the file again, without any flags. :)")
# parser.add_argument("--new","-n", nargs = "+", help = "Create new task. Requires a title. Accepts due date and priority, but they are optional.")
# parser.add_argument("--show","-s", action="store_true", help = "Display the table of tasks to be completed. Will run after any other flags have been passed. Pass --all to show all tasks.")
# parser.add_argument("--all", "-a", action="store_true", help = "Show all tasks. Used in conjunction with --show")
# args = parser.parse_args()


# #argparse - figure out if no flags called
# #https://stackoverflow.com/questions/10698468/argparse-check-if-any-arguments-have-been-passed


# ### Main loop - runs when no args ###
# if not len(sys.argv) > 1:
#     pandaDF = populateDF()
#     continueFlag = True
#     lastUpdate = time.time()

#     while(continueFlag == True):
#         continueFlag = mainView(pandaDF)
#         #print("checking time")
#         lastUpdate = checkTime(AUTOSAVE_DELAY, lastUpdate, pandaDF)
# ### Dealing with commandline arguments
# else:
#     cmlDF = populateDF()
#     if(args.show == False and args.all == True):
#         print("--all cannot be used without calling --show!")
    
#     #automatic saving because come ON
#     updateSQL(cmlDF)
#     #args show and all. To run last.
#     if(args.show == True):
#         #this is stolen from mainView() but slightly modified to work with the args
#         displayTasks = pd.DataFrame(cmlDF.sort_values(["due_date", "priority"], ascending=[True, False]))
#         displayTasks.drop(columns = ["changed", "new", "completion_date"], inplace = True)
#         displayTasks.set_index("id", inplace=True)
#         colReorder = ["name", "priority", "due_date", "complete"]
#         displayTasks = displayTasks[colReorder]
#         if(args.all == False):
#             #drop rows based on condition: https://stackoverflow.com/questions/13851535/how-to-delete-rows-from-a-pandas-dataframe-based-on-a-conditional-expression
#             displayTasks.drop(displayTasks[displayTasks["complete"] == 1].index, inplace=True)
#             displayTasks.drop(columns = ["complete"], inplace = True)
#             print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date"], tablefmt = "rounded_grid", numalign="center"))
#         elif(args.all == True):
#             print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date", "Completed?"], tablefmt = "rounded_grid", numalign="center"))