import streamlit as st
import pandas as pd
from database import *
from datetime import datetime
import plotly.express as px
import io

create_tables()

st.set_page_config(page_title="Family Finance Tracker", layout="wide")

st.title("🏦 Family Finance Tracker")

# ---------- FAMILY MEMBERS ----------
family_members = [
"Sunil Patil",
"Anil Patil",
]
family_members_2 = [
"Sunil",
"Anil",
"Sarthak",
"Archana",
"Sunita",
]
# ---------- LOGIN ----------
users = {
"Sarthak":"1234",
"Archana":"1234",
"Sunil":"1234",
"Sunita":"1234",
"Anil":"1234"
}

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

    data = get_transactions()

    df = pd.DataFrame(
        data,
        columns=["ID","Date","User","Person","Type","Category","Amount"]
    )

    # ---------- BALANCE ----------
    if not df.empty:
        credit = df[df["Type"]=="Credit"]["Amount"].sum()
        debit = df[df["Type"]=="Debit"]["Amount"].sum()
        balance = credit - debit
    else:
        credit = debit = balance = 0

    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Family Balance")
    st.sidebar.metric("Available Balance", f"₹{balance}")

    col1,col2 = st.columns(2)

    # ---------- ADD MONEY ----------
    with col1:

        st.header("💰 Add Money")

        add_person = st.selectbox("Who Added Money", family_members)

        add_amount = st.number_input("Enter Amount", min_value=0.0)

        if st.button("Add to Balance"):

            add_transaction(
                st.session_state["user"],
                add_person,
                "Credit",
                "Deposit",
                add_amount
            )

            st.success("Money Added")
            st.rerun()

    # ---------- SPEND MONEY ----------
    with col2:

        st.header("💸 Spend Money")

        spend_person = st.selectbox("Who Spent", family_members_2)

        category = st.text_input("Category (Food, Rent, Travel)")

        spend_amount = st.number_input("Spend Amount", min_value=0.0)

        if st.button("Debit from Balance"):

            add_transaction(
                st.session_state["user"],
                spend_person,
                "Debit",
                category,
                spend_amount
            )

            st.success("Amount Debited")
            st.rerun()

    # ---------- REPORT ----------
    if not df.empty:

        df["Date"] = pd.to_datetime(df["Date"])

        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        st.header("📅 Monthly Report")

        month = st.selectbox("Select Month", df["Month"].unique())

        monthly_df = df[df["Month"]==month]

        st.dataframe(monthly_df)

        # ---------- CHART ----------
        pie = px.pie(
            monthly_df[monthly_df["Type"]=="Debit"],
            names="Category",
            values="Amount",
            title="Spending Distribution"
        )

        st.plotly_chart(pie,use_container_width=True)

        # ---------- DELETE ----------
        st.subheader("🗑 Delete Transaction")

        delete_id = st.selectbox("Select ID", df["ID"])

        if st.button("Delete Entry"):
            delete_transaction(delete_id)
            st.success("Deleted")
            st.rerun()

        # ---------- DOWNLOAD ----------
        st.subheader("📥 Download Report")
        
        export_full = df.drop(columns=["User","ID"], errors="ignore")

        buffer_full = io.BytesIO()
        export_full.to_excel(buffer_full, index=False)

        st.download_button(
            "Download Full Report",
            data=buffer_full,
            file_name="full_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )