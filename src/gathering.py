import requests 
import json
import os
import pandas as pd
from pandas import json_normalize
#import tweepy
import time
from datetime import datetime
import sys
sys.path.append('../')
from config import *
from src import functions as fn 



def get_list():
    players_list = []
    for tir in tier[3:]:
        for div in division:
            n=1000
            players_list += (fn.players_rank(tir,div,n))
        print(tir, " done")
        print(len(players_list), " players")
    for tir in tier[:3]:
        players_list += (fn.players_rank(tir,"I",n))
        print(tir, " done")
        print(len(players_list), " players")
    print("base list ", len(players_list)," players")
    with open(f'../data/players_list.json', 'w') as f:
        json.dump(players_list,f)
    print("done")
    return players_list


def build_list(players_list):
    players = []

    for ind,player in enumerate(players_list):
        if fn.get_puuid(player)== []:
            print(f"player {player['summonerName']} no longer exists")
            #players_list.remove(player)

        else:
            players.append(fn.get_puuid(player))
            players.append(fn.get_games_list(player))
            #players_list[ind] = fn.usefull_info(player)
            
            if (ind+1)%10 == 0:
                print(ind+1," players info fixed")
                #with open(filename, "a") as f:
                    #json.dump(data,f)

    with open(f'../data/players.json', 'a') as f:
        json.dump(players,f)
    print("done")


"""
mongoimport --db LeagueRank --collection players --jsonArray players_sample

# Loading or Opening the json file
with open('data.json') as file:
    file_data = json.load(file)
     
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    c.insert_many(file_data)  
else:
    c.insert_one(file_data)
""" 


## make for loop to gather player data

#getting rank list

## make for loop to gather player data


"""
    url_match_id2= f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?type=ranked&start=0&count=50&api_key={API_KEY}"
    url_match_id = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?start=0&count=50&api_key={API_KEY}"
    match_ids = requests.get(url_match_id).json()
""" 
"""
    player_stats=[]
    for match_id in match_ids:
        time.sleep(0.11)

        url_match = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
        match_detail = requests.get(url_match).json()
        game_stats={}
        game_stats['gameDuration']=match_detail["info"]["gameDuration"]
        game_stats['gameMode']=match_detail["info"]["gameMode"]
        game_stats['gameStartTimestamp']= datetime.fromtimestamp(match_detail["info"]["gameStartTimestampddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"])



        for player in match_detail["info"]["participants"]:
            if player['summonerName'] == "jalex141":
                for key,value in player.items():
                    game_stats[key]= value
        player_stats.append(game_stats)
    df = pd.DataFrame(player_stats)
    df.to_csv(f"./data/player_data.csv")
"""