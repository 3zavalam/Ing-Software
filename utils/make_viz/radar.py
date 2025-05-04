from ..extras.stats import *

import pandas as pd
from mplsoccer import PyPizza
from scipy import stats
import math
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy import stats
from mplsoccer import PyPizza

def parse_number(v):
    try:
        if isinstance(v, str):
            v = v.replace(",", "")  # Elimina separadores de miles
        return float(v)
    except:
        return 0

def generate_player_radar(df, player1_name, pos, positions_stats):
    valid_positions = positions_options[pos]

    # Filtrar jugadores según posición
    df = df[df['stats_Pos'].isin(valid_positions)] if pos != 'keepers' else df[df['keepers_Pos'].isin(valid_positions)]

    # Lista original de columnas para esa posición
    original_columns = positions_stats[pos]

    # Filtrar solo columnas que existen realmente en el DataFrame
    available_columns = [col for col in original_columns if col in df.columns]
    missing_columns = [col for col in original_columns if col not in df.columns]

    if missing_columns:
        print(f"⚠️ Missing columns in DataFrame for position '{pos}': {missing_columns}")

    df = df[available_columns]

    # Separar nombre del jugador y columnas numéricas
    params = [col for col in available_columns if col != "Player"]
    cleaned_params = [col.split('_', 1)[1] if '_' in col else col for col in params]

    # Buscar jugador
    player = df[df["Player"] == player1_name].reset_index(drop=True)
    if player.empty:
        raise ValueError(f"Player '{player1_name}' not found for position '{pos}'")

    # Obtener valores numéricos
    raw_values = [player.loc[0, col] if col in player.columns else 0 for col in params]
    numeric_values = [parse_number(v) for v in raw_values]

    # Calcular percentiles robustamente
    percentiles = []
    for col, val in zip(params, numeric_values):
        if col in df.columns:
            try:
                series = df[col].astype(str).str.replace(",", "").astype(float)
                percentile = math.floor(stats.percentileofscore(series, val))
                percentiles.append(99 if percentile == 100 else percentile)
            except:
                percentiles.append(0)
        else:
            percentiles.append(0)

    # Verificar longitud
    if len(params) != len(percentiles):
        raise ValueError(f"❌ Mismatch: {len(params)} params vs {len(percentiles)} values")

    # Crear radar
    baker = PyPizza(
        params=cleaned_params,
        straight_line_color='white',
        straight_line_lw=1,
        last_circle_lw=1,
        other_circle_lw=1,
        other_circle_ls="-."
    )

    fig, ax = baker.make_pizza(
        percentiles,
        figsize=(8, 8),
        param_location=110,
        kwargs_slices=dict(facecolor='#4682B4', edgecolor='#4682B4', zorder=2, linewidth=1, alpha=0.8),
        kwargs_params=dict(color='black', fontsize=12, va="center"),
        kwargs_values=dict(color='white', fontsize=12, zorder=3,
                           bbox=dict(edgecolor="#4682B4", facecolor="#4682B4", boxstyle="round,pad=0.2", lw=1))
    )

    pos_name = pos.replace("_", " ").title()
    fig.text(0.5, 1.02, f'{player1_name} as {pos_name}', size=18, ha="center", weight='bold', color='black')
    fig.text(0.5, 0.98, f"{league} | {seasons}", size=15, ha="center", color='black')
    fig.text(0.5, 0.005, f"Data via Fbref |  @MatchSense", color='gray', ha='center')

    return fig


def generate_2players_radar(df, player1_name, player2_name, pos, positions_stats):
    valid_positions = positions_options[pos]

    # Filtrar por posición
    df = df[df['stats_Pos'].isin(valid_positions)] if pos != 'keepers' else df[df['keepers_Pos'].isin(valid_positions)]

    # Lista original de columnas relevantes
    original_columns = positions_stats[pos]

    # Verificar qué columnas están realmente disponibles en el DataFrame
    available_columns = [col for col in original_columns if col in df.columns]
    missing_columns = [col for col in original_columns if col not in df.columns]

    if missing_columns:
        print(f"⚠️ Missing columns in DataFrame for position '{pos}': {missing_columns}")

    # Usar solo columnas que existen
    df = df[available_columns]

    # Separar nombre del jugador y columnas de stats
    params = [col for col in available_columns if col != "Player"]
    cleaned_params = [col.split('_', 1)[1] if '_' in col else col for col in params]

    # Extraer los datos de los jugadores
    def extract_player_percentiles(df, player_name, columns):
        player = df[df["Player"] == player_name].reset_index(drop=True)
        if player.empty:
            raise ValueError(f"Player '{player_name}' not found for position '{pos}'")

        raw_values = [player.loc[0, col] if col in player.columns else 0 for col in columns]
        numeric_values = [parse_number(v) for v in raw_values]

        percentiles = []
        for col, val in zip(columns, numeric_values):
            if col in df.columns:
                try:
                    series = df[col].astype(str).str.replace(",", "").astype(float)
                    percentile = math.floor(stats.percentileofscore(series, val))
                    percentiles.append(99 if percentile == 100 else percentile)
                except:
                    percentiles.append(0)
            else:
                percentiles.append(0)

        return percentiles

    percentiles1 = extract_player_percentiles(df, player1_name, params)
    percentiles2 = extract_player_percentiles(df, player2_name, params)

    if not (len(params) == len(percentiles1) == len(percentiles2)):
        raise ValueError(f"❌ Mismatch: {len(params)} params, {len(percentiles1)} p1, {len(percentiles2)} p2")

    # Crear radar plot
    baker = PyPizza(
        params=cleaned_params,
        straight_line_color='white',
        straight_line_lw=1,
        last_circle_lw=1,
        other_circle_lw=1,
        other_circle_ls="-."
    )

    fig, ax = baker.make_pizza(
        percentiles1,
        figsize=(8, 8),
        param_location=110,
        kwargs_slices=dict(facecolor='#4682B4', edgecolor='#4682B4', zorder=2, linewidth=1, alpha=.8),
        kwargs_params=dict(color='black', alpha=0.75, fontsize=12, va="center"),
        kwargs_values=dict(color='black', alpha=0.75, fontsize=12, zorder=3, bbox=dict(
            edgecolor='#4682B4', facecolor='#4682B4', boxstyle="round,pad=0.2", lw=1))
    )

    baker.make_pizza(
        percentiles2,
        ax=ax,
        param_location=110,
        kwargs_slices=dict(facecolor='#ff6961', edgecolor='#ff6961', zorder=2, alpha=.8, linewidth=1),
        kwargs_params=dict(color='black', alpha=0.75, fontsize=12, va="center"),
        kwargs_values=dict(color='black', alpha=0.75, fontsize=12, zorder=3, bbox=dict(
            edgecolor='#ff6961', facecolor='#ff6961', boxstyle="round,pad=0.2", lw=1))
    )

    pos_name = pos.replace("_", " ").title()
    fig.text(0.515, 0.97, f'{player1_name} vs {player2_name} as {pos_name}', size=18, ha="center", weight='bold', color='black')
    fig.text(0.515, 0.939, f'{player1_name} vs {player2_name} | {league} {seasons}', size=15, ha="center", color='black')
    fig.text(0.01, 0.005, f'{player1_name}', color='#4682B4', size=12)
    fig.text(0.01, 0.04, f'{player2_name}', color='#ff6961', size=12)
    fig.text(0.5, 0.005, f"Data via Fbref | @MatchSense", color='gray', ha='center')

    return fig