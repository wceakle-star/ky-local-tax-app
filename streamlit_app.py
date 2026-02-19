import streamlit as st

st.title("Kentucky Local Tax Test App")

income = st.number_input("Enter income", value=0.0)

if st.button("Calculate"):
    st.write("Tax (2%) =", income * 0.02)
