import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap

from ..extras.stats import *
from ..extras.colors_fonts import *

def make_dynamic_table(df, pos, main_stat, background_color="#F6F0ED", text_color="black"):
    # Ensure position exists in the defined stats
    if pos not in positions_stats:
        raise ValueError(f"Position '{pos}' is not recognized. Available positions: {list(positions_stats.keys())}")

    stats = positions_stats[pos]
    new_stats = [stat.split('_')[1] if '_' in stat else stat for stat in stats]

    # Filter DataFrame for selected stats
    df_final = df[stats].sort_values(by=main_stat, ascending=False).reset_index(drop=True)

    # Clean column names
    cleaned_names = [stat.split('_')[1] if '_' in stat else stat for stat in stats]
    df_final.columns = cleaned_names

    # Update main_stat to reflect the cleaned name
    cleaned_main_stat = main_stat.split('_')[1] if '_' in main_stat else main_stat

    # Define column definitions dynamically
    col_defs = []

    for stat in new_stats:
        col_def = ColumnDefinition(
            name=stat,
            textprops={"ha": "center", "va": "center", "color": text_color, "fontsize": "12"},
            width=0.5
        )

        # Add specific formatting for the main stat
        if stat == cleaned_main_stat:
            col_def = ColumnDefinition(
                name=stat,
                textprops={"ha": "center", "color": text_color, "weight": "bold", 
                           "bbox": {"boxstyle": "circle", "pad": .35}},
                cmap=normed_cmap(df_final[stat], cmap=matplotlib.cm.PiYG, num_stds=2),
                width=0.5
            )
        col_defs.append(col_def)

    # Create the table
    fig, ax = plt.subplots(figsize=(16, 20))
    fig.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    table = Table(
        df_final[:16],
        column_definitions=col_defs,
        index_col="Player",
        row_dividers=True,
        row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
        footer_divider=True,
        textprops={"fontsize": 15}, 
        ax=ax
    )
    
    # Update title
    plt.title(f'{pos.capitalize()} Stats Sorted by {cleaned_main_stat}', fontsize=30, color=text_color)
    
    return fig