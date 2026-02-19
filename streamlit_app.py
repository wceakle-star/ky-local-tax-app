import streamlit as st
import pandas as pd

st.title("Kentucky Local Occupational Tax – OL-S Prototype")

st.header("Global Totals")

total_sales = st.number_input("Total Sales Everywhere", value=0.0)
total_payroll = st.number_input("Total Payroll Everywhere", value=0.0)
total_net_income = st.number_input("Total Net Income", value=0.0)

st.header("Select Tax District")

district_data = pd.DataFrame({
    "district":[
        "Lexington-Fayette",
        "Louisville Metro",
        "Boone County",
        "Frankfort"
    ],
    "net_rate":[0.0225, 0.022, 0.01, 0.02]
})

district = st.selectbox(
    "Choose District",
    district_data["district"]
)

st.header("Apportionment Inputs")

local_sales = st.number_input("Sales in Selected District", value=0.0)
local_payroll = st.number_input("Payroll in Selected District", value=0.0)

if st.button("Calculate OL-S Tax"):

    row = district_data[district_data["district"]==district].iloc[0]

    sales_factor = 0
    payroll_factor = 0

    if total_sales > 0:
        sales_factor = local_sales / total_sales

    if total_payroll > 0:
        payroll_factor = local_payroll / total_payroll

    apportionment = (sales_factor + payroll_factor) / 2

    taxable_income = total_net_income * apportionment

    tax = taxable_income * row["net_rate"]

    st.subheader("OL-S Calculation")

    st.write("Sales Factor:", sales_factor)
    st.write("Payroll Factor:", payroll_factor)
    st.write("Apportionment %:", apportionment)
    st.write("Taxable Net Income:", taxable_income)
    st.write("Tax Due:", tax)
