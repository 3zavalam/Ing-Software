# Keepers
keepers = [
    "Player", "keepers_Save%", "keepers_GA90", "keepers_CS%",
    "keepersadv_PSxG+/-", "keepersadv_PSxG/SoT"
]

# Laterals (full-backs or wing-backs)
laterals = [
    "Player", "defense_TklW", "defense_Int", "defense_Clr",
  "passing_Cmp%", "passing_CrsPA", "playingtime_Min"
]

# Centrals (center-backs)
centrals = [
    "Player", "defense_TklW", "defense_Blocks", "defense_Int",
    "defense_Clr", "passing_Cmp%", "passing_PrgDist"
]

# Defensive Midfielders (CDMs)
defensive_midfielders = [
    "Player", "defense_TklW", "defense_Int", "defense_Tkl+Int",
    "passing_Cmp%", "passing_1/3"
]

# Midfielders (box-to-box or central midfielders)
midfielders = [
    "Player", "stats_Gls", "stats_Ast", "stats_G+A",
    "passing_Cmp%", "passing_PrgDist" 
]

# Attacking Midfielders (AMs)
attacking_midfielders = [
    "Player", "stats_Gls", "stats_Ast", "stats_G+A", "gca_SCA"
]

# Number 10s (playmakers)
number_10s = [
    "Player", "stats_Ast", "stats_G+A", "passing_PPA",
    "gca_SCA", "possession_Att 3rd", "shooting_Gls"
]

# Wingers
wingers = [
    "Player", "stats_Gls", "stats_Ast", "shooting_SoT",
    "passing_CrsPA"
]

# Strikers (forwards)
strikers = [
    "Player", "shooting_Gls",
    "shooting_SoT", "shooting_G/Sh", "misc_PKwon"
]

positions_options = {
    "keepers": ["GK"],
    "laterals": ["DF"],
    "centrals": ["DF"],
    "defensive_midfielders": ["MF"],
    "midfielders": ["MF"],
    "attacking_midfielders": ["MF"],
    "number_10s": ["FW", "MF"],
    "wingers": ["FW"],
    "strikers": ["FW"]
}

positions_stats = {
    "keepers": keepers,
    "laterals": laterals,
    "centrals": centrals,
    "defensive_midfielders": defensive_midfielders,
    "midfielders": midfielders,
    "attacking_midfielders": attacking_midfielders,
    "number_10s": number_10s,
    "wingers": wingers,
    "strikers": strikers
}

leagues_seasons = {
    'MLS': '2024',
    'Liga MX': '2024-2025'
} 
league = " and ".join(leagues_seasons.keys())
seasons = '2024-2025'