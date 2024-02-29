import pandas as pd
import sqlite3
import datetime


###Constants###
DATABASE = "tasklist.db"

### TO DO:
###     - create a system to minimize number of connections made.
###

### Refactoring - All functions to interface w/ SQL Database ###

def initialize_table() -> None:
    '''
    To run when program starts. Creates DB and attempts to connect to it, and also makes any tables if they do not exist.
    For development: It might be wise to also create a connection function so I don't need to write conection = sqlite3.connect(DATABASE) constantly for updates to it. Additionally, need to make ure variables like the pandas DB are GLOBAL SCOPE or else this will suck lol (could also pass them along constantly but I'm not sure if there's any benefit to that.)
    '''
    #create DB using connection function: https://www.sqlitetutorial.net/sqlite-python/creating-database/
    connection = sqlite3.connect(DATABASE)
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
    #close sql database call
    connection.close()
    return

def create(tasks: list) -> None:
    #formatting for task [[dict],[dict],...,[dict]]
    #ok you can apparently do this https://stackoverflow.com/questions/31324310/how-to-convert-rows-in-dataframe-in-python-to-dictionaries
    #open sql
    connection = sqlite3.connect(DATABASE)
    curs = connection.cursor()
    #add tasks in
    for x in tasks:
        #due date formatting
        tempDate3 = x["due_date"]
        if (type(tempDate3) != type(pd.NaT) and tempDate3 != None):
            strNewDate = tempDate3.strftime("%Y-%m-%d %H:%M:%S")
        else:
            strNewDate = None
        #not sure why this is here but it's probably necessary for if you make and immediately complete a task
        tempDate4 = x["completion_date"]
        if (tempDate4 != None and type(tempDate4) != type(pd.NaT)):
            strNewCompletion = tempDate4.strftime("%Y-%m-%d %H:%M:%S")
        else:
            strNewCompletion = None
        newValues = (int(x["id"]), str(x["name"]), int(x["complete"]), strNewDate, int(x["priority"]), strNewCompletion)
        #added or ignore because sometimes it randomly fails (probably because there's nothing to update)
        insertString = ''' INSERT OR IGNORE INTO tasks('id', 'name', 'complete', 'due_date', 'priority', 'completion_date')
        VALUES(?,?,?,?,?,?)
        '''
        curs.execute(insertString, newValues)
    connection.commit()
    connection.close()
    return

def update(tasks:list) -> None:
    connection = sqlite3.connect(DATABASE)
    curs = connection.cursor()
    for x in tasks:
        #convert datetime into strings (sqlite.... why can't you be normal about this one)
        #refactoring update - they are apparently strings now. cool.
        tempDate = x["due_date"]
        if(type(tempDate) != type(pd.NaT) and tempDate != None):
            strDueDate = tempDate#.strftime("%Y-%m-%d %H:%M:%S")
        else:
            strDueDate = None
        tempDate2 = x["completion_date"]
        if(type(tempDate2) != type(pd.NaT) and tempDate2 != None):
            strCompletionDate = tempDate2#.strftime("%Y-%m-%d %H:%M:%S")
        else:
            strCompletionDate = None
        #set values and set the SQL request string
        values = (str(x["name"]), int(x["complete"]), strDueDate, int(x["priority"]), strCompletionDate, int(x["id"]))
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
    connection.commit()
    connection.close()
    return

def delete(tasks:list)-> None:
    connection = sqlite3.connect(DATABASE)
    curs = connection.cursor()
    #https://www.sqlitetutorial.net/sqlite-delete/
    for x in tasks:
        deletionID = int(x["id"])
        deletionString = ''' DELETE from tasks
        WHERE
            id = ?;
        '''
        #fails when doing tuple, using list as per https://stackoverflow.com/questions/11853167/parameter-unsupported-when-inserting-int
        curs.execute(deletionString,[deletionID])
    connection.commit()
    connection.close()
    return

def select(ids:list): #returns task list from ids, list has ints. Task list is list of dicts.
    connection = sqlite3.connect(DATABASE)
    curs = connection.cursor()
    rows = []
    selectString = """ SELECT * 
    FROM tasks
    WHERE id = ?
    """
    for x in ids:
        #https://pynative.com/python-sqlite-select-from-table/
        curs.execute(selectString, [x]) #gets all tasks with id = x
        tempRow = curs.fetchone() #gets the first task from the list
        #print(tempRow)
        #Return format:
        #tuple -> (id, name, completed, due date, priority, completion date)
        if tempRow == None: #check if the fetch exists
            pass
        else:
            rows.append({"id":tempRow[0], "name": tempRow[1], "complete": tempRow[2], "due_date": tempRow[3], "priority": tempRow[4], "completion_date": tempRow[5]})
    connection.close()
    return rows


def createDF() ->pd.DataFrame:
    connection = sqlite3.connect(DATABASE)
    #can i just select * from tasks
    #also just uncompleted or all? Uncompleted would be better for saving disk space
    df = pd.read_sql("SELECT id, name, complete, due_date, priority, completion_date FROM tasks", connection)
    connection.close()
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

def newID() -> int:
    """
    Used for generating new task IDs. Gets the largest ID in the dataframe and then adds 1 to it.
    Can also be used for getting current largest ID.
    """
    connection = sqlite3.connect(DATABASE)
    curs = connection.cursor()
    #grab max id value - https://www.w3schools.com/sql/sql_min_max.asp
    toExecute = """ SELECT MAX(id)
    FROM tasks
    """
    curs.execute(toExecute)
    temp = int(curs.fetchone()[0]) #get tuple, get first element of tuple, convert to int
    #while i would like to just return using curs.fetchone we gotta close that connection
    #also fetchone returns a tuple. no matter what. weird
    connection.close()
    return temp + 1 #I forgot to increment orz