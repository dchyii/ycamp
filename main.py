import streamlit as st  
from helper_functions.utility import check_password  
from dotenv import load_dotenv
import os
from streamlit_gsheets import GSheetsConnection


st.title("全球青少年研習營")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# Link to GSheets
load_dotenv('.env')
url = os.getenv("LINK")
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(data)



# st.write("hello")