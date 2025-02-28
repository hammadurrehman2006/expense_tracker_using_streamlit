import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Title using Html
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Personal Expense Tracker</h1>", unsafe_allow_html=True)

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Amount", "Category"])

# Input form for expenses
st.subheader("Add a New Expense")
with st.form(key="expense_form"):
    date = st.date_input("Date", value=datetime.today())
    amount = st.number_input("Amount ($)", min_value=1.0, step=1.0)
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
    submit_button = st.form_submit_button(label="Add Expense")

# When the form is submitted, add the expense to the list 
if submit_button:
    new_expense = pd.DataFrame({
        "Date": [date],
        "Amount": [amount],
        "Category": [category]
    })
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
    st.success("Expense added!")

# File upload for CSV
st.subheader("Or Upload Expenses")
uploaded_file = st.file_uploader("Upload a CSV (Date,Amount,Category)", type="csv")
if uploaded_file:
    uploaded_data = pd.read_csv(uploaded_file)
    st.session_state.expenses = pd.concat([st.session_state.expenses, uploaded_data], ignore_index=True)
    st.success("Expenses uploaded successfully!")

# Budget tracker
st.subheader("Budget Overview")
budget = st.number_input("Set Monthly Budget ($)", min_value=0.0, value=100.0)
total_spent = st.session_state.expenses["Amount"].sum()
st.write(f"Total Spent: ${total_spent:.2f} / Budget: ${budget:.2f}")
if total_spent > budget:
    st.warning("You've exceeded your budget!")

# Display the expense table
st.subheader("Your Expenses")
if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses)
else:
    st.write("No expenses added yet.")

#Graphs representation
if not st.session_state.expenses.empty:
    # Pie chart
    st.subheader("Spending by Category")
    pie_fig = px.pie(st.session_state.expenses, values="Amount", names="Category", title="Expense Distribution")
    st.plotly_chart(pie_fig)

    # Line graph
    st.subheader("Spending Over Time")
    time_data = st.session_state.expenses.groupby("Date").sum().reset_index()
    line_fig = px.line(time_data, x="Date", y="Amount", title="Daily Spending Trend")
    st.plotly_chart(line_fig)

# Clear all expenses in table
if st.button("Reset Tracker"):
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Amount", "Category"])
    st.success("Tracker reset!")