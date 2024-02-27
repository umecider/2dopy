from backend import updateSQL, addRow
import pandas as pd
from tabulate import tabulate
import dateutil
import datetime

def parseArgs(args, df, parser):
#new task
    if(args.new == True):
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
                print("Priority is out of range. Omitting.")
        addRow(df, " ".join(args.name), dateTime, priorityLevel)
        print("Task added.\nName:", " ".join(args.name), "| Due Date:", dateTime, "| Priority:", priorityLevel, "| ID Number:", (df.at[(len(df)-1),"id"]))
#complete task 
    if(args.complete == True and args.edit == False):
        #check for if ID is in range
        if (args.ID[0] > len(df) or args.ID[0] < 0):
            parser.error("That ID does not exist.")
        elif(args.id[0] != 0):
            #from main: 
            index = df[df["id"] == int(args.ID[0])].index.item()
            df.at[index, "complete"] = 1
            df.at[index, "completion_date"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            df.at[index, "changed"] = 1
            print("Task",args.complete[0],"marked as complete. Name:", df.at[index,"name"])

#editing
    if(args.edit == True):
        index = df[df["id"] == int(args.ID[0])].index.item()
    #Name
        if(args.name != None):
            df.at[index, "name"] = " ".join(args.name)
            df.at[index,"changed"] = 1
            print("Name changed to:"," ".join(args.name))
    #Date    
        if(args.date != None):
            try:
                dateTime = dateutil.parser.parse(args.date[0])
                df.at[index, "due_date"] = dateTime
                df.at[index, "changed"] = 1
                print("Date changed to",dateTime.strftime("Task due date set as: %B-%d-%Y"))
            except:
                print("Date is invalid. Keeping saved value.")
    #Priority
        if(args.priority != None):
            if(0 < args.priority[0] and args.priority[0] < 6):
                df.at[index, "priority"] = args.priority[0]
                df.at[index, "changed"] = 1
                print("Priority Level changed to:", args.priority[0])
            else:
                print("Priority is out of range. Keeping saved value.")
        if(args.complete == True):
            compareValue = df.at[index,"complete"]
            if (compareValue == 0):
                df.at[index,"complete"] = 1
                df.at[index, "completion_date"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                df.at[index, "changed"] = 1
                print("Task marked as complete. Completion Time set to now.")
            else:
                df.at[index,"complete"] = 0
                df.at[index, "completion_date"] = None
                df.at[index, "changed"] = 1
                print("Task marked as incomplete. The completion date has been set to none.")
#Removal
    if(args.remove == True):
        index = df[df["id"] == int(args.ID[0])].index.item()
        df.at[index,"deletion"] = 1
        print("Task deleted. Task name:", df.at[index,"name"])
#automatic saving because come ON
    justDoubleCheckin = updateSQL(df)
    if justDoubleCheckin == True:
        print("Changes Saved.")
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