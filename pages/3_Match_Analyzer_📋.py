import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from data.videoupload import videoupload_app1 as vidapp1
from classes import video_class as vclass


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 2
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)

videoupload = vclass.VideoUpload()
videoupload.run()