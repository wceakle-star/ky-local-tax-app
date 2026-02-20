import streamlit as st
import pandas as pd

st.title("Kentucky Local Occupational Tax – OL-S Engine")

# ----------------------------
# LOAD DISTRICT DATA
# ----------------------------
district_data = pd.read_csv("ky_districts.csv")
district_list = district_data["district"].tolist()

# ----------------------------
# GLOBAL TOTALS
# ----------------------------
st.header("Step 1 – Global Totals")

col1, col2, col3 = st.columns(3)

with col1:
    total_sales = st.number_input("Total Sales Everywhere", value=0.0)

with col2:
    total_payroll = st.number_input("Total Payroll Everywhere", value=0.0)

with col3:
    total_net_income = st.number_input("Total Net Income", value=0.0)

# ----------------------------
# SESSION ROW COUNT
# ----------------------------
if "rows" not in st.session_state:
    st.session_state.rows = 1

st.header("Step 2 – Locality Allocation")

if st.button("Add Locality"):
    st.session_state.rows += 1

allocations = []

for i in range(st.session_state.rows):

    st.subheader(f"Locality #{i+1}")

    colA, colB, colC = st.columns(3)

    with colA:
        district = st.selectbox(
            "District",
            district_list,
            key=f"district_{i}"
        )

    with colB:
        sales = st.number_input(
            "Sales",
            value=0.0,
            key=f"sales_{i}"
        )

    with colC:
        payroll = st.number_input(
            "Payroll",
            value=0.0,
            key=f"payroll_{i}"
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

# ----------------------------
# TOTALS DISPLAY
# ----------------------------
st.divider()
st.subheader("Allocation Summary")

sum1, sum2 = st.columns(2)

with sum1:
    st.write("### Sales")
    st.write("Allocated:", allocated_sales)
    st.write("Remaining:", remaining_sales)

with sum2:
    st.write("### Payroll")
    st.write("Allocated:", allocated_payroll)
    st.write("Remaining:", remaining_payroll)

sales_match = abs(remaining_sales) < 1
payroll_match = abs(remaining_payroll) < 1

if not sales_match:
    st.warning("Sales not fully allocated")

if not payroll_match:
    st.warning("Payroll not fully allocated")

# ----------------------------
# OL-S CALCULATION
# ----------------------------
if st.button("Calculate OL-S"):

    if not sales_match or not payroll_match:
        st.error("Allocations must equal totals before calculation.")
        st.stop()

    st.header("OL-S District Results")

    results = []

    for row in allocations:

        d = district_data[
            district_data["district"] == row["district"]
        ].iloc[0]

        sales_factor = row["sales"] / total_sales if total_sales else 0
        payroll_factor = row["payroll"] / total_payroll if total_payroll else 0

        if total_sales > 0 and total_payroll > 0:
            apportionment = (sales_factor + payroll_factor) / 2
        else:
            apportionment = sales_factor + payroll_factor

        taxable_income = total_net_income * apportionment
        tax = taxable_income * d["net_rate"]

        results.append({
            "District": row["district"],
            "Apportionment": apportionment,
            "Taxable Income": taxable_income,
            "Tax": tax
        })

    result_df = pd.DataFrame(results)
    st.dataframe(result_df)
