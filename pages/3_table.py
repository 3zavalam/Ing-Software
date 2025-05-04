import streamlit as st
import pandas as pd
import io
import os

from utils.make_viz.table import make_dynamic_table
from utils.extras.stats import positions_stats, positions_options

# Configure the Streamlit page
st.set_page_config(page_title="🪑 Dynamic Table", layout="wide", initial_sidebar_state="collapsed")

# Main page title
st.title("🪑 Dynamic Table")

# Add a visual divider
st.markdown("---")


# Create selection inputs for position and main stat
with st.container():
    left, center, right = st.columns(3)
    with left:
        leagues = ['MLS', 'Liga MX']
        league = st.selectbox(
            'Pick a league:',
            leagues
        )
    with center:
        position = st.selectbox(
            'Pick a position:',
            positions_stats.keys()
        )
    with right:
        main_stat = st.selectbox(
            'Pick a main stat:',
            positions_stats[position][1:] # Skip the 'Player' stat
        )

# Construct the path for the selected league
league_path = os.path.join('./data/radar', league.replace(" ", "_"))

if position in positions_stats:
    valid_positions = positions_options.get(position, [])
    if position == 'keepers':
        df = os.path.join(league_path, 'keepers.csv')
        df = pd.read_csv(df)
    else:
        df = os.path.join(league_path, 'players.csv')
        df = pd.read_csv(df)
    
    # Select relevant columns based on the position
    relevant_columns = positions_stats.get(position, [])
    df = df[[col for col in relevant_columns if col in df.columns]]

# Generate and display the dynamic table
with st.container():
    # Generate the visualization figure
    fig = make_dynamic_table(df, position, main_stat)
    
    # Display the figure in the Streamlit app
    st.pyplot(fig)
    
    # Create an in-memory buffer to save the figure
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    # Add a download button for the figure
    st.download_button(
        label="Download Image",
        data=buffer,
        file_name=f"table_{main_stat}.png",
        mime="image/png"
    )
