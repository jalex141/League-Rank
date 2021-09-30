import requests 
import json
import os
from getpass import getpass
import pandas as pd
from pandas import json_normalize
#import tweepy
import time
import config
from datetime import datetime



def players_rank(tir,div,n):
    """
    calls the riot api to gather player names and other data
    recieves 'tier', 'division' and n (number to gather)
    returns a list of n or max players from a specific rank 
    """
    i=0; p=1; players =[]
    while i<n:
        url_rank = f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tir}/{div}?page={p}&api_key={API_KEY}"
        response = requests.get(f"{url_rank}").json()
        players += response
        i = len(players)
        p +=1
        if response == []:
            i=n
    return players


def get_puuid(player_data):
    """
    calls the riot api to get 'puuid' and player level
    recieves a dictionary with player data
    returns same dic plus 'puuid' and player level
    """
    player = watcher.summoner.by_name(my_region, name])
    player_data['puuid'] = player['puuid']
    player_data['summonerLevel'] = player['summonerLevel']
    return player_data

def usefull_info(player):
    """
    selects information from player data
    recieves a dictionary with player data
    returns dic with data I can use 
    """
    player_new={}
    player_new['tier'] = player['tier']
    player_new['rank'] = player['rank']
    player_new['summonerName'] = player['summonerName']
    player_new['leaguePoints'] = player['leaguePoints']
    player_new['wins'] = player['wins']
    player_new['losses'] = player['losses']
    player_new['veteran'] = player['veteran']
    player_new['puuid'] = player['puuid']
    player_new['summonerLevel'] = player['summonerLevel']
    return player_new

def get_games_list(player):
    """
    calls the riot api to gather a list of player games 
    recieves a dictionary with player data
    returns same dic plus 'match_ids' list 
    """
    url_match_id= f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?type=ranked&start=0&count=100&api_key={API_KEY}"
    player["match_ids"] = requests.get(url_match_id).json()
    return player
    
