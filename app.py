import streamlit as st
import pandas as pd
from database import * 
from datetime import datetime
import plotly.express as px

create_tables()
st.set_page_config(page_title="Family Finance Tracker", layout="wide")

st.title("🏦 Family Finance Tracker")

# ---------- FIXED FAMILY USERS ----------
users = {
    "Sarthak": "1234",
    "Mom": "1111",
    "Dad": "2222",
    "Sister": "3333"
}

# ---------- LOGIN ----------
st.sidebar.header("🔐 Login")
username = st.sidebar.selectbox("User", list(users.keys()))
password = st.sidebar.text_input("PIN", type="password")

if st.sidebar.button("Login"):
    if users.get(username) == password:
        st.session_state["user"] = username
        st.sidebar.success("Logged in")
    else:
        st.sidebar.error("Wrong PIN")

# ---------- AFTER LOGIN ----------
if "user" in st.session_state:

    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Family Balance")

    data = get_transactions()
    df = pd.DataFrame(data, columns=["ID","Date","User","Type","Category","Amount"])

    if not df.empty:
        total_credit = df[df["Type"]=="Credit"]["Amount"].sum()
        total_debit = df[df["Type"]=="Debit"]["Amount"].sum()
        balance = total_credit - total_debit
    else:
        total_credit = total_debit = balance = 0

    st.sidebar.metric("Available Balance", f"₹{balance}")

    # ---------- ADD TRANSACTION ----------
    st.header("Add Transaction")

    col1, col2 = st.columns(2)

    with col1:
        t_type = st.selectbox("Transaction Type", ["Credit", "Debit"])
        category = st.text_input("Category (Food, Rent, Travel)")
        amount = st.number_input("Enter Amount", min_value=0.0)

        if st.button("Add Entry"):
            add_transaction(st.session_state["user"], t_type, category, amount)
            st.success("Transaction Added")
            st.rerun()

    # ---------- CALCULATOR ----------
    with col2:
        st.subheader("🧮 Quick Calculator")
        calc_input = st.text_input("Enter calculation (Example: 500+200-50)")
        if st.button("Calculate"):
            try:
                result = eval(calc_input)
                st.success(f"Result: ₹{result}")
            except:
                st.error("Invalid Calculation")

    # ---------- MONTH WISE REPORT ----------
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        st.header("📅 Month-wise Report")
        month_selected = st.selectbox("Select Month", df["Month"].unique())

        monthly_df = df[df["Month"] == month_selected]

        st.write("Total Credit:",
                 monthly_df[monthly_df["Type"]=="Credit"]["Amount"].sum())
        st.write("Total Debit:",
                 monthly_df[monthly_df["Type"]=="Debit"]["Amount"].sum())

        st.dataframe(monthly_df)

        # Pie Chart
        pie = px.pie(monthly_df[monthly_df["Type"]=="Debit"],
                     names="Category",
                     values="Amount",
                     title="Spending Distribution")
        st.plotly_chart(pie, use_container_width=True)
        
# -------- DOWNLOAD MONTH REPORT --------
import io

st.subheader("📥 Download Reports")

# Create Excel in memory
month_buffer = io.BytesIO()
monthly_df.to_excel(month_buffer, index=False, engine='openpyxl')

st.download_button(
    label="Download Selected Month Report",
    data=month_buffer,
    file_name=f"{month_selected}_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# -------- DOWNLOAD FULL REPORT --------
full_buffer = io.BytesIO()
df.to_excel(full_buffer, index=False, engine='openpyxl')

st.download_button(
    label="Download Full Family Report",
    data=full_buffer,
    file_name="full_family_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)