## Notes for gui version
Do not need to use a dataframe - can work with just SQL (since no need to print tables using term stuff) 
(tbh i can also implement stuff for this using the normal version but not right now lol)

fetchall() for sqlite returns list of tuples, values in tuple being in the same order as the sqlite table.

should probably init by doing fetchall w/ no completions (implement an option later for this) and then create new objects in a scrollable container, which should only take up maybe like, 3/4th of the terminal (need some room for that add/edit/remove bar at the bottom)

after any action using the bottom row - update the SQLite database and then completely recompose the table from scratch - completed tasks should be removed and new tasks added, and so on (though actually pushing completed actions should probably occur later, so people can unmark things as completed before they're pushed. auto push when performing other actions or quitting?)

contrary to earlier beliefs, edit should bring up a new menu - so it can show ALL tasks and not just the ones shown (or have to hastily add more in there). Same thing as remove.

remove and edit should have the same menu - show all tasks, with a button to select tasks. actual *actions* will differ when selected. 
    - for remove, bg should change and those tasks should be marked as tasks to be deleted. set them as a new class in textual and then grab the IDs and use the remove function.
    - for edit - just bring up new edit menu for when something is selected. Probaby isolate the task w/ buttons under each element that can be edited + check box for if it's completed or not (though needs a sanity check for if not complete and completed date is added.... though honestly does it even really matter LOL)
        - could also implement input boxes for each task, with the placeholder name for it being the old name (would need to have a widget for all of this)

not sure how to do the new views for the different apps, though. Maybe just... run new apps???? idk how you'd completely destroy and then recreate a new thing. ContentSwitcher? maybe just mount/remove widgets - making each view be it's own widget (seems weird but ok whatever)

ok actually maybe do something with TabbedContent? might be a little difficult though https://textual.textualize.io/widgets/tabbed_content/
either do that, or use screens https://textual.textualize.io/guide/screens/












## Misc Notes
- Found this going through my stuff again - might be worth looking into again, though I think first character of command/ full command is fine
    - #maybe do this??? https://stackoverflow.com/questions/52143468/python-tab-autocompletion-in-script
- Might be worth looking back into autosave and if it's necessary; most functions should push to SQL basically immediately, and with no way to save tasks from deletion idk what we're doing here lol
- Should probably get the config file to work soon - maybe the best option is to just re-write all the python stuff in it but replace the values lmao
    - though honestly at this point... do we even need it if i'm getting rid of the auto save.....



## About implementing search:
- Actually setting up the table shouldn't be too bad 

- After brainstorming a bit I will probably need to redo most of how the SQL stuff is handeled - atm it syncs up at the autosave/save function. I'll need it to immediately push changes to the both SQL tables (the one i store data in and the virtual one that should get deleted when the file starts/ends idk)
    - Maybe something like DELETE TABLE foo IF EXISTS and then CREATE VIRTUAL TABLE foo(id, name)

- virtual table setup is just 2 cols: id and then task name. for searching, grab the rows it returns and then return the IDs/names to another backend program (probably dataframe in this case, the pure search function should just return the output to cml)

- Search Function (sql.py)
    - get text
    - return list of rows that it gives you from there.

- Search Function (database.py)
    - prompt for text to search
    - send text to sql.py search function
    - after you get the IDs/Names, ask user to confirm (even if one)
        - just display id - name and then ask for which ID they want to choose
        - if none returned, go to redo prompt 
        - if user says no go to redo prompt
    - After, return **ONLY THE ID**
        - this should hook into the other functions that have a prompt asking for an ID number really nicely.
        - Maybe have an override for if they know the ID number in the specific prompts, ie "Please input the ID of the task you wish to mark as complete, or type text to search"
            - note that this fucks over any tasks with numbers in the name and they want to just search for "1" or something like that.
            - could force a specific input format like "ID: 15" or something
            - this wont be an issue in the GUI - we have tools to deal with this and could have like a check box or something.
    - Make sure to have an exit clause! Just return exit (many of these tasks have that implementation in place, just need to change what var it's checking and make it to only check for "quit" or whatever)