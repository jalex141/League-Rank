from getpass import getpass

from riotwatcher import LolWatcher, ApiError
API_KEY = getpass("input your api key:  ")

watcher = LolWatcher(API_KEY)


#form url for API call
base = "api.riotgames.com/lol/"
endpoints = [""]
queue = "RANKED_SOLO_5x5"
tier = ["CHALLENGER", "GRANDMASTER","MASTER", "DIAMOND", "PLATINUM", "GOLD", "SILVER","BRONZE", "IRON"]
division = ["I", "II", "III", "IV"]
platform = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ru","tr1"]
region = ["europe","asia","americas"]
my_region = 'euw1'
