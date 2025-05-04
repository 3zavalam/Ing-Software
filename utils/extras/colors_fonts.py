import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
#from sklearn.metrics import pairwise_distances_argmin_min

# Add custom fonts
regular_font_path = '/Users/emilio/Documents/4- Archive/fonts/Exo_2/static/Exo2-Black.ttf'
bold_font_path = '/Users/emilio/Documents/4- Archive/fonts/Exo_2/static/Exo2-Bold.ttf'

regular_font = font_manager.FontProperties(fname=regular_font_path)
bold_font = font_manager.FontProperties(fname=bold_font_path)

# Define the colors using hexadecimal representations
background_color = '#191919'  # Gray
title_color = '#000000'       # Black
text_color = '#333333'        # Dark Gray
sub_text_color = '#808080'    # Medium Gray
accent_color1 = '#4682B4'     # Blue
accent_color2 = '#ff6961'     # Orange
accent_color3 = '#ffcc00'     # Yellow

# Function to calculate Euclidean distance between two colors in RGB space
def color_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

# Convert color names to RGB values (you can use a color dictionary or manually specify)
def hex_to_rgb(hex_color):
    return np.array([int(hex_color[i:i+2], 16) for i in (1, 3, 5)])

colors_hexmap = [
    '#d0d6d4',
    '#c5d0cd',
    '#bbcac7',
    '#b0c3c1',
    '#a6bdbb',
    '#9bb7b5',
    '#91b1af',
    '#86aaa8',
    '#7ca4a2',
    '#719e9c',
    '#679896',
    '#5c9190',
    '#528b8a',
    '#478583',
    '#3d7f7d',
    '#327877',
    '#287271',
]

# Function to calculate Euclidean distance between two colors in RGB space
def color_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

# Convert color names to RGB values (you can use a color dictionary or manually specify)
def hex_to_rgb(hex_color):
    return np.array([int(hex_color[i:i+2], 16) for i in (1, 3, 5)])

""" Tablesn """
row_colors = {
    "even": "#8380B6",
    "odd": "#8789C0"
}
plt.rcParams["text.color"] = text_color
plt.rcParams["font.family"] = "Exo 2"