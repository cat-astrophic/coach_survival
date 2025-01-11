# Scrapes data on NFL coaches

# Importing required modules

import pandas as pd
import urllib
from bs4 import BeautifulSoup as bs

# Directory info

direc = 'D:/coach_survival/'

# url from which individual coach links are obtained

base = 'https://www.pro-football-reference.com/'
url0 = base + 'coaches/'

# Getting coach links

page = urllib.request.Request(url0, headers = {'User-Agent': 'Mozilla/5.0'})  # Go to the url and get some data
response = urllib.request.urlopen(page) # Go to the url and get some data
soup = bs(response, 'html.parser') # Go to the url and get some data
data = soup.find_all('tr') # Get the correct type of data
data = data[1:] # Pare down to the coach entries

links = []

for d in data:
   
    tag = str(d.find_all('a')[0])
    idx = tag.find('/')
    tag = tag[idx:]
    idx = tag.find('"')
    tag = tag[:idx]
    links.append(base + tag)

# Getting coach level data

coaches = []
years = []
ages = []
teams = []
leagues = []
games = []
wins = []
losses = []
ties = []
wpcts = []
srs = []
osrs = []
dsrs = []
playg = []
playw = []
playl = []
playpct = []
ranks = []

for l in links:
   
    page = urllib.request.Request(l + '#coaching_results', headers = {'User-Agent': 'Mozilla/5.0'})  # Go to the url and get some data
    response = urllib.request.urlopen(page) # Go to the url and get some data
    soup = bs(response, 'html.parser') # Go to the url and get some data
    data = soup.find_all('table')[0] # extract table
    dx = data.find_all('tr') # extract table
    dx = dx[2:] # extract annual data from table
   
    # Parse the table
   
    for d in dx:
       
        try:
           
            cx = soup.find_all('h1')
            cx = str(cx[0])
            cx = cx[27:]
            idx = cx.find('<')
            cx = cx[:idx]
            coaches.append(cx)
           
            dt = d.find_all('td')
            ages.append(str(dt[0])[34:36])
            years.append(str(dt[1])[54:58])
            teams.append(str(dt[1])[64:67])
            leagues.append(str(dt[2])[39:42])
            games.append(str(dt[3])[102:104].replace('<',''))
           
            w = str(dt[4])[35:37].replace('<','')
            b = str(dt[5])[37:39].replace('<','')
            t = str(dt[6])[38]
            p = str(dt[7])[44:48]
            s = str(dt[8])[40:44].replace('<','')
            o = str(dt[9])[42:46].replace('<','')
            e = str(dt[10])[42:46].replace('<','')
           
            if w == 's"':
               
                wins.append('0')
               
            else:
               
                wins.append(w)
               
            if b == 's"':
               
                losses.append('0')
               
            else:
               
                losses.append(b)
               
            if t == 't':
               
                ties.append('1')
               
            else:
               
                ties.append(t)
               
            if p == 'c">.':
               
                wpcts.append('0')
               
            else:
               
                wpcts.append(p)
               
            if s == 'l">0':
               
                srs.append('0')
               
            else:
               
                srs.append(s)
               
            if o == 'e">0':
               
                osrs.append('0')
               
            else:
               
                osrs.append(o)
               
            if e == 'e">0':
               
                dsrs.append('0')
               
            else:
               
                dsrs.append(e)
               
            if 'iz' in str(dt[11]):
               
                pg = str(dt[11])[44].replace('<','')
               
            else:
               
                pg = str(dt[11])[41]
               
            if 'iz' in str(dt[12]):
               
                pw = str(dt[12])[47].replace('<','')
               
            else:
               
                pw = str(dt[12])[44]
               
            if 'iz' in str(dt[13]):
               
                pl = str(dt[13])[49].replace('<','')
               
            else:
               
                pl = str(dt[13])[46]
               
            if 'iz' in str(dt[14]):
               
                pp =  str(dt[14])[56:60].replace('<','').replace('/','').replace('t','').replace('d','')
               
            else:
               
                pp =  str(dt[14])[53:57]
               
            if pg == '':
               
                pg = '0'
               
            if pw == '':
               
                pw = '0'
               
            if pl == '':
               
                pl = '0'
               
            if pp == '':
               
                pp = '0'
               
            playg.append(pg)
            playw.append(pw)
            playl.append(pl)
            playpct.append(pp)
            ranks.append(str(dt[15])[40])
           
        except:
           
            continue
           
# Build a dataframe

coaches = pd.Series(coaches, name = 'Coach')
years = pd.Series(years, name = 'Year')
ages = pd.Series(ages, name = 'Age')
teams = pd.Series(teams, name = 'Team')
leagues = pd.Series(leagues, name = 'League')
games = pd.Series(games, name = 'Games')
wins = pd.Series(wins, name = 'Wins')
losses = pd.Series(losses, name = 'Losses')
ties = pd.Series(ties, name = 'Ties')
wpcts = pd.Series(wpcts, name = 'WinPct')
srs = pd.Series(srs, name = 'SRS')
osrs = pd.Series(osrs, name = 'OSRS')
dsrs = pd.Series(dsrs, name = 'DSRS')
playg = pd.Series(playg, name = 'PlayoffGames')
playw = pd.Series(playw, name = 'PlayoffWins')
playl = pd.Series(playl, name = 'PlayoffLosses')
playpct = pd.Series(playpct, name = 'PlayoffWinPct')
ranks = pd.Series(ranks, name = 'DivPlace')

