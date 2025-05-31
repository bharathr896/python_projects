import streamlit as st
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
)
st.subheader("💰 Expense Tracker")

# Initialize session states
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "incomes" not in st.session_state:
    st.session_state.incomes = []

if "show_expense_form" not in st.session_state:
    st.session_state.show_expense_form = False

if "show_income_form" not in st.session_state:
    st.session_state.show_income_form = False

# Tabs
overview_tab, transaction_tab, accounts_tab, reports_tab = st.tabs(
    ["Overview", "Transactions", "Accounts", "Reports"]
)

# --- OVERVIEW TAB ---
with overview_tab:
    st.subheader("Overview")

    # Metrics section
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Summary", "₹10,000", delta="↑ ₹500", delta_color="normal")
    with col2:
        st.metric("Accounts", "5", delta="↑ 1", delta_color="off")

    # Action buttons for Expense and Income
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Expense"):
            st.session_state.show_expense_form = True
            st.session_state.show_income_form = False

    with col2:
        if st.button("💵 Income"):
            st.session_state.show_income_form = True
            st.session_state.show_expense_form = False

    # EXPENSE FORM
    if st.session_state.show_expense_form:
        with st.form("expense_form"):
            st.subheader("Add Expense")
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Education"])
            amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f", key="expense_amount")
            account = st.selectbox("Account", ["Cash", "Credit Card", "Bank Account"], key="expense_account")
            date = st.date_input("Date", key="expense_date")
            description = st.text_input("Description", key="expense_desc")
            submit_expense = st.form_submit_button("Add Expense")

            if submit_expense:
                st.session_state.expenses.append({
                    "Type": "Expense",
                    "Date": date,
                    "Category": category,
                    "Amount (₹)": amount,
                    "Account": account,
                    "Description": description
                })
                st.success("Expense added!")

            #st.session_state.show_expense_form = False

    # INCOME FORM
    if st.session_state.show_income_form:
        with st.form("income_form"):
            st.subheader("Add Income")
            source = st.selectbox("Source", ["Salary", "Freelance", "Business", "Investments", "Other"])
            amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f", key="income_amount")
            account = st.selectbox("Account", ["Cash", "Bank Account"], key="income_account")
            date = st.date_input("Date", key="income_date")
            description = st.text_input("Description", key="income_desc")
            submit_income = st.form_submit_button("Add Income")

            if submit_income:
                st.session_state.incomes.append({
                    "Type": "Income",
                    "Date": date,
                    "Source": source,
                    "Amount (₹)": amount,
                    "Account": account,
                    "Description": description
                })
                st.success("Income added!")

    # Display all transactions
    st.subheader("📋 All Entries")
    if st.session_state.expenses or st.session_state.incomes:
        st.session_state.show_expense_form = False

        df_exp = pd.DataFrame(st.session_state.expenses)
        df_inc = pd.DataFrame(st.session_state.incomes)

        combined_df = pd.concat([df_exp, df_inc], ignore_index=True)
        combined_df.sort_values("Date", ascending=False, inplace=True)
        st.dataframe(combined_df, use_container_width=True)
    else:
        st.info("No transactions added yet.")

        

