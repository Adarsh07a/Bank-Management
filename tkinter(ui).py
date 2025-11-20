import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import json
import random
import string

class Bank:
    database='datbase.json'
    data=[]

    try: 
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("Sorry we are facing some issues: ")

    except Exception as err:
        print(f"An error occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(cls.data))
    
    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id_list = alpha + digits
        random.shuffle(id_list)
        return "".join(id_list)

    def create_account(self):
        name = simpledialog.askstring("Create Account", "Enter your name:")
        email = simpledialog.askstring("Create Account", "Enter your email:")
        phone = simpledialog.askstring("Create Account", "Enter your phone number (10 digits):")
        pin = simpledialog.askstring("Create Account", "Enter your 4-digit PIN:")

        if not (name and email and phone and pin):
            messagebox.showerror("Error", "All fields are required.")
            return

        if len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Error", "Invalid phone number.")
            return
        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN must be 4 digits.")
            return

        d={
            "name": name,
            "email": email,
            "phone no.": int(phone),
            "pin": int(pin),
            "Account no.":Bank.__accountno(),
            "Balance": 0
        }
        messagebox.showinfo("Account Created", f"Your account number is: {d['Account no.']}")
        Bank.data.append(d)
        Bank.__update()

    def deposite_money(self):
        accNo = simpledialog.askstring("Deposit", "Enter your account no.:")
        pin = simpledialog.askstring("Deposit", "Enter your pin:")
        if not (accNo and pin):
            messagebox.showerror("Error", "All fields are required.")
            return
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == int(pin)]
        if not user_data:
            messagebox.showerror("Error", "User not found.")
            return
        amount_str = simpledialog.askstring("Deposit", "Enter amount to be deposited (max 10000):")
        if not amount_str or not amount_str.isdigit():
            messagebox.showerror("Error", "Invalid amount.")
            return
        amount = int(amount_str)
        if amount <=0 or amount > 10000:
            messagebox.showerror("Error", "Amount should be between 1 and 10000.")
            return
        user_data[0]['Balance'] += amount
        Bank.__update()
        messagebox.showinfo("Success", "Amount credited successfully.")

    def withdraw_money(self):
        accNo = simpledialog.askstring("Withdraw", "Enter your account no.:")
        pin = simpledialog.askstring("Withdraw", "Enter your pin:")
        if not (accNo and pin):
            messagebox.showerror("Error", "All fields are required.")
            return
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == int(pin)]
        if not user_data:
            messagebox.showerror("Error", "User not found.")
            return
        amount_str = simpledialog.askstring("Withdraw", "Enter amount to be withdrawn (max 10000):")
        if not amount_str or not amount_str.isdigit():
            messagebox.showerror("Error", "Invalid amount.")
            return
        amount = int(amount_str)
        if amount <=0 or amount > 10000:
            messagebox.showerror("Error", "Amount should be between 1 and 10000.")
            return
        if user_data[0]['Balance'] < amount:
            messagebox.showerror("Error", "Insufficient balance.")
            return
        user_data[0]['Balance'] -= amount
        Bank.__update()
        messagebox.showinfo("Success", "Amount debited successfully.")

    def details(self):
        accNo = simpledialog.askstring("Details", "Enter your account no.:")
        pin = simpledialog.askstring("Details", "Enter your pin:")
        if not (accNo and pin):
            messagebox.showerror("Error", "All fields are required.")
            return
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == int(pin)]
        if not user_data:
            messagebox.showerror("Error", "User not found.")
            return
        details_str = ""
        for key, value in user_data[0].items():
            details_str += f"{key}: {value}\n"
        messagebox.showinfo("Account Details", details_str)

    def update_details(self):
        accNo = simpledialog.askstring("Update", "Enter your account no.:")
        pin = simpledialog.askstring("Update", "Enter your pin:")
        if not (accNo and pin):
            messagebox.showerror("Error", "All fields are required.")
            return
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == int(pin)]
        if not user_data:
            messagebox.showerror("Error", "User not found.")
            return
        current_data = user_data[0]
        messagebox.showinfo("Update Info", "Leave field blank to keep current value.")
        name = simpledialog.askstring("Update", f"Enter new name (current: {current_data['name']}):")
        email = simpledialog.askstring("Update", f"Enter new email (current: {current_data['email']}):")
        phone = simpledialog.askstring("Update", f"Enter new phone no. (current: {current_data['phone no.']}):")
        pin = simpledialog.askstring("Update", f"Enter new pin (current: {current_data['pin']}):")
        if name:
            current_data['name'] = name
        if email:
            current_data['email'] = email
        if phone:
            if len(phone)==10 and phone.isdigit():
                current_data['phone no.'] = int(phone)
            else:
                messagebox.showerror("Error", "Invalid phone number.")
                return
        if pin:
            if len(pin)==4 and pin.isdigit():
                current_data['pin'] = int(pin)
            else:
                messagebox.showerror("Error", "Invalid PIN.")
                return
        Bank.__update()
        messagebox.showinfo("Success", "Details updated!")

    def delete_account(self):
        accNo = simpledialog.askstring("Delete", "Enter your account no.:")
        pin = simpledialog.askstring("Delete", "Enter your pin:")
        if not (accNo and pin):
            messagebox.showerror("Error", "All fields are required.")
            return
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == int(pin)]
        if not user_data:
            messagebox.showerror("Error", "User not found.")
            return
        for i in Bank.data:
            if i["Account no."] == accNo and i["pin"] == int(pin):
                Bank.data.remove(i)
                break
        Bank.__update()
        messagebox.showinfo("Success", "Account deleted successfully!")

# Tkinter GUI setup
app = tk.Tk()
app.title("Bank Management System")
app.geometry("400x400")

bank_user = Bank()

# Buttons for each operation
btn_create = tk.Button(app, text="Create Account", width=20, command=bank_user.create_account)
btn_deposit = tk.Button(app, text="Deposit Money", width=20, command=bank_user.deposite_money)
btn_withdraw = tk.Button(app, text="Withdraw Money", width=20, command=bank_user.withdraw_money)
btn_details = tk.Button(app, text="Account Details", width=20, command=bank_user.details)
btn_update = tk.Button(app, text="Update Details", width=20, command=bank_user.update_details)
btn_delete = tk.Button(app, text="Delete Account", width=20, command=bank_user.delete_account)

# Layout
btn_create.pack(pady=10)
btn_deposit.pack(pady=10)
btn_withdraw.pack(pady=10)
btn_details.pack(pady=10)
btn_update.pack(pady=10)
btn_delete.pack(pady=10)

app.mainloop()