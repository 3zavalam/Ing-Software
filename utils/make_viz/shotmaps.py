from PIL import Image
from mplsoccer import VerticalPitch, Pitch

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import matplotlib.patheffects as path_effects
from highlight_text import fig_text
import matplotlib as mpl
import matplotlib.colors as mcolors

from ..get_data.images import get_team_logo, get_player_image
from ..extras.colors_fonts import *

from utils.extras.teams_players import *
from utils.extras.stats import *

def playerShotmap(player_df):
    df = player_df

    player_name = df['playerName'].iloc[0]
    player_id = df['playerId'].iloc[0]

    xG_player = round(df['expectedGoals'].sum(), 2)
    xG_perShot = round(df['expectedGoals'].sum() / df.shape[0], 2)

    goles = df[df['eventType'] == 'Goal']
    no_goles = df[df['eventType'] != 'Goal']

    player_shots = df.shape[0]
    player_goals = goles.shape[0]

    fig, ax = plt.subplots(figsize=(16,9))
    pitch = VerticalPitch(pitch_type='custom', pitch_length=105, pitch_width=68, 
                        goal_type='box', half=True, pitch_color='black')

    fig.set_facecolor('black')

    pitch.draw(ax=ax)

    plt.ylim(50, 115)

    pitch.scatter(goles.x, goles.y, ax=ax, s=goles.expectedGoals*1400, alpha=.9, ec='white', label='Goals', color='#45b6fe', zorder=.999)
    pitch.scatter(no_goles.x, no_goles.y, ax=ax, s=no_goles.expectedGoals*1400, alpha=.3, ec='white', label='Shots', color='#45b6fe', zorder=0)

    ax.text(10, 65, f'{round(xG_player, 2)}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
    ax.text(15, 65, 'xG', va='center', ha='center', fontsize=18, color='white')

    ax.text(10, 70, f'{round(xG_perShot, 2)}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
    ax.text(18, 70, f'xG per Shot', va='center', ha='center', fontsize=18, color='white')

    ax.text(55, 65, f'{player_shots}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
    ax.text(60, 65, f'Shots', va='center', ha='center', fontsize=18, color='white')

    ax.text(55, 70, f'{player_goals}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
    ax.text(60, 70, f'Goals', va='center', ha='center', fontsize=18, color='white')

    plt.text(33, 110, f'{player_name}', fontsize=35, color='white', va='bottom', ha='center',  fontweight='bold')
    plt.imshow(get_player_image(player_id), extent=(0, 5, 106, 114), aspect='auto')

    plt.legend(ncol=2, loc='lower center', prop={'size' : 16}, shadow=True, edgecolor='black')

    #file_path = f'{output_path}/shotmap_{player_name}.png'
    #plt.savefig(file_path)
    #print(f'Shotmap saved')

    #plt.show()

    return fig

def playerShotmapHex(player_df):
    df = player_df

    if 'SOC' not in mpl.colormaps:
        soc_cm = mcolors.LinearSegmentedColormap.from_list('SOC', colors_hexmap, N=50)
        mpl.colormaps.register(name='SOC', cmap=soc_cm)


    # function for semicircle
    def semicircle(r, h, k):
        x0 = h - r  # determine x start
        x1 = h + r  # determine x finish
        x = np.linspace(x0, x1, 10000)  # many points to solve for y

        # use numpy for array solving of the semicircle equation
        y = k - np.sqrt(r**2 - (x - h)**2)  
        return x, y
    
    # Extract necessary information
    team_id = df['teamId'].iloc[0]
    player_id = df['playerId'].iloc[0]
    player_name = df['playerName'].iloc[0]
    data = df[['eventType', 'playerName', 'x', 'y', 'expectedGoals', 'teamId', 'teamColor', 'teamId']]

    # Setup pitch
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    fig.set_facecolor('white')
    pitch = VerticalPitch(
        pitch_type='custom',
        half=True,
        goal_type='box',
        linewidth=1.25,
        line_color='black',
        pad_bottom=-8,
        pad_top=10,
        pitch_length=105,
        pitch_width=68
    )
    pitch.draw(ax=ax)

    # Hexbin plot
    hb = pitch.hexbin(x=data['x'], y=data['y'], ax=ax, cmap='SOC', gridsize=(14, 14), zorder=-1, edgecolors='#efe9e6', alpha=0.9, lw=.25)

    # Add a colorbar for the hexbin plot
    cb = fig.colorbar(hb, ax=ax, orientation='horizontal', fraction=0.02, pad=0.15)
    cb.set_label('Density of Shots', fontsize=5)  # Label for colorbar
    cb.ax.tick_params(labelsize=5)  # Adjust tick labels' size
    cb.ax.set_position([0.25, 0.2, 0.2, 0.02])  # Adjust the values to center the colorbar

    # Hexbin plot
    pitch.hexbin(x=data['x'], y=data['y'], ax=ax, cmap='SOC', gridsize=(14, 14), zorder=-1, edgecolors='#efe9e6', alpha=0.9, lw=.25)

    # Draw median distance semicircle
    x_circle, y_circle = semicircle(104.8 - data['x'].median(), 34, 104.8)
    ax.plot(x_circle, y_circle, ls='--', color='red', lw=.75)

    # Hexagon annotations
    # Updated order for xG per shot first, then total shots
    annot_x = [54 - x * 14 for x in range(0, 4)]
    annot_texts = ['Goals', 'xG', 'xG/Shot', 'Shots']
    annot_stats = [
        data[data['eventType'] == 'Goal'].shape[0],              # Goals
        round(data.expectedGoals.sum(), 2),                      # Total xG
        round(data['expectedGoals'].sum() / data.shape[0], 2),   # xG per shot
        data.shape[0],                                           # Total shots
    ]

    # Plotting the annotations
    for x, s, stat in zip(annot_x, annot_texts, annot_stats):
        hex_annotation = RegularPolygon((x, 68), numVertices=6, radius=4.5, edgecolor='black', fc='white', lw=1.25, color='black')
        ax.add_patch(hex_annotation)
        ax.annotate(
            xy=(x, 70), 
            text=s, 
            xytext=(0, -14), 
            textcoords='offset points', 
            size=5, 
            ha='center', 
            va='center', 
            color='black'
        )
        text_stat = f'{stat:.0f}' if isinstance(stat, int) else f'{stat:.2f}'
        text_ = ax.annotate(
            xy=(x, 69), 
            text=text_stat, 
            xytext=(0, 0), 
            textcoords='offset points', 
            size=5, 
            ha='center', 
            va='center', 
            weight='bold', 
            color='black'
        )
        text_.set_path_effects([path_effects.Stroke(linewidth=.20, foreground='black'), path_effects.Normal()])

    # Median distance annotation
    ax.annotate(
        xy=(34, 110),
        xytext=(x_circle[-1], 110),
        text=f"{((105 - data['x'].median()) * 18) / 16.5:.1f} m.",
        size=4,
        color='red',
        ha='right',
        va='center',
        arrowprops=dict(arrowstyle='<|-, head_width=0.35, head_length=0.65', color='red', fc='#efe9e6', lw=0.75)
    )
    ax.annotate(xy=(34, 110), xytext=(4, 0), text="Avg Shot Distance", textcoords='offset points', size=4, color='red', ha='left', va='center', alpha=0.5)

    # Subtitle
    ax.annotate(xy=(34, 114), text=f"Shotmap for Season {seasons}", size=7.5, color='black', ha='center', va='center', alpha=0.8)

    # --- Transformation functions ---
    DC_to_FC = ax.transData.transform
    FC_to_NFC = fig.transFigure.inverted().transform
    DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))

    # --- Team logo ---
    ax_coords = DC_to_NFC((60, 108))
    ax_size = 0.08
    image_ax = fig.add_axes([ax_coords[0], ax_coords[1], ax_size, ax_size], fc='None')
    image_ax.imshow(get_team_logo(team_id))  
    image_ax.axis('off')

    # --- Player image ---
    ax_coords = DC_to_NFC((14, 108))
    ax_size = 0.08
    image_ax = fig.add_axes([ax_coords[0], ax_coords[1], ax_size, ax_size], fc='None')
    image_ax.imshow(get_player_image(player_id))  
    image_ax.axis('off')

    # --- Title and subtitle ---
    fig_text(
        x=0.52, y=0.90,
        s=f"{player_name}",
        va="bottom", ha="center",
        fontsize=18, color="black", weight="bold"
    )
    fig_text(
        x=0.65, y=0.22,
        s="Data via FotMob | @MatchSense",
        ha="center",
        fontsize=5, color='black', alpha=0.6
    )

    #file_path = f'{output_path}/shotmapHex_{player_name}.png'
    #plt.savefig(file_path)
    #print(f'Shotmap Hex saved')

    #plt.show()

    return fig

def teamShotmap(match_df):
    df = match_df

    home_team_id = int(list(df['teamId'].unique())[0])
    away_team_id = int(list(df['teamId'].unique())[1])

    # Initialize variables for team names
    home_team_name = None
    away_team_name = None

    # Mapear los IDs con los nombres usando fotmob_leaguesCup
    for team_name, team_id in fotmob_leaguesCup.items():
        if team_id == home_team_id:
            home_team_name = team_name
        if team_id == away_team_id:
            away_team_name = team_name

    # Dictionary to store figures for each team
    figures = {}

    # Process each team
    for team_name, team_id in [(home_team_name, home_team_id), (away_team_name, away_team_id)]:
        against_team_name = away_team_name if team_name == home_team_name else home_team_name
        team_df = df[df['teamId'] == team_id]  # Adjust 'teamId' to match your column name

        xG_team = round(team_df['expectedGoals'].sum(), 2)
        xG_perShot = round(team_df['expectedGoals'].sum() / team_df.shape[0], 2) if team_df.shape[0] > 0 else 0

        goles = team_df[team_df['eventType'] == 'Goal']
        no_goles = team_df[team_df['eventType'] != 'Goal']

        num_goals = goles.shape[0]
        team_shots = team_df.shape[0]

        # Create a figure
        fig, ax = plt.subplots(figsize=(16, 9))
        pitch = VerticalPitch(pitch_type='custom', pitch_length=105, pitch_width=68,
                              goal_type='box', half=True, pitch_color='black')
        fig.set_facecolor('black')
        pitch.draw(ax=ax)

        # Scatter goals and shots
        pitch.scatter(goles.x, goles.y, ax=ax, s=goles.expectedGoals * 1400, alpha=.9, ec='white', label='Goals', color='#45b6fe', zorder=.999)
        pitch.scatter(no_goles.x, no_goles.y, ax=ax, s=no_goles.expectedGoals * 1400, alpha=.3, ec='white', label='Shots', color='#45b6fe', zorder=0)

        plt.ylim(50, 115)

        # Stats
        ax.text(10, 65, f'{round(xG_perShot, 2)}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
        ax.text(18, 65, f'xG per Shot', va='center', ha='center', fontsize=18, color='white')

        ax.text(10, 70, f'{round(xG_team, 2)}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
        ax.text(15, 70, 'xG', va='center', ha='center', fontsize=18, color='white')

        ax.text(55, 65, f'{team_shots}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
        ax.text(60, 65, f'Shots', va='center', ha='center', fontsize=18, color='white')

        ax.text(55, 70, f'{num_goals}', va='center', ha='center', fontsize=18, fontweight='bold', color='white')
        ax.text(60, 70, f'Goals', va='center', ha='center', fontsize=18, color='white')

        # Team name and opponent
        plt.text(33, 110, f'{team_name}', fontsize=35, color='white', va='bottom', ha='center', fontweight='bold')
        plt.text(33, 107.5, f'vs {against_team_name}', fontsize=20, color='white', va='bottom', ha='center', alpha=0.7)

        # Add logo (ensure `get_team_logo` returns a valid image)
        plt.imshow(get_team_logo(team_id), extent=(0, 5, 106, 114), aspect='auto')

        # Add legend
        plt.legend(ncol=2, loc='lower center', prop={'size': 16}, shadow=True, edgecolor='black')

        # Store the figure in the dictionary
        figures[team_name] = fig

        #plt.show()

    return home_team_name, away_team_name, figures