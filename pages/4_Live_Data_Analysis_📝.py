import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from data.charts import chart_app1 as chart1, chart_app2 as chart2,  chart_app3 as chart3



# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 3
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)


chart3.get_chart_app3()