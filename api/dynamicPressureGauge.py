# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import matplotlib.animation as animation
from IPython.display import HTML
from random import sample
import datetime

pd.options.mode.chained_assignment = None 
pd.set_option('display.max_columns', None)

import warnings 
warnings.filterwarnings("ignore")

from scipy.spatial.distance import pdist, squareform
plt.switch_backend('Agg') 



# Read data
# Import Data
games = pd.read_csv("https://storage.googleapis.com/big-data-bowl/games.csv", low_memory=False)
plays = pd.read_csv("https://storage.googleapis.com/big-data-bowl/plays.csv", low_memory=False)
players = pd.read_csv("https://storage.googleapis.com/big-data-bowl/players.csv", low_memory=False)

week1 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week1.csv", low_memory=False)
#week2 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week2.csv", low_memory=False)
#week3 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week3.csv", low_memory=False)
#week4 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week4.csv", low_memory=False)
#week5 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week5.csv", low_memory=False)
#week6 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week6.csv", low_memory=False)
#week7 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week7.csv", low_memory=False)
#week8 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week8.csv", low_memory=False)

pffScoutingData = pd.read_csv("https://storage.googleapis.com/big-data-bowl/pffScoutingData.csv", low_memory=False)


tracking = week1
    #.append([
    #week2,
    #week3,
    #week4,
    #week5,
    #week6,
    #week7,
    #week8
#])

print(tracking.head())
# Merge Data
print("merging data")
joined_all = pd.merge(games,plays,how="inner",on = "gameId")
print(joined_all.count())
joined_all = pd.merge(joined_all,tracking,how="inner",on=["gameId","playId"])
print(joined_all.count())
# left join on players to keep football records
joined_all = pd.merge(joined_all,players,how="left",on = "nflId")
print(joined_all.count())
joined_all = pd.merge(joined_all,pffScoutingData,how="left",on=["gameId","playId",'nflId'])
print(joined_all.count())
print(joined_all.head())



# This function is designed for the user to pick specific plays to analyze

def returnHtml(gameId,playId):
    # do work
    print("generating html")
    print(gameId)
    print(playId)
    return pickingPressurePlay(int(gameId),int(playId))

