# This script runs the survival analysis

# Importing required modules

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

# Project directory

direc = 'D:/coach_survival/'

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
IND = []
MIA = []
CHI = []
CLE = []
NWE = []
DAL = []
PHI = []
KAN = []
CIN = []
WAS = []
LAC = []
PIT = []
DEN = []
NYG = []
ATL = []
LAR = []
BUF = []
SEA = []
TEN = []
NYJ = []
JAX = []
LVR = []
GNB = []
MIN = []
NOR = []
TAM = []
BAL = []
CAR = []
STL = []
SFO = []
ARI = []
HOU = []
DET = []

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
    
    IND.append(int(tmp.Team[0] == 'IND'))
    MIA.append(int(tmp.Team[0] == 'MIA'))
    CHI.append(int(tmp.Team[0] == 'CHI'))
    CLE.append(int(tmp.Team[0] == 'CLE'))
    NWE.append(int(tmp.Team[0] == 'NWE'))
    DAL.append(int(tmp.Team[0] == 'DAL'))
    PHI.append(int(tmp.Team[0] == 'PHI'))
    KAN.append(int(tmp.Team[0] == 'KAN'))
    CIN.append(int(tmp.Team[0] == 'CIN'))
    WAS.append(int(tmp.Team[0] == 'WAS'))
    LAC.append(int(tmp.Team[0] == 'LAC'))
    PIT.append(int(tmp.Team[0] == 'PIT'))
    DEN.append(int(tmp.Team[0] == 'DEN'))
    NYG.append(int(tmp.Team[0] == 'NYG'))
    ATL.append(int(tmp.Team[0] == 'ATL'))
    LAR.append(int(tmp.Team[0] == 'LAR'))
    BUF.append(int(tmp.Team[0] == 'BUF'))
    SEA.append(int(tmp.Team[0] == 'SEA'))
    TEN.append(int(tmp.Team[0] == 'TEN'))
    NYJ.append(int(tmp.Team[0] == 'NYJ'))
    JAX.append(int(tmp.Team[0] == 'JAX'))
    LVR.append(int(tmp.Team[0] == 'LVR'))
    GNB.append(int(tmp.Team[0] == 'GNB'))
    MIN.append(int(tmp.Team[0] == 'MIN'))
    NOR.append(int(tmp.Team[0] == 'NOR'))
    TAM.append(int(tmp.Team[0] == 'TAM'))
    BAL.append(int(tmp.Team[0] == 'BAL'))
    CAR.append(int(tmp.Team[0] == 'CAR'))
    STL.append(int(tmp.Team[0] == 'STL'))
    SFO.append(int(tmp.Team[0] == 'SFO'))
    ARI.append(int(tmp.Team[0] == 'ARI'))
    HOU.append(int(tmp.Team[0] == 'HOU'))
    DET.append(int(tmp.Team[0] == 'DET'))

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
IND = pd.Series(IND, name = 'IND')
MIA = pd.Series(MIA, name = 'MIA')
CHI = pd.Series(CHI, name = 'CHI')
CLE = pd.Series(CLE, name = 'CLE')
NWE = pd.Series(NWE, name = 'NWE')
DAL = pd.Series(DAL, name = 'DAL')
PHI = pd.Series(PHI, name = 'PHI')
KAN = pd.Series(KAN, name = 'KAN')
CIN = pd.Series(CIN, name = 'CIN')
WAS = pd.Series(WAS, name = 'WAS')
LAC = pd.Series(LAC, name = 'LAC')
PIT = pd.Series(PIT, name = 'PIT')
DEN = pd.Series(DEN, name = 'DEN')
NYG = pd.Series(NYG, name = 'NYG')
ATL = pd.Series(ATL, name = 'ATL')
LAR = pd.Series(LAR, name = 'LAR')
BUF = pd.Series(BUF, name = 'BUF')
SEA = pd.Series(SEA, name = 'SEA')
TEN = pd.Series(TEN, name = 'TEN')
NYJ = pd.Series(NYJ, name = 'NYJ')
JAX = pd.Series(JAX, name = 'JAX')
LVR = pd.Series(LVR, name = 'LVR')
GNB = pd.Series(GNB, name = 'GNB')
MIN = pd.Series(MIN, name = 'MIN')
NOR = pd.Series(NOR, name = 'NOR')
TAM = pd.Series(TAM, name = 'TAM')
BAL = pd.Series(BAL, name = 'BAL')
CAR = pd.Series(CAR, name = 'CAR')
STL = pd.Series(STL, name = 'STL')
SFO = pd.Series(SFO, name = 'SFO')
ARI = pd.Series(ARI, name = 'ARI')
HOU = pd.Series(HOU, name = 'HOU')
DET = pd.Series(DET, name = 'DET')

