from pathlib import Path
import json
import string
import random

class Bank:
    database='database2.json'
    data=[]


    try:
        if Path(database).exists():
            with open (database) as fs:
                data=json.loads(fs.read())

        else:
            print("Sorry we are facing some issues!")

    except Exception as err:
        print(f"An error occured as {err}")

    @classmethod
    def __update(cls):
        with open (cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def __accountNo():
        alpha=random.choices(string.ascii_letters,k=5)
        digits=random.choices(string.digits,k=4)
        id=alpha+digits
        random.shuffle(id)
        return "".join(id)
    
    def create_account(self):
        d={
            "Name":input("Enter your name: "),
            "Email":input("Enter your email address: "),
            "Phone no.":int(input("Enter your phone number: ")),
            "Pin":int(input("Enter your pin: ")),
            "AccountNo.":Bank.__accountNo(),
            "Balance":0

        }

        print(f"Please remember your Account Number: {d['AccountNo.']}")

        if len(str(d['Pin']))!=4:
            print("Your pin should contain 4 digits")

        if len(str(d['Phone no.']))!=10:
            print("Please enter a valid phone number(10 digits)")

        else:
            Bank.data.append(d)
            Bank.__update()

user=Bank()
user.create_account()
    


