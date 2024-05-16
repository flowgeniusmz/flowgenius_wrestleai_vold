import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from data.charts import chart_app1 as chart1, chart_app2 as chart2,  chart_app3 as chart3, chart_app4 as chart4



# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 4
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)

chart_radio = st.radio(label="Data View Selection", options=["Charts 1", "Charts 2", "Charts 3"], horizontal=True)
if chart_radio == "Charts 1":
    chart1.get_chart_app1()
elif chart_radio == "Charts 2":
    chart2.get_chart_app2()
elif chart_radio == "Charts 3": 
    chart4.show()

# chart_tabs = st.tabs(tabs=["Charts 1", "Charts 2", "Charts 3"])
# with chart_tabs[0]:
#     chart1.get_chart_app1()
# with chart_tabs[1]:
#     chart2.get_chart_app2()
# with chart_tabs[2]:
#     chart4.get_chart_app4()