surv = pd.concat([event, tt, clen, black, divwins, papps, pwpct, wpct, osrs, dsrs, sbsbin, be, rooney, rxb,
                  IND, MIA, CHI, CLE, NWE, DAL, PHI, KAN, CIN, WAS, LAC, PIT, DEN, NYG, ATL, LAR, BUF,
                  SEA, TEN, NYJ, JAX, LVR, GNB, MIN, NOR, TAM, BAL, CAR, STL, SFO, ARI, HOU], axis = 1)
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
IND = []
MIA = []
CHI = []
CLE = []
NWE = []
DAL = []
PHI = []
KAN = []
CIN = []
WAS = []
LAC = []
PIT = []
DEN = []
NYG = []
ATL = []
LAR = []
BUF = []
SEA = []
TEN = []
NYJ = []
JAX = []
LVR = []
GNB = []
MIN = []
NOR = []
TAM = []
BAL = []
CAR = []
STL = []
SFO = []
ARI = []
HOU = []
DET = []

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
    
    IND.append(int(tmp.Team[0] == 'IND'))
    MIA.append(int(tmp.Team[0] == 'MIA'))
    CHI.append(int(tmp.Team[0] == 'CHI'))
    CLE.append(int(tmp.Team[0] == 'CLE'))
    NWE.append(int(tmp.Team[0] == 'NWE'))
    DAL.append(int(tmp.Team[0] == 'DAL'))
    PHI.append(int(tmp.Team[0] == 'PHI'))
    KAN.append(int(tmp.Team[0] == 'KAN'))
    CIN.append(int(tmp.Team[0] == 'CIN'))
    WAS.append(int(tmp.Team[0] == 'WAS'))
    LAC.append(int(tmp.Team[0] == 'LAC'))
    PIT.append(int(tmp.Team[0] == 'PIT'))
    DEN.append(int(tmp.Team[0] == 'DEN'))
    NYG.append(int(tmp.Team[0] == 'NYG'))
    ATL.append(int(tmp.Team[0] == 'ATL'))
    LAR.append(int(tmp.Team[0] == 'LAR'))
    BUF.append(int(tmp.Team[0] == 'BUF'))
    SEA.append(int(tmp.Team[0] == 'SEA'))
    TEN.append(int(tmp.Team[0] == 'TEN'))
    NYJ.append(int(tmp.Team[0] == 'NYJ'))
    JAX.append(int(tmp.Team[0] == 'JAX'))
    LVR.append(int(tmp.Team[0] == 'LVR'))
    GNB.append(int(tmp.Team[0] == 'GNB'))
    MIN.append(int(tmp.Team[0] == 'MIN'))
    NOR.append(int(tmp.Team[0] == 'NOR'))
    TAM.append(int(tmp.Team[0] == 'TAM'))
    BAL.append(int(tmp.Team[0] == 'BAL'))
    CAR.append(int(tmp.Team[0] == 'CAR'))
    STL.append(int(tmp.Team[0] == 'STL'))
    SFO.append(int(tmp.Team[0] == 'SFO'))
    ARI.append(int(tmp.Team[0] == 'ARI'))
    HOU.append(int(tmp.Team[0] == 'HOU'))
    DET.append(int(tmp.Team[0] == 'DET'))

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
IND = pd.Series(IND, name = 'IND')
MIA = pd.Series(MIA, name = 'MIA')
CHI = pd.Series(CHI, name = 'CHI')
CLE = pd.Series(CLE, name = 'CLE')
NWE = pd.Series(NWE, name = 'NWE')
DAL = pd.Series(DAL, name = 'DAL')
PHI = pd.Series(PHI, name = 'PHI')
KAN = pd.Series(KAN, name = 'KAN')
CIN = pd.Series(CIN, name = 'CIN')
WAS = pd.Series(WAS, name = 'WAS')
LAC = pd.Series(LAC, name = 'LAC')
PIT = pd.Series(PIT, name = 'PIT')
DEN = pd.Series(DEN, name = 'DEN')
NYG = pd.Series(NYG, name = 'NYG')
ATL = pd.Series(ATL, name = 'ATL')
LAR = pd.Series(LAR, name = 'LAR')
BUF = pd.Series(BUF, name = 'BUF')
SEA = pd.Series(SEA, name = 'SEA')
TEN = pd.Series(TEN, name = 'TEN')
NYJ = pd.Series(NYJ, name = 'NYJ')
JAX = pd.Series(JAX, name = 'JAX')
LVR = pd.Series(LVR, name = 'LVR')
GNB = pd.Series(GNB, name = 'GNB')
MIN = pd.Series(MIN, name = 'MIN')
NOR = pd.Series(NOR, name = 'NOR')
TAM = pd.Series(TAM, name = 'TAM')
BAL = pd.Series(BAL, name = 'BAL')
CAR = pd.Series(CAR, name = 'CAR')
STL = pd.Series(STL, name = 'STL')
SFO = pd.Series(SFO, name = 'SFO')
ARI = pd.Series(ARI, name = 'ARI')
HOU = pd.Series(HOU, name = 'HOU')
DET = pd.Series(DET, name = 'DET')

survh = pd.concat([event, tt, clen, black, divwins, papps, pwpct, wpct, osrs, dsrs, sbsbin, be, rooney, rxb,
                   IND, MIA, CHI, CLE, NWE, DAL, PHI, KAN, CIN, WAS, LAC, PIT, DEN, NYG, ATL, LAR, BUF,
                   SEA, TEN, NYJ, JAX, LVR, GNB, MIN, NOR, TAM, BAL, CAR, STL, SFO, ARI, HOU], axis = 1)
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

