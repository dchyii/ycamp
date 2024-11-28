import streamlit as st  
from helper_functions.utility import check_password  
from dotenv import load_dotenv
import os
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="研習營", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        div[data-testid="stSidebarCollapsedControl"] {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("全球青少年研習營")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# Link to GSheets
load_dotenv('.env')
url = os.getenv("LINK")
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet=url, ttl=60, usecols=[0,1,2,3,5,6,7,8,9])

# st.dataframe(df)

# Form for serial number input
with st.form("display_details"):
    name_input = st.text_input("請輸入您的姓名 Please enter your name in Chinese:")

    submitted = st.form_submit_button("Submit")
    if submitted:
        # Convert serial number input to match dataframe column type
        # try:
        name = str(name_input)  # Convert to int if `编号` column is numeric
        # except ValueError:
        #     sn = serial_number  # Keep as string if the column is string type

        # Filter the dataframe
        detailsdf = df[df['姓名'] == name]

        if detailsdf.empty:
            st.warning("沒有此學員資料。請確認您的名字。")
        else:
            st.dataframe(detailsdf)


# st.write("hello")