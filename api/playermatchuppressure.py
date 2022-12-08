# Call player_matchup(nflId_defense, nflId_offense) for defensive pressure %, offensive pressure % and gauge html

# Import dependencies
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm
from statistics import mean, stdev
import math, kaleido
import plotly.graph_objects as go
from IPython.display import HTML

plt.switch_backend('Agg') 

# Read data
red_zone_qb_proximity = pd.read_csv('https://storage.googleapis.com/big-data-bowl/redZoneQBProximity.csv')


def pressure_probability(nflId):
    player_pressure = red_zone_qb_proximity[red_zone_qb_proximity['nflId2'] == nflId][['gameId', 'playId', 'distance']].groupby(['gameId', 'playId']).min().reset_index()
    if len(player_pressure) > 5:
        return norm(loc = mean(player_pressure['distance']) , scale = stdev(player_pressure['distance'])).cdf(1)
    else:
        return np.nan


def pressure_allowed_probability(nflId):
    plays = red_zone_qb_proximity[red_zone_qb_proximity['nflId2'] == nflId][['gameId', 'playId']].drop_duplicates()
    plays_opposing = plays.merge(red_zone_qb_proximity[red_zone_qb_proximity['matchupOpposing'] == 1])
    play_pressure = plays_opposing[['gameId', 'playId', 'distance']].groupby(['gameId', 'playId']).min().reset_index()
    if len(play_pressure) > 5:
        return norm(loc = mean(play_pressure['distance']) , scale = stdev(play_pressure['distance'])).cdf(1)
    else:
        return np.nan


def format_pct(dec):
    return str(round(dec*100,2)) + '%'


def player_matchup(nflId_defense, nflId_offense):
    pressure_metric_defense = pressure_probability(nflId_defense)
    pressure_metric_offense = pressure_allowed_probability(nflId_offense)
    matchup_metric = pressure_metric_defense * pressure_metric_offense
    
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = 3000*matchup_metric,
        mode = "gauge+number",
        title = {'text': "Pressure Metric"},
        gauge = {'axis': {'range': [None, 100]},
            'bar': {'color': "gray"},
            'steps' : [
                {'range': [0, 33], 'color': "lightgreen"},
                {'range': [33, 66], 'color': "lightyellow"},
                {'range': [66, 100], 'color': "indianred"}],}))

    filename = f'images/player-matchup_{nflId_defense}-{nflId_offense}.jpg'
    fig.write_image(f'static/{filename}', engine="kaleido")
    
    if pressure_metric_offense == pressure_metric_offense and pressure_metric_defense == pressure_metric_defense:
        return filename, ''
    else:
        return filename, 'ERROR: Insufficient data to evaluate this player matchup.'

if __name__ == '__main__':
    print(player_matchup(30869, 35442))