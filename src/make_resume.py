import os
import sys
sys.path.append('../')
from src import mongo_functions as mn
from src import cleaning as cl
from src import functions as fn 
import pandas as pd
from IPython.display import clear_output
duration = 1  # seconds
freq = 440  # Hz

players_list = mn.get_players()
n=0
averege_stats=[]
for player in players_list:
    player_stats_a= fn.usefull_info(player)
    player_stats = []
    filtro = {"metadata.matchId": {"$in":player["match_ids"]}}
    proj = {"info":1,"_id":0}
    
    match_list = mn.get_games(filtro,proj)
    if len(match_list)== 0:
        continue
    else:
        for match_detail in match_list:

            game_stats={}
            game_stats['gameDuration']=match_detail["info"]["gameDuration"]
            game_stats['gameMode']=match_detail["info"]["gameMode"]
            game_stats['gameStartTimestamp']= (match_detail["info"]["gameStartTimestamp"])


            for participant in match_detail["info"]["participants"]:
                if participant['summonerName'] == player['summonerName']:
                    for key,value in participant.items():
                        game_stats[key]= value
            player_stats.append(game_stats)
        df = pd.DataFrame(player_stats)
        chewed = cl.chew_data(df)
        if chewed == []:
            n+=1
            clear_output(wait=True)
            print(len(averege_stats)," done")
            print(n," failed")
            continue
        else:
            for key,value in chewed.items():
                player_stats_a[key]= value  

    averege_stats.append(player_stats_a)
data_a = pd.DataFrame(averege_stats)
data_a.to_csv("../data/dataframe2.csv",index=False)
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


