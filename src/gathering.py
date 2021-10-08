import requests 
import json
import os
import pandas as pd
#import tweepy
import time
import sys
sys.path.append('../')
from config import *
from src import functions as fn 
import pickle
from IPython.display import clear_output
from src import cleaning as cl




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
    """
    uses the players_list and calls the roit API for extra data and the game ids for the last 100 matches 
    takes a players_list containing item['summonerName'] 
    returns a list with extra info from those players whose data is available
    """
    players = []
    try:
        for ind,player in enumerate(players_list):
            if fn.get_puuid(player)== []:
                print(f"player {player['summonerName']} no longer exists")
                #players_list.remove(player)

            else:
                players.append(fn.get_games_list(fn.get_puuid(player)))
                #players.append(fn.get_games_list(player))
                #players_list[ind] = fn.usefull_info(player)
                
                if (ind+1)%10 == 0:
                    print(ind+1," players info fixed")
                    #with open(filename, "a") as f:
                        #json.dump(data,f)

        with open(f'../data/players.json', 'a') as f:
            json.dump(players,f)
        print("done")
    except:
        print(ind+1," players info fixed")
        with open(f'../data/trouble_players.json', 'a') as f:
            json.dump(players,f)


def get_player(name):
    """
    gets game data for a single player
    takes a name 
    returns player game stats
    """
    player = fn.get_league(name)
    player =fn.get_games_list(fn.get_puuid(player))
    player_stats=[]
    match_ids = player["match_ids"]
    for game in match_ids:
        url_match = f"https://europe.api.riotgames.com/lol/match/v5/matches/{game}?api_key={API_KEY}"
        match_detail = fn.api_call(url_match)

        game_stats={}
        game_stats['gameDuration']=match_detail["info"]["gameDuration"]
        game_stats['gameMode']=match_detail["info"]["gameMode"]
        game_stats['gameStartTimestamp']= (match_detail["info"]["gameStartTimestamp"])


        for player in match_detail["info"]["participants"]:
            if player['summonerName'] == name:
                for key,value in player.items():
                    game_stats[key]= value
        player_stats.append(game_stats)
    df = pd.DataFrame(player_stats)
    df.to_csv("./data/playerdata.csv",index=False)
    return df




def build_games(match_id_list,from_,to):
    """
    calls riot Api to gather game data for a list of game ids
    takes a list of game ids
    returns a json with those games data
    """

    games = []
    try:    
        for ind,match_id in enumerate(match_id_list[from_:to]):
            url_match = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
            match_detail = fn.api_call(url_match)
            if match_detail== []:
                    print(f"match {match_id} can no longer be accessed")

            else:
                games.append(match_detail)
                
                if (ind+1)%10 == 0:
                    clear_output(wait=True)
                    print(ind+1," games data gathered")
                    #with open(filename, "a") as f:
                        #json.dump(data,f)
                if (ind+1)%1000 == 0 or (ind+1)== len(match_id_list[from_:to]):
                    print(ind+1," games data saved")
                    with open(f'../games/games_{from_}-{to}.json', 'a') as f:
                        json.dump(games,f)
                    #with open(filename, "a") as f:
                        #json.dump(data,f)
                    games = []

        print("done")
            #with open("../data/trouble_games.txt", "wb") as fp:
                #pickle.dump(games,fp)
            
    except Exception:
        print(Exception)
        print(ind+1," players info fixed")
        #with open(f'../data/trouble_games.json', 'a') as f:
            #json.dump(games,f)

def player_resume(name):
    """
    creates the resume for a player
    takes a name
    returns a pd series
    """
    player = fn.get_league(name)
    player =fn.get_games_list(fn.get_puuid(player))
    averege_stats=[]
    player_stats_a= fn.usefull_info(player)
    player_stats = []
    match_ids = player["match_ids"]
    for game in match_ids:
        url_match = f"https://europe.api.riotgames.com/lol/match/v5/matches/{game}?api_key={API_KEY}"
        match_detail = fn.api_call(url_match)
        

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
    for key,value in chewed.items():
            player_stats_a[key]= value  
    averege_stats.append(player_stats_a)
    data_a = pd.DataFrame(averege_stats)
    data_a.to_csv("./data/plyerresume.csv",index=False)
    return data_a

