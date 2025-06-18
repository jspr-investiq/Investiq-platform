import streamlit as st

st.title("Test App")

name = st.text_input("Enter name")

if st.button("Submit"):
    if name:
        st.success(f"Hello {name}")
    else:
        st.error("Please enter a name")
