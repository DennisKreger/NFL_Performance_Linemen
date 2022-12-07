# Team pressure graphic: call generate_plot(team_abbreviation) which returns html for density plot.

# Import dependencies
import pandas as pd
from matplotlib import pyplot as plt

# Read data
red_zone_qb_proximity = pd.read_csv('https://storage.googleapis.com/big-data-bowl/redZoneQBProximity.csv')
week1 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week1.csv')

player_teams = week1[['nflId', 'team']].groupby(['nflId', 'team']).first().reset_index()

red_zone_qb_proximity_team = red_zone_qb_proximity.merge(
    player_teams,
    left_on=['nflId2'],
    right_on=['nflId']
)
red_zone_qb_proximity_team

max_pressure = red_zone_qb_proximity_team[red_zone_qb_proximity_team['matchupOpposing'] == 1][['playId', 'distance', 'team']].groupby('playId').min().reset_index()

def generate_plot_home(team):
    fig, ax1 = plt.subplots()
    max_pressure[max_pressure['team'] == team]['distance'].plot.density(figsize=(10,4),
                              xlim=(5,0))
    ax2 = ax1.twinx()
    ax2.hist(max_pressure[max_pressure['team'] == team]['distance'], alpha=0.1, bins=18)
    plt.xlabel('Distance from QB')
    plt.ylabel('Frequency')
    plt.title(f'Max Pressure by Play - {team}')
    filename = f'images/pressure-home_' + team + '.jpg'
    fig.savefig(f'static/{filename}', bbox_inches='tight')
    return filename

def generate_plot_away(team):
    fig, ax1 = plt.subplots()
    max_pressure[max_pressure['team'] == team]['distance'].plot.density(figsize=(10,4),
                              xlim=(5,0))
    ax2 = ax1.twinx()
    ax2.hist(max_pressure[max_pressure['team'] == team]['distance'], alpha=0.1, bins=18)
    plt.xlabel('Distance from QB')
    plt.ylabel('Frequency')
    plt.title(f'Max Pressure by Play - {team}')
    filename = f'images/pressure-away_' + team + '.jpg'
    fig.savefig(f'static/{filename}', bbox_inches='tight')
    return filename