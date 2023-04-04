#import rich
import pandas as pd
import sqlite3
import dateutil
import datetime
import re

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
    df = pd.read_sql("SELECT id, name, complete, due_date, priority, completion_date FROM tasks", connection, parse_dates=["due_date", "completion_date"])
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
    return df

def usrInput():
    '''
    Checks the user's input. Does not have any arguments, and could be merged with mainView. If the input matches with known strings (or some shortened versions) then it will call a function related to them (ie: create a task, update a task, ect.)
    '''
    inputStr = input()
    #done
    if(inputStr == "new" or inputStr == "n"):
        createTask()
        #print("n")
        return True
    #incomplete
    if(inputStr == "c"or inputStr == "complete"): #change to be "first few characters = c"
        #truncate input to just the task to complete and link it up
        #maybe do this??? https://stackoverflow.com/questions/52143468/python-tab-autocompletion-in-script
        completeTask()
        #print("C")
        return True
    #incomplete
    if(inputStr == "e" or inputStr == "edit"):
        #print("E")
        editTask()
        return True
    #incomplete
    if(inputStr == "q" or inputStr == "quit"):
        #print("Q")
        return False
    #incomplete
    if(inputStr == "h" or inputStr == "help"):
        print("help")
        return True
    if(inputStr == "s" or inputStr == "save"):
        updateSQL(pandaDF)
        pandaDF["new"] = 0
        pandaDF["changed"] = 0
        return True
    else:
       print("Input not recognized, please try again")
       usrInput()
    return

def editTask():
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


    return
    

def completeTask():
    '''
    Function that takes in a specific task, and then updates both dataframes (pandas and SQL table) with complete = true and the date/time at which it was completed.
    '''

    #update values for date completed and completion status: https://www.sqlitetutorial.net/sqlite-update/
    return

def createTask():
    '''
    Function to create a new task in the SQL database. Takes in multiple arguments and then uses the insert keyword to create a new row in the SQL database. Additionally, should add a new row to the pandas library.
    '''
    #Get Task Name
    print("Please type the task to complete and press enter.")
    taskName = input()
   
    #Get date: Loop until valid date or empty line
    while True:
        try:
            print("Please type the date the task is due in MM/DD/YY format, and press enter.")
            print("If there is no due date, simply press enter.")
            taskDate = input()
             #Parse the string, make sure that it's in the correct format. No need to use stptime, dateutil works great
            #to implement wild card, use dateutil as suggested in (https://stackoverflow.com/questions/1258199/python-datetime-strptime-wildcard)
            taskDate = dateutil.parser.parse(taskDate)
            today = datetime.datetime.today()
            #documentation for string formatting: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
            #If there's a better way of doing this I'd gladly just do that instead because this is sort of ugly.
            if (taskDate.strftime("%Y")==today.strftime("%Y")):
                if(taskDate.strftime("%d")=="01" or taskDate.strftime("%d")=="21" or taskDate.strftime("%d")=="31"):
                    print(taskDate.strftime("Task due date set as: %A, %B %dst."))
                elif(taskDate.strftime("%d")=="02" or taskDate.strftime("%d")=="22"):
                    print(taskDate.strftime("Task due date set as: %A, %B %dnd."))
                elif(taskDate.strftime("%d")=="03" or taskDate.strftime("%d")=="23"):
                    print(taskDate.strftime("Task due date set as: %A, %B %drd."))
                else:
                    print(taskDate.strftime("Task due date set as: %A, %B %dth."))
            else:
                if(taskDate.strftime("%d")=="01" or taskDate.strftime("%d")=="21" or taskDate.strftime("%d")=="31"):
                    print(taskDate.strftime("Task due date set as: %B %dst, %Y"))
                elif(taskDate.strftime("%d")=="02" or taskDate.strftime("%d")=="22"):
                    print(taskDate.strftime("Task due date set as: %B %dnd, %Y"))
                elif(taskDate.strftime("%d")=="03" or taskDate.strftime("%d")=="23"):
                    print(taskDate.strftime("Task due date set as: %B %drd, %Y"))
                else:
                    print(taskDate.strftime("Task due date set as: %B %dth, %Y"))
        except:
            #check if it's blank because there is no due date.
            if taskDate == "":
                taskDate = None
                print("No task due date set.")
                break
            #maybe add a check so you can quit out of this part?
            #just boot you back to the main view.
            print("That date doesn't seem correct. Please try again.")
            continue
        break
    #Get priority of task. Can be left blank. Will compare to regex, [1-5].
    #If there's an error, ask user to repeat putting it in.
    while True:
        print("Please input the priority of the task from 1-5. and press enter.")
        print("If you do not want to set a priority level, simply press enter.")
        priorityLevel = input()
        if(priorityLevel == ''):
            print("No priority level set.")
            priorityLevel = 0
            break
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
    #loop end
    #Now, collect all data and put it into corresponding things.
    print("Task Name: ", taskName, ", Due Date:", taskDate,", Priority Level: ", priorityLevel)
    idNumber = len(pandaDF) + 1
    pandaDF.loc[idNumber] = [idNumber, taskName, 0, taskDate, priorityLevel, None, 0, 1]
    print("Task Added. Returning to main view.")
    return

