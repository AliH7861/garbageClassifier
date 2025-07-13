import streamlit as st
import os
import base64
from image_utils import DEFAULT_IMAGES, BIN_FILENAMES, get_all_bin_images, fixed_size_image

from streamlit_cookies_manager import EncryptedCookieManager

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
            st.switch_page("login.py")
    st.stop()

# --- Fonts and style ---
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

def render_image_with_hover(img_str, container, caption=None):
    container.markdown(f"""
        <style>
            .parent {{
                position: relative;
                display: inline-block; 
                width: 100%;
                margin-bottom: 32px;   /* Adds space below each image/card */
            }}
            .hover-img {{
                display: block;
                border-radius: 10px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.13);
                width: 100%;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .hover-img:hover {{
                transform: scale(1.05);
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
            }}
            .caption {{
                text-align: center;
                margin-top: 8px;
                color: #444;
                font-size: 1rem;
                font-family: 'Poppins', sans-serif;
            }}
        </style>
        <div class='parent'>  
            <img class='hover-img' src="data:image/png;base64,{img_str}" width='100%'>
            <div class='caption'>{caption if caption else ""}</div>
        </div>
        """, unsafe_allow_html=True)

bin_types = list(DEFAULT_IMAGES.keys())
user_id = st.session_state.get("username", "guest")
user_folder = os.path.join("user_images", user_id)
os.makedirs(user_folder, exist_ok=True)

# --- UI Title ---
st.markdown("""
    <h1 style=' text-align: center; font-size: 2.8rem; font-weight: 800; letter-spacing: 1px; color: #22223b;
        font-family: Poppins, Roboto, sans-serif; margin-bottom: 18px; margin-top: 10px;'> Updating Bins Page </h1>
        <p style='margin-top: 20px;'></p> """, unsafe_allow_html=True
)

# --- Bin update selection ---
selected_bins = []
uploaded_files = []

cols = st.columns([2, 5], border=True)
cols[0].markdown('<h4 style="text-align:center;">Name</h4>', unsafe_allow_html=True)
cols[1].markdown('<h4 style="text-align:center;">Upload File</h4>', unsafe_allow_html=True)

for i in range(4):
    row = st.columns([2, 5], border=True)
    with row[0]:
        bin_choice = st.selectbox(
            f"Select Bin Type for Slot {i+1}",
            bin_types,
            key=f"name_{i+1}"
        )
        selected_bins.append(bin_choice)
    with row[1]:
        upload = st.file_uploader(
            f"Upload Image for Slot {i+1}",
            key=f"file_{i+1}"
        )
        uploaded_files.append(upload)

cols2 = st.columns([4, 5], border=False)

with cols2[0]:
    if st.button("Return Original", key="originalPicture_button", use_container_width=True):
        # Delete all custom user images for this user
        for fname in os.listdir(user_folder):
            file_path = os.path.join(user_folder, fname)
            if os.path.isfile(file_path):
                os.remove(file_path)
        st.success("All bin images returned to original defaults.")

with cols2[1]:
    if st.button("Submit", key="submit_button", use_container_width=True):
        updated = False
        # Only save uploaded images for the selected bin type
        for bin_type, uploaded_file in zip(selected_bins, uploaded_files):
            if uploaded_file is not None:
                file_path = os.path.join(user_folder, BIN_FILENAMES[bin_type])
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"{bin_type} image updated!")
                updated = True
        if not updated:
            st.info("No new images uploaded.")
        else:
            st.success("Picture(s) Updated!")

# --- Display Current Bin Images ---
bin_images_base64 = get_all_bin_images(user_id)


# Lets create a 2 v 2 grid, and have the first two on the first row and the last two on the second row hence it would look cleaner

st.markdown("<hr><h2 style='text-align:center'>Current Bin Images</h2><br>", unsafe_allow_html=True)
cols = st.columns(2)
for idx, bin_type in enumerate(bin_types):
    col = cols[idx % 2]
    custom_path = os.path.join(user_folder, BIN_FILENAMES[bin_type])
    is_custom = os.path.exists(custom_path)
    caption = f"{bin_type} (your custom image)" if is_custom else f"{bin_type} (default)"
    img_bytes = fixed_size_image(bin_images_base64[bin_type])
    import base64
    img_b64_str = base64.b64encode(img_bytes).decode("utf-8")
    with col:
        render_image_with_hover(img_b64_str, col, caption=caption)
    # Add vertical space after every row except the last
    if idx % 2 == 1 and idx < len(bin_types) - 1:
        st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)
        cols = st.columns(2)

st.markdown(""" """)
st.info("Note: These images are stored locally and will be lost if the server restarts.")





# First Step
# 1) Figure Out How Each User can Have a unique USER iD
# 2) Setup how, each deployment would be unique
# 3) Accept Session Inputs
# 4) Send User Id, and Uploaded Image, and Upload Images Group to Backend
# 5) App loads user specific image, if it exists, otherwise its default
# 6) Setup the button to revert to Original Images (Make Sure Oriignal Images are not deleted)
# 7) Practice Error Handling Throughout the Program
#8 ) Setup CI/CD placement
# 9) Setup a deployment on ralway.app
# 10) Upload on Github and Make a Readme

# 2) How to store the uploaded pictures
# 3)