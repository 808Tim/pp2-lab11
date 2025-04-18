import psycopg2
import csv

conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL
);
""")
conn.commit()

# Function to show all contacts

def show_all_contacts():
    cur.execute("SELECT * FROM contacts ORDER BY id")
    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
    else:
        # print("\nAll Contacts:")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")


# Insert contact from console

def add_contact_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    # Check if user exists

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    existing = cur.fetchone()

    if existing:

        # Update phone number

        cur.execute("UPDATE contacts SET phone = %s WHERE name = %s", (phone, name))
        print("Contact updated!")
    else:

        # Insert new contact

        cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        print("Contact added!")

    conn.commit()

def query_contacts_paginated():
    try:
        limit = int(input("How many contacts per page? "))
        page = int(input("Enter page number: "))

        offset = (page - 1) * limit
        cur.execute("SELECT * FROM contacts ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()

        if not rows:
            print("No contacts found on this page.")
        else:
            print(f"\nContacts — Page {page}:")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")


# Using CSV file

def add_contacts_from_csv():
    file_name = input("Enter CSV file name:")
    try:
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:
                    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row[0], row[1]))
            conn.commit()
            print("Contacts loaded from CSV!")
    except Exception as e:
        print("[ERROR]:", e)

# Update contact data

def update_contact():
    field = input("What do you want to update? (name/phone): ").strip().lower()
    if field == "name":
        old = input("Enter current name: ")
        new = input("Enter new name: ")
        cur.execute("UPDATE contacts SET name = %s WHERE name = %s", (new, old))
    elif field == "phone":
        old = input("Enter current phone: ")
        new = input("Enter new phone: ")
        cur.execute("UPDATE contacts SET phone = %s WHERE phone = %s", (new, old))
    else:
        print("Invalid option")
        return
    conn.commit()
    print("Contact updated!")

# Query contacts with filters

def query_contacts():
    field = input("Search by name or phone: ").strip().lower()
    value = input("Enter search value: ")
    if field == "name":
        cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", (f"%{value}%",))
    elif field == "phone":
        cur.execute("SELECT * FROM contacts WHERE phone ILIKE %s", (f"%{value}%",))
    else:
        print("Invalid search field")
        return
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

# Delete contact by name or phone

def delete_contact():
    field = input("Delete by name or phone: ").strip().lower()
    value = input("Enter value to delete: ")
    if field == "name":
        cur.execute("DELETE FROM contacts WHERE name = %s", (value,))
    elif field == "phone":
        cur.execute("DELETE FROM contacts WHERE phone = %s", (value,))
    else:
        print("Invalid field")
        return
    conn.commit()
    print("Contact deleted!")

# Menu

if __name__ == "__main__":
    while True:
        print("\nPhoneBook Menu:")
        print("1. Show contacts")
        print("2. Add contact from console")
        print("3. Load contacts from CSV")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("7. Show contacts with pagination")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            show_all_contacts()
        elif choice == "2":
            add_contact_console()
        elif choice == "3":
            add_contacts_from_csv()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            query_contacts_paginated()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")

    cur.close()
    conn.close()
