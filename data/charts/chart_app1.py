import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def get_chart_app1():
    
    # Sample data
    data = {
        "Date": ["2024-04-07", "2024-03-29", "2023-09-24", "2023-09-17", "2023-08-31", "2023-05-28", "2023-05-28", "2023-05-21",
                "2023-04-08", "2023-04-08", "2023-04-07", "2023-04-07", "2023-02-04", "2023-01-07", "2023-01-07"],
        "Tournament": ["2024 Last Chance OTT Qualifier", "PAUSAW Warrior Run FS/GR Qualifi", "Tyrant Nationals", "Elite 8 Duals- Folk 2023",
                    "High School Boys Season", "PNL Pennsylvania", "PNL Pennsylvania", "2023 PAUSAW FS State Championshi",
                    "PAUSAW Freestyle and Greco Bisho", "PAUSAW Freestyle and Greco Bisho", "PAUSAW Freestyle and Greco Warri",
                    "PAUSAW Freestyle and Greco Warri", "MHSA AA Eastern Divisional", "Bozeman Schools JV 2023 JV Tourn",
                    "2023 East Coast Catholic Classic"],
        "Weight Class": ["Freestyle 65", "Boys Junior", "High School", "132", "114", "Junior 120-1", "Test Group T", "Boys Junior",
                        "Boys Junior", "Boys Junior", "Boys Junior", "Boys Junior", "132", "JV 132B", "120"],
        "Place": ["2nd", "1st", "1st", None, None, "2nd", "4th", "1st", "1st", "1st", "1st", "1st", "DNP", "7th", "1st"]
    }
    
    # DataFrame creation
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Convert places to numerical values
    place_mapping = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6, "7th": 7, "8th": 8, "DNP": None}
    df['Place'] = df['Place'].map(place_mapping)
    
    # Visualization 1: Line Chart with Scatter Points
    fig1 = go.Figure()
    
    for weight_class in df['Weight Class'].unique():
        class_data = df[df['Weight Class'] == weight_class]
        fig1.add_trace(go.Scatter(
            x=class_data['Date'],
            y=class_data['Place'],
            mode='lines+markers',
            name=weight_class,
            text=class_data['Tournament']
        ))
    
    fig1.update_layout(
        title='Wrestler Performance Over Time',
        xaxis_title='Date',
        yaxis_title='Placement',
        yaxis=dict(autorange='reversed'), # Reverse y-axis to show 1st place at the top
        hovermode='x unified'
    )
    
    # Visualization 2: Box Plot
    fig2 = go.Figure()
    
    for weight_class in df['Weight Class'].unique():
        class_data = df[df['Weight Class'] == weight_class]
        fig2.add_trace(go.Box(
            y=class_data['Place'],
            name=weight_class,
            boxpoints='all', # show all points
            jitter=0.3, # spread out points for better visibility
            pointpos=-1.8 # offset points to the left
        ))
    
    fig2.update_layout(
        title='Distribution of Placements by Weight Class',
        xaxis_title='Weight Class',
        yaxis_title='Placement',
        yaxis=dict(autorange='reversed') # Reverse y-axis to show 1st place at the top
    )
    
    # Streamlit app
    st.title('Wrestler Dashboard')
    
    with st.container():
        st.header("Performance Over Time")
        st.plotly_chart(fig1, use_container_width=True)
    
    with st.container():
        st.header("Distribution of Placements by Weight Class")
        st.plotly_chart(fig2, use_container_width=True)