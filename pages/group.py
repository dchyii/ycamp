import streamlit as st  
from helper_functions.utility import check_password  
from dotenv import load_dotenv
import os
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="研習營", layout="wide", initial_sidebar_state="collapsed")


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
    group_input = st.text_input("請輸入组别号数:")

    submitted = st.form_submit_button("Submit")
    if submitted:
        # Convert serial number input to match dataframe column type
        # try:
        groupsn = str(group_input)  # Convert to int if `编号` column is numeric
        group = "第 " + groupsn + " 組"
        # except ValueError:
        #     sn = serial_number  # Keep as string if the column is string type

        # Filter the dataframe
        detailsdf = df[df['組別'] == group]

        if detailsdf.empty:
            st.warning("沒有此組別資料。請確認您的組別號數。")
        else:
            st.dataframe(detailsdf)