from pymongo import MongoClient
client = MongoClient("localhost:27017")
db = client.get_database("LeagueRank")
c = db.get_collection("players")

