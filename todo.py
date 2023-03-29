#import rich
import pandas as pd
import sqlite3

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
    completion_date - text. same boat as due_date.
    """

    tableCreationString = '''CREATE TABLE IF NOT EXISTS tasks (
    id integer PRIMARY KEY,
    name text NOT NULL,
    complete integer NOT NULL,
    due_date text,
    priority integer NOT NULL,
    completion_date text
    )
    '''
    cursor.execute(tableCreationString)
    #create pandas DF from the sql database and return it. 
    #note: ID will be the same as the index in the dataframe. importing it and then replacing the dataframe index is probably the best route to take here. Unsure about it atm but still importing id
    df = pd.read_sql("SELECT id, name, complete, due_date, priority, completion_date FROM tasks", connection, parse_dates=["due_date", "completion_date"])
    #close sql database call
    connection.close()
    return df

def usrInput():
    '''
    Checks the user's input. Does not have any arguments, and could be merged with mainView. If the input matches with known strings (or some shortened versions) then it will call a function related to them (ie: create a task, update a task, ect.)
    '''
    inputStr = input()
    if(inputStr == "new" or inputStr == "n"):
        #function to make new task
        return
    if(inputStr == "c"or inputStr == "complete"): #change to be "first few characters = c"
        #truncate input to just the task to complete and link it up
        #maybe do this??? https://stackoverflow.com/questions/52143468/python-tab-autocompletion-in-script
        return
    else:
       print("Input not recognized, please try again")
       usrInput()
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
    #Insert documentation: https://www.sqlitetutorial.net/sqlite-python/insert/
    #pandas concat documentation: https://pandas.pydata.org/docs/reference/api/pandas.concat.html#pandas.concat
    #use https://stackoverflow.com/questions/41217310/get-index-of-a-row-of-a-pandas-dataframe-as-an-integer to return index as an integer

    return

def mainView():
    '''
    Main overview of the program. In end result, should display a table of tasks to complete, along with other statistics to be decided (total tasks completed/completed in a week, completed task streak?, ect.)
    '''
    while True:
        print("main view goes here :3")
        #need to figure out how to actually get the main view to look cool
        print("cml input: -h for help")
        #run input function
        usrInput()
    return

pandaDF = initialize()
#mainView() <- don't run this yet, test the SQL functionality first.
