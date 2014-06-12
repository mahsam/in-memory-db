# in-memory-db

A simple in-memory database which I wrote it for fun.

## Data Commands:
 - `SET name value` - set value to the variable name
 - `GET name` - get the value of the variable name, returns null if name doens't exist
 - `UNSET name` - unset the variable, makes it like it was never set
 - `NUMEQUALTO value` - return the number of variables that currently are set to value
 - `END`: Exit the program.

## Transaction Commands:
 - `BEGIN` - Open a new transaction block. Transaction blocks can be nested; a BEGIN can be issued inside of an existing block.
 - `COMMIT` - Close all open transaction blocks, permanently applying the changes made in them. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
 - `ROLLBACK` - Undo all of the commands issues in the most recent transaction block, and close the block. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
 
## How to run:

 Run the script with your filename as an argument. There's some files in examples folder. 

```bash
$ python simple_db.py examples/file1.txt
```