import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from datetime import datetime



def get_chart_app3():
    # Sample data for upcoming events
    data = {
        "Date": ["2024-05-15", "2024-05-17", "2024-05-17", "2024-05-17", "2024-05-17", "2024-05-17", "2024-05-17", "2024-05-17", "2024-05-18", "2024-05-18"],
        "Tournament": ["May 15 Event", "University of Wrestling SUMMER SEASON 2024", "2024 CAUSA Assoc Duals - Schoolboys", "2024 CAUSA Association Duals - BOYS", "2024 CAUSA Association Duals - GIRLS", "PAUSAW State FS/GR Championship", "AZ-USAW `State Freestyle Tournament`", "2024 Dynamic Friday Night Throw Down / Canceled", "2024 USA Wrestling Central Regional Champ - FS", "2024 Brady Strong National Duals (HS)"],
        "Location": ["Allen, TX 75002", "Bountiful, UT 84010", "Fresno, CA 93721", "Fresno, CA 93721", "Fresno, CA 93721", "State College, PA 16803", "Phoenix, AZ 85048", "Raleigh, NC 27603", "Fort Wayne, IN 46805", "Whitesboro, NY 13492"],
        "Latitude": [33.1032, 40.8894, 36.7378, 36.7378, 36.7378, 40.7934, 33.3076, 35.7715, 41.1239, 43.1251],
        "Longitude": [-96.6706, -111.8802, -119.7871, -119.7871, -119.7871, -77.8616, -112.0144, -78.6401, -85.1413, -75.3451]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Function to get color based on date proximity
    def get_color(date):
        days_to_event = (date - datetime.now()).days
        if days_to_event <= 7:
            return 'red'
        elif days_to_event <= 14:
            return 'orange'
        else:
            return 'green'
    
    # Create map
    map_center = [39.8283, -98.5795] # Center of the USA
    m = folium.Map(location=map_center, zoom_start=4)
    
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers to map
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Tournament']}<br>{row['Date'].strftime('%Y-%m-%d')}<br>{row['Location']}",
            icon=folium.Icon(color=get_color(row['Date']))
        ).add_to(marker_cluster)
    
        # Display the map
    st_folium(m, width=700, height=500, use_container_width=True)