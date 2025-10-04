import streamlit as st
import pandas as pd
from datetime import date
import os

EXPENSE_FILE = "expenses.csv"
PEOPLE_FILE = "people.csv"

# ---------------------------
# Data helpers
# ---------------------------
def load_expenses():
    try:
        df = pd.read_csv(EXPENSE_FILE)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Note", "Paid By", "Split Between"])

    expected = ["Date", "Category", "Amount", "Note", "Paid By", "Split Between"]
    for col in expected:
        if col not in df.columns:
            df[col] = ""
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    return df


def save_expenses(df):
    df.to_csv(EXPENSE_FILE, index=False)


def add_expense(exp_date, category, amount, note, paid_by, split_between):
    df = load_expenses()
    date_str = exp_date.isoformat() if hasattr(exp_date, "isoformat") else str(exp_date)
    new_entry = pd.DataFrame([[
        date_str, category, float(amount), note, paid_by, ",".join(split_between)
    ]], columns=["Date", "Category", "Amount", "Note", "Paid By", "Split Between"])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_expenses(df)


def load_people():
    try:
        return pd.read_csv(PEOPLE_FILE)["Person"].tolist()
    except (FileNotFoundError, pd.errors.EmptyDataError, KeyError):
        return []


def save_people(people_list):
    pd.DataFrame({"Person": people_list}).to_csv(PEOPLE_FILE, index=False)

#UI
st.title("💰 Split it ")

# Manage People
st.sidebar.header("👥 Manage People")
people = load_people()

with st.sidebar.form("people_form", clear_on_submit=True):
    new_person = st.text_input("Add a person")
    add_person = st.form_submit_button("➕ Add")
    if add_person and new_person:
        if new_person not in people:
            people.append(new_person)
            save_people(people)
            st.sidebar.success(f"Added {new_person}")
        else:
            st.sidebar.warning(f"{new_person} already exists!")

if people:
    remove_person = st.sidebar.selectbox("Remove person", options=[""] + people)
    if st.sidebar.button("❌ Remove") and remove_person:
        people = [p for p in people if p != remove_person]
        save_people(people)
        st.sidebar.success(f"Removed {remove_person}")

# Add Expense
st.sidebar.header("➕ Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    exp_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=1.0, step=50.0, format="%.2f")
    note = st.text_input("Note")

    paid_by = st.selectbox("Paid By", people if people else [""])
    split_between = st.multiselect("Split Between", options=people, default=people)

    submit = st.form_submit_button("Add Expense")
    if submit:
        if not people:
            st.sidebar.error("⚠️ Please add people first before adding an expense!")
        else:
            add_expense(exp_date, category, amount, note, paid_by, split_between)
            st.sidebar.success("✅ Expense added!")

# Show Data
df = load_expenses()
if not df.empty:
    st.subheader("📋 All Expenses")
    st.dataframe(df)
else:
    st.info("No expenses recorded yet. Use the sidebar to add your first one!")


# import streamlit as st
# import pandas as pd
# from datetime import date

# FILE = "expenses.csv"

# def load_expenses():
#     """Load data from the CSV if there; normalize types and handle empty file."""
#     try:
#         df = pd.read_csv(FILE)
#     except (FileNotFoundError, pd.errors.EmptyDataError):
#         return pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

    
#     expected = ["Date", "Category", "Amount", "Note"]
#     if not all(col in df.columns for col in expected):
#         return pd.DataFrame(columns=expected)
#     df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
#     df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

#     return df


# def add_expenses(exp_date, category, amount, note):
#     """Add new expense to the CSV file (stores date as ISO string)."""
#     df = load_expenses()
#     date_str = exp_date.isoformat() if hasattr(exp_date, "isoformat") else str(exp_date)
#     new_entry = pd.DataFrame([[date_str, category, float(amount), note]],
#                              columns=["Date", "Category", "Amount", "Note"])
#     df = pd.concat([df, new_entry], ignore_index=True)
#     df.to_csv(FILE, index=False)


# st.title("💰 Split it ")

# st.sidebar.header("➕ Add New Expense")

# with st.sidebar.form("expense_form"):
#     exp_date = st.date_input("Date", date.today())
#     category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
#     amount = st.number_input("Amount (₹)", min_value=1.0, step=1.0, format="%.2f")
#     note = st.text_input("Note")
#     submit = st.form_submit_button("Add Expense")
#     if submit:
#         add_expenses(exp_date, category, amount, note)
#         st.sidebar.success("✅ Expense added!")


# df = load_expenses()

# if not df.empty:
#     # Summary metrics
#     total_spent = df["Amount"].sum()
#     avg_spent = df["Amount"].mean()
#     tx_count = len(df)

#     st.subheader("📊 Summary")
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Total Spent", f"₹{total_spent:,.2f}")
#     c2.metric("Average per Transaction", f"₹{avg_spent:,.2f}")
#     c3.metric("Transactions", f"{tx_count}")

#     # Category breakdown
#     st.subheader("📂 Category Breakdown")
#     cat_sum = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
#     if not cat_sum.empty:
#         st.bar_chart(cat_sum)
#     else:
#         st.info("No category data to display yet.")

#     st.subheader("📋 All Expenses")
#     st.dataframe(df)
# else:
#     st.info("No expenses recorded yet. Use the sidebar to add your first one!")
