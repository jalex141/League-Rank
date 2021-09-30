import requests 
import json
import os
from getpass import getpass
import pandas as pd
from pandas import json_normalize
#import tweepy
import time
from datetime import datetime

from src import functions as fn 
from riotwatcher import LolWatcher, ApiError


API_KEY = getpass("input your api key:  ")
watcher = LolWatcher(API_KEY)
my_region = 'euw1'

response_riot = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/jalex141?api_key={API_KEY}")
response_riot

#form url for API call
base = "api.riotgames.com/lol/"
endpoints = [""]
queue = "RANKED_SOLO_5x5"
tier = ["CHALLENGER", "GRANDMASTER","MASTER", "DIAMOND", "PLATINUM", "GOLD", "SILVER","BRONZE", "IRON"]
division = ["I", "II", "III", "IV"]
platform = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ru","tr1"]
region = ["europe","asia","americas"]


players_list = []
for tir in tier[3:]:
    for div in division:
        n=1000
        players_list += (fn.players_rank(tir,div,n))
for tir in tier[:3]:
    players_list += (fn.players_rank(tir,"I",n))

for ind,player in enumerate(players_list):
    players_list[ind] = fn.get_puuid(player)
    players_list[ind] = fn.

## make for loop to gather player data

#getting rank list
response_rank = requests.get(f"{url_rank}").json()

## make for loop to gather player data


for player in response_rank:
    player_data = {}
    player_data['tier'] = player['tier']
    player_data['rank'] = player['rank']
    player_data['summonerName'] = player['summonerName']
    player_data['leaguePoints'] = player['leaguePoints']
    player_data['wins'] = player['wins']
    player_data['losses'] = player['losses']
    player_data['veteran'] = player['veteran']

    player = watcher.summoner.by_name(my_region, player['summonerName'])
    player_data['puuid'] = player['puuid']
    player_data['summonerLevel'] = player['summonerLevel']
## I can filter start index
    url_match_id2= f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?type=ranked&start=0&count=50&api_key={API_KEY}"
    url_match_id = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?start=0&count=50&api_key={API_KEY}"
    match_ids = requests.get(url_match_id).json()
    

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
