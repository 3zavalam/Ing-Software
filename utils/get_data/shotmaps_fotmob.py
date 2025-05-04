import LanusStats as ls
fotmob = ls.FotMob()

def get_player_shotmap(player_id):
    player_df = fotmob.get_player_shotmap("0", "0", player_id)
    print('Player shotmap completed!')

    return player_df

def get_match_shotmap(match_id):    
    match_df = fotmob.get_match_shotmap(match_id)
    print('Match shotmap completed!')

    return match_df

