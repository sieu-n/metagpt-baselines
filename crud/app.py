import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('client.db')
c = conn.cursor()

# Create new SQLite table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS customer (
        name TEXT,
        birthday TEXT,
        age INTEGER,
        sex TEXT,
        phone TEXT
    )
''')
conn.commit()

# Function to add a new customer
def add_customer(name, birthday, age, sex, phone):
    c.execute('''
        INSERT INTO customer (name, birthday, age, sex, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, birthday, age, sex, phone))
    conn.commit()

# Function to view all customers
def view_customers():
    c.execute('''
        SELECT * FROM customer
    ''')
    data = c.fetchall()
    return data

# Function to view customer by name
def view_customer_by_name(name):
    c.execute('''
        SELECT * FROM customer WHERE name=?
    ''', (name,))
    data = c.fetchall()
    return data

# Function to update customer details by name
def update_customer(name, birthday, age, sex, phone):
    c.execute('''
        UPDATE customer SET birthday=?, age=?, sex=?, phone=? WHERE name=?
    ''', (birthday, age, sex, phone, name))
    conn.commit()

# Function to delete a customer by name
def delete_customer(name):
    c.execute('''
        DELETE FROM customer WHERE name=?
    ''', (name,))
    conn.commit()

# Streamlit UI
st.title('Customer Management Program')

menu = ['Add', 'Retrieve', 'Update', 'Delete']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Add':
    st.subheader('Add New Customer')
    name = st.text_input('Name')
    birthday = st.date_input('Birthday')
    age = st.number_input('Age', value=0)
    sex = st.radio('Sex', ['Male', 'Female'])
    phone = st.text_input('Phone')

    if st.button('Add'):
        add_customer(name, birthday, age, sex, phone)
        st.success(f"Customer {name} added successfully!")

elif choice == 'Retrieve':
    st.subheader('Retrieve Customer Data')
    name = st.text_input('Enter Name to Retrieve')
    if name:
        customer = view_customer_by_name(name)
        if customer:
            st.write(pd.DataFrame(customer, columns=["Name", "Birthday", "Age", "Sex", "Phone"]))
        else:
            st.warning('No data found for the entered name')

elif choice == 'Update':
    st.subheader('Update Customer Data')
    name = st.text_input('Name')
    customer = view_customer_by_name(name)
    if customer:
        birthday = st.date_input('Birthday', datetime.strptime(customer[0][1], "%Y-%m-%d").date())
        age = st.number_input('Age', value=customer[0][2])
        sex = st.radio('Sex', ['Male', 'Female'], index=(0 if customer[0][3] == 'Male' else 1))
        phone = st.text_input('Phone', value=customer[0][4])

        if st.button('Update'):
            update_customer(name, str(birthday), age, sex, phone)
            st.success(f"Customer {name} updated successfully!")
    elif name:
        st.warning('No data found for the entered name')

elif choice == 'Delete':
    st.subheader('Delete Customer Data')
    name = st.text_input('Enter Name to Delete')
    if st.button('Delete'):
        delete_customer(name)
        st.warning(f"Customer {name} deleted successfully!")
