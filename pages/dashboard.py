import streamlit as st
from PIL import Image
import base64
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objs as go
import requests
from streamlit_autorefresh import st_autorefresh
import concurrent.futures
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
            st.switch_page("login.py")  # Use just "login" if your login.py is in /pages/
    st.stop()



# This will refresh the dashboard every 10 seconds
st_autorefresh(interval=10 * 1000, key="refresh")

# Set Opens Sans Font Style
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">                
    <style>
    body, .stDataFrame, .stTable {
        font-family: 'Poppins', sans-serif !important;

    }
    th {
        background-color: red;
    }
    td {
        text-align: center !important;
        vertical-align: middle !important;
    }
    tr {
       padding: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)


# Import data from the api

@st.cache_data(ttl=2000)
def get_alltimestats():
    return requests.get("http://localhost:8000/stats/alltimescans").json()

@st.cache_data(ttl=2000)
def get_todaystats():
    return requests.get("http://localhost:8000/stats/todayscans").json()

@st.cache_data(ttl=2000)
def get_barstats():
    return requests.get("http://localhost:8000/stats/bargraphdata").json()

@st.cache_data(ttl=2000)
def get_classstats():
    return requests.get("http://localhost:8000/stats/classCircleGraphData").json()

@st.cache_data(ttl=2000)
def get_dailyStats():
    return requests.get("http://localhost:8000/stats/dailyScanStats").json()

@st.cache_data(ttl=2000)
def get_scansuptotodaystats():
    return requests.get("http://localhost:8000/stats/changeinAllScanItems").json()

@st.cache_data(ttl=2000)
def get_scansdifferenceStats():
    return requests.get("http://localhost:8000/stats/changeinAllScanItemsDaily").json()

@st.cache_data(ttl=2000)
def get_tableStats():
    return requests.get("http://localhost:8000/stats/tableStats").json()

@st.cache_data(ttl=2000)
def get_most_common_bin_today():
    return requests.get("http://localhost:8000/stats/mostCommonBinToday").json()

@st.cache_data(ttl=2000)
def get_most_common_bin_changetoday():
    return requests.get("http://localhost:8000/stats/mostCommonBinChangeToday").json()

@st.cache_data(ttl=2000)
def get_most_common_bin_changeAll():
    return requests.get("http://localhost:8000/stats/mostCommonBinChangeAll").json()



funcs = [
    get_alltimestats, get_todaystats, get_barstats, get_classstats, get_dailyStats,
    get_scansuptotodaystats, get_scansdifferenceStats, get_tableStats, get_most_common_bin_today,
    get_most_common_bin_changetoday, get_most_common_bin_changeAll 
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(lambda f: f(), funcs))

(
    alltimestats, todaystats, barstats, classstats, dailyStats,
    scansUpToday, scansdifference, tableStats, mostCommonBinToday,
    mostCommonBinChangeToday, mostCommonBinChangeAll
) = results

# Set up the colors
bin_pie_color_dic = {"Paper Box":"#0865AC" , "Garbage":"#090101", "Organics Bin":"#1F3E06", "Containers Box": "#0C304B"}
class_pie_color_dic = { 'Biological': '#1F3E06','Brown-glass': '#0C304B','Green-glass': '#0C304B', 'White-glass': '#0C304B',
'Metal': '#0C304B', 'Plastic': '#0C304B', 'Cardboard': '#0865AC','Paper': '#0865AC', 'Clothes': '#090101','Shoes': '#090101',
'Trash': '#090101'}

# renders with a wide-screen layout
st.set_page_config(layout="wide")

# Dumpy Setup to be removed
bar_data = pd.DataFrame({
    "Garbage Type": list(barstats.keys()),
    "Count": list(barstats.values())
})

pie_class = pd.DataFrame({
    "Category": list(classstats.keys()),
    "Count": list(classstats.values())
})

pie_bin = pd.DataFrame({
    "Category": list(barstats.keys()),
    "Count": list(barstats.values())
})





# Line Graph Data Input
line_df = pd.DataFrame({
    "Date": [d["date"] for d in dailyStats],
    "Checks": [d["scan_count"] for d in dailyStats]
})
line_df = line_df.set_index("Date")


# Setting up Table
data = tableStats["recent_table_data"]
table_df = pd.DataFrame(data)
table_df = table_df.rename(columns={
    "date_time": "Time",
    "predicted_class": "Class",
    "predicted_bin": "Bin"
})
table_df["Time"] = pd.to_datetime(table_df["Time"])            # Step 1: convert to datetime
table_df["Time"] = table_df["Time"].dt.tz_localize("UTC")      # Step 2: add UTC tz info if missing
table_df["Time"] = table_df["Time"].dt.tz_convert("America/Toronto")   # Step 3: convert to Toronto time


table_df.index = range(1, len(table_df) + 1)


st.markdown("""
    <h1 style=' text-align: center; font-size: 2.8rem; font-weight: 800; letter-spacing: 1px; color: #22223b;
        font-family: Poppins, Roboto, sans-serif; margin-bottom: 18px; margin-top: 10px;'> Dashboard Page </h1>
        <p style='margin-top: 20px;'></p> """, unsafe_allow_html=True
)


# --- Fake Metrics Row ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    col1.metric("Items Scanned All-Time", f"{alltimestats['total_scans_count']}", delta=f"{scansUpToday['scanChange']:.2f}%", border=True)

with col2:
   col2.metric("Items Scanned Today", f"{todaystats['total_today_scans']}", delta=f"{scansdifference['scanDailyChange']:.2f}%", border=True)
   
with col3:
    col3.metric("Most Scanned Bin Today", mostCommonBinToday.get("mostCommonBin", "None"), delta=mostCommonBinChangeToday.get("bin_changed_to", "No Change"), border=True)