def updateSQL(df):
    #Updates SQL from the dataframe.
    changedRows = df[df["changed"] == 1]
    newRows = df[df["new"] == 1]
    connection = sqlite3.connect("tasklist.db")
    curs = connection.cursor()
    print(changedRows)
    print(newRows)
    for x in range(len(changedRows)):
        #convert datetime into strings (sqlite.... why can't you be normal about this one)
        tempDate = changedRows.iloc[x]["due_date"]
        if(tempDate != pd.NaT):
            strDueDate = tempDate.strftime("%Y-%M-%D")
        else:
            strDueDate = None
        tempDate2 = changedRows.iloc[x]["completion_date"]
        if(tempDate2 != pd.NaT):
            strCompletionDate = tempDate2.strftime("%Y-%M-%D")
        else:
            strCompletionDate = None
        #https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds
        
        
        #set values and set the SQL request string
        values = (str(changedRows.iloc[x]["name"]), int(changedRows.iloc[x]["complete"]), strDueDate, int(changedRows.iloc[x]["priority"]), strCompletionDate, int(changedRows.iloc[x]["id"]))
        updateString = ''' UPDATE tasks
        SET name = ?
            due_date = ?
            complete = ?
            due_date = ?
            priority = ?
            completion_date = ?
        WHERE id = ?
        '''
        curs.execute(updateString, values)
    for y in range(len(newRows)):
        tempDate3 = newRows.iloc[y]["due_date"]
        if (tempDate3 != pd.NaT):
            strNewDate = tempDate3.strftime("%Y-%M-%D")
        else:
            strNewDate = None
        tempDate4 = newRows.iloc[y]["completion_date"]
        if (tempDate4 != None):
            strNewCompletion = tempDate4.strftime("%Y-%M-%D")
        else:
            strNewCompletion = None
        newValues = (int(newRows.iloc[y]["id"]), str(newRows.iloc[y]["name"]), int(newRows.iloc[y]["complete"]), strNewDate, int(newRows.iloc[y]["priority"]), strNewCompletion)
        insertString = ''' INSERT INTO tasks(id, name, complete, due_date, priority, completion_date)
        VALUES(?,?,?,?,?,?)
        '''
        curs.execute(insertString, newValues)
    connection.close()
    return

def mainView():
    '''
    Main overview of the program. In end result, should display a table of tasks to complete, along with other statistics to be decided (total tasks completed/completed in a week, completed task streak?, ect.)
    Make sure overdue tasks are in their own category at the top.
    '''
    continueFlag = True
    while continueFlag == True:
        print(pandaDF)
        #need to figure out how to actually get the main view to look cool
        print("terminal input: h for help")
        #run input function
        continueFlag = usrInput()
    return

pandaDF = initialize()
#implementing new column variable to cut down on how many rows the program will update
#0 = not changed 1 = changed
#only update changed values in database
pandaDF["changed"] = 0
#Implementing column variable to also flag when I need to use a different function to update the database.
#0 = not new, 1 = new
#if new need to add a row rather than update it.
pandaDF["new"] = 0
mainView()