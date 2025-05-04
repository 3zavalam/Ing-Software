import streamlit as st

from utils.extras.teams_players import fotmob_MLS_2024_players, fotmob_leaguesCup_2024_players
from utils.make_viz.shotmaps import playerShotmap, playerShotmapHex
from utils.get_data.shotmaps_fotmob import get_player_shotmap

# Configure the Streamlit page
st.set_page_config(page_title="🎯 Shotmaps", layout="wide", initial_sidebar_state="collapsed")

# Main page title
st.title("🎯 Shotmaps")

# Add a visual divider
st.markdown("---")

# Team and Player Selection
with st.container():
    teams, players = st.columns([1.5, 1.5])  # Adjust column proportions

    # Dictionary containing team and player data
    team_dict = fotmob_MLS_2024_players  # Replace with your default data source

    if team_dict:
        # Team Selection
        with teams:
            st.subheader("Teams")
            team_names = list(team_dict.keys())
            team_selected = st.selectbox('Pick a team:', team_names)

        # Player Selection
        if team_selected:
            team_data = team_dict.get(team_selected, {})
            team_id = team_data.get('id', 'No ID Available')

            with players:
                st.subheader("Player")
                player_names = list(team_data.get('players', {}).keys())
                player_selected = st.selectbox('Pick a player:', player_names)

# Shotmap Visualization
if player_selected:
    try:
        # Fetch player data
        player_id = team_data['players'][player_selected]
        player_df = get_player_shotmap(player_id)

        # Two-column layout for visualization
        col1, col2 = st.columns([2, 1])  # Adjusted proportions

        # Column 1: Shotmap Visualization
        with col1:
            fig = playerShotmap(player_df)
            st.pyplot(fig)

        # Column 2: Hexagonal Shotmap Visualization
        with col2:
            fig = playerShotmapHex(player_df)
            st.pyplot(fig)

        # Display Notes
        st.markdown(
            """
            <div style="font-size: 22px; font-weight: bold; margin-top: 20px;">
                Notes
            </div>
            <ul style="font-size: 18px; margin-top: 10px; list-style-type: disc; padding-left: 20px;">
                <li>The shotmaps show shot attempts.</li>
                <li>The hexagon map highlights key areas and density of shots.</li>
            </ul>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Error generating the Shotmaps: {e}")
else:
    st.info("Pick a player to view the shotmaps.")
