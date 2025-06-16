import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

# File to store transactions
CSV_FILE = "transactions.csv"

# Load or create data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Type", "Date", "Category/Source", "Amount (₹)", "Account", "Description"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Page setup
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
st.title("💰 Expense Tracker")

# Tabs
overview_tab, add_tab, transactions_tab, reports_tab = st.tabs(["Overview", "➕ Add Entry", "Transactions", "Reports"])

# --- OVERVIEW TAB ---
with overview_tab:
    st.subheader("📊 Overview")

    df = load_data()  # Refresh data for accurate metrics
    total_exp = df[df["Type"] == "Expense"]["Amount (₹)"].sum()
    total_inc = df[df["Type"] == "Income"]["Amount (₹)"].sum()
    balance = total_inc - total_exp

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_inc:,.2f}")
    col2.metric("Total Expense", f"₹{total_exp:,.2f}")
    col3.metric("Net Balance", f"₹{balance:,.2f}")

    if not df.empty:
        with st.expander("📊 Expense Breakdown"):
            exp_data = df[df["Type"] == "Expense"]
            if not exp_data.empty:
                cat_sum = exp_data.groupby("Category/Source")["Amount (₹)"].sum()
                fig, ax = plt.subplots(figsize=(2.5, 2.5))  # Compact size
                ax.pie(
                    cat_sum,
                    labels=cat_sum.index,
                    autopct="%1.1f%%",
                    startangle=90,
                    textprops={'fontsize': 7}
                )
                ax.axis("equal")
                st.pyplot(fig, use_container_width=False)  # Prevent auto-expansion


# --- ADD ENTRY TAB ---
with add_tab:
    st.subheader("➕ Add New Entry")
    entry_type = st.radio("Select Type", ["Expense", "Income"], horizontal=True)

    with st.form("entry_form", clear_on_submit=True):
        if entry_type == "Expense":
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Education"])
            amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
            account = st.selectbox("Account", ["Cash", "Credit Card", "Bank Account"])
            date_input = st.date_input("Date", value=date.today())
            description = st.text_input("Description")

            submitted = st.form_submit_button("Add Expense")
            if submitted and amount > 0:
                new_row = {
                    "Type": "Expense",
                    "Date": pd.to_datetime(date_input),
                    "Category/Source": category,
                    "Amount (₹)": amount,
                    "Account": account,
                    "Description": description
                }
                df = load_data()
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success("✅ Expense added!")
                st.rerun()
            elif submitted:
                st.warning("Amount must be greater than ₹0")

        else:
            source = st.selectbox("Source", ["Salary", "Freelance", "Business", "Investments", "Other"])
            amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
            account = st.selectbox("Account", ["Cash", "Bank Account"])
            date_input = st.date_input("Date", value=date.today())
            description = st.text_input("Description")

            submitted = st.form_submit_button("Add Income")
            if submitted and amount > 0:
                new_row = {
                    "Type": "Income",
                    "Date": pd.to_datetime(date_input),
                    "Category/Source": source,
                    "Amount (₹)": amount,
                    "Account": account,
                    "Description": description
                }
                df = load_data()
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success("✅ Income added!")
                st.rerun()
            elif submitted:
                st.warning("Amount must be greater than ₹0")

# --- TRANSACTIONS TAB ---
with transactions_tab:
    st.subheader("📋 All Transactions")

    df = load_data()
    if not df.empty:
        df = df.sort_values("Date", ascending=False)
        df["Date"] = pd.to_datetime(df["Date"]).dt.date  # Show only date (no time)

        with st.expander("🔍 Filter"):
            filter_type = st.multiselect("Filter by Type", ["Expense", "Income"], default=["Expense", "Income"])

            # Dynamic category/source filtering
            if filter_type:
                filtered_df_temp = df[df["Type"].isin(filter_type)]
                available_categories = sorted(filtered_df_temp["Category/Source"].unique())
            else:
                available_categories = []

            filter_cat = st.multiselect("Filter by Category/Source", available_categories)

            # Apply filters
            filtered_df = df[df["Type"].isin(filter_type)]
            if filter_cat:
                filtered_df = filtered_df[filtered_df["Category/Source"].isin(filter_cat)]

        st.dataframe(filtered_df, use_container_width=True)

        st.download_button(
            "📥 Download CSV",
            data=filtered_df.to_csv(index=False),
            file_name="transactions.csv",
            mime="text/csv"
        )
    else:
        st.info("No transactions available.")


# --- REPORTS TAB ---
with reports_tab:
    st.subheader("📈 Monthly Report")
    df = load_data()

    if not df.empty:
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        monthly_summary = df.groupby(["Month", "Type"])["Amount (₹)"].sum().unstack().fillna(0)
        st.bar_chart(monthly_summary)

        with st.expander("📌 Income vs Expense by Month"):
            st.dataframe(monthly_summary.style.format("₹{:.2f}"))
    else:
        st.info("Add some transactions to generate reports.")
