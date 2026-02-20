import streamlit as st
import pandas as pd

st.title("KY Local Occupational Tax Engine")

# -----------------------------
# LOAD DATA
# -----------------------------
district_data = pd.read_csv("ky_districts.csv")
district_list = district_data["district"].tolist()

# -----------------------------
# GLOBAL TOTALS
# -----------------------------
st.header("Global Totals")

c1, c2, c3 = st.columns(3)

with c1:
    total_sales = st.number_input("Total Sales", value=0.0)

with c2:
    total_payroll = st.number_input("Total Payroll", value=0.0)

with c3:
    total_income = st.number_input("Total Net Income", value=0.0)

# -----------------------------
# LOCALITY COLUMN COUNT
# -----------------------------
if "cols" not in st.session_state:
    st.session_state.cols = 2

if st.button("Add Locality Column"):
    st.session_state.cols += 1

st.header("Locality Allocation")

cols = st.columns(st.session_state.cols)

allocations = []

for i in range(st.session_state.cols):

    with cols[i]:

        st.subheader(f"Locality {i+1}")

        district = st.selectbox(
            "District",
            district_list,
            key=f"d{i}"
        )

        sales = st.number_input(
            "Sales",
            value=0.0,
            key=f"s{i}"
        )

        payroll = st.number_input(
            "Payroll",
            value=0.0,
            key=f"p{i}"
        )

        allocations.append({
            "district": district,
            "sales": sales,
            "payroll": payroll
        })

alloc_df = pd.DataFrame(allocations)

allocated_sales = alloc_df["sales"].sum()
allocated_payroll = alloc_df["payroll"].sum()

remaining_sales = total_sales - allocated_sales
remaining_payroll = total_payroll - allocated_payroll

# -----------------------------
# TOTALS PANEL
# -----------------------------
st.divider()
st.subheader("Allocation Status")

t1, t2 = st.columns(2)

with t1:
    st.write("Sales Allocated:", allocated_sales)
    st.write("Sales Remaining:", remaining_sales)

with t2:
    st.write("Payroll Allocated:", allocated_payroll)
    st.write("Payroll Remaining:", remaining_payroll)

sales_ok = abs(remaining_sales) < 1
payroll_ok = abs(remaining_payroll) < 1

if not sales_ok:
    st.warning("Sales not fully allocated")

if not payroll_ok:
    st.warning("Payroll not fully allocated")

# -----------------------------
# CALCULATION ENGINE
# -----------------------------
if st.button("Calculate Tax"):

    if not sales_ok or not payroll_ok:
        st.error("Allocations must equal totals")
        st.stop()

    results = []

    for row in allocations:

        d = district_data[
            district_data["district"] == row["district"]
        ].iloc[0]

        sales_factor = row["sales"] / total_sales if total_sales else 0
        payroll_factor = row["payroll"] / total_payroll if total_payroll else 0

        apportionment = (sales_factor + payroll_factor) / 2

        taxable_income = total_income * apportionment
        tax = taxable_income * d["net_profit_rate"]

        results.append({
            "District": row["district"],
            "Apportionment": apportionment,
            "Taxable Income": taxable_income,
            "Tax": tax
        })

    result_df = pd.DataFrame(results)
    st.dataframe(result_df)
