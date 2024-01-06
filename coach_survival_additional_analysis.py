# This script runs the aditional analysis on mid-season changes

# Importing required modules

import pandas as pd

# Project directory

direc = 'D:/coach_survival/'

# Reading in the data set

data = pd.read_csv(direc + 'data/data.csv')

# Look at events during the superbowl era (need to add a year to ID the previous coach)

dx = data[data.Year >= 1967].reset_index(drop = True)

# Identify the times a coach was fired mid-season

fired = []

for year in dx.Year.unique():
    
    tmpy = dx[dx.Year == year]
    
    for team in dx.Team.unique():
        
        tmp = tmpy[tmpy.Team == team]
        
        if len(tmp) > 1:
            
            fired.append([team,year])
            
# Finding the new coaches

new_coach = []

for x in fired:
    
    tmp = dx[dx.Team == x[0]]
    tmp2 = tmp[tmp.Year == x[1]-1]
    prev_coaches = list(tmp2.Coach)
    tmp3 = tmp[tmp.Year == x[1]]
    xxx = []
    
    for coach in tmp3.Coach:
        
        if coach not in prev_coaches:
            
            xxx.append(coach)
            
    if len(xxx) == 1:
        
        new_coach.append(xxx[0])
        
    else:
        
        new_coach.append(x)

# Below is a list of the lists of remaining issues

bugs = [['LAC', 1971], ['NYJ', 1976], ['NWE', 1978], ['SFO', 1978], ['ATL', 2007], ['NOR', 2012], ['JAX', 2021]]

# First None because the HC was suspended by the team but reinstated same season
# Second None because this was the year Sean Payton was suspended for Bountygate

better_tasting_bugs = ['Harland Svare', 'Mike Holovak', None, "Fred O'Connor", 'Emmitt Thomas', None, 'Darrell Bevell']

# Fixing the bugs

for bunny in range(len(bugs)):
    
    idx = new_coach.index(bugs[bunny])
    new_coach[idx] = better_tasting_bugs[bunny]

# Making a reference dataframe

teams = [f[0] for f in fired]
years = [f[1] for f in fired]

ref = pd.concat([pd.Series(teams, name = 'Team'), pd.Series(years, name = 'Year'), pd.Series(new_coach, name = 'Coach')], axis = 1)

# Drop Nones

ref = ref.dropna().reset_index(drop = True)

# Add data to ref

keeper = []
games = []
black = []
rooney = []
wp = []
prev_exp = []

for i in range(len(ref)):
    
    tmp = dx[dx.Team == ref.Team[i]]
    check = tmp[tmp.Year == ref.Year[i] + 1].reset_index(drop = True)
    tmp = tmp[tmp.Year == ref.Year[i]]
    tmp = tmp[tmp.Coach == ref.Coach[i]].reset_index(drop = True)
    tmp2 = dx[dx.Year < ref.Year[i]]
    tmp2 = tmp2[tmp2.Coach == ref.Coach[i]].reset_index(drop = True)
    
    keeper.append(int(ref.Coach[i] in list(check.Coach)))
    games.append(tmp.Games[0])
    black.append(tmp.Black[0])
    rooney.append(int(ref.Year[i] >= 2003))
    wp.append((tmp.Wins[0] + .5*tmp.Ties[0] ) / tmp.Games[0])
    prev_exp.append(len(tmp2))
    
games_bin = [int(g>=4) for g in games]
games_bin2 = [int(g>=8) for g in games]
prev_exp_bin = [int(p>0) for p in prev_exp]

keeper = pd.Series(keeper, name = 'Y')
games = pd.Series(games, name = 'Games')
games_bin = pd.Series(games_bin, name = 'Games4')
games_bin2 = pd.Series(games_bin2, name = 'Games8')
black = pd.Series(black, name = 'Black')
rooney = pd.Series(rooney, name = 'Rooney')
wp = pd.Series(wp, name = 'Win_Percentage')
prev_exp = pd.Series(prev_exp, name = 'Previous_Experience')
prev_exp_bin = pd.Series(prev_exp_bin, name = 'Any_Previous_Experience')
constant = pd.Series([1]*len(games), name = 'Constant')

ref = pd.concat([ref, keeper, constant, games, games_bin, games_bin2, black, rooney, wp, prev_exp, prev_exp_bin], axis = 1)

# Save this to file

ref.to_csv(direc + 'data/ref.csv', index = False)

