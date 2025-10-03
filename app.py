import streamlit as st
import pandas as pd 
import datetime as date 

FILE = "expenses.csv"

def load_expenses():
    """load data from the csv if there"""
    try:
        return read.csv(FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

def add_expenses(date,category,amount,note):
    """add new expense to the csv file"""
    df = load_expenses()
    new_entry = pd.DataFrame([[date, category, amount, note]], 
                             columns=["Date", "Category", "Amount", "Note"])
    df = pd.concat([df,new_entry], ignore_index=True)
    df.to_csv(FILE,index=FALSE)

st.title("💰 Personal Expense Tracker")

st.sidebar.header("➕ Add New Expense")

with st.sidebar.form("expense_form"):
    exp_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=1, step=1)
    note = st.text_input("Note")
    submit = st.form_submit_button("Add Expense")
    if submit:
        add_expense(exp_date, category, amount, note)
        st.sidebar.success("✅ Expense added!")
df = load_expenses()
if not df.empty:
    st.subheader("📋 All Expenses")
    st.dataframe(df)
else:
    st.info("No expenses recorded yet. Use the sidebar to add your first one!")
