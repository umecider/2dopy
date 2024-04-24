#from rich import print
#from rich.table import Table 
#from rich_tools import df_to_table
import backend.sql as sql
import pandas as pd
import dateutil
import datetime
import re
import warnings
import time
#pandas keeps saying i'm concating empty frames but.... i'm literally just using df.loc
warnings.simplefilter(action='ignore', category=FutureWarning)

#https://stackoverflow.com/questions/37288421/how-to-plot-a-chart-in-the-terminal cool idea for future implementation; output a graph/date time chart through the terminal, though could also just generate and output them like normal.

def editTask(df):
    '''
    Function to edit existing task and change or add parts to it.
    '''
    #update values for specified parts: https://www.sqlitetutorial.net/sqlite-update/
    '''
    Methodology: 
    1 Obtain values from DataFrame for a specific task (will need to figure out how to search efficiently and deal with duplicate results later) 
    2 Ask for what to change in menu, with options for name, due date, completed status, completed date, and priority
    Also have a "complete" option
    Make this a while loop until complete option is selected.
    3 Update values for task, exit loop and function
    '''
    while True:
        try:
            print("Please type the ID Number of the task you would like to edit.")
            print("If you would like to return to the main menu, please type 'quit'")
            idNumber = input()
            #quit to menu
            if(idNumber.rstrip().lower() == "quit" or idNumber.rstrip().lower() == 'q'):
                return
            if(re.match(r"\d+", idNumber) != None):
                while True:
                    print(df[df["id"] == int(idNumber)])
                    index = df[df["id"] == int(idNumber)].index.item()
                    print("Please type what element you would like to change, and press enter. If you would like to quit, please type 'quit'.")
                    match input():
                        case "quit":
                            break
                        case "q":
                            break
                        case "due_date":
                            dateTime = getDate()
                            if dateTime != "quit":
                                df.at[index, "due_date"] = dateTime
                                df.at[index, "changed"] = 1
                        case "priority":
                            priorityNew = prioritySet()
                            if priorityNew != "quit":
                                df.at[index, "priority"] = priorityNew
                                df.at[index, "changed"] = 1
                        case "name":
                            print("Please type the new name of the task and press enter.")
                            df.at[index,"name"] = input()
                            df.at[index,"changed"] = 1
                        case "complete":
                            while True:
                                print("Please type 0 for not complete, and 1 for complete.")
                                completionBinary = input()
                                if(re.match(r"[0-1]", completionBinary) !=0):
                                    completionBinary = int(completionBinary)
                                    if(completionBinary == 1):
                                        df.at[index, "complete"] = 1
                                        df.at[index, "completion_date"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                                        df.at[index, "changed"] = 1
                                        break
                                    if(completionBinary == 0):
                                        df.at[index, "complete"] = 0
                                        df.at[index, "completion_date"] = None
                                        df.at[index, "changed"] = 1
                                        break
                                else:
                                    print("That doesn't seem to be valid.")
            else:
                print("The ID Provided does not seem to be valid. Please try one with only numbers.")
        except:
            print("The ID Provided seems to be invalid.")
            continue
        break
    return df
    
def getDate():
    #making this it's own function because I'm using it multiple times.
    while True:
        try:
            print("Please type the date the task is due in MM/DD/YY format, and the time it's due and press enter.")
            print("If you'd like to return to the previous menu, please type 'quit' and press enter.")
            print("If there is no due date, simply press enter.")
            taskDate = input()
             #Parse the string, make sure that it's in the correct format. No need to use stptime, dateutil works great
            #to implement wild card, use dateutil as suggested in (https://stackoverflow.com/questions/1258199/python-datetime-strptime-wildcard)
            taskDate = dateutil.parser.parse(taskDate)
            today = datetime.datetime.today()
            #documentation for string formatting: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
            #If there's a better way of doing this I'd gladly just do that instead because this is sort of ugly.
            #12/26/23 - to past me: why do we care about the hours when we don't accept that as input (adding this to the to-implement list)
            if(pd.Timestamp.min < taskDate < pd.Timestamp.max):
                if (taskDate.strftime("%Y")==today.strftime("%Y")):
                    if(taskDate.strftime("%d")=="01" or taskDate.strftime("%d")=="21" or taskDate.strftime("%d")=="31"):
                        print(taskDate.strftime("Task due date set as: %A, %B %dst at %I:%M %p."))
                    elif(taskDate.strftime("%d")=="02" or taskDate.strftime("%d")=="22"):
                        print(taskDate.strftime("Task due date set as: %A, %B %dnd at %I:%M %p."))
                    elif(taskDate.strftime("%d")=="03" or taskDate.strftime("%d")=="23"):
                        print(taskDate.strftime("Task due date set as: %A, %B %drd at %I:%M %p."))
                    else:
                        print(taskDate.strftime("Task due date set as: %A, %B %dth at %I:%M %p."))
                else:
                    if(taskDate.strftime("%d")=="01" or taskDate.strftime("%d")=="21" or taskDate.strftime("%d")=="31"):
                        print(taskDate.strftime("Task due date set as: %B %dst, %Y at %I:%M %p."))
                    elif(taskDate.strftime("%d")=="02" or taskDate.strftime("%d")=="22"):
                        print(taskDate.strftime("Task due date set as: %B %dnd, %Y at %I:%M %p."))
                    elif(taskDate.strftime("%d")=="03" or taskDate.strftime("%d")=="23"):
                        print(taskDate.strftime("Task due date set as: %B %drd, %Y at %I:%M %p."))
                    else:
                        print(taskDate.strftime("Task due date set as: %B %dth, %Y at %I:%M %p."))
                break
            else:
                print("That date appears to be too far away from the present!")
        except:
            #check if it's blank because there is no due date.
            if taskDate == "":
                taskDate = None
                print("No task due date set.")
                break
            if taskDate == "quit" or taskDate == "q":
                return "quit"
            #maybe add a check so you can quit out of this part?
            #just boot you back to the main view.
            print("That date doesn't seem correct. Please try again.")
    return taskDate

def prioritySet():
    while True:
        print("Please type the priority of the task from 1-5. and press enter.")
        print("If you do not want to set a priority level, simply press enter.")
        print("If you'd like to go back to the previous menu, please type 'quit'.")
        priorityLevel = input().strip()
        if(priorityLevel == ''):
            print("No priority level set.")
            priorityLevel = 0
            break
        if(priorityLevel.rstrip().lower() == "quit" or priorityLevel.rstrip().lower() == 'q'):
            return "quit"
        try:
            #Try regex for 1-5 in a string (and just one of them), and check that it doesn't return none
            #(can't just have it equal true because re.match returns a match object)
            if(re.match(r"[1-5]", priorityLevel)!=None):
                #convert priorityLevel to int and compare it to a switch case
                #(convert to int because that's what the table takes in, makes it easier to sort)
                priorityLevel = int(priorityLevel)
                match priorityLevel:
                    case 1:
                        print("Priority level set as Very Low Priority.")
                        break
                    case 2:
                        print("Priority level set as Low Priority.")
                        break
                    case 3:
                        print("Priority level set as Medium Priority.")
                        break
                    case 4:
                        print("Priority level set as High Priority.")
                        break
                    case 5:
                        print("Priority level set as Very High Priority.")
                        break
            else:
                print("Sorry, that doesn't appear to be correct. Please try again.")
        except:
            print("Sorry, that doesn't appear to be correct. Please try again.")
            continue
    return priorityLevel

def completeTask(df):
    '''
    Function that takes in a specific task, and then updates both dataframes (pandas and SQL table) with complete = true and the date/time at which it was completed.
    '''
    #main loop to get the ID number
    while True:
        print("Please type the ID Number of the task to be completed and press enter.")
        print("If you would like to return to the previous menu, please type 'quit'")
        toComplete = input()
        #exit loop
        if(toComplete.rstrip().lower() == "quit" or toComplete.rstrip().lower() == 'q'):
           return
        #check for only numbers
        if(re.match(r"\d+", toComplete) != None):
            #solution for getting index as an int is https://stackoverflow.com/questions/41217310/get-index-of-a-row-of-a-pandas-dataframe-as-an-integer
            #try to find id number in the dataframe
            completedIndex = df[df["id"] == int(toComplete)].index.item()
            #for df.at functionality: https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index
            df.at[completedIndex, "complete"] = 1
            df.at[completedIndex, "completion_date"] = datetime.datetime.today()#.strftime("%Y-%m-%d %H:%M:%S")
            df.at[completedIndex, "changed"] = 1
            print("Task status updated.")
            break
        else:
            print("Something went wrong, please try again.")

    return df

def createTask(df):
    '''
    Function to create a new task in the SQL database. Takes in multiple arguments and then uses the insert keyword to `create` a new row in the SQL database. Additionally, should add a new row to the pandas library.
    '''
    #Get Task Name
    print("Please type the name of the task to create and press enter.")
    print("If you'd like to return to the main view, just input 'quit' with no other characters.")
    taskName = input()
    if(taskName.rstrip() == 'quit' or taskName.rstrip() == "q" or taskName.rstrip() == ""):
        print("Exiting to menu...")
        return
    #Get date: Loop until valid date or empty line
    taskDate = getDate()
    if taskDate == "quit":
        print("Exiting to menu...")
        return
    priorityLevel = prioritySet()
    if(priorityLevel == 'quit'):
        print("Exiting to menu...")
        return
    #Now, collect all data and put it into corresponding things.
    print("Task Name: ", taskName, ", Due Date:", taskDate,", Priority Level: ", priorityLevel)
    addRow(df, taskName, taskDate, priorityLevel)
    print("Task Added. Returning to main view.")
    return df

def addRow(df, name, date = None, priority = 0):
    index = len(df) - 1
    if (index < 0):
        idNumber = 1
    else:
        idNumber = df.at[index,"id"] + 1
    df.loc[index+1] = [idNumber, name, 0, date, priority, None, 0, 1, 0] #id, name, complete, date, priority, completion_date, changed, new, deletion
    return

def deleteRow(df, id):
    index = df[df["id"] == int(id)].index.item()
    #print(index)
    #print(df)
    df.at[index, "deletion"] = 1
    return df

def removeRow(df) -> pd.DataFrame:
    while True:
        print("Please input the ID number of the task you'd like to delete, or input quit to go back to the main menu.\n !!! WARNING: THIS CANNOT BE UNDONE. !!!")
        toRemove = input()
        #quit to menu
        if(toRemove.rstrip().lower() == "quit" or toRemove.rstrip().lower() == 'q'):
            return
        if(re.match(r"\d+", toRemove) != None):
            return deleteRow(df, int(toRemove))

def updateSQL(df) -> bool:
    #Updates SQL from the dataframe.
    changedRows = pd.DataFrame(df[df["changed"] == 1]).to_dict("records")
    newRows = pd.DataFrame(df[df["new"] == 1]).to_dict("records")
    toDelete = pd.DataFrame(df[df["deletion"] == 1]).to_dict("records")
    sql.create(newRows)
    sql.update(changedRows)
    sql.delete(toDelete)
    return True

def usrInput(df) -> bool:
    '''
    Checks the user's input. Does not have any arguments, and could be merged with mainView. If the input matches with known strings (or some shortened versions) then it will call a function related to them (ie: create a task, update a task, ect.)

    unsure why i have a bunch listed as incomplete.
    '''
    inputStr = input()
    #standardize input
    inputStr = inputStr.rstrip().lower()
    #done
    if(inputStr == "new" or inputStr == "n"):
        df=createTask(df)
        #print("n")
        return True
    #incomplete
    if(inputStr == "c"or inputStr == "complete"): #change to be "first few characters = c"
        #truncate input to just the task to complete and link it up
        #maybe do this??? https://stackoverflow.com/questions/52143468/python-tab-autocompletion-in-script
        df=completeTask(df)
        #print("C")
        return True
    #incomplete
    if(inputStr == "e" or inputStr == "edit"):
        #print("E")
        df=editTask(df)
        return True
    #incomplete
    if(inputStr == "q" or inputStr == "quit"):
        #print("Q")
        autoSaveFlag = updateSQL(df)
        if(autoSaveFlag == True):
            print("Data Saved.\nHave a nice day! :)")
        else:
            print("Have a nice day! :)")
        return False
    #incomplete
    if(inputStr == "h" or inputStr == "help"):
        print("List of commands:")
        print("You can just input the first letter of each command as well.")
        commandList = [
            "New: Create a new task.",
            "Edit: Edit details of a task.",
            "Complete: Mark a task as complete.",
            "Remove: Mark a task for deletion upon saving.",
            "Save: Manually save the tasks to the database.",
            "Help: Display this message.",
            "Quit: Exit the program."
        ]
        #iterate through command list and print each string
        for x in commandList:
            print(x)
        return True
    if(inputStr == "s" or inputStr == "save"):
        changedFlag = updateSQL(df)
        df["new"] = 0
        df["changed"] = 0
        df.drop(df[df["deletion"] == 1].index, inplace = True)
        if(changedFlag == True):
            print("Data has been saved! Returning to menu.")
        elif(changedFlag == False):
            print("No changes or new data found! Returning to menu.")
        else:
            print("Something went wrong. Please try again.")
        time.sleep(1)
        return True
    if(inputStr == "r" or inputStr == "remove"):
        df = removeRow(df)
        return True
    else:
       print("Input not recognized, please try again")
       usrInput(df)
    return