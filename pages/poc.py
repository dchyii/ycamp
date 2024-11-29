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
st.subheader("道場資料")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# Link to GSheets
load_dotenv('.env')
url = os.getenv("LINK")
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet=url, ttl=60, usecols=[0,1,2,3,5,6,7,8,9,10])

# st.dataframe(df)

# Form 
with st.form("display_details"):
    dc_input = st.selectbox('請選擇您所屬的道場', [' ','天和道場','天祥道場','天臺道場','天遵道場','聖林道場','天一道場','天合道場','天律道場','天本道場','天寬道場','天倫道場','苗新道場','新加坡道場','馬來西亞道場','澳洲道場'])

    submitted = st.form_submit_button("Submit")
    if submitted:
        # Filter the dataframe
        detailsdf = df[df['道場單位'].str.contains(dc_input, na=False)]

        if detailsdf.empty:
            st.warning("沒有此組別資料。請確認您所屬的道場。")
        else:
            st.dataframe(detailsdf,hide_index=True, use_container_width=True)
