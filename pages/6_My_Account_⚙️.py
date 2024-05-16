import streamlit as st
from config import pagesetup as ps, sessionstates as ss
import json
from classes import chathistory_class as chathistory


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 5
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)
a = "a"


# 1. Set My Tabs
account_tabs = st.tabs(tabs=st.secrets.tabconfig.account_sections)
with account_tabs[0]:
    st.markdown("profile")
    
with account_tabs[1]:
    chat_history = chathistory.ChatHistory()
    
with account_tabs[2]:
    st.markdown("pther")