import streamlit as st
import plotly.express as px
import pandas as pd

def get_chart_app2():
     
    # Sample data for significant wins
    data = {
        "Date": ["2023-05-28", "2023-09-17", "2023-05-21", "2024-03-29", "2023-09-17", "2023-09-17", "2023-09-24", "2024-04-07", "2023-09-24", "2023-05-28", "2023-05-28"],
        "Tournament": ["PNL Pennsylvania", "Elite 8 Duals- Folk 2023", "2023 PAUSAW FS State Championship", "PAUSAW Warrior Run FS/GR Qualifier", "Elite 8 Duals- Folk 2023", "Elite 8 Duals- Folk 2023", "Tyrant Nationals", "2024 Last Chance OTT Qualifier", "Tyrant Nationals", "PNL Pennsylvania", "PNL Pennsylvania"],
        "Match": ["Josh Vazquez (TF)", "Cooper Hilton (Maj)", "Josef Garshnick (TF)", "Griffin Walizer (TF)", "Casen Roark (TF)", "Elias Navida (TF)", "Kai Vielma (TF)", "Aden Valencia (Dec)", "William Sakoutis (TF)", "Adrian Meza (Dec)", "Nathan Desmond (TF)"],
        "Result": ["TF", "Maj", "TF", "TF", "TF", "TF", "TF", "Dec", "TF", "Dec", "TF"]
    }
    
    # DataFrame creation
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Define bubble sizes based on match result
    result_size_mapping = {"TF": 40, "Maj": 30, "Dec": 20}
    df['Size'] = df['Result'].map(result_size_mapping)
    
    # Define bubble color based on match result
    result_color_mapping = {"TF": 'blue', "Maj": 'green', "Dec": 'red'}
    df['Color'] = df['Result'].map(result_color_mapping)
    
    # Plotly bubble chart
    fig = px.scatter(df, x='Date', y='Tournament', size='Size', color='Result',
                    hover_name='Match', title='Significant Wins',
                    labels={'Date': 'Date', 'Tournament': 'Tournament', 'Size': 'Type of Win'},
                    color_discrete_map={"TF": 'blue', "Maj": 'green', "Dec": 'red'})
    
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                    selector=dict(mode='markers'))
    
    # Streamlit app
    st.title('Wrestler Dashboard - Significant Wins')
    
    with st.container():
        st.plotly_chart(fig, use_container_width=True)