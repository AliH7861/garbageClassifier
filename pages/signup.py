import streamlit as st
import requests


if st.session_state.get("logged_in", False):
    st.switch_page("login.py")
    st.stop()


# Import Basically the Fonts
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">                
    <style>
    body, .stDataFrame, .stTable, h4, p {
        font-family: 'Poppins', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)



st.title("Sign Up")

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")

if st.button("Sign Up"):
    if not username or not password:
        st.warning("Please fill in both fields.")
    else:
        response = requests.post(
            "http://localhost:8000/createUser",  # Change if deployed
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            st.success("Account created! You can log in now.")
            st.switch_page("login.py")
        elif response.status_code == 400 and "exists" in response.text:
            st.error("Username already exists.")
        else:
            st.error("Something went wrong. Please try again.")
