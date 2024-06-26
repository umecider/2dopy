
from backend.sql import createDF, initialize_table, searchTable
from backend.dataframe import usrInput, updateSQL
from backend.cml import parseArgs
import pandas as pd
import time
from tabulate import tabulate
import argparse
import sys
from config import SHOW_COMPLETED, AUTOSAVE_DELAY


### FUNCTIONS ###
def mainView(df):
    '''
    Main overview of the program. In end result, should display a table of tasks to complete, along with other statistics to be decided (total tasks completed/completed in a week, completed task streak?, ect.)
    Make sure overdue tasks are in their own category at the top.
    

    '''
    #this conditional will need to be updated at a later point in time. (clarification: because we might be removing completed tasks.)
    if len(df) == 0:
        print("There are no tasks to display at the moment. Why not add one? :)\n")
    else:
        displayTasks = pd.DataFrame(df.sort_values(["due_date", "priority"], ascending=[True, False]))
        displayTasks.drop(columns = ["changed", "new", "completion_date"], inplace = True)
        displayTasks.set_index("id", inplace=True)
        displayTasks.drop(displayTasks[displayTasks["deletion"] == 1].index, inplace=True)
        colReorder = ["name", "priority", "due_date", "complete"]
        displayTasks = displayTasks[colReorder]
        if(SHOW_COMPLETED == False):
            #drop rows based on condition: https://stackoverflow.com/questions/13851535/how-to-delete-rows-from-a-pandas-dataframe-based-on-a-conditional-expression
            displayTasks.drop(displayTasks[displayTasks["complete"] == 1].index, inplace=True)
            displayTasks.drop(columns = ["complete"], inplace = True)
            if len(displayTasks) == 0:
                print("You've completed all of your tasks. Well done! :D\nIf you're up to it, why not add a new one?\n") #this should be the fix the conditional in line 22 wanted
            else:
                print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date"], tablefmt = "rounded_grid", numalign="center", stralign="center"))
        elif(SHOW_COMPLETED == True):
            displayTasks.loc[displayTasks["complete"] == 1, "complete"] = "\u2713"
            displayTasks.loc[displayTasks["complete"] == 0, "complete"] = "X"
            print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date", "Completed?"], tablefmt = "rounded_grid", numalign="center", stralign="center"))
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
    


""" to revamp later
### ARGPARSE ###
#https://docs.python.org/3/library/argparse.html
arguments to implement
100% Done.        "New: Create a new task.",
100% Done (USES ID)            "Edit: Edit details of a task.",
100% Done (USES ID)            "Complete: Mark a task as complete.",
100% Done.            Show Table
handled by python.           "Help: Display this message.", """

parser = argparse.ArgumentParser(description="Simple to-do list, from the comfort of your terminal! \nIf you want to use the Terminal UI, please run the file again, without any flags. :)")
parser.add_argument("-n","--new", action = "store_true", help = "Create new task. REQUIRES THE -t ARGUMENT. Can be combined with -d and -p.")
parser.add_argument("-e", "--edit", action = "store_true", help = "Edit a task based on ID number. REQUIRES the -i ARGUMENT. Use -t, -d and -p to edit the respective values. You can also pass -c without an ID modifier to change the completion status.")
parser.add_argument("-c","--complete", action = "store_true", help = "Mark the task with the ID passed as complete. REQUIRES THE -i ARGUMENT UNLESS BEING USED WITH -e")
parser.add_argument("-r","--remove", action = "store_true", help = "Remove a task from the database. REQUIRES THE -i ARGUMENT.")
parser.add_argument("-s", "--search", action="store_true", help = "Searches the database for a given task name. REQUIRES THE -t ARGUMENT.")
parser.add_argument("-sh","--show", action="store_true", help = "Display the table of tasks to be completed. Will run after any other flags have been passed. Pass -a to show all tasks.")
parser.add_argument("-i", "--ID", nargs = "+", type = int, help = "Adds an ID modifier. Used with -e, -c, and -r. Multiple can be passed to -c and -r")
parser.add_argument("-t", "--task-name", nargs = "+", dest="name", action = "extend", help = "Adds a task name modifier. Used in conjunction with -e and -n.")
parser.add_argument("-d","--date",nargs=1, help = "Add date to a task in the format MM/DD/YY. Used in conjunction with -n and -e") #can probably also use this with edit
parser.add_argument("-p","--priority",nargs=1, metavar="level", type=int, help="Add a priority level to a task, on a level from 1-5. Used in conjunction with -n and -e")#can also probably be used with edit
parser.add_argument("-a", "--all", action="store_true", help = "Show all tasks. Used in conjunction with -s")
args = parser.parse_args()


#argparse - figure out if no flags called
#https://stackoverflow.com/questions/10698468/argparse-check-if-any-arguments-have-been-passed


### Main loop - runs when no args ###
if not len(sys.argv) > 1:
    initialize_table()
    pandaDF = createDF()
    continueFlag = True
    lastUpdate = time.time()
    while(continueFlag == True):
        continueFlag = mainView(pandaDF)
        #print("checking time")
        if(continueFlag!=False):
            lastUpdate = checkTime(AUTOSAVE_DELAY, lastUpdate, pandaDF)
### Dealing with commandline arguments
else:
    #Error Handling for dependencies
    #all flag used without show
    if(args.show == False and args.all == True):
        parser.error("--all cannot be used without calling --show!")
    #title/date/priority used without new/edit
    if (args.new == False and args.priority != None and args.edit == None):
        parser.error("-p must be used with -n or -e!")
    if (args.new == False and args.date != None and args.edit == None):
        parser.error("-d must be used with -n or -e!")
    if (args.new == False and args.name != None and args.edit == None):
        parser.error("-t must be used with -n or -e!")
    #new task created but no title passed
    if (args.new == True and args.name == None):
        parser.error("-n requires a -t modifier to create a task!")
    #search but no title passed
    if (args.search == True and args.name == None):
        parser.error("-s requires a -t modifier to search for a task!")
    #default complete flag passed without edit
    if (args.complete == True and args.edit == False and args.ID == None):
        parser.error("-c must be passed with an ID number using the -i modifier!")
    #edit passed without an ID
    if (args.edit == True and args.ID == None):
        parser.error("-e requires an ID number using the -i modifier!")
    #remove called without an ID
    if (args.remove == True and args.ID == None):
        parser.error("-r requires an ID number using the -i modifier!")
    #bad -i call
    if(args.complete == False and args.edit == False and args.ID != None and args.remove == False):
        parser.error("-i can only be used with -e, -c, and -r!")
    if(args.complete == False and args.edit == True and len(args.ID) >=1 and args.remove == False):
        parser.error("-i can only have multiple values when used with -c or -r!")
    #only one flag at a time - I need to come up with a better system.
    #if((args.complete == True and args.edit == True) or (args.new == True and args.complete == True) or (args.edit == True and args.new == True) or (args.new == True and args.remove == True) or (args.complete == True and args.remove == True) or (args.edit == True and args.remove == True)):
    #shoutout to ser for this one
    if(sum([args.complete,args.new,args.edit,args.remove])>1):
        if(sum([args.complete,args.edit]) == 2):
            pass
        else:
            parser.error("At the moment, multi argument support is not supported.")
    if(args.ID != None and args.ID[0] < 0):
        parser.error("The ID number has been input incorrectly. Please try again.")
    parseArgs(args, parser)
