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
st.subheader("小組資料")

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
    group_input = st.text_input("請輸入组别号数:")

    submitted = st.form_submit_button("Submit")
    if submitted:

        groupsn = str(group_input)  # Convert to str
        group = "第 " + groupsn + " 組"

        # Filter the dataframe
        detailsdf = df[df['組別'] == group]

        if detailsdf.empty:
            st.warning("沒有此組別資料。請確認您的組別號數。")
        else:
            data_container = st.container(border=True)
            with data_container:
                st.markdown("**小組數據**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    dcdf = detailsdf["道場單位"].value_counts()
                    st.dataframe(dcdf, use_container_width=True)

                with col2:
                    genderdf = detailsdf["乾坤"].value_counts()
                    st.dataframe(genderdf, use_container_width=True)

                with col3:
                    daysdf = detailsdf["參與日期"].value_counts()
                    st.dataframe(daysdf, use_container_width=True)
            st.divider()
            st.markdown("**小組名單**")
            st.dataframe(detailsdf,hide_index=True, use_container_width=True)
