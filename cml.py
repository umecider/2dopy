from backend import updateSQL, addRow
import pandas as pd
from tabulate import tabulate
import dateutil
import re

def parseArgs(args, df):
## Causing errors for incorrect usage.
    if(args.show == False and args.all == True):
        print("--all cannot be used without calling --show!")
    if (args.new == None and args.priority != None):
        print("--priority must be used with --new!")
    if (args.new == None and args.date != None):
        print("--date must be used with --new!")
    #new task
    #make something to throw an error if more than 3 objects are passed through
    if(args.new != None):
        dateTime = None
        priorityLevel = 0
        if(args.date != None):
            try:
                dateTime = dateutil.parser.parse(args.date[0])
            except:
                print("Date is invalid. Omitting.")
        if(args.priority != None):
            if(0 < args.priority[0] and args.priority[0] < 6):
                priorityLevel = args.priority[0]
            else:
                print("Priority is too big or small. Omitting.")
        addRow(df, args.new[0], dateTime, priorityLevel)
        
    # if(len(args.new)==1):
    #     df = addRow(df, args.new[0])
    #     print("Task added!")
    # elif(len(args.new)>1):
    #     if(len(args.new[1])==1):
    #         if(len(args.new)==2):
    #             #new task
    #         el

    #     date: taskDate = dateutil.parser.parse(taskDate)
    #     #adding new task 
        pass
    #automatic saving because come ON
    updateSQL(df)
    #args show and all. To run last.
    if(args.show == True):
        #this is stolen from mainView() but slightly modified to work with the args
        displayTasks = pd.DataFrame(df.sort_values(["due_date", "priority"], ascending=[True, False]))
        displayTasks.drop(columns = ["changed", "new", "completion_date"], inplace = True)
        displayTasks.set_index("id", inplace=True)
        colReorder = ["name", "priority", "due_date", "complete"]
        displayTasks = displayTasks[colReorder]
        if(args.all == False):
            #drop rows based on condition: https://stackoverflow.com/questions/13851535/how-to-delete-rows-from-a-pandas-dataframe-based-on-a-conditional-expression
            displayTasks.drop(displayTasks[displayTasks["complete"] == 1].index, inplace=True)
            displayTasks.drop(columns = ["complete"], inplace = True)
            print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date"], tablefmt = "rounded_grid", numalign="center"))
        elif(args.all == True):
            print(tabulate(displayTasks, ["id","Task Name", "Priority", "Due Date", "Completed?"], tablefmt = "rounded_grid", numalign="center"))