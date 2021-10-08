import requests 
import json
import os
from pandas import json_normalize
#import tweepy
import time
from datetime import datetime

import pandas as pd
#import tweepy
import sys
sys.path.append('../')
import os
from src import functions as fn 
from datetime import time

# standar data for cleaning (first iteration)
interesting_columns = ['role','gameStartTimestamp','assists','champExperience','championName','damageDealtToBuildings',
'damageDealtToObjectives','damageDealtToTurrets','damageSelfMitigated','deaths','firstBloodAssist',
'firstBloodKill','goldEarned','kills','timeCCingOthers','timePlayed',
'totalDamageDealt','totalDamageDealtToChampions','totalMinionsKilled','totalTimeSpentDead',
'visionScore','win']
time_cols = ["assists","champExperience","damageDealtToBuildings","damageDealtToObjectives",
"damageSelfMitigated","deaths","goldEarned","kills","timeCCingOthers","totalDamageDealt",
"totalDamageDealtToChampions","totalMinionsKilled","totalTimeSpentDead","visionScore"]
count_cols = ["gameStartTimestamp","championName"]
percent_cols = ["firstBloodAssist","firstBloodKill","win","timePlayed"]
d = {24: 'DIAMONDI', 23: 'DIAMONDII', 22: 'DIAMONDIII', 21: 'DIAMONDIV', 20: 'PLATINUMI',
 19: 'PLATINUMII', 18: 'PLATINUMIII', 12: 'SILVERI', 11: 'SILVERII', 10: 'SILVERIII',
 9: 'SILVERIV', 8: 'BRONZEI', 7: 'BRONZEII', 6: 'BRONZEIII', 5: 'BRONZEIV', 4: 'IRONI',
 3: 'IRONII', 2: 'IRONIII', 15: 'GOLDII', 14: 'GOLDIII', 13: 'GOLDIV', 1: 'IRONIV',
 27: 'CHALLENGERI', 26: 'GRANDMASTERI', 25: 'MASTERI', 17: 'PLATINUMIV', 16: 'GOLDI'}

def chew_data(dfr):
    """
    recieves a dataframe
    returns a dictionary with the averaged or most common values for some key data
    """
    resume = {}

    dfr.gameStartTimestamp = dfr.gameStartTimestamp.apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%H"))
    
    try:
        dfr.timePlayed = dfr.timePlayed.apply(lambda x: x/60)
        dfr_f = dfr[dfr.role == dfr.role.value_counts().index[0]]
        resume['role'] = dfr.role.value_counts().index[0]
        dfr_fr = dfr_f[interesting_columns]
        dfr_fr.drop_duplicates(inplace=True)
    except:
        return []
    


    for col in time_cols:
        dfr_fr[col] = dfr_fr[col]/dfr_fr["timePlayed"]
    for col in time_cols:
        resume[col] = dfr_fr[col].median()
    for col in count_cols:
        resume[col] = dfr_fr[col].value_counts().index[0]
        [0]
    for col in percent_cols:
        resume[col] = dfr_fr[col].sum()/len(dfr_fr[col])
    return resume


def duration(mili):
    """
    translates a timestamp in miliseconds to datetime HH:mm:ss
    """
    mili = int(mili/1000)
    sec = mili % 60; mili = mili//60
    minutes = mili % 60; mili = mili//60
    h = mili
    #time_ = (h,minutes,sec)
    date_time = time(h,minutes,sec)
    date_time = date_time.strftime("%H:%M:%S")
    return date_time