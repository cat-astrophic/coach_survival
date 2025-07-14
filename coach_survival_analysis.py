# This script runs the survival analysis

# Importing required modules

import numpy as np
import pandas as pd
import scipy
from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter
from lifelines import WeibullAFTFitter

# Project directory

direc = 'D/:coach_survival/'

# Reading in the data set

data = pd.read_csv(direc + 'data/data.csv')

# Look at events during the superbowl era

dx = data[data.Year >= 1966].reset_index(drop = True)

# Create final data set with coach-team level observations with all coaches

ids = [dx.Coach[i] + '-' + dx.Team[i] for i in range(len(dx))]
dx = pd.concat([dx, pd.Series(ids, name = 'id')], axis = 1)
dh = dx[~dx.Coach.isin(['Ron Rivera', 'Tom Flores', 'Tom Fears'])].reset_index(drop = True)

ages = []
wins = []
losses = []
ties = []
wpct = []
srs = []
osrs = []
dsrs = []
pwins = []
plosses = []
pwpct = []
sbs = []
papps = []
divplace = []
divwins = []
divwinpct = []
clen = []
tt = []
event = []
black = []
s1 = []
s2 = []
s5 = []
drought = []
fywins = []
fywpct = []
fypwpct = []
fydev = []
rooney1 = []
rooney2 = []