df = pd.concat([coaches, years, ages, teams, leagues, games, wins, losses, ties,
                wpcts, srs, osrs, dsrs, playg, playw, playl, playpct, ranks], axis = 1)

df = df[df.Year != ''].reset_index(drop = True)

# Remove Bruce Arians 2012 season due to wins being allocated to Chuck Pagano

df = df[df.DivPlace != 'm'].reset_index(drop = True)

# Need to know pct of each season was coached (divide games by max(games-years))

maxgames = []
pctcoached = []

for i in range(len(df)):
   
    y = df.Year[i]
    tmp = df[df.Year == y]
   
    try:
       
        stuff = [int(x) for x in tmp.Games]
        g = max(stuff)
        maxgames.append(int(g))
       
    except:
       
        maxgames.append(None)
       
    try:
       
        pctcoached.append(int(df.Games[i]) / maxgames[i])
       
    except:
       
        pctcoached.append(None)
       
df = pd.concat([df, pd.Series(pctcoached, name = 'PctCoached')], axis = 1)

# Number of seasons with team

seasons_all = []
seasons_team = []

df.Year = df.Year.astype(int)

for i in range(len(df)):
   
    tmp = df[df.Coach == df.Coach[i]]
    tmp = tmp[tmp.Year <= df.Year[i]]
    seasons_all.append(len(tmp))
    tmp = tmp[tmp.Team == df.Team[i]]
    seasons_team.append(len(tmp))
   
df = pd.concat([df, pd.Series(seasons_all, name = 'CareerLength'), pd.Series(seasons_team, name = 'TeamTenure')], axis = 1)

# Events

events = []

for i in range(len(df)):
    
    c = df.Coach[i]
    y = df.Year[i]
    t = df.Team[i]
    tmp = df[df.Coach == c]
    tmp = tmp[tmp.Team == t]
    m = max(tmp.Year)
    
    if m == 2021:
        
        if c in ['Sean Payton', 'David Culley', 'Joe Judge', 'Matt Nagy', 'Mike Zimmer', 'Vic Fangio', 'Urban Meyer', 'John Gruden']:
            
            events.append(1)
            
        else:
            
            events.append(0)
            
    elif m == y:
        
        events.append(1)
        
    else:
        
        events.append(0)
        
df = pd.concat([df, pd.Series(events, name = 'Event')], axis = 1)

# Update team relocations

for i in range(len(df)):
    
    if df.Team[i] == 'STL':
        
        if df.Year[i] > 1959:
            
            if df.Year[i] < 1988:
                
                df.Team[i] = 'ARI'
                
        else:
            
            df.Team[i] = 'LAR'
        
    if df.Team[i] == 'SDG':
        
        df.Team[i] = 'LAC'
        
    if df.Team[i] == 'BOS':
        
        df.Team[i] = 'NWE'
        
    if df.Team[i] == 'HOU':
        
        if df.Year[i] < 1997:
            
            df.Team[i] = 'TEN'
            
    if df.Team[i] == 'OAK':
        
        df.Team[i] = 'LVR'
        
    if df.Team[i] == 'RAI':
        
        df.Team[i] = 'LVR'
        
    if df.Team[i] == 'PHO':
        
        df.Team[i] = 'ARI'
        
    if df.Team[i] == 'NYT':
        
        df.Team[i] = 'NYJ'
        
    if df.Team[i] == 'DTX':
        
        df.Team[i] = 'KAN'
        
    if df.Team[i] == 'BAL':
        
        if df.Year[i] < 1984:
            
            df.Team[i] = 'IND'
            
    if df.Team[i] == 'RAM':
        
        df.Team[i] = 'LAR'
            
# List of all black coaches from: https://newsone.com/playlist/nfl-black-head-coaches-full-list/

black_coaches = ['Fritz Pollard', 'Art Shell', 'Dennis Green', 'Ray Rhodes',
                 'Tony Dungy', 'Herm Edwards', 'Marvin Lewis', 'Lovie Smith',
                 'Terry Robiskie', 'Romeo Crennel', 'Mike Tomlin', 'Emmitt Thomas',
                 'Mike Singletary', 'Jim Caldwell', 'Raheem Morris', 'Perry Fewell',
                 'Leslie Frazier', 'Eric Studesville', 'Mel Tucker', 'Todd Bowles',
                 'Hue Jackson', 'Anthony Lynn', 'Vance Josep', 'Brian Flores']

black = [1 if c in black_coaches else 0 for c in df.Coach]
df = pd.concat([df, pd.Series(black, name = 'Black')], axis = 1)

# Save to file

df.to_csv(direc + 'data.csv', index = False)

