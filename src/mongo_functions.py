import pandas as pd
import pickle
import json
import sys
sys.path.append('../')
from pymongo import MongoClient
client = MongoClient("localhost:27017")
db = client.get_database("LeagueRank")
c = db.get_collection("players")
g = db.get_collection("games")



def get_players():
    """
    brings all players from players mongo collection
    """
    players = list(c.find({},{"_id":0}))
    return players

def get_games(filtro,proj):
    """
    brings all games from games mongo collection
    takes a filter and a projection
    returns a list of games info
    """
    games = list(g.find(filtro,proj))
    return games