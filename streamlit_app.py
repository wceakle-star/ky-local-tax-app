import streamlit as st
import pandas as pd

st.title("Kentucky Local Occupational Tax – Multi District OL-S Prototype")

# -----------------------------
# GLOBAL TOTALS
# -----------------------------
st.header("Step 1 – Global Totals")

total_sales = st.number_input("Total Sales Everywhere", value=0.0)
total_payroll = st.number_input("Total Payroll Everywhere", value=0.0)
total_net_income = st.number_input("Total Net Income", value=0.0)

# -----------------------------
# DISTRICT DATA (TEMP SAMPLE)
# -----------------------------
district_data = pd.DataFrame({
    "district":[
        "Lexington-Fayette",
        "Louisville Metro",
        "Boone County",
        "Frankfort",
        "Bowling Green",
        "Covington"
    ],
    "net_rate":[0.0225,0.022,0.01,0.02,0.02,0.0245]
})

district_list = district_data["district"].tolist()

# -----------------------------
# SESSION STATE FOR ROWS
# -----------------------------
if "rows" not in st.session_state:
    st.session_state.rows = 1

st.header("Step 2 – Allocate Sales and Payroll by Locality")

if st.button("Add Locality"):
    st.session_state.rows += 1

allocations = []

for i in range(st.session_state.rows):

    st.subheader(f"Locality #{i+1}")

    district = st.selectbox(
        f"District {i+1}",
        district_list,
        key=f"district_{i}"
    )

    sales = st.number_input(
        f"Sales for {district}",
        value=0.0,
        key=f"sales_{i}"
    )

    payroll = st.number_input(
        f"Payroll for {district}",
        value=0.0,
        key=f"payroll_{i}"
    )

    allocations.append({
        "district": district,
        "sales": sales,
        "payroll": payroll
    })

alloc_df = pd.DataFrame(allocations)

total_alloc_sales = alloc_df["sales"].sum()
total_alloc_payroll = alloc_df["payroll"].sum()

st.divider()
st.subheader("Allocation Totals")

st.write("Allocated Sales:", total_alloc_sales)
st.write("Allocated Payroll:", total_alloc_payroll)

sales_match = abs(total_alloc_sales - total_sales) < 1
payroll_match = abs(total_alloc_payroll - total_payroll) < 1

if not sales_match:
    st.warning("Sales are not fully allocated")

if not payroll_match:
    st.warning("Payroll is not fully allocated")

# -----------------------------
# CALCULATE TAX
# -----------------------------
if st.button("Calculate OL-S Taxes"):

    if not sales_match or not payroll_match:
        st.error("Sales and payroll must be fully allocated before calculation.")
        st.stop()

    st.header("OL-S District Calculations")

    results = []

    for row in allocations:

        district_row = district_data[
            district_data["district"] == row["district"]
        ].iloc[0]

        sales_factor = 0
        payroll_factor = 0

        if total_sales > 0:
            sales_factor = row["sales"] / total_sales

        if total_payroll > 0:
            payroll_factor = row["payroll"] / total_payroll

        apportionment = (sales_factor + payroll_factor) / 2

        taxable_income = total_net_income * apportionment

        tax = taxable_income * district_row["net_rate"]

        results.append({
            "District": row["district"],
            "Apportionment": apportionment,
            "Taxable Income": taxable_income,
            "Tax": tax
        })

    result_df = pd.DataFrame(results)

    st.dataframe(result_df)
