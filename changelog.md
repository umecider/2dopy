12/27:
- added change log
- added cml edit function
- changed cml edit and complete function to be true/false flags that require an ID modifier (so you can adjust completion status)
- added rules for id flag dependencies (enforces that it must be used with cml edit/complete)
- As of right now, before title search is implemented, the CML is completely done. adding title search will be a pain for CML inputs specifically so I'm planning to keep it in the way of using ID only, so it can be used for automation purposes or in the way of an API of sorts
- found bug with calling multiple functions at once. Have applied a limit to ensure only one action is used at once.
- implemented basic removal system
    - main issue is that it doesn't explicitly remove it from the pandas table until exit - even after saving. This is pretty bad because it means that the ID number won't free up until the next time the application is used, and could cause issues due to the way that ID numbers are assigned (it's based on length)
    - so basically if one were to have four tasks and delete any task but the fourth one, 2 tasks would be assigned the same ID.
        -probably just going to have it assign the ID based on the last task to be added to the list, adding an edge case for when the database is empty.
- revamped ID system in the way previously discussed
    - thought it broke all ID based indexing systems but I was already doing it properly, it seems.
- fixed complete function for command line (i forgot to adjust how it worked after changing the ID system :/)
- fixed indexing for edit/delete in command line (was operating under the faulty old way of  ID-1)
- added remove command for commandline
- fixed broken ID reporting for new command for cml
- added a check for inputting a negative ID number
- made the main view remove deleted rows after the change had been made in the SQL
    - Will need to update the view somehow to indicate files marked for deletion. with a TUI/rich I could show with strikethrough but I doubt tabulate has that feature.

2/28/24:
refactoring code. SQL and Dataframe files/functions have been made/converted. Need to overhaul how the CML arguments work.
Need to finalize how to work with datetimes - at the moment, considering storing and working with them in string format in the dataframe, and converting if/when it is needed.
The alternative is only working in timestamps - this would be easier as the conversion just needs to happen upon startup and when pulling from SQL. However, if they aren't used, a bit of performance is lost. Regardless right now I'm working with both which is less than ideal.