#from rich import print
#from rich.table import Table 
#from rich_tools import df_to_table
import pandas as pd
import sqlite3
import dateutil
import datetime
import re
import time
import warnings
#pandas keeps saying i'm concating empty frames but.... i'm literally just using df.loc
warnings.simplefilter(action='ignore', category=FutureWarning)

#https://stackoverflow.com/questions/37288421/how-to-plot-a-chart-in-the-terminal cool idea for future implementation; output a graph/date time chart through the terminal, though could also just generate and output them like normal.

def initialize():
    '''
    To run when program starts. Creates DB and attempts to connect to it, and also makes any tables if they do not exist.
    For development: It might be wise to also create a connection function so I don't need to write conection = sqlite3.connect("tasklist.db") constantly for updates to it. Additionally, need to make ure variables like the pandas DB are GLOBAL SCOPE or else this will suck lol (could also pass them along constantly but I'm not sure if there's any benefit to that.)
    '''
    #create DB using connection function: https://www.sqlitetutorial.net/sqlite-python/creating-database/
    connection = sqlite3.connect("tasklist.db")
    #creating tables if they do not already exist: https://www.sqlitetutorial.net/sqlite-python/creating-tables/
    cursor = connection.cursor()
    
    """
    Table Documention.
    see https://www.digitalocean.com/community/tutorials/sql-data-types for data type explanations.
    id - primary key, is the main indicator of each row. Cannot be name because of repeat tasks
    name - text, cannot be null. This is the task to be completed.
    complete - integer, cannot be null. 0 for incomplete, 1 for complete. Can add other numbers for different categorizations; could also use text but brain small and it makes it a bit more complicated.
    due_date - text...? Could also be DATETIME, though it would require user correction because no one is going to put seconds for their todos.
    priority - integer. cannot be null, just add 0 for cases without priority. Could also be text. 0-5 in terms of how to prioritize it, should affect the order in which things are displayed in the actual list. ie: sort by due date, then sub sort by priority value.
          -For this, 0 = No priority, 1= Very Low priority, 2 = Low Priority, 3 = Medium Priority, 4 = High Priority, 5 = Very High Priority.
    completion_date - text. same boat as due_date.
    potential additon:
    date added: allows to track how fast you complete tasked based on when you put them in. might be useful?
    """
#sql was wrong for this one: https://www.sqlitetutorial.net/sqlite-date/
#need to then parse the imported data to datetime objects
    tableCreationString = '''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    complete INTEGER NOT NULL,
    due_date TEXT,
    priority INTEGER NOT NULL,
    completion_date TEXT
    )
    '''
    cursor.execute(tableCreationString)
    #create pandas DF from the sql database and return it. 
    #note: ID will be the same as the index in the dataframe. importing it and then replacing the dataframe index is probably the best route to take here. Unsure about it atm but still importing id
    df = pd.read_sql("SELECT id, name, complete, due_date, priority, completion_date FROM tasks", connection)
    #close sql database call
    connection.close()
    #convert string to datetime
    #https://stackoverflow.com/questions/26763344/convert-pandas-column-to-datetime
    #using format as reccommended by https://stackoverflow.com/questions/26763344/convert-pandas-column-to-datetime/75277434#75277434
    df["due_date"] = pd.to_datetime(df["due_date"], format = "%Y-%m-%d %H:%M:%S")
    df["completion_date"] = pd.to_datetime(df["completion_date"], format = "%Y-%m-%d %H:%M:%S")

    '''
    note: Will be using pandas.DataFrame object for editing and changing values.
    When quitting application, values will then be written out to the SQL file.
    Should write a way to add a new column to the dataframe, called "changed" for editing values
    (that way we don't need to update all values, and just the ones that have been changed)
    ''' 

    #implementing new column variable to cut down on how many rows the program will update
    #0 = not changed 1 = changed
    #only update changed values in database
    df["changed"] = 0
    #Implementing column variable to also flag when I need to use a different function to update the database.
    #0 = not new, 1 = new
    #if new need to add a row rather than update it.
    df["new"] = 0
    #Implementing column variable to mark rows for deletion upon an update. Will exclude these from the main view.'
    df["deletion"] = 0

    return df

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
            df.at[completedIndex, "completion_date"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
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
        return
    priorityLevel = prioritySet()
    if(priorityLevel == 'quit'):
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
        print("Please input the ID number of the task you'd like to delete, or input quit to go back to the main menu.")
        toRemove = input()
        #quit to menu
        if(toRemove.rstrip().lower() == "quit" or toRemove.rstrip().lower() == 'q'):
            return
        if(re.match(r"\d+", toRemove) != None):
            return deleteRow(df, int(toRemove))

def updateSQL(df) -> bool:
    #Updates SQL from the dataframe.
    changedRows = df[df["changed"] == 1]
    newRows = df[df["new"] == 1]
    toDelete = df[df["deletion"] == 1]
    if(len(changedRows)==0 and len(newRows)==0 and len(toDelete) == 0):
        return False
    connection = sqlite3.connect("tasklist.db")
    curs = connection.cursor()
    #print(changedRows)
    #print(newRows)
    if(len(newRows)>0):
        for y in range(len(newRows)):
            tempDate3 = newRows.iloc[y]["due_date"]
            if (type(tempDate3) != type(pd.NaT) and tempDate3 != None):
                strNewDate = tempDate3.strftime("%Y-%m-%d %H:%M:%S")
            else:
                strNewDate = None
            tempDate4 = newRows.iloc[y]["completion_date"]
            if (tempDate4 != None and type(tempDate4) != type(pd.NaT)):
                strNewCompletion = tempDate4.strftime("%Y-%m-%d %H:%M:%S")
            else:
                strNewCompletion = None
            newValues = (int(newRows.iloc[y]["id"]), str(newRows.iloc[y]["name"]), int(newRows.iloc[y]["complete"]), strNewDate, int(newRows.iloc[y]["priority"]), strNewCompletion)
            #added or ignore because sometimes it randomly fails (probably because there's nothing to update)
            insertString = ''' INSERT OR IGNORE INTO tasks('id', 'name', 'complete', 'due_date', 'priority', 'completion_date')
            VALUES(?,?,?,?,?,?)
            '''
            curs.execute(insertString, newValues)
    if(len(changedRows)>0):
        for x in range(len(changedRows)):
            #convert datetime into strings (sqlite.... why can't you be normal about this one)
            tempDate = changedRows.iloc[x]["due_date"]
            if(type(tempDate) != type(pd.NaT) and tempDate != None):
                strDueDate = tempDate.strftime("%Y-%m-%d %H:%M:%S")
            else:
                strDueDate = None
            tempDate2 = changedRows.iloc[x]["completion_date"]
            if(type(tempDate2) != type(pd.NaT) and tempDate2 != None):
                strCompletionDate = tempDate2.strftime("%Y-%m-%d %H:%M:%S")
            else:
                strCompletionDate = None
            #set values and set the SQL request string
            values = (str(changedRows.iloc[x]["name"]), int(changedRows.iloc[x]["complete"]), strDueDate, int(changedRows.iloc[x]["priority"]), strCompletionDate, int(changedRows.iloc[x]["id"]))
            updateString = ''' UPDATE tasks
            SET name = ?,
                complete = ?,
                due_date = ?,
                priority = ?,
                completion_date = ? 
            WHERE 
                id = ?;
            '''
            curs.execute(updateString, values)
    if(len(toDelete) > 0):
        for z in range(len(toDelete)):
            #https://www.sqlitetutorial.net/sqlite-delete/
            deletionID = int(toDelete.iloc[z]["id"])
            deletionString = ''' DELETE from tasks
            WHERE
                id = ?;
            '''
            #fails when doing tuple, using list as per https://stackoverflow.com/questions/11853167/parameter-unsupported-when-inserting-int
            curs.execute(deletionString,[deletionID])
    connection.commit()
    connection.close()
    return True

