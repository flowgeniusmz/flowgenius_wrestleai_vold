import streamlit as st
from config import pagesetup as ps, sessionstates as ss

# 1. Set Page Config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)

ps.get_page_styling()

ps.display_background_image()

# 3. Session States
ss.initial_session_State()

# 2. Set Page Title
ps.set_title_manual(varTitle="WrestleAI", varSubtitle="Login / Registration", varDiv=True)