# User input on selecting a play 
# Select Team, Formation, Pass Result
def pickingPressurePlay(gameId,playId):
    print("inside pickingPressurePlay")
    
    def draw_barchart(frame):
        print("inside draw_barchart")
        dff = df[df['frameId'].eq(frame)].sort_values(by='pressureValue', ascending=True)
        ax.clear()
        ax.barh(dff['displayName'], dff['pressureValue'].round(decimals = 3), color=[colors[group_lk[x]] for x in dff['displayName']])
        dx = dff['pressureValue'].max() / 200
        for i, (value, name) in enumerate(zip(dff['pressureValue'].round(decimals = 3), dff['displayName'])):
            ax.text(value-dx, i-.05,     name,           size=14, weight=800, ha='right', va='bottom')
            ax.text(value-dx, i+.25, group_lk[name], size=10, color='#444444', ha='right', va='baseline')
            ax.text(value-dx*10, i-.25,     value,  size=14, ha='left',  va='center')
        # ... polished styles
        ax.text(1, 0.4, frame, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=500)
        ax.text(0, 1.06, 'pressureValue', transform=ax.transAxes, size=12, color='#777777')
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', colors='#777777', labelsize=12)
        ax.set_yticks([])
        ax.margins(0, 0.01)
        ax.grid(which='major', axis='x', linestyle='-')
        ax.set_axisbelow(True)
        ax.text(0, 1.12, f'{playDescription}',
                transform=ax.transAxes, size=24, weight=600, ha='left')
        ax.text(1, 0, 'by Dennis K.', transform=ax.transAxes, ha='right',
                color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
        plt.box(False)
        
    


    print(joined_all.count())
    print(joined_all.head())
    # load data here
    print("df loaded")
    df = joined_all.loc[joined_all['gameId']==gameId]
    print(df.count())
    df = df.loc[df['playId']==playId]
    print(df.count())
    print(df.head())

    print("joined data")

    # Create empty Pandas DataFrames for user to input and for pre_snap information 
    #gameList = pd.DataFrame()

    df_presnap = pd.DataFrame()

    # Creating the pressure Gauge                        
    pressureDF = pd.DataFrame()

    print("before gid loop")
    print(df.head())

    # loop through each game 
    for gid in df['gameId'].unique():
        print("inside for gid loop")
        # subset the data down to one game
        one_game = df.loc[df['gameId']==gid]
    
        # loop through each play
        for pid in one_game['playId'].unique():
            print("Inside onne_game")

            # subset game data down to one play 
            one_play = df.loc[df['playId']==pid]

            for oneFrame in one_play['frameId'].unique():
                print("inside one_frame")
                one_frame = one_play.loc[one_play['frameId'] == oneFrame]


                # reset index (saving the original index as a column) and set new index as player ID 
                one_frame = one_frame.reset_index().set_index('nflId')

                # turn PFF player positioning info into unique positions given the play (for modeling purposes)
                one_frame['officialPosition'] = one_frame['officialPosition'] + one_frame.groupby('officialPosition', as_index=False).cumcount().astype(str).str.replace('0', '')
                
                # get pairwise distance, turn it into a pairwise matrix, set it in a pandas dataframe with index as nflId and columns as positions 
                _df = pd.DataFrame(squareform(pdist(one_frame.loc[:, ['x','y']])), index=one_frame.index, columns=one_frame['officialPosition'].unique())

                # concat pairwise matrix column-wise onto original one_frame data
                one_frame = pd.concat([one_frame,_df], axis=1).rename(columns={np.nan:'dist_from_ball'})

                # change index back to nflId column, set the column "index" to the true index 
                one_frame = one_frame.reset_index().set_index('index')

                # clear the index name for prettyfication 
                one_frame.index.name = None

                # append to output dataframe
                df_presnap = df_presnap.append(one_frame)


                # creating distance from QB
                

                # creating pressure value
                pressureValue = 1 / df_presnap['QB']

                df_presnap['pressureValue'] = pressureValue

                # Creating Pressure DF
                pressureDF = df_presnap[df_presnap.team != 'football']


    # fill the nulled sparse positions with -1, indicating that position was not apparent on a given play and/or frame
    positions = [x for x in df_presnap.columns.values if x not in one_game.columns.values]
    df_presnap.loc[:, positions] = df_presnap.loc[:, positions].fillna(-1)  
    # df_presnap.loc[:, ['frameId','nflId', 'officialPosition', 'gameId', 'playId','QB', 'dist_from_ball']]
    print(pressureDF)
    pressureDF.loc[:,['pressureValue','officialPosition']]
    # Creating Animated Pressure Gauge for individual plays

    defense = [
    'OLB','MLB','ILB','DE','SS','FS','CB','DT','NT',
    'OLB1','OLB2','OLB3','OLB4','OLB5',
    'MLB1','MLB2','MLB3','MLB4','MLB5',
    'ILB1','ILB2','ILB3','ILB4','ILB5',
    'DE1','DE2','DE3','DE4','DE5',
    'SS1','SS2','SS3','SS4','SS5',
    'FS1','FS2','FS3','FS4','FS5',
    'CB1','CB2','CB3','CB4','CB5','CB6','CB7',
    'DT1','DT2','DT3','DT4','DT5',
    'NT1','NT2','NT3','NT4','NT5'
    ]

    offense = [
    'QB','RB','WR','TE','FB','T','G','C',
    'QB1','QB2','QB3',
    'RB1','RB2','RB3','RB4',
    'WR','WR1','WR2','WR3','WR4','WR5','WR6','WR7','WR8',
    'TE','TE1','TE2','TE3','TE4',
    'FB1','FB2','FB3',
    'T','T1','T2','T3','T4',
    'G','G1','G2','G3','G4',
    'C','C1','C2','C3'
    ]

    pressureRange = pressureDF[['frameId','officialPosition','pressureValue','displayName', 'gameId','playDescription']]

    for offender in offense:
        pressureRange = pressureRange[pressureRange.officialPosition != offender]
        
    

    df = pressureRange 

    current_frame = 1
    frameMin = df['frameId'].min()
    frameMax = df['frameId'].max()
    playDescription = df.playDescription.values[0]
    if len(playDescription.split(" "))>15 and len(playDescription)>115:
        playDescription = " ".join(playDescription.split(" ")[0:16]) + "<br>" + " ".join(playDescription.split(" ")[16:])
    dff = df[df['frameId'].eq(current_frame)].sort_values(by='pressureValue',ascending=False)

    
    colors = dict(zip([
    'OLB','MLB','ILB','DE','SS','FS','CB','DT','NT',
    'OLB1','OLB2','OLB3','OLB4','OLB5',
    'MLB1','MLB2','MLB3','MLB4','MLB5',
    'ILB1','ILB2','ILB3','ILB4','ILB5',
    'DE1','DE2','DE3','DE4','DE5',
    'SS1','SS2','SS3','SS4','SS5',
    'FS1','FS2','FS3','FS4','FS5',
    'CB1','CB2','CB3','CB4','CB5','CB6','CB7',
    'DT1','DT2','DT3','DT4','DT5',
    'NT1','NT2','NT3','NT4','NT5'],
    ['#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
    '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
    '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
    '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
    '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
    '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
    '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
    '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',]
    ))

    group_lk = df.set_index('displayName')['officialPosition'].to_dict()

    dff = dff[::-1]   # flip values from top to bottom
    
    fig, ax = plt.subplots(figsize=(10, 10))
    animator = animation.FuncAnimation(fig, draw_barchart, frames=range(frameMin, frameMax))
    return HTML(animator.to_jshtml()) 


    

    


# returnHtml(2021090900,137)

