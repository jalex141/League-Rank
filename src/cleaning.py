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
'firstBloodKill','goldEarned','inhibitorTakedowns','kills','timeCCingOthers','timePlayed',
'totalDamageDealt','totalDamageDealtToChampions','totalMinionsKilled','totalTimeSpentDead',
'visionScore','win']
time_cols = ["assists","champExperience","damageDealtToBuildings","damageDealtToObjectives",
"damageSelfMitigated","deaths","goldEarned","kills","timeCCingOthers","totalDamageDealt",
"totalDamageDealtToChampions","totalMinionsKilled","totalTimeSpentDead","visionScore"]
count_cols = ["gameStartTimestamp","championName"]
percent_cols = ["firstBloodAssist","firstBloodKill","inhibitorTakedowns","win"]


def chew_data(dfr):
    """
    recieves a dataframe
    returns a dictionary with the averaged or most common values for some key data
    """
    dfr.gameStartTimestamp = dfr.gameStartTimestamp.apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%H"))
    dfr.gameDuration = dfr.gameDuration.apply(duration)
    dfr.timePlayed = dfr.timePlayed.apply(lambda x: x/60)
    dfr_f = dfr[dfr.role == dfr.role.value_counts().index[0]]
    dfr_fr = dfr_f[interesting_columns]

    for col in time_cols:
        dfr_fr[col] = dfr_fr[col]/dfr_fr.timePlayed
    resume = {}
    for col in time_cols:
        resume[col] = dfr_fr[col].median()
    for col in count_cols:
        resume[col] = dfr_fr[col].value_counts().index[0]
        [0]
    for col in percent_cols:
        resume[col] = dfr_fr[col].sum()/len(dfr_fr[col])
    resume["timePlayed"] = dfr_fr.timePlayed.sum()/len(dfr_fr[col])
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