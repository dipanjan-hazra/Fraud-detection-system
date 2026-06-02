import streamlit as st

from pages.login import login_page
from pages.register import register_page
from pages.dashboard import dashboard_page
from pages.upload_page import uploader
from pages.history import history_page

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="wide"
)

st.header("💳Transation  Fraud  detection")
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.page == "login":
    login_page()
   

elif st.session_state.page == "register":
    register_page()
   

elif st.session_state.page == "dashboard":
    dashboard_page()
   

elif st.session_state.page == "upload":
    uploader()

elif st.session_state.page == "history":

    history_page()