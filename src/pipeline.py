import os
import sys
sys.path.append('../')
from src import gathering as ga
import json

#ga.get_list()
with open('data.txt') as json_file:
    data = json.load(json_file)
ga.build_list()