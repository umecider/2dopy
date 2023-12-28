12/27:
- added change log
- added cml edit function
- changed cml edit and complete function to be true/false flags that require an ID modifier (so you can adjust completion status)
- added rules for id flag dependencies (enforces that it must be used with cml edit/complete)
- As of right now, before title search is implemented, the CML is completely done. adding title search will be a pain for CML inputs specifically so I'm planning to keep it in the way of using ID only, so it can be used for automation purposes or in the way of an API of sorts
- found bug with calling multiple functions at once. Have applied a limit to ensure only one action is used at once.