from pathlib import Path 
import random
import string
import json

class Bank:
    database= 'database.json'
    data=[]

    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.reads())

        else:
            print("Sorry we are facing some issues:")

    except Exception as err:
        print (f"An error occured as {err}:")

