""" Library Management System """

from pathlib import Path
import string
import random
import json


class Library:
    database='database3.json'
    data={"users": [], "books": []}



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
    def __card_id():
        alpha=random.choices(string.ascii_letters,k=3)
        digits=random.choices(string.digits,k=3)
        id=alpha+digits
        return "".join(id)
    
    def create_card(self):
        d={
            "Name":input("Enter your name: "),
        "Email":input("Enter your email address: "),
        "Phone":int(input("Enter your phone number: ")),
        "id":Library.__card_id()
        }

        

        print(f"You are registered succesfully\nYour card id is:{d['id']}")

        

        if len(str(d['Phone']))!=10:
            print("Please enter a correct phone number(10 digits)")

        else:
            Library.data["users"].append(d)
            Library.__update()

    def add_book(self):
        books={
            "Name":input("Enter the title of the book: ")
        }

        Library.data["books"].append(books)
        Library.__update()
        print("Book added successfully")

    def issue_book(self):
        card_id = input("Enter your card ID: ")

    
        user_found = None
        for user in Library.data["users"]:
            if user["id"] == card_id:
                user_found = user
                break

        if not user_found:
            print("Invalid Card ID! No user found.")
            return

    
        book_name = input("Enter the name of the book you want to issue: ")

    
        book_found = None
        for book in Library.data["books"]:
            if book["Name"].lower() == book_name.lower():
                book_found = book
                break

        if not book_found:
            print("Sorry! Book not found in the library.")
            return

    
        user_found["Issued_Book"] = book_found["Name"]

    
        Library.data["books"].remove(book_found)

        Library.__update()
        print(f"Book '{book_found['Name']}' issued successfully to {user_found['Name']}.")

    def return_book(self):
        card_id = input("Enter your card ID: ")

        user_found = None
        for user in Library.data["users"]:
            if user["id"] == card_id:
                user_found = user
                break

        if not user_found:
            print("Invalid Card ID!")
            return

        if "Issued_Book" not in user_found:
            print("You have no issued book.")
            return

        book_name = user_found["Issued_Book"]

        Library.data["books"].append({"Name": book_name})
        del user_found["Issued_Book"]

        Library.__update()
        print(f"Book '{book_name}' returned successfully.")

    def remove_book(self):

        book_name=input("Enter the title of the book you want to remove: ")

        for book in Library.data["books"]:
            if book["Name"].lower() == book_name.lower():
                book_found = book
                break

        if not book_found:
            print("Sorry! Book not found in the library.")
            
        else:
            Library.data["books"].remove(book_found)

        Library.__update()

    def delete_user(self):

        card_id = input("Enter your card ID: ")

        user_found = None
        for user in Library.data["users"]:
            if user["id"] == card_id:
                user_found = user
                break

        if not user_found:
            print("Invalid Card ID!")
            
        else:
            Library.data["users"].remove(user_found)

        Library.__update()
        print(f"User '{user_found['Name']}' deleted successfully")



print("Press 1 to create library card")
print("Press 2 to add a book")
print("Press 3 to issue a book")
print("Press 4 to return a book")
print("Press 5 to remove a book")
print("Press 6 to delete user account:")

obj=Library()
choice=int(input("Enter your choice: "))


if choice==1:
    obj.create_card()

if choice==2:
    obj.add_book()

if choice==3:
    obj.issue_book()

if choice==4:
    obj.return_book()

if choice==5:
    obj.remove_book()

if choice==6:
    obj.delete_user()


