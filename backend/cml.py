import backend.sql as sql
import pandas as pd
from tabulate import tabulate
import dateutil
import datetime

def checkID(args, parser) -> None:
    for x in args.ID:
        if (x > (sql.newID()-1) or x <= 0): #note: newID()-1 = current largest ID.
            parser.error("The provided ID does not exist.")
    return

def addTask(name:str, date:datetime, priority:int) -> int:
    """
    Add task to SQL. Doesn't really need to be it's own function but it's easier to read.
    """
    id = sql.newID()
    newTask = {"id": id, "name": name, "complete": 0, "due_date": date, "priority": priority, "completion_date": None}
    sql.create([newTask])
    return id

def parseArgs(args, parser):
    sql.initialize_table()
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
        id = addTask(" ".join(args.name), dateTime, priorityLevel)
        print("Task added.\nName:", " ".join(args.name), "| Due Date:", dateTime, "| Priority:", priorityLevel, "| ID Number:", id)
#complete task 
    if(args.complete == True and args.edit == False):
        #check for if ID is in range
            checkID(args, parser)
            toComplete = sql.select(args.ID)
            if len(toComplete) < len(args.ID):
                parser.error("The provided ID does not exist.")
            else:
                for task in toComplete:
                    task["complete"] = 1
                    print("Task",task["id"],"marked as complete. Name:", task["name"])
                sql.update(toComplete)
                

#editing
    if(args.edit == True):
        task = sql.select(args.ID)[0]
    #Name
        if(args.name != None):
            task["name"] = " ".join(args.name)
            print("Name changed to:"," ".join(args.name))
    #Date    
        if(args.date != None):
            try:
                dateTime = dateutil.parser.parse(args.date[0])
                task["due_date"] = dateTime
                print("Date changed to",dateTime.strftime("Task due date set as: %B-%d-%Y"))
            except:
                print("Date is invalid. Keeping saved value.")
    #Priority
        if(args.priority != None):
            if(0 < args.priority[0] and args.priority[0] < 6):
                task["priority"] = args.priority[0]
                print("Priority Level changed to:", args.priority[0])
            else:
                print("Priority is out of range. Keeping saved value.")
        if(args.complete == True):
            compareValue = task["complete"]
            if (compareValue == 0):
                task["complete"] = 1
                task["completion_date"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                print("Task marked as complete. Completion Time set to now.")
            else:
                task["complete"] = 0
                task["completion_date"] = None
                print("Task marked as incomplete. The completion date has been set to none.")
        #COMMIT THE CHANGES MADE
        sql.update([task])
        print("Changes commited to SQL Database.")
#Removal
    if(args.remove == True):
        checkID(args, parser)
        tasks = sql.select(args.ID)
        if len(tasks) != len(args.ID):
            print("One or more of the IDs provided is invalid.")
        else:
            sql.delete(tasks)
        print("Tasks Deleted:")
        for task in tasks:
            print("ID:", task["id"], "|Name:", task["name"])
#search
    if(args.search == True):
        sql.searchTable(args.name[0])
#args show and all. To run last.
    if(args.show == True):
        #this is stolen from mainView() but slightly modified to work with the args
        df = sql.createDF()
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