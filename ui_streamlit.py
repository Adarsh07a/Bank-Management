import ui_streamlit as st
from pathlib import Path
import json
import random
import string

# Your Bank class code here
class Bank:
    database='datbase.json'
    data=[]

    try: 
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read_text())
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
        alpha=random.choices(string.ascii_letters,k=5)
        digits=random.choices(string.digits,k=4)
        id=alpha+digits
        id_list=list(id)
        random.shuffle(id_list)
        return "".join(id_list)
    
    def create_account(self):
        d={
            "name":st.text_input("Please enter your name: "),
            "email":st.text_input("Please enter your email: "),
            "phone no.":st.number_input("Enter your phone number:", min_value=1000000000, max_value=9999999999),
            "pin":st.number_input("Enter your pin (4 digits):", min_value=1000, max_value=9999),
            "Account no.":Bank.__accountno(),
            "Balance": 0
        }
        st.write(f"Please remember your account number: {d['Account no.']}")
        # Validate pin and phone number again if needed
        if len(str(d['pin']))!=4:
            st.error("Pin must be 4 digits.")
        elif len(str(d['phone no.']))!=10:
            st.error("Phone number must be 10 digits.")
        else:
            Bank.data.append(d)
            Bank.__update()
            st.success("Account created successfully!")

    def deposite_money(self):
        accNo = st.text_input("Enter your account no.:")
        pin = st.number_input("Enter your pin:", min_value=1000, max_value=9999)
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        amount = st.number_input("Enter amount to be deposited:", min_value=1)
        if not user_data:
            st.error("User not found")
        else:
            if amount <= 0:
                st.error("Invalid amount")
            elif amount > 10000:
                st.error("Cannot deposit more than 10,000 at once")
            else:
                user_data[0]['Balance'] += amount
                Bank.__update()
                st.success("Amount credited successfully!")

    def withdraw_money(self):
        accNo = st.text_input("Enter your account no.:")
        pin = st.number_input("Enter your pin:", min_value=1000, max_value=9999)
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        amount = st.number_input("Enter amount to be withdrawn:", min_value=1)
        if not user_data:
            st.error("User not found")
        else:
            if amount <= 0:
                st.error("Invalid amount")
            elif amount > 10000:
                st.error("Cannot withdraw more than 10,000 at once")
            elif user_data[0]['Balance'] < amount:
                st.error("Insufficient balance")
            else:
                user_data[0]['Balance'] -= amount
                Bank.__update()
                st.success("Amount debited successfully!")

    def details(self):
        accNo = st.text_input("Enter your account no.:")
        pin = st.number_input("Enter your pin:", min_value=1000, max_value=9999)
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            st.error("User not found!")
        else:
            st.write("Account Details:")
            for key, value in user_data[0].items():
                st.write(f"{key}: {value}")

    def update_details(self):
        accNo = st.text_input("Enter your account no.:")
        pin = st.number_input("Enter your pin:", min_value=1000, max_value=9999)
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            st.error("User not found!")
        else:
            st.write("Update your details (leave blank to skip):")
            new_name = st.text_input("New Name:")
            new_email = st.text_input("New Email:")
            new_phone = st.text_input("New Phone no.:")
            new_pin_input = st.text_input("New PIN:")

            new_data = {
                'name': new_name if new_name else user_data[0]['name'],
                'email': new_email if new_email else user_data[0]['email'],
                'phone no.': int(new_phone) if new_phone else user_data[0]['phone no.'],
                'pin': int(new_pin_input) if new_pin_input else user_data[0]['pin'],
                'Account no.': user_data[0]['Account no.'],
                'Balance': user_data[0]['Balance']
            }

            # Update data
            for i in Bank.data:
                if i['Account no.'] == accNo:
                    i.update(new_data)
            Bank.__update()
            st.success("Details updated!")

    def delete_account(self):
        accNo = st.text_input("Enter your account no.:")
        pin = st.number_input("Enter your pin:", min_value=1000, max_value=9999)
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            st.error("User not found!")
        else:
            Bank.data.remove(user_data[0])
            Bank.__update()
            st.success("Account deleted successfully!")

# Streamlit UI
st.title("Bank Management System")

bank = Bank()

option = st.selectbox("Choose an operation:",
                        ["Create Account", "Deposit Money", "Withdraw Money", "Account Details",
                         "Update Details", "Deactivate Account"])

if option == "Create Account":
    st.header("Create New Account")
    bank.create_account()

elif option == "Deposit Money":
    st.header("Deposit Money")
    bank.deposite_money()

elif option == "Withdraw Money":
    st.header("Withdraw Money")
    bank.withdraw_money()

elif option == "Account Details":
    st.header("Account Details")
    bank.details()

elif option == "Update Details":
    st.header("Update Account Details")
    bank.update_details()

elif option == "Deactivate Account":
    st.header("Deactivate Account")
    bank.delete_account()