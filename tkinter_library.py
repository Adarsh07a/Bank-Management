import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path
import string
import random
import json


class Library:
    database = 'database3.json'
    data = {"users": [], "books": []}

    # Load database
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("Database not found, creating new file...")
    except Exception as err:
        print(f"Error reading DB: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def __card_id():
        alpha = random.choices(string.ascii_letters, k=3)
        digits = random.choices(string.digits, k=3)
        return "".join(alpha + digits)

    # ---------- FUNCTIONS ----------

    @classmethod
    def create_card(cls):
        name = simpledialog.askstring("Name", "Enter your name:")
        email = simpledialog.askstring("Email", "Enter your email:")
        phone = simpledialog.askstring("Phone", "Enter your phone number:")

        if not (name and email and phone):
            return

        if len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Error", "Phone number must be 10 digits!")
            return

        user = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "id": cls.__card_id()
        }

        cls.data["users"].append(user)
        cls.__update()

        messagebox.showinfo("Success", f"User created.\nCard ID: {user['id']}")

    @classmethod
    def add_book(cls):
        book = simpledialog.askstring("Book Name", "Enter book title:")
        if not book:
            return
        cls.data["books"].append({"Name": book})
        cls.__update()
        messagebox.showinfo("Success", "Book added successfully")

    @classmethod
    def issue_book(cls):
        card = simpledialog.askstring("Card ID", "Enter your card ID:")
        if not card:
            return

        user = None
        for u in cls.data["users"]:
            if u["id"] == card:
                user = u
                break

        if not user:
            messagebox.showerror("Error", "User not found!")
            return

        book_name = simpledialog.askstring("Book", "Enter book name:")
        if not book_name:
            return

        book = None
        for b in cls.data["books"]:
            if b["Name"].lower() == book_name.lower():
                book = b
                break

        if not book:
            messagebox.showerror("Error", "Book not found!")
            return

        user["Issued_Book"] = book["Name"]
        cls.data["books"].remove(book)
        cls.__update()

        messagebox.showinfo("Success", f"Book '{book['Name']}' issued to {user['Name']}")

    @classmethod
    def return_book(cls):
        card = simpledialog.askstring("Card ID", "Enter your card ID:")
        if not card:
            return

        user = None
        for u in cls.data["users"]:
            if u["id"] == card:
                user = u
                break

        if not user:
            messagebox.showerror("Error", "User not found!")
            return

        if "Issued_Book" not in user:
            messagebox.showerror("Error", "You have no issued book.")
            return

        book_name = user["Issued_Book"]
        cls.data["books"].append({"Name": book_name})

        del user["Issued_Book"]

        cls.__update()
        messagebox.showinfo("Success", f"Book '{book_name}' returned successfully")

    @classmethod
    def remove_book(cls):
        book_name = simpledialog.askstring("Remove Book", "Enter book name to remove:")
        if not book_name:
            return

        book = None
        for b in cls.data["books"]:
            if b["Name"].lower() == book_name.lower():
                book = b
                break

        if not book:
            messagebox.showerror("Error", "Book not found!")
            return

        cls.data["books"].remove(book)
        cls.__update()
        messagebox.showinfo("Success", "Book removed successfully")

    @classmethod
    def delete_user(cls):
        card = simpledialog.askstring("Card ID", "Enter card ID to delete user:")
        if not card:
            return

        user = None
        for u in cls.data["users"]:
            if u["id"] == card:
                user = u
                break

        if not user:
            messagebox.showerror("Error", "User not found!")
            return

        cls.data["users"].remove(user)
        cls.__update()

        messagebox.showinfo("Success", f"User '{user['Name']}' deleted successfully")


# ----------- TKINTER WINDOW -----------

root = tk.Tk()
root.title("Library Management System")
root.geometry("400x450")
root.config(bg="#ECECEC")

title = tk.Label(root, text="Library Management System", font=("Arial", 16, "bold"), bg="#ECECEC")
title.pack(pady=20)

# Buttons (same colors, same style)
btn_style = {"width": 25, "height": 2, "font": ("Arial", 12)}

tk.Button(root, text="Create Library Card", command=Library.create_card, **btn_style).pack(pady=5)
tk.Button(root, text="Add Book", command=Library.add_book, **btn_style).pack(pady=5)
tk.Button(root, text="Issue Book", command=Library.issue_book, **btn_style).pack(pady=5)
tk.Button(root, text="Return Book", command=Library.return_book, **btn_style).pack(pady=5)
tk.Button(root, text="Remove Book", command=Library.remove_book, **btn_style).pack(pady=5)
tk.Button(root, text="Delete User Account", command=Library.delete_user, **btn_style).pack(pady=5)

root.mainloop()