for c in list(dx.id.unique()):
    
    tmp = dx[dx.id == c].reset_index(drop = True)
    ages.append(max(tmp.Age))
    wins.append(sum(tmp.Wins))
    losses.append(sum(tmp.Losses))
    ties.append(sum(tmp.Ties))
    wpct.append(sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    games = tmp.Wins + tmp.Losses + tmp.Ties
    srs.append(np.dot(games,tmp.SRS) / sum(games))
    osrs.append(np.dot(games,tmp.OSRS) / sum(games))
    dsrs.append(np.dot(games,tmp.DSRS) / sum(games))
    pwins.append(sum(tmp.PlayoffWins))
    plosses.append(sum(tmp.PlayoffLosses))
    
    if max(sum(tmp.PlayoffWins), sum(tmp.PlayoffLosses)) > 0:
        
        pwpct.append(sum(tmp.PlayoffWins) / (sum(tmp.PlayoffWins) + sum(tmp.PlayoffLosses)))
        
    else:
        
        pwpct.append(0)
    
    sbs.append(len([x for x in tmp.PlayoffWinPct if x >= 1]))
    papps.append(len([i for i in range(len(tmp)) if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0]))
    divplace.append(np.mean(tmp.DivPlace))
    divwins.append(len([x for x in tmp.DivPlace if x == 1]))
    divwinpct.append(len([x for x in tmp.DivPlace if x == 1]) / max(tmp.TeamTenure))
    clen.append(max(tmp.CareerLength))
    tt.append(max(tmp.TeamTenure))
    event.append(max(tmp.Event))
    black.append(max(tmp.Black))
    
    m = max(tmp.Year)
    m2 = min(tmp.Year)
    tmp1 = tmp[tmp.Year == m]
    tmp2 = tmp[tmp.Year >= m-1]
    tmp5 = tmp[tmp.Year >= m-4]
    s1.append(len([x for x in tmp1.PlayoffWinPct if x == 1]))
    s2.append(len([x for x in tmp2.PlayoffWinPct if x == 1]))
    s5.append(len([x for x in tmp5.PlayoffWinPct if x == 1]))
    
    app = [1 if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0 else 0 for i in range(len(tmp))]
    tmp = pd.concat([tmp, pd.Series(app, name = 'PApp')], axis = 1)
    tmpapp = tmp[tmp.PApp == 1]
    
    try:
        
        m2 = max(tmpapp.Year)
        drought.append(m-m2)
        
    except:
        
        drought.append(len(tmp)-1)
        
    fywins.append(max(tmp1.Wins))
    fywpct.append(max(tmp1.WinPct))
    fypwpct.append(max(tmp1.PlayoffWinPct))
    fydev.append(max(tmp1.WinPct) - sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    rooney1.append(int(m > 2003))
    rooney2.append(int(m2 > 2003))

sbsbin = pd.Series([1 if s > 0 else 0 for s in sbs], name = 'Super Bowl Champion')    
ages = pd.Series(ages, name = 'Age')
ages2 = pd.Series([a*a for a in list(ages)], name = 'Age2')
wins = pd.Series(wins, name = 'Wins')
losses = pd.Series(losses, name = 'Losses')
ties = pd.Series(ties, name = 'Ties')
wpct = pd.Series(wpct, name = 'Win Pct')
srs = pd.Series(srs, name = 'SRS')
osrs = pd.Series(osrs, name = 'OSRS')
dsrs = pd.Series(dsrs, name = 'DSRS')
pwins = pd.Series(pwins, name = 'Playoff Wins')
plosses = pd.Series(plosses, name = 'Playoff Losses')
pwpct = pd.Series(pwpct, name = 'Playoff Win Pct')
sbs = pd.Series(sbs, name = 'Super Bowl Wins')
papps = pd.Series(papps, name = 'Playoff Appearances')
divplace = pd.Series(divplace, name = 'Division Place')
divwins = pd.Series(divwins, name = 'Division Wins')
divwinpct = pd.Series(divwinpct, name = 'Division Win Pct')
clen = pd.Series(clen, name = 'Experience')
tt = pd.Series(tt, name = 'Duration')
event = pd.Series(event, name = 'Event')
black = pd.Series(black, name = 'Black')
s1 = pd.Series(s1, name = 'SB Past Year')
s2 = pd.Series(s2, name = 'SB Past 2 Years')
s5 = pd.Series(s5, name = 'SB Past 5 Years')
drought = pd.Series(drought, name = 'Playoff Drought')
fywins = pd.Series(fywins, name = 'FY Wins') # Create same data set with hispanic coaches removed
fywpct = pd.Series(fywpct, name = 'FY Win Pct')
fypwpct = pd.Series(fypwpct, name = 'FY Playoff Win Pct')
fydev = pd.Series(fydev, name = 'FY Win Pct Change')
be = pd.Series([black[x]*clen[x] for x in range(len(black))], name = 'Black x Experience')
rooney = pd.Series(rooney1, name = 'Rooney')
rooney2 = pd.Series(rooney2, name = 'Rooney')
rxb = pd.Series([black[x]*rooney[x] for x in range(len(black))], name = 'Black x Rooney')
rxb2 = pd.Series([black[x]*rooney2[x] for x in range(len(black))], name = 'Black x Rooney')

surv = pd.concat([event, tt, clen, black, divwins, papps, pwpct, wpct, osrs, dsrs, sbsbin, be, rooney, rxb], axis = 1)
surv0 = surv[surv['Super Bowl Champion'] == 0].reset_index(drop = True)
surv0 = surv0.drop(['Super Bowl Champion'], axis = 1)

# Repeat with hispanic coaches removed

ages = []
wins = []
losses = []
ties = []
wpct = []
srs = []
osrs = []
dsrs = []
pwins = []
plosses = []
pwpct = []
sbs = []
papps = []
divplace = []
divwins = []
divwinpct = []
clen = []
tt = []
event = []
black = []
s1 = []
s2 = []
s5 = []
drought = []
fywins = []
fywpct = []
fypwpct = []
fydev = []
rooney1 = []
rooney2 = []

for c in list(dh.id.unique()):
    
    tmp = dh[dh.id == c].reset_index(drop = True)
    ages.append(max(tmp.Age))
    wins.append(sum(tmp.Wins))
    losses.append(sum(tmp.Losses))
    ties.append(sum(tmp.Ties))
    wpct.append(sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    games = tmp.Wins + tmp.Losses + tmp.Ties
    srs.append(np.dot(games,tmp.SRS) / sum(games))
    osrs.append(np.dot(games,tmp.OSRS) / sum(games))
    dsrs.append(np.dot(games,tmp.DSRS) / sum(games))
    pwins.append(sum(tmp.PlayoffWins))
    plosses.append(sum(tmp.PlayoffLosses))
    
    if max(sum(tmp.PlayoffWins), sum(tmp.PlayoffLosses)) > 0:
        
        pwpct.append(sum(tmp.PlayoffWins) / (sum(tmp.PlayoffWins) + sum(tmp.PlayoffLosses)))
        
    else:
        
        pwpct.append(0)
    
    sbs.append(len([x for x in tmp.PlayoffWinPct if x >= 1]))
    papps.append(len([i for i in range(len(tmp)) if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0]))
    divplace.append(np.mean(tmp.DivPlace))
    divwins.append(len([x for x in tmp.DivPlace if x == 1]))
    divwinpct.append(len([x for x in tmp.DivPlace if x == 1]) / max(tmp.TeamTenure))
    clen.append(max(tmp.CareerLength))
    tt.append(max(tmp.TeamTenure))
    event.append(max(tmp.Event))
    black.append(max(tmp.Black))
    
    m = max(tmp.Year)
    m2 = min(tmp.Year)
    tmp1 = tmp[tmp.Year == m]
    tmp2 = tmp[tmp.Year >= m-1]
    tmp5 = tmp[tmp.Year >= m-4]
    s1.append(len([x for x in tmp1.PlayoffWinPct if x == 1]))
    s2.append(len([x for x in tmp2.PlayoffWinPct if x == 1]))
    s5.append(len([x for x in tmp5.PlayoffWinPct if x == 1]))
    
    app = [1 if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0 else 0 for i in range(len(tmp))]
    tmp = pd.concat([tmp, pd.Series(app, name = 'PApp')], axis = 1)
    tmpapp = tmp[tmp.PApp == 1]
    
    try:
        
        m2 = max(tmpapp.Year)
        drought.append(m-m2)
        
    except:
        
        drought.append(len(tmp)-1)
        
    fywins.append(max(tmp1.Wins))
    fywpct.append(max(tmp1.WinPct))
    fypwpct.append(max(tmp1.PlayoffWinPct))
    fydev.append(max(tmp1.WinPct) - sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    rooney1.append(int(m > 2003))
    rooney2.append(int(m2 > 2003))

sbsbin = pd.Series([1 if s > 0 else 0 for s in sbs], name = 'Super Bowl Champion')    
ages = pd.Series(ages, name = 'Age')
ages2 = pd.Series([a*a for a in list(ages)], name = 'Age2')
wins = pd.Series(wins, name = 'Wins')
losses = pd.Series(losses, name = 'Losses')
ties = pd.Series(ties, name = 'Ties')
wpct = pd.Series(wpct, name = 'Win Pct')
srs = pd.Series(srs, name = 'SRS')
osrs = pd.Series(osrs, name = 'OSRS')
dsrs = pd.Series(dsrs, name = 'DSRS')
pwins = pd.Series(pwins, name = 'Playoff Wins')
plosses = pd.Series(plosses, name = 'Playoff Losses')
pwpct = pd.Series(pwpct, name = 'Playoff Win Pct')
sbs = pd.Series(sbs, name = 'Super Bowl Wins')
papps = pd.Series(papps, name = 'Playoff Appearances')
divplace = pd.Series(divplace, name = 'Division Place')
divwins = pd.Series(divwins, name = 'Division Wins')
divwinpct = pd.Series(divwinpct, name = 'Division Win Pct')
clen = pd.Series(clen, name = 'Experience')
tt = pd.Series(tt, name = 'Duration')
event = pd.Series(event, name = 'Event')
black = pd.Series(black, name = 'Black')
s1 = pd.Series(s1, name = 'SB Past Year')
s2 = pd.Series(s2, name = 'SB Past 2 Years')
s5 = pd.Series(s5, name = 'SB Past 5 Years')
drought = pd.Series(drought, name = 'Playoff Drought')
fywins = pd.Series(fywins, name = 'FY Wins')
fywpct = pd.Series(fywpct, name = 'FY Win Pct')
fypwpct = pd.Series(fypwpct, name = 'FY Playoff Win Pct')
fydev = pd.Series(fydev, name = 'FY Win Pct Change')
be = pd.Series([black[x]*clen[x] for x in range(len(black))], name = 'Black x Experience')
rooney = pd.Series(rooney1, name = 'Rooney')
rooney2 = pd.Series(rooney2, name = 'Rooney')
rxb = pd.Series([black[x]*rooney[x] for x in range(len(black))], name = 'Black x Rooney')
rxb2 = pd.Series([black[x]*rooney2[x] for x in range(len(black))], name = 'Black x Rooney')

survh = pd.concat([event, tt, clen, black, divwins, papps, pwpct, wpct, osrs, dsrs, sbsbin, be, rooney, rxb], axis = 1)
survh0 = survh[survh['Super Bowl Champion'] == 0].reset_index(drop = True)
survh0 = survh0.drop(['Super Bowl Champion'], axis = 1)

# Run the hazard model

cph = CoxPHFitter()
cph.fit(surv, 'Duration', event_col = 'Event')

# View results

cph.print_summary(decimals = 3)
cph.plot()

# Run the hazard model now with Hispanic coaches dropped

cphh = CoxPHFitter()
cphh.fit(survh, 'Duration', event_col = 'Event')

# View results

cphh.print_summary(decimals = 3)
cphh.plot()

# Creating a results table

m_vars = list(cph.summary.index)
m_rats = list(cph.hazard_ratios_)
m_coef = list(cph.params_)
m_serr = list(cph.standard_errors_)
m_t = [m_coef[i] / m_serr[i] for i in range(len(m_coef))]
m_p = [scipy.stats.t.sf(abs(m_t[i]),11) for i in range(len(m_coef))]

mh_vars = list(cphh.summary.index)
mh_rats = list(cphh.hazard_ratios_)
mh_coef = list(cphh.params_)
mh_serr = list(cphh.standard_errors_)
mh_t = [mh_coef[i] / mh_serr[i] for i in range(len(mh_coef))]
mh_p = [scipy.stats.t.sf(abs(mh_t[i]),11) for i in range(len(mh_coef))]

# Some plots

view = surv.groupby('Black').mean()
view.reset_index(inplace = True)
plot = cph.predict_survival_function(view).plot()

xxx = survh0[survh0.Duration <= 10]
xx = survh0[survh0.Duration <= 5]
T = xxx['Duration']
E = xxx['Event']
groups = xxx['Black']
ix = (groups == 1)
kmf = KaplanMeierFitter()
kmf.fit(T[~ix], E[~ix], label = 'White')
ax = kmf.plot_survival_function()
kmf.fit(T[ix], E[ix], label = 'Black')
ax = kmf.plot_survival_function(ax = ax)

frog = cphh.fit(xx, 'Duration', event_col = 'Event')
frog.plot_partial_effects_on_outcome('Black', values = np.arange(1, 2), cmap = 'coolwarm')

# Repeating over 1989 on

dx = data[data.Year >= 1989].reset_index(drop = True)

# Create final data set with coach-team level observations with all coaches

ids = [dx.Coach[i] + '-' + dx.Team[i] for i in range(len(dx))]
dx = pd.concat([dx, pd.Series(ids, name = 'id')], axis = 1)
dh = dx[~dx.Coach.isin(['Ron Rivera', 'Tom Flores', 'Tom Fears'])].reset_index(drop = True)

ages = []
wins = []
losses = []
ties = []
wpct = []
srs = []
osrs = []
dsrs = []
pwins = []
plosses = []
pwpct = []
sbs = []
papps = []
divplace = []
divwins = []
divwinpct = []
clen = []
tt = []
event = []
black = []
s1 = []
s2 = []
s5 = []
drought = []
fywins = []
fywpct = []
fypwpct = []
fydev = []
rooney1 = []
rooney2 = []

for c in list(dx.id.unique()):
    
    tmp = dx[dx.id == c].reset_index(drop = True)
    ages.append(max(tmp.Age))
    wins.append(sum(tmp.Wins))
    losses.append(sum(tmp.Losses))
    ties.append(sum(tmp.Ties))
    wpct.append(sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    games = tmp.Wins + tmp.Losses + tmp.Ties
    srs.append(np.dot(games,tmp.SRS) / sum(games))
    osrs.append(np.dot(games,tmp.OSRS) / sum(games))
    dsrs.append(np.dot(games,tmp.DSRS) / sum(games))
    pwins.append(sum(tmp.PlayoffWins))
    plosses.append(sum(tmp.PlayoffLosses))
    
    if max(sum(tmp.PlayoffWins), sum(tmp.PlayoffLosses)) > 0:
        
        pwpct.append(sum(tmp.PlayoffWins) / (sum(tmp.PlayoffWins) + sum(tmp.PlayoffLosses)))
        
    else:
        
        pwpct.append(0)
    
    sbs.append(len([x for x in tmp.PlayoffWinPct if x >= 1]))
    papps.append(len([i for i in range(len(tmp)) if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0]))
    divplace.append(np.mean(tmp.DivPlace))
    divwins.append(len([x for x in tmp.DivPlace if x == 1]))
    divwinpct.append(len([x for x in tmp.DivPlace if x == 1]) / max(tmp.TeamTenure))
    clen.append(max(tmp.CareerLength))
    tt.append(max(tmp.TeamTenure))
    event.append(max(tmp.Event))
    black.append(max(tmp.Black))
    
    m = max(tmp.Year)
    m2 = min(tmp.Year)
    tmp1 = tmp[tmp.Year == m]
    tmp2 = tmp[tmp.Year >= m-1]
    tmp5 = tmp[tmp.Year >= m-4]
    s1.append(len([x for x in tmp1.PlayoffWinPct if x == 1]))
    s2.append(len([x for x in tmp2.PlayoffWinPct if x == 1]))
    s5.append(len([x for x in tmp5.PlayoffWinPct if x == 1]))
    
    app = [1 if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0 else 0 for i in range(len(tmp))]
    tmp = pd.concat([tmp, pd.Series(app, name = 'PApp')], axis = 1)
    tmpapp = tmp[tmp.PApp == 1]
    
    try:
        
        m2 = max(tmpapp.Year)
        drought.append(m-m2)
        
    except:
        
        drought.append(len(tmp)-1)
        
    fywins.append(max(tmp1.Wins))
    fywpct.append(max(tmp1.WinPct))
    fypwpct.append(max(tmp1.PlayoffWinPct))
    fydev.append(max(tmp1.WinPct) - sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    rooney1.append(int(m > 2003))
    rooney2.append(int(m2 > 2003))

sbsbin = pd.Series([1 if s > 0 else 0 for s in sbs], name = 'Super Bowl Champion')    
ages = pd.Series(ages, name = 'Age')
ages2 = pd.Series([a*a for a in list(ages)], name = 'Age2')
wins = pd.Series(wins, name = 'Wins')
losses = pd.Series(losses, name = 'Losses')
ties = pd.Series(ties, name = 'Ties')
wpct = pd.Series(wpct, name = 'Win Pct')
srs = pd.Series(srs, name = 'SRS')
osrs = pd.Series(osrs, name = 'OSRS')
dsrs = pd.Series(dsrs, name = 'DSRS')
pwins = pd.Series(pwins, name = 'Playoff Wins')
plosses = pd.Series(plosses, name = 'Playoff Losses')
pwpct = pd.Series(pwpct, name = 'Playoff Win Pct')
sbs = pd.Series(sbs, name = 'Super Bowl Wins')
papps = pd.Series(papps, name = 'Playoff Appearances')
divplace = pd.Series(divplace, name = 'Division Place')
divwins = pd.Series(divwins, name = 'Division Wins')
divwinpct = pd.Series(divwinpct, name = 'Division Win Pct')
clen = pd.Series(clen, name = 'Experience')
tt = pd.Series(tt, name = 'Duration')
event = pd.Series(event, name = 'Event')
black = pd.Series(black, name = 'Black')
s1 = pd.Series(s1, name = 'SB Past Year')
s2 = pd.Series(s2, name = 'SB Past 2 Years')
s5 = pd.Series(s5, name = 'SB Past 5 Years')
drought = pd.Series(drought, name = 'Playoff Drought')
fywins = pd.Series(fywins, name = 'FY Wins') # Create same data set with hispanic coaches removed
fywpct = pd.Series(fywpct, name = 'FY Win Pct')
fypwpct = pd.Series(fypwpct, name = 'FY Playoff Win Pct')
fydev = pd.Series(fydev, name = 'FY Win Pct Change')
be = pd.Series([black[x]*clen[x] for x in range(len(black))], name = 'Black x Experience')
rooney = pd.Series(rooney1, name = 'Rooney')
rooney2 = pd.Series(rooney2, name = 'Rooney')
rxb = pd.Series([black[x]*rooney[x] for x in range(len(black))], name = 'Black x Rooney')
rxb2 = pd.Series([black[x]*rooney2[x] for x in range(len(black))], name = 'Black x Rooney')

surv = pd.concat([event, tt, clen, black, divwins, papps, pwpct, wpct, osrs, dsrs, sbsbin, be, rooney, rxb], axis = 1)
surv0 = surv[surv['Super Bowl Champion'] == 0].reset_index(drop = True)
surv0 = surv0.drop(['Super Bowl Champion'], axis = 1)

# Repeat with hispanic coaches removed

ages = []
wins = []
losses = []
ties = []
wpct = []
srs = []
osrs = []
dsrs = []
pwins = []
plosses = []
pwpct = []
sbs = []
papps = []
divplace = []
divwins = []
divwinpct = []
clen = []
tt = []
event = []
black = []
s1 = []
s2 = []
s5 = []
drought = []
fywins = []
fywpct = []
fypwpct = []
fydev = []
rooney1 = []
rooney2 = []

for c in list(dh.id.unique()):
    
    tmp = dh[dh.id == c].reset_index(drop = True)
    ages.append(max(tmp.Age))
    wins.append(sum(tmp.Wins))
    losses.append(sum(tmp.Losses))
    ties.append(sum(tmp.Ties))
    wpct.append(sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    games = tmp.Wins + tmp.Losses + tmp.Ties
    srs.append(np.dot(games,tmp.SRS) / sum(games))
    osrs.append(np.dot(games,tmp.OSRS) / sum(games))
    dsrs.append(np.dot(games,tmp.DSRS) / sum(games))
    pwins.append(sum(tmp.PlayoffWins))
    plosses.append(sum(tmp.PlayoffLosses))
    
    if max(sum(tmp.PlayoffWins), sum(tmp.PlayoffLosses)) > 0:
        
        pwpct.append(sum(tmp.PlayoffWins) / (sum(tmp.PlayoffWins) + sum(tmp.PlayoffLosses)))
        
    else:
        
        pwpct.append(0)
    
    sbs.append(len([x for x in tmp.PlayoffWinPct if x >= 1]))
    papps.append(len([i for i in range(len(tmp)) if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0]))
    divplace.append(np.mean(tmp.DivPlace))
    divwins.append(len([x for x in tmp.DivPlace if x == 1]))
    divwinpct.append(len([x for x in tmp.DivPlace if x == 1]) / max(tmp.TeamTenure))
    clen.append(max(tmp.CareerLength))
    tt.append(max(tmp.TeamTenure))
    event.append(max(tmp.Event))
    black.append(max(tmp.Black))
    
    m = max(tmp.Year)
    m2 = min(tmp.Year)
    tmp1 = tmp[tmp.Year == m]
    tmp2 = tmp[tmp.Year >= m-1]
    tmp5 = tmp[tmp.Year >= m-4]
    s1.append(len([x for x in tmp1.PlayoffWinPct if x == 1]))
    s2.append(len([x for x in tmp2.PlayoffWinPct if x == 1]))
    s5.append(len([x for x in tmp5.PlayoffWinPct if x == 1]))
    
    app = [1 if max(tmp.PlayoffWins[i], tmp.PlayoffLosses[i]) > 0 else 0 for i in range(len(tmp))]
    tmp = pd.concat([tmp, pd.Series(app, name = 'PApp')], axis = 1)
    tmpapp = tmp[tmp.PApp == 1]
    
    try:
        
        m2 = max(tmpapp.Year)
        drought.append(m-m2)
        
    except:
        
        drought.append(len(tmp)-1)
        
    fywins.append(max(tmp1.Wins))
    fywpct.append(max(tmp1.WinPct))
    fypwpct.append(max(tmp1.PlayoffWinPct))
    fydev.append(max(tmp1.WinPct) - sum(tmp.Wins) / (sum(tmp.Wins) + sum(tmp.Losses) + sum(tmp.Ties)))
    rooney1.append(int(m > 2003))
    rooney2.append(int(m2 > 2003))

sbsbin = pd.Series([1 if s > 0 else 0 for s in sbs], name = 'Super Bowl Champion')    
ages = pd.Series(ages, name = 'Age')
ages2 = pd.Series([a*a for a in list(ages)], name = 'Age2')
wins = pd.Series(wins, name = 'Wins')
losses = pd.Series(losses, name = 'Losses')
ties = pd.Series(ties, name = 'Ties')
wpct = pd.Series(wpct, name = 'Win Pct')
srs = pd.Series(srs, name = 'SRS')
osrs = pd.Series(osrs, name = 'OSRS')
dsrs = pd.Series(dsrs, name = 'DSRS')
pwins = pd.Series(pwins, name = 'Playoff Wins')
plosses = pd.Series(plosses, name = 'Playoff Losses')
pwpct = pd.Series(pwpct, name = 'Playoff Win Pct')
sbs = pd.Series(sbs, name = 'Super Bowl Wins')
papps = pd.Series(papps, name = 'Playoff Appearances')
divplace = pd.Series(divplace, name = 'Division Place')
divwins = pd.Series(divwins, name = 'Division Wins')
divwinpct = pd.Series(divwinpct, name = 'Division Win Pct')
clen = pd.Series(clen, name = 'Experience')
tt = pd.Series(tt, name = 'Duration')
event = pd.Series(event, name = 'Event')
black = pd.Series(black, name = 'Black')
s1 = pd.Series(s1, name = 'SB Past Year')
s2 = pd.Series(s2, name = 'SB Past 2 Years')
s5 = pd.Series(s5, name = 'SB Past 5 Years')
drought = pd.Series(drought, name = 'Playoff Drought')
fywins = pd.Series(fywins, name = 'FY Wins')
fywpct = pd.Series(fywpct, name = 'FY Win Pct')
fypwpct = pd.Series(fywpct, name = 'FY Playoff Win Pct')
fydev = pd.Series(fydev, name = 'FY Win Pct Change')
be = pd.Series([black[x]*clen[x] for x in range(len(black))], name = 'Black x Experience')
rooney = pd.Series(rooney1, name = 'Rooney')
rooney2 = pd.Series(rooney2, name = 'Rooney')
rxb = pd.Series([black[x]*rooney[x] for x in range(len(black))], name = 'Black x Rooney')
rxb2 = pd.Series([black[x]*rooney2[x] for x in range(len(black))], name = 'Black x Rooney')

survh = pd.concat([event, tt, clen, black, divwins, papps, pwpct, wpct, osrs, dsrs, sbsbin, be, rooney, rxb], axis = 1)
survh0 = survh[survh['Super Bowl Champion'] == 0].reset_index(drop = True)
survh0 = survh0.drop(['Super Bowl Champion'], axis = 1)

# Run the hazard model

cph = CoxPHFitter()
cph.fit(surv, 'Duration', event_col = 'Event')

# View results

cph.print_summary(decimals = 3)
cph.plot()

# Run the hazard model now with Hispanic coaches dropped

cphh = CoxPHFitter()
cphh.fit(survh, 'Duration', event_col = 'Event')

# View results

cphh.print_summary(decimals = 3)
cphh.plot()

# Some plots again

view = surv.groupby('Black').mean()
view.reset_index(inplace = True)
plot = cph.predict_survival_function(view).plot()

xxx = survh0[survh0.Duration <= 10]
xx = survh0[survh0.Duration <= 5]
T = xxx['Duration']
E = xxx['Event']
groups = xxx['Black']
ix = (groups == 1)
kmf = KaplanMeierFitter()
kmf.fit(T[~ix], E[~ix], label = 'White')
ax = kmf.plot_survival_function()
kmf.fit(T[ix], E[ix], label = 'Black')
ax = kmf.plot_survival_function(ax = ax)

frog = cphh.fit(xx, 'Duration', event_col = 'Event')
frog.plot_partial_effects_on_outcome('Black', values = np.arange(1, 2), cmap = 'coolwarm')

# Running a robustness check using a Weibull model

surv0x = surv0.drop(['Black x Experience'], axis = 1)
survh0x = survh0.drop(['Black x Experience'], axis = 1)

aft = WeibullAFTFitter()
aft.fit(survh0, 'Duration', 'Event', ancillary = survh0)
aft.print_summary()
aft.predict_median(survh0)

# Repeating main analyses with different specifications of the Black variable and Hispanic coaches omitted

# Creating a Black variable only setup

survb = survh0[['Event', 'Duration', 'Experience', 'Black', 'Division Wins',
       'Playoff Appearances', 'Playoff Win Pct', 'Win Pct', 'OSRS', 'DSRS',
       'FY Win Pct', 'FY Win Pct Change', 'Rooney', 'Black x Rooney']]

# Run the hazard model now with Hispanic coaches dropped

cphb = CoxPHFitter()
cphb.fit(survb, 'Duration', event_col = 'Event')

# View results

cphb.print_summary(decimals = 3)
cphb.plot()



"""
If the hazard ratio for a predictor is close to 1 then that predictor does not affect survival.
If the hazard ratio is less than 1, then the predictor is protective (i.e., associated with improved survival)
and if the hazard ratio is greater than 1, then the predictor is associated with increased risk (or decreased survival).
"""

"""
this means that log(HR) ~ 0 is the criterion used here rather than HR ~ 1
"""

"""
https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_survival/BS704_Survival6.html
"""

