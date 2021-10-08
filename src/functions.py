import requests 
import json
import os
import pandas as pd
from pandas import json_normalize
#import tweepy
import time
from datetime import datetime

from config import *
class Error(Exception):
    pass

class ExpiredError(Error):
    """
    Exception raised for expired key.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message



def players_rank(tir,div,n):
    """
    calls the riot api to gather player names and other data
    recieves 'tier', 'division' and n (number to gather)
    returns a list of n or max players from a specific rank 
    """
    i=0; p=1; players =[]
    while i<n:
        url_rank = f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tir}/{div}?page={p}&api_key={API_KEY}"
        response = api_call(url_rank)
        #response = requests.get(f"{url_rank}").json()

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
    url_name = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_data['summonerName']}?api_key={API_KEY}"
    player =  api_call(url_name)
    #player = watcher.summoner.by_name(my_region, player_data["summonerName"])
    if player == []:
        return []
    else:
        player_data['puuid'] = player['puuid']
        player_data['summonerLevel'] = player['summonerLevel']

        return player_data

def usefull_info(player):
    """
    selects information from player data
    recieves a dictionary with player data
    returns dic with data I can use 
    """
    player_stats={}
    player_stats['summonerName'] = player['summonerName']
    player_stats['tier'] = player['tier']
    player_stats['division'] = player['rank']
    player_stats['leaguePoints'] = player['leaguePoints']
    player_stats['wins'] = player['wins']
    player_stats['losses'] = player['losses']
    player_stats['veteran'] = player['veteran']
    player_stats['freshBlood'] = player['freshBlood']
    player_stats['hotStreak'] = player['hotStreak']
    player_stats['summonerLevel'] = player['summonerLevel']
    
    return player_stats

def get_games_list(player):
    """
    calls the riot api to gather a list of player games 
    recieves a dictionary with player data
    returns same dic plus 'match_ids' list 
    """
    url_match_id= f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{player['puuid']}/ids?type=ranked&start=0&count=25&api_key={API_KEY}"
    player["match_ids"] = api_call(url_match_id)
    #player["match_ids"] = requests.get(url_match_id).json()
    return player
    
def api_call(url):
    """
    defensive programming to ensure api calls are working propperly
    takes an url
    returns a response json
    """
    response_riot = requests.get(f"{url}")

    while response_riot.status_code != 200:
        if response_riot.status_code == 429:
            print(f"{response_riot} {response_riot.headers['Retry-After']}")
            time.sleep(int(response_riot.headers['Retry-After']))
            response_riot = requests.get(f"{url}")
        
        if response_riot.status_code != 429 and response_riot.status_code != 200:
            print("BREAK!", url," ", response_riot)
            if response_riot.status_code == 404:
                return [] 
            elif response_riot.status_code == 403:
                raise ExpiredError
            else:
                with open(f'../data/trouble_players.json', 'a') as f:
                    json.dump(url,f)
                return []
    return response_riot.json()


def get_league(player_name):
    """
    calls the riot api to get 'puuid' and player level
    recieves a player name
    returns  dic with 'puuid' and player level
    """
    url_name = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={API_KEY}"
    player_id =  api_call(url_name)["id"]
    league_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_id}?api_key={API_KEY}"
    player = api_call(league_url)[0]

    return player
