import streamlit as st
from PIL import Image
import pandas as pd
from src import gathering as ga
from src import cleaning as cl
import pickle


with open("./data/decisiontree1.pkl", "rb") as f:
    model=pickle.load(f)
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWY3rFJXeH8ya-hGFqD_ZfV6tjLdqnHt4zXw&usqp=CAU",
width=400)

st.write ("""
# League Rank
""")

st.write('''In this platform you will be able to check your most recent stats and get a rank estimation 
comparing your stats with other players accross ranks''')

left_column,mid_column, right_column = st.columns(3)
with left_column:

    st.write(""" 
    ### Summoner Name:""")
    name = st.text_input('Enter your summoner name')
if st.button('search'):
    df = ga.get_player(name)
    st.write(""" 
    ### Your games:""")
    df = df[cl.interesting_columns]
    st.dataframe(df)
    dfr = ga.player_resume(name)#.iloc[0]
    st.write(""" 
    ### Average values by minute and accross  your games:""")
    st.dataframe(dfr)
    dfr["rank"] = dfr.tier + dfr.division
    with mid_column:
        st.write(""" 
    ### Your Rank """)
        st.write(dfr["rank"])
    dfr["win_r"]= dfr.wins/(dfr.wins + dfr.losses)
    y_r = dfr["rank"]
    dfr = dfr.drop(["summonerName","tier","division","championName","rank"],axis=1)

    
    columns = ['leaguePoints', 'wins', 'losses', 'veteran', 'freshBlood', 'hotStreak',
       'summonerLevel', 'assists', 'champExperience', 'damageDealtToBuildings',
       'damageDealtToObjectives', 'damageSelfMitigated', 'deaths',
       'goldEarned', 'kills', 'timeCCingOthers', 'totalDamageDealt',
       'totalDamageDealtToChampions', 'totalMinionsKilled',
       'totalTimeSpentDead', 'visionScore', 'gameStartTimestamp',
       'firstBloodAssist', 'firstBloodKill', 'win', 'timePlayed', 'win_r',
       'role_CARRY', 'role_DUO', 'role_NONE', 'role_SOLO', 'role_SUPPORT']
    roles = ['CARRY', 'DUO', 'NONE', 'SOLO', 'SUPPORT']

    for r in roles:
        print(r)
        if dfr["role"][0] == r:
            dfr[f"role_{r}"] = 1
        else:
            dfr[f"role_{r}"] = 0
    dfr =dfr.drop("role",axis=1)
    pred= model.predict(dfr)
    
    with right_column:
        st.write(""" 
    ### Your Rank potencial""")
        st.write(str(cl.d[int(round(pred[0],0))]))

st.write(""" 
### Average values by minute and accross games for all ranks:""")
hu = pd.read_csv("./data/dataframe2.csv")
st.dataframe(hu)



