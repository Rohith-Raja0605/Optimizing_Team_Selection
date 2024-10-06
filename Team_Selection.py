import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle
def get_datas():
    #Loading matches.csv
    matches = pd.read_csv('Datasets\\matches.csv')
    
    #Loading ball_by_ball.csv
    ball_by_ball = pd.read_csv('Datasets\\ball_by_ball.csv')
    
    #Loading stadium.csv
    stadiums = pd.read_csv('Datasets\\stadium.csv')
    
    #Getting batters name
    batters = ball_by_ball['batter']
    batters = batters.unique()
    
    #Getting bowlers name
    bowlers = ball_by_ball['bowler']
    bowlers = bowlers.unique()
    
    matchid = matches['ID']
    
    season = matches['Season']
    season = season.unique()
    
    matches_per_season = {}
    matches = matches.values.tolist()
    for i in season:
      l = []
      for j in matches:
        if i in j:
          l.append(j[0])
      matches_per_season[i] = l
    
    batter_season = {}
    balls_list = ball_by_ball.values.tolist()
    matches_season = matches_per_season.items()
    
    for i in balls_list:
      for j in matches_season:
        if i[0] in j[1]:
          if i[4]  not in batter_season:
            batter_season[i[4]] = [j[0],]
          elif j[0] not in batter_season[i[4]]:
            batter_season[i[4]].append(j[0])
    
    bowler_season = {}
    balls_list = ball_by_ball.values.tolist()
    matches_season = matches_per_season.items()
    
    for i in balls_list:
      for j in matches_season:
        if i[0] in j[1]:
          if i[5]  not in bowler_season:
            bowler_season[i[5]] = [j[0],]
          elif j[0] not in bowler_season[i[5]]:
            bowler_season[i[5]].append(j[0])
    batters_available = batter_season.copy()
    for i in batter_season:
      if '2022' not in batter_season[i]:
        del batters_available[i]
    
    bowlers_available = bowler_season.copy()
    for i in bowler_season:
      if '2022' not in bowler_season[i]:
        del bowlers_available[i]
        
        
    allrounders_available = []
    batters_available = list(batters_available.keys())
    bowlers_available = list(bowlers_available.keys())
    all_rounders_available = ['Rashid Khan', 'HH Pandya','R Ashwin','GJ Maxwell','Shahbaz Ahmed','Washington Sundar',
                              'AR Patel','MJ Santner','S Dube','DJ Hooda','R Powell','V Shankar','Tilak Varma','R Parag','DJ Mitchell',
                              'Shashank Singh','AK Markram', 'RA Jadeja', 'R Tewatia','VR Iyer','MP Stoinis','A Badoni','Abhishek Sharma','AD Russell', 'N Rana','SP Narine']
    
    for i in all_rounders_available:
        if i in batters_available:
            batters_available.pop(batters_available.index(i))
        if i in bowlers_available:
            bowlers_available.pop(bowlers_available.index(i))
    matches = pd.read_csv('Datasets\\matches.csv')
    
    stadium = {}
    for i in stadiums['Stadium']:
        stadium[i]=[]
    for i in matches['ID']:
        stadium[str(matches['Venue'][matches['ID']==i].values[0])].append(i)
    
    sorted_stadium = []
    for i in stadium.keys():
        for j in stadium[i]:
            if i not in sorted_stadium:
                if (1136561<= j <= 1136620) or (1304047<=j<=1312200):
                    sorted_stadium.append(i)
             
    return (batters_available,all_rounders_available, bowlers_available, list(sorted_stadium))
    
def selection(batters,allrounders,bowlers,stadium):
    #Player Classification
    playing_11 = pd.DataFrame()
    playing_11['player'] = None
    playing_11['stadium'] = None
    playing_11['balls_faced'] = None
    playing_11['runs_scored'] = None
    playing_11['dismissals'] = None
    playing_11['batting_strike_rate'] = None
    playing_11['batting_average'] = None
    playing_11['balls_bowled'] = None
    playing_11['runs_given'] = None
    playing_11['wickets_taken'] = None
    playing_11['bowling_economy_rate'] = None
    playing_11['bowling_strike_rate'] = None
    playing_11['category'] = None
    playing_11['label'] = None
    
    def player_label(player, std, category):
        ball_by_ball = pd.read_csv('Datasets\\ball_by_ball.csv')
        stadiums = pd.read_csv('Datasets\\stadium.csv')
        # Filter ball_by_ball DataFrame for the given player and stadium
        player_matches = ball_by_ball[ball_by_ball['batter'] == player]
        bowler_matches = ball_by_ball[ball_by_ball['bowler'] == player]
    
        player_stadium_matches = player_matches[player_matches['ID'].isin(stadiums['Stadium'])]
        bowler_stadium_matches = bowler_matches[bowler_matches['ID'].isin(stadiums['Stadium'])]
    
        # Calculate batting statistics
        balls_faced = player_stadium_matches.shape[0]
        runs_scored = player_stadium_matches['batsman_run'].sum()
        dismissals = player_stadium_matches['isWicketDelivery'].sum()
        batting_strike_rate = (runs_scored / balls_faced) * 100 if balls_faced > 0 else 0
        batting_average = (runs_scored / dismissals) if dismissals > 0 else 0
    
        # Calculate bowling statistics
        balls_bowled = bowler_stadium_matches.shape[0]
        runs_given = bowler_stadium_matches['batsman_run'].sum()
        wickets_taken = bowler_stadium_matches['isWicketDelivery'].sum()
        bowling_economy_rate = (runs_given / (balls_bowled / 6)) if balls_bowled > 0 else 0
        bowling_strike_rate = (balls_bowled / wickets_taken) if wickets_taken > 0 else balls_bowled
    
        # Assign label based on thresholds
        if (batting_strike_rate >= 150 or batting_average >= 50) or (0 < bowling_economy_rate <= 6):
            label = 'Good'
        elif (100 <= batting_strike_rate < 150) or (30 <= batting_average < 50) or (7 <= bowling_economy_rate <= 10):
            label = 'Average'
        else:
            label = 'Poor'
    
        playing_11.loc[len(playing_11.index)] = {
        'player': player,
        'stadium': std,
        'balls_faced': balls_faced,
        'runs_scored': runs_scored,
        'dismissals': dismissals,
        'batting_strike_rate': batting_strike_rate,
        'batting_average': batting_average,
        'balls_bowled': balls_bowled,
        'runs_given': runs_given,
        'wickets_taken': wickets_taken,
        'bowling_economy_rate': bowling_economy_rate,
        'bowling_strike_rate': bowling_strike_rate,
        'label': label, 'category':category
        }
    std = stadium
    batter = batters
    all_rounders = allrounders
    bowler = bowlers
    for i in batters+bowlers+all_rounders:
        if i in batter:
            player_label(i,std,'Batters')
        elif i in all_rounders:
            player_label(i,std,'All Rounder')
        else:
            player_label(i,std,'Bowler')
    
    
    #Plotting Tree
    '''
    X = playing_11.drop(columns=['player', 'stadium','label','category'])
    y = playing_11['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    plt.figure(figsize=(20,10))
    tree.plot_tree(clf, feature_names=X.columns, class_names=clf.classes_, filled=True)
    plt.show()
    '''
    
    X = playing_11.drop(columns=['player', 'stadium', 'label', 'category'])
    y = playing_11['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    
    selected_batters = playing_11[playing_11['category'] == 'Batters'].nlargest(5, 'batting_average')
    selected_all_rounders = playing_11[playing_11['category'] == 'All Rounder'].nlargest(2, 'batting_average')
    selected_bowlers = playing_11[playing_11['category'] == 'Bowler'].nlargest(4, 'bowling_strike_rate')
    
    return selected_batters['player'],selected_all_rounders['player'],selected_bowlers['player']