with col4:
    col4.metric("Most Scanned Bin All-Time", alltimestats.get("mostCommonBin", "None"), delta=mostCommonBinChangeAll.get("bin_changed_to", "No Change"), border=True)

# --- Fake Bar and Pie Chart Row
col5, col6, col7 = st.columns(3 , border=True)

with col5:
    st.markdown(
    "<h3 style='font-size:2rem; font-weight:700; letter-spacing:0.5px; color:#3949AB; font-family:Poppins,Roboto,sans-serif; margin-bottom:12px;'> Total Scans Today </h3>",
    unsafe_allow_html=True
    )
    bar_fig = px.bar(
    bar_data,
    x="Garbage Type",
    y="Count",
    
    text="Count",
    color="Garbage Type",
    color_discrete_map= bin_pie_color_dic,
    
)
    
    bar_fig.update_layout(
    font=dict(family="Poppins, Inter, Roboto, Open Sans, sans-serif", size=18),
    plot_bgcolor="#fff",
    paper_bgcolor="#fff",
    showlegend = False
)
    st.plotly_chart(bar_fig, use_container_width=True)


with col6:
    st.markdown(
    "<h3 style='font-size:2rem; font-weight:700; letter-spacing:0.5px; color:#3949AB; font-family:Poppins,Roboto,sans-serif; margin-bottom:12px;'>Output by Class</h3>",
    unsafe_allow_html=True
    )
    pie_class_nonzero = pie_class[pie_class["Count"] > 0]
    pull_class = [0.08 if i == np.argmax(pie_class_nonzero["Count"]) else 0 for i in range(len(pie_class_nonzero))]
    pie1_fig = px.pie(pie_class_nonzero, names="Category", values="Count", color="Category",color_discrete_map=class_pie_color_dic, hole = 0.45)
    pie1_fig.update_traces(textinfo="label+value", pull=pull_class, insidetextorientation='auto')
    
    pie1_fig.update_layout(
    font=dict(family="Poppins, Inter, Roboto, Open Sans", size=12),
    showlegend = False
    )
    pie1_fig.update_traces(textinfo="label+value", insidetextorientation='auto', pull=pull_class)
    st.plotly_chart(pie1_fig, use_container_width=True)

with col7:
    st.markdown(
    "<h3 style='font-size:2rem; font-weight:700; letter-spacing:0.5px; color:#3949AB; font-family:Poppins,Roboto,sans-serif; margin-bottom:12px;'>Output By Bin </h3>",
    unsafe_allow_html=True
)
    pie_bin_nonzero = pie_bin[pie_bin["Count"] > 0]
    pull_bin = [0.08 if i == np.argmax(pie_bin_nonzero["Count"]) else 0 for i in range(len(pie_bin_nonzero))]
    pie2_fig = px.pie(pie_bin_nonzero, names="Category", values="Count", color="Category", color_discrete_map=bin_pie_color_dic, hole=0.45)
    pie2_fig.update_layout(
    font=dict(family="Poppins, Open Sans", size=13),
    showlegend = False
    )
    pie2_fig.update_traces(textinfo="label+value", insidetextorientation='auto', pull=pull_bin)


    st.plotly_chart(pie2_fig, use_container_width=True)


# --- Fake Line Chart, and Tablw)
col8, col9 = st.columns(2 , border=True)

with col8:
    st.markdown(
        "<h3 style='font-size:2.3rem; font-weight:700; letter-spacing:0.5px; color:#3949AB; font-family:Poppins,Roboto,sans-serif; margin-bottom:12px;'> Daily Scans </h3>",
        unsafe_allow_html=True
    )
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=line_df.index,
        y=line_df['Checks'],
        mode='lines',
        line=dict(color="#0865AC", width=4, shape='spline'), # Solid curved line
        fill='tozeroy',
        fillcolor='rgba(8,101,172,0.15)', # Soft shaded area below
        hoverinfo='x+y',
        name='Open deals'
    ))

    fig.update_layout(
        margin=dict(l=15, r=15, t=30, b=20),
        plot_bgcolor='#F8FAFD',
        paper_bgcolor='#F8FAFD',
        font=dict(family='Poppins, sans-serif', size=16),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#D8E4F7", zeroline=False),
    )

    st.plotly_chart(fig, use_container_width=True)

with col9:
        st.markdown(
            "<h3 style='font-size:2.3rem; font-weight:700; letter-spacing:0.5px; color:#3949AB; font-family:Poppins,Roboto,sans-serif; margin-bottom:12px;'> Recent Submissions </h3>",
            unsafe_allow_html=True
        )
        styled_df = table_df.style.set_table_styles([
        {
            'selector': 'table',
            'props': [
                ('border', "2px solid grey"),
                ('border-radius', "20px"),
                ('color', "#FFFFFFAC"),
                ('font-size', '40px'),
                ('font-family', 'Poppins, sans-serif'),
                
            ]
        },
        {
            'selector': 'th',
            'props': [
                ('background-color', "#1F3E06"),
                ('border-radius', "3px"),
                ('color', "#FFFFFF"),
                ('padding', '15px'),
                ('font-size', '20px'),
                ('font-family', 'Poppins, sans-serif'),
                ('font-weight', '600'),
                ('text-align', 'center'),
            ]
        },
        {
            'selector': 'td',
            'props': [
                ('background-color', "#FFFFFF"),
                ('color', '#103755'),
                ('font-size', '50px'),
                ('font-family', 'Poppins, sans-serif'),
                ('text-align', 'center'),
            ]
        }
        
    ]).set_properties(**{
        'text-align': 'center'
    })
    
        
        st.table(styled_df) 
        


