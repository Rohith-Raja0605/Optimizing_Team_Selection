import streamlit as st
import pandas as pd
import pickle
import importlib

my_module = importlib.import_module('Team_Selection')

st.set_page_config(
    page_title="IPL Team Selection",
    page_icon="https://bl-i.thgim.com/public/incoming/1ogk5e/article25940328.ece/alternates/FREE_1200/IPL-400x400jpg",
    layout="wide",
)

base="dark"
primaryColor="#3fe682"
backgroundColor="#000000"
secondaryBackgroundColor="#9055d6"
font="monospace"


original_title = '<h1 style="font-family: monospace; color:cyan; font-size: 60px;">IPL Team Selection </h1>'
st.markdown(original_title, unsafe_allow_html=True)
st.markdown(
    """
    ## Welcome to IPL Team Selection! Select your players and playing ground from the options below.
    """
)

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://wallpapercave.com/wp/wp7486102.jpg");
    background-size: 100vw 100vh; 
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)
batting_teams,all_rounders, bowling_teams, grounds = my_module.get_datas()

col1, col2,col3,col4= st.columns(4)

with col1:
    st.subheader('Select Batsman')
    batsman = st.multiselect('', sorted(batting_teams))
    selected_batters = list(batsman)


with col2:
    st.subheader('Select All Rounder')
    all_rounder = st.multiselect(' ', sorted(all_rounders))
    selected_allrounder = list(all_rounder)
    

with col3:
    st.subheader('Select Bowlers')
    bowler=st.multiselect('',sorted(bowling_teams))
    selected_bowler = list(bowler)

with col4:
        st.subheader('Select Stadium')
        ground = st.selectbox(' ', sorted(grounds))
if st.button("Result"):
    if len(selected_batters)+len(selected_allrounder)+len(selected_bowler) <15:
        st.write("Enter atleast 15 players in the squad")
    else:
        st.write("Playing Ground:", ground)
        selected_batters,selected_all_rounders,selected_bowlers = my_module.selection(selected_batters, selected_allrounder, selected_bowler, ground)
        selected_players = {
            "Batsmen": selected_batters,
            "All-Rounders": selected_all_rounders,
            "Bowlers": selected_bowlers
        }

        all_selected_players = []

        for players in selected_players.values():
            all_selected_players.extend(players)

        st.write("Selected Players:")
        st.write(pd.DataFrame(all_selected_players, columns=["Selected Players"]))







