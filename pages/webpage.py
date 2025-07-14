import streamlit as st
from PIL import Image
import base64
import io
import os
# Rewquests is what allows python code to communicate with the backend server
import requests
from streamlit_cookies_manager import EncryptedCookieManager
from image_utils import load_image_as_base64, get_all_bin_images, BIN_FILENAMES

filename_to_bin_type = {v: k for k, v in BIN_FILENAMES.items()}

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

# --- Require login ---
if not st.session_state.get("logged_in", False):
    with st.container():
        st.markdown("""
            <div style='border:2px solid #ff4b4b; border-radius:10px; padding:16px; margin-bottom:16px; text-align:center;'>
                <span style='color:#ff4b4b; font-weight:bold;'>Please log in first!</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Login Page"):
            st.switch_page("login.py")  # Use just "login" if your login.py is in /pages/
    st.stop()

    
img = Image.open('placeholder.jpg')
dashboard_url = "http://localhost:8080/dashboard"
updatepicture_url = "http://localhost:8080/pictures"
signOut_url = "http://localhost:8080"


# Convert to base64
buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

user_id = st.session_state.get("username", "guest")
bin_images_base64 = get_all_bin_images(user_id)

# If you still want individual variables, you can do:
black_garbage_b64 = bin_images_base64["Black garbage"]
green_bin_b64 = bin_images_base64["Green bin"]
lightblue_b64   = bin_images_base64["Light blue box"]
darkblue_b64    = bin_images_base64["Dark blue box"]


# render placeholder with this string
def render_image_with_button(img_str, container):
        container.markdown(f"""
    <style>
        .parent {{
            position: relative;
            display: inline-block; 
            width: 100%;
        }}
        .hover-img {{
            display: block;
            border-radius: 10px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.13);
            width: 100%;
        }}
        .hover-img:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
        }}
        
        .parent:hover  {{
            display: block;
        }}
    </style>
    <div class='parent'>  
        <img class='hover-img' src="data:image/png;base64,{img_str}" width='100%'>
    </div>
    """, unsafe_allow_html=True)
  

# Styled box start
st.markdown("""
<div style='border: 1px solid #ccc; padding: 25px; border-radius: 10px; background-color: #f9f9f9; margin-bottom: 20px;'>
<h2 style='text-align:center;'>EcoBin AI</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(""" <h4 style='text-align:center; margin-bottom: 0px;'>Upload Original Image</h4> """, unsafe_allow_html=True)
    original_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="original")
    if original_file is not None:
        original_image = Image.open(original_file)
        st.image(original_image, caption="Original Image", use_container_width=True)

with col2:
    st.markdown(""" <h4 style='text-align:center; margin-bottom: 10px;'>Outputed Bin</h4> """, unsafe_allow_html=True)
    
    my_placeholder = st.empty()


# --- Button actions ---
with col2:
    st.markdown("""  """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    

    with col1:
        if st.button("Submit", key="submit_button", use_container_width=True):
            if original_file is not None:
                files = {'file': (original_file.name, original_file.getvalue(), original_file.type)}
                response = requests.post("http://localhost:8000/submit", files=files)
                result = response.json()
                if response.status_code == 200:
                    st.success("Image processed successfully!")
                    # Save result in session_state before rerun
                    st.session_state['last_result'] = result
                    st.session_state['last_file_name'] = original_file.name
                    st.cache_data.clear()  # optional, only if you really want to clear cache
                    st.rerun()
                else:
                    st.error("Failed to process the image. Please try again.")
            else:
                st.warning("Please upload an image before submitting.")

    if 'last_result' in st.session_state:
        result = st.session_state['last_result']
        bin_image_filename = result["bin_image"]
        bin_filename = os.path.basename(bin_image_filename)
        bin_type = filename_to_bin_type.get(bin_filename)
        if bin_type and bin_type in bin_images_base64:
            render_image_with_button(bin_images_base64[bin_type], my_placeholder)
        else:
            st.error(f"Could not match bin type for image: {bin_filename}")
        
    with col2:
        if st.button("Dashboard", key="dashboard_button", use_container_width=True):
            try:
                st.success("Dashboard clicked!")
                st.switch_page("pages/dashboard.py")
                
            except Exception as e:
                st.error(f"Dashboard Failed To Load: {e}")
    
    
    wide_col = st.columns([1])[0]
    with wide_col:
        if st.button("Edit Bin Pictures", key="edit_bin_button", use_container_width=True):
            try:
                st.success("Edit Bin Pictures clicked!")
                st.switch_page("pages/pictures.py")
            except Exception as e:
                st.error("Pictures Session Failed To Load")


    wide_col2 = st.columns([1])[0]
    with wide_col2:
        if st.button("Sign Out", key="SignOut_bin_button", use_container_width=True):
            try:
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={signOut_url}">', unsafe_allow_html=True)
                st.success("Sign Out Page clicked!")
            except Exception as e:
                st.error("Sign Out Page Failed To Load")
 
st.markdown("</div>", unsafe_allow_html=True)