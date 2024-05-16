import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

categories = np.random.choice(['Lightweight', 'Middleweight', 'Heavyweight'], 100)
wins = np.random.randint(0, 10, 100)  # Random win count per category
# Assuming weights is defined somewhere in your code
weights = [150, 150, 155, 160, 160, 160, 170, 180, 185, 190, 190, 190, 200, 200, 210]  # example weights

# Sample dataframe
df = pd.DataFrame({
    'Weight Category': categories,
    'Wins': wins
})


# Graph 1: Histogram of Weights
def create_weight_histogram(weights):
    st.header("Graph 1: Histogram of Athlete Weights")
    fig1, ax1 = plt.subplots()
    ax1.hist(weights, bins=15, color='orange', edgecolor='black')
    ax1.set_title('Distribution of Athlete Weights')
    ax1.set_xlabel('Weight (lbs)')
    ax1.set_ylabel('Number of Athletes')
    st.pyplot(fig1)
    st.markdown("**Interpretation**: This histogram shows the distribution of wrestler weights, which can help coaches understand the weight classes most represented on the team.")

# Graph 4: Bar Plot of Wins per Weight Category
def team_wins_weight():
    st.header("Graph 4: Bar Plot of Wins per Weight Category")
    fig4, ax4 = plt.subplots()
    sns.barplot(x='Weight Category', y='Wins', data=df, ax=ax4, palette='coolwarm')
    ax4.set_title('Total Wins per Weight Category')
    st.pyplot(fig4)
    st.markdown("**Interpretation**: This bar plot compares total wins across different weight categories, providing insights into which groups have been most successful.")


# Generating random season data
matches = np.arange(1, 21)  # 20 matches in a season
team_points = np.cumsum(np.random.randint(5, 15, 20))  # cumulative points scored

# Plotting
def Team_season():
    fig, ax = plt.subplots()
    ax.plot(matches, team_points, marker='o', linestyle='-', color='b')
    ax.set_title('Team Points Scored Over the Season')
    ax.set_xlabel('Match Number')
    ax.set_ylabel('Cumulative Points Scored')
    st.pyplot(fig)
    st.markdown("**Interpretation**: This line graph tracks the cumulative points scored by the team over the season, illustrating overall performance trends and the effectiveness of training regimens.")

# Sample data
weight_classes = ['Lightweight', 'Middleweight', 'Heavyweight']
athletes = [15, 10, 5]  # Example counts

# Pie chart
def pie_chart():
    fig, ax = plt.subplots()
    ax.pie(athletes, labels=weight_classes, autopct='%1.1f%%', startangle=90, colors=['gold', 'lightblue', 'lightgreen'])
    ax.set_title('Distribution of Athletes by Weight Class')
    st.pyplot(fig)
    st.markdown("**Interpretation**: This pie chart shows the percentage of athletes in each weight class, helping coaches to balance training resources and focus.")

# Generating random scores data
np.random.seed(42)
average_scores = np.random.randint(10, 20, size=3)  # random average scores for 3 weight classes

# Bar chart
def bar_chart():
    fig, ax = plt.subplots()
    ax.bar(weight_classes, average_scores, color='teal')
    ax.set_title('Average Match Scores by Weight Class')
    ax.set_xlabel('Weight Class')
    ax.set_ylabel('Average Score')
    st.pyplot(fig)
    st.markdown("**Interpretation**: This bar chart compares the average scores per match across different weight classes, highlighting performance disparities and successes.")


def show():
    def page_stylable_container1():
        with stylable_container(
            key="Blue",
            css_styles="""
                {
                    height: "500"px;
                    background-color: #3F9EED80;
                    color: #e6e6e6;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 10px;
                    border: 1px solid #ccc;
                    box-shadow: 0px 0px 8px #FFCB0B;
                    overflow-x: auto;
                }
            """,
        ):
            st.markdown("A tab dedicated to the team as a whole, similar to the individual, but larger scale")
    
    page_stylable_container1()


    #first box
    def container1():
        return st.container(border=True)
    def container1a():
        return st.container(border=True)
    def container1b():
        return st.container(border=True)
    def container1c():
        return st.container(border=True)
    def container1c1():
        return st.container(border=True)
    #second box
    def container2():
        return st.container(border=True)
    def container2a():
        return st.container(border=True)
    def container2b():
        return st.container(border=True)
    def container2c():
        return st.container(border=True)

    with container1():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,10,1,5,1,7,1])
        with col2:
            with container1a():
                st.dataframe(df)
        with col4:
            with container1b():
                team_wins_weight()
        with col6:
            with container1c():
                Team_season()
            with container1c1():
                st.write("Containers can be moved anywhere in the UI, and filled with text, graphs, input boxes, and so much more!")
    with container2():
        col1_1, col2_1, col3_1, col4_1, col5_1, col6_1, col7_1 = st.columns([1,6,1,4,1,4,1])
        with col2_1:
            with container2a():
                create_weight_histogram(weights)
        with col4_1:
            with container2b():
                bar_chart()
        with col6_1:
            with container2c():
                pie_chart()