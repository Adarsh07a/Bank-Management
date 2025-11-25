import streamlit as st
from pathlib import Path
import string
import random
import json

# --------------------- Backend Class ---------------------
class Library:
    database = 'database3.json'
    data = {"users": [], "books": []}

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
    except Exception as err:
        st.error(f"An error occurred: {err}")

    @classmethod
    def update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def generate_card_id():
        alpha = random.choices(string.ascii_letters, k=3)
        digits = random.choices(string.digits, k=3)
        return "".join(alpha + digits)

    # --------------------- Main Operations -------------------------
    def create_card(self, name, email, phone):
        if len(str(phone)) != 10:
            return "❌ Phone number must be 10 digits."

        user = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "id": Library.generate_card_id()
        }

        Library.data["users"].append(user)
        Library.update()
        return f"✅ Registered Successfully!\nYour Card ID is: **{user['id']}**"

    def add_book(self, title):
        Library.data["books"].append({"Name": title})
        Library.update()
        return "📚 Book added successfully!"

    def issue_book(self, card_id, book_name):
        user = next((u for u in Library.data["users"] if u["id"] == card_id), None)
        if not user:
            return "❌ Invalid Card ID!"

        book = next((b for b in Library.data["books"] if b["Name"].lower() == book_name.lower()), None)
        if not book:
            return "❌ Book not found in library!"

        Library.data["books"].remove(book)
        user["Issued_Book"] = book["Name"]
        Library.update()

        return f"✅ Book '{book['Name']}' issued successfully to {user['Name']}."

    def return_book(self, card_id):
        user = next((u for u in Library.data["users"] if u["id"] == card_id), None)
        if not user:
            return "❌ Invalid Card ID!"

        if "Issued_Book" not in user:
            return "❌ You have no issued book."

        book_name = user["Issued_Book"]
        Library.data["books"].append({"Name": book_name})
        del user["Issued_Book"]

        Library.update()
        return f"🔄 Book '{book_name}' returned successfully!"

    def remove_book(self, title):
        book = next((b for b in Library.data["books"] if b["Name"].lower() == title.lower()), None)
        if not book:
            return "❌ Book not found"

        Library.data["books"].remove(book)
        Library.update()
        return "🗑️ Book removed successfully!"

    def delete_user(self, card_id):
        user = next((u for u in Library.data["users"] if u["id"] == card_id), None)
        if not user:
            return "❌ Invalid Card ID!"

        Library.data["users"].remove(user)
        Library.update()
        return f"🗑️ User '{user['Name']}' deleted successfully!"

    # --------------------- New Feature 1: Search ---------------------
    def search_books(self, keyword):
        keyword = keyword.lower()
        results = [b for b in Library.data["books"] if keyword in b["Name"].lower()]
        return results

    # --------------------- New Feature 2: Issued Books ---------------------
    def get_issued_books(self):
        issued = [u for u in Library.data["users"] if "Issued_Book" in u]
        return issued

    # --------------------- New Feature 3: Available Books ---------------------
    def get_available_books(self):
        return Library.data["books"]


# --------------------- Streamlit UI -----------------------

st.title("📚 Library Management System (Streamlit)")

obj = Library()

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Create Card", "Add Book", "Issue Book", "Return Book",
        "Remove Book", "Delete User", "Search Books",
        "Show Issued Books", "Show Available Books", "View Database"
    ]
)

# --------------------- UI Screens -------------------------

if menu == "Create Card":
    st.header("Create Library Card")
    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone Number")

    if st.button("Create"):
        if name and email and phone:
            st.success(obj.create_card(name, email, phone))
        else:
            st.error("Please fill all fields!")

elif menu == "Add Book":
    st.header("Add Book")
    title = st.text_input("Book Title")

    if st.button("Add"):
        st.success(obj.add_book(title))

elif menu == "Issue Book":
    st.header("Issue Book")
    card = st.text_input("Card ID")
    bname = st.text_input("Book Name")

    if st.button("Issue"):
        st.success(obj.issue_book(card, bname))

elif menu == "Return Book":
    st.header("Return Book")
    cid = st.text_input("Card ID")

    if st.button("Return"):
        st.success(obj.return_book(cid))

elif menu == "Remove Book":
    st.header("Remove Book")
    t = st.text_input("Book Title")

    if st.button("Remove"):
        st.success(obj.remove_book(t))

elif menu == "Delete User":
    st.header("Delete User")
    cid = st.text_input("Card ID")

    if st.button("Delete"):
        st.success(obj.delete_user(cid))

# --------------------- Search Feature -----------------------------
elif menu == "Search Books":
    st.header("🔍 Search Books")
    keyword = st.text_input("Enter keyword")

    if st.button("Search"):
        results = obj.search_books(keyword)
        if results:
            st.subheader("Results:")
            st.table(results)
        else:
            st.error("No matching books found.")

# --------------------- Show Issued Books --------------------------
elif menu == "Show Issued Books":
    st.header("📘 Issued Books")
    issued = obj.get_issued_books()

    if issued:
        st.table(issued)
    else:
        st.info("No books are issued currently.")

# --------------------- Show Available Books ------------------------
elif menu == "Show Available Books":
    st.header("📚 Available Books")
    books = obj.get_available_books()

    if books:
        st.table(books)
    else:
        st.info("No books available.")

# --------------------- View Raw Database ---------------------------
elif menu == "View Database":
    st.header("Users")
    st.json(Library.data["users"])

    st.header("Books")
    st.json(Library.data["books"])
