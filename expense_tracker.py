import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set up the Streamlit app
st.title("Personal Expense Tracker")

# Initialize a session state to store expenses
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Amount", "Category"])

# Input form for expenses
st.subheader("Add a New Expense")
with st.form(key="expense_form"):
    date = st.date_input("Date", value=datetime.today())
    amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
    submit_button = st.form_submit_button(label="Add Expense")

# When the form is submitted, add the expense to the dataframe
if submit_button:
    new_expense = pd.DataFrame({
        "Date": [date],
        "Amount": [amount],
        "Category": [category]
    })
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
    st.success("Expense added!")

# Display the expense table
st.subheader("Your Expenses")
if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses)
else:
    st.write("No expenses added yet.")

# Visualizations
if not st.session_state.expenses.empty:
    # Pie chart for category breakdown
    st.subheader("Spending by Category")
    pie_fig = px.pie(st.session_state.expenses, values="Amount", names="Category", title="Expense Distribution")
    st.plotly_chart(pie_fig)

    # Line graph for spending over time
    st.subheader("Spending Over Time")
    # Group by date to handle multiple entries per day
    time_data = st.session_state.expenses.groupby("Date").sum().reset_index()
    line_fig = px.line(time_data, x="Date", y="Amount", title="Daily Spending Trend")
    st.plotly_chart(line_fig)

# Optional: Clear all expenses (for testing)
if st.button("Reset Tracker"):
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Amount", "Category"])
    st.success("Tracker reset!")