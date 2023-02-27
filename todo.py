import rich
import pandas
#check for existing database

def initialize():
    #add code here

def usrInput():
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

def mainView():
    while True:
        print("main view goes here :3")
        #need to figure out how to actually get the main view to look cool
        print("cml input: -h for help")
        #run input function
        usrInput()
    return
