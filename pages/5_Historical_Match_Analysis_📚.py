import streamlit as st
from config import pagesetup as ps, sessionstates as ss
import matplotlib.pyplot as plt
import pandas as pd



# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 4
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)



# Load datasets
attendance_df = pd.read_csv('bo_bassett_attendance.csv')
injury_df = pd.read_csv('bo_bassett_injury_reports.csv')
weight_df = pd.read_csv('bo_bassett_weight.csv')

# Example match data
# Example match data
match_data = {
    'Date': ['2024-01-15', '2024-02-20', '2024-03-10'],
    'Opponent': ['Anthony Ashnault', 'David Evans', 'Aden Valencia'],
    'Result': ['Win', 'Win', 'Win'],
    'Score': ['12-2', '10-0', '9-1']
}
match_df = pd.DataFrame(match_data)

# Profile Section
st.title("Bo Bassett - WrestleAI Profile")
st.image("bobasset.jpeg", caption="Bo Bassett", use_column_width=False)

# Layout
st.write("---")
st.subheader("Athlete Overview")
col1, col2 = st.columns(2)

with col1:
    st.metric("Ranking", "#2 in the class of 2026")
    st.metric("Weight Class", "138 lbs")

with col2:
    st.metric("Current Record", "3-0")

# Performance Metrics
st.write("---")
st.subheader("Performance Metrics")

with st.container():
    st.write("### Match Results")
    st.table(match_df)

    st.write("### Win/Loss Record")
    fig, ax = plt.subplots()
    ax.plot(match_df['Date'], match_df['Result'], marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Result')
    ax.set_title('Win/Loss Record')
    st.pyplot(fig)

# Improvement Areas
st.write("---")
st.subheader("Improvement Areas")
st.text("Main focus areas for improvement...")

# Weight Management
st.write("---")
st.subheader("Weight Management")
with st.container():
    st.write(weight_df)
    fig, ax = plt.subplots()
    ax.plot(weight_df['Date'], weight_df['Weight'], marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Weight (lbs)')
    ax.set_title('Weight Management Over Time')
    st.pyplot(fig)

# AI Recommendations
st.write("---")
st.subheader("AI Recommendations")
st.multiselect("AI Suggested Improvements", ['Technical Skills', 'Mental Toughness', 'Endurance'])

# Coach Comments
st.write("---")
st.subheader("Coach Comments")
st.text_area("Coach Feedback")

# Attendance and Practice Details
st.write("---")
st.subheader("Attendance and Practice Details")
with st.container():
    st.write(attendance_df)

# Injury Reports
st.write("---")
st.subheader("Injury Reports")
with st.container():
    st.write(injury_df)

st.write("---")