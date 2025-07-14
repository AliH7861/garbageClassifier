import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager
import threading
from main import app
import uvicorn

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run_fastapi, daemon=True).start()

# --- Setup cookies ---
cookies = EncryptedCookieManager(
    prefix="garbage_project_",
    password="your_secret_key_here"
)
if not cookies.ready():
    st.stop()

# --- Always sync session state to cookie at the top ---
if cookies.get("logged_in") == "true":
    st.session_state["logged_in"] = True
    st.session_state["username"] = cookies.get("username")
else:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# --- If already logged in ---
if st.session_state.get("logged_in"):
    st.title("Sign Out")
    st.success(f"You're already logged in as **{st.session_state.get('username', '')}**.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to App", use_container_width=True):
            st.switch_page("pages/webpage.py")
    with col2:
        if st.button("Go to Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
    with col3:
        if st.button("Log Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            cookies["logged_in"] = ""
            cookies["username"] = ""
            cookies.save()
            st.rerun()

# --- Login Form (if not logged in) ---
else:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.markdown(""" 
        

    """)

    if st.button("Login", use_container_width=True):
        if not username or not password:
            st.warning("Please fill in both fields.")
        else:
            try:
                response = requests.post(
                    "http://localhost:8000/login",
                    json={"username": username, "password": password}
                )
                if response.status_code == 200:
                    user_data = response.json()
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_data["id"]
                    st.session_state["username"] = user_data["user_id"]
                    cookies["logged_in"] = "true"
                    cookies["username"] = user_data["user_id"]
                    cookies.save()
                    st.success(f"Logged in as {user_data['user_id']}!")
                    st.switch_page("pages/webpage.py")
                else:
                    st.error("Incorrect username or password.")
            except Exception as e:
                st.error(f"Failed to connect to server: {e}")
    if st.button("Sign Up", use_container_width=True):
        st.switch_page("pages/signup.py")