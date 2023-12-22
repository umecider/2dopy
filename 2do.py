from backend import usrInput, initialize, updateSQL
import pandas as pd
from tabulate import tabulate
import time

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
        updateSQL(df)
        return currentTime
    else:
        return lastRun


#print("init")
pandaDF = initialize()
#implementing new column variable to cut down on how many rows the program will update
#0 = not changed 1 = changed
#only update changed values in database
pandaDF["changed"] = 0
#Implementing column variable to also flag when I need to use a different function to update the database.
#0 = not new, 1 = new
#if new need to add a row rather than update it.
pandaDF["new"] = 0
#print("entering main")

continueFlag = True
lastUpdate = time.time()
autoSaveDuration = 20 #this should hopefully be stored in a config file somewhere, which could also contain other options
while(continueFlag == True):
    continueFlag = mainView(pandaDF)
    #print("checking time")
    lastUpdate = checkTime(autoSaveDuration, lastUpdate, pandaDF)