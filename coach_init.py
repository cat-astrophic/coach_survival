# This script runs the initial conditions analysis

# Importing required modules

import pandas as pd
import numpy as np
import scipy.stats

# Project directory

direc = 'D:/coach_survival/'

# Reading in the data set

data = pd.read_csv(direc + 'data/data.csv')

# Filter for first year observations

xxx = data[data.TeamTenure == 1].reset_index(drop = True)

# Filter for same time period as rest of study

xxx = xxx[xxx.Year >= 1966].reset_index(drop = True)

# Omit any mid-season changes

xxx = xxx[xxx.PctCoached == 1].reset_index(drop = True)

# Add a new column for reference to each df

xxx = pd.concat([xxx, pd.Series([xxx.Team[i] + str(xxx.Year[i]-1) for i in range(len(xxx))], name = 'REF')], axis = 1)
data = pd.concat([data, pd.Series([data.Team[i] + str(data.Year[i]) for i in range(len(data))], name = 'REF')], axis = 1)

# Get the previous year performance data for each first year coach

xWinPct = []
xSRS = []
xOSRS = []
xDSRS = []
xPlayoffs = []
xPlayoffWinPct = []
xBlack = []

for i in range(len(xxx)):
    
    print(i)
    
    tmp = data[data.REF == xxx.REF[i]].reset_index(drop = True)
    
    if len(tmp) == 0:
        
        continue
        
    else:
        
        xWinPct.append(tmp.WinPct[0])
        xSRS.append(tmp.SRS[0])
        xOSRS.append(tmp.OSRS[0])
        xDSRS.append(tmp.DSRS[0])
        xPlayoffs.append(int(tmp.PlayoffGames[0] > 0))
        xPlayoffWinPct.append(tmp.PlayoffWinPct[0])
        xBlack.append(xxx.Black[i])

# Computing differences

black_ids = [i for i in range(len(xBlack)) if xBlack[i] == 1]
white_ids = [i for i in range(len(xBlack)) if xBlack[i] == 0]

mean_WP_1 = np.mean([xWinPct[i] for i in black_ids])
mean_WP_0 = np.mean([xWinPct[i] for i in white_ids])
t_WP, p_WP = scipy.stats.ttest_ind([xWinPct[i] for i in black_ids], [xWinPct[i] for i in white_ids])

mean_SRS_1 = np.mean([xSRS[i] for i in black_ids])
mean_SRS_0 = np.mean([xSRS[i] for i in white_ids])
t_SRS, p_SRS = scipy.stats.ttest_ind([xSRS[i] for i in black_ids], [xSRS[i] for i in white_ids])

mean_OSRS_1 = np.mean([xOSRS[i] for i in black_ids])
mean_OSRS_0 = np.mean([xOSRS[i] for i in white_ids])
t_OSRS, p_OSRS = scipy.stats.ttest_ind([xOSRS[i] for i in black_ids], [xOSRS[i] for i in white_ids])

mean_DSRS_1 = np.mean([xDSRS[i] for i in black_ids])
mean_DSRS_0 = np.mean([xDSRS[i] for i in white_ids])
t_DSRS, p_DSRS = scipy.stats.ttest_ind([xDSRS[i] for i in black_ids], [xDSRS[i] for i in white_ids])

mean_Play_1 = np.mean([xPlayoffs[i] for i in black_ids])
mean_Play_0 = np.mean([xPlayoffs[i] for i in white_ids])
t_P, p_P = scipy.stats.ttest_ind([xPlayoffs[i] for i in black_ids], [xPlayoffs[i] for i in white_ids])

mean_PWP_1 = np.mean([xPlayoffWinPct[i] for i in black_ids])
mean_PWP_0 = np.mean([xPlayoffWinPct[i] for i in white_ids])
t_PWP, p_PWP = scipy.stats.ttest_ind([xPlayoffWinPct[i] for i in black_ids], [xPlayoffWinPct[i] for i in white_ids])

# Saving results

c_WP = pd.Series([mean_WP_1, mean_WP_0, t_WP, p_WP], name = 'WinPct')
c_SRS = pd.Series([mean_SRS_1, mean_SRS_0, t_SRS, p_SRS], name = 'SRS')
c_OSRS = pd.Series([mean_OSRS_1, mean_OSRS_0, t_OSRS, p_OSRS], name = 'OSRS')
c_DSRS = pd.Series([mean_DSRS_1, mean_DSRS_0, t_DSRS, p_DSRS], name = 'DSRS')
c_P = pd.Series([mean_Play_1, mean_Play_0, t_P, p_P], name = 'Playoffs')
c_PWP = pd.Series([mean_PWP_1, mean_PWP_0, t_PWP, p_PWP], name = 'PlayoffWinPct')

res = pd.concat([c_WP, c_SRS, c_OSRS, c_DSRS, c_P, c_PWP], axis = 1)
res.to_csv(direc + 'results/init_conditions.csv', index = False)

