# %%
# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import psycopg2
import sys

import bar_chart_race as bcr

import matplotlib.animation as animation
from IPython.display import HTML


pd.options.mode.chained_assignment = None 
pd.set_option('display.max_columns', None)

import warnings 
warnings.filterwarnings("ignore")

from scipy.spatial.distance import pdist, squareform


# %%
# Store environment variable
from getpass import getpass
dbPassword = getpass('Enter database password')

# %%
param_dic = {
        'database': 'big-data-bowl',
        'user': 'postgres',
        'password': dbPassword,
        'host': '34.72.136.99',
        'port': 5432,
}
def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn

# %%
def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df

# %%
# Connect to the database
gameId = 2021090900
playId = 137

# %%
def returnHtml(gameId,playId):
    # do work
    return pickingPressurePlay(gameId,playId)

# User input on selecting a play 
# Select Team, Formation, Pass Result
def pickingPressurePlay(gameId,playId):


    conn = connect(param_dic)
    column_names = [
    "gameId", 
    "playId", 
    "nflId",
    "displayName",
    "officialPosition",
    "playDescription",
    "frameId",
    "x",
    "y"
    ]
    query = f"SELECT ALL trd.\"gameId\", \
    trd.\"playId\", \
    trd.\"nflId\",  \
    pl.\"displayName\", \
    pl.\"officialPosition\",  \
    ply.\"playDescription\", \
    trd.\"frameId\", \
    trd.\"x\",        \
    trd.\"y\"         \
    FROM trackingdata as trd                                            \
    LEFT JOIN players as pl                                             \
    ON trd.\"nflId\" = pl.\"nflID\" \
    LEFT JOIN plays as ply \
    ON trd.\"playId\" = ply.\"playId\"       \
    WHERE trd.\"gameId\" = {gameId} AND trd.\"playId\" = {playId} "

    # Execute the "SELECT" query
    pff_joined_df = postgresql_to_dataframe(conn, query, column_names)

    df = pff_joined_df.loc[pff_joined_df['gameId']==gameId]
    df = df.loc[df['playId']==playId]

    df_presnap = pd.DataFrame()

    for oneFrame in pff_joined_df['frameId'].unique():
        one_frame = df.loc[df['frameId'] == oneFrame]


        # reset index (saving the original index as a column) and set new index as player ID 
        one_frame = one_frame.reset_index().set_index('nflId')
        one_frame = one_frame[one_frame.displayName.notnull()]

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

        offense = (
        'QB','RB','WR','TE','FB','T','G','C',
        'QB1','QB2','QB3',
        'RB1','RB2','RB3','RB4',
        'WR','WR1','WR2','WR3','WR4','WR5','WR6','WR7','WR8',
        'TE','TE1','TE2','TE3','TE4',
        'FB1','FB2','FB3',
        'T','T1','T2','T3','T4',
        'G','G1','G2','G3','G4',
        'C','C1','C2','C3'
        )


        one_frame = one_frame[['nflId','gameId','playId','displayName','officialPosition','playDescription','frameId','x','y','QB']]



        # append to output dataframe
        df_presnap = df_presnap.append(one_frame)

        # creating distance from QB


        # creating pressure value
        pressureValue = (1 / df_presnap['QB'])*100

        df_presnap['pressureValue'] = pressureValue

        pressureDF = df_presnap

        # Using DataFrame.isin() to Create Filter
        # Replace infinite updated data with nan
        pressureDF.replace([np.inf, -np.inf], np.nan, inplace=True)
        # Drop rows with NaN
        pressureDF.dropna(inplace=True)

        with pd.option_context('mode.use_inf_as_na', True):
            pressureDF.dropna(inplace=True)
        
        pressureDF = pressureDF.replace([np.inf, -np.inf], np.nan).dropna(axis=0)

        pd.set_option('mode.use_inf_as_na', True)
        pressureDF.dropna(inplace=True)

        df_filter = pressureDF.isin([np.nan, np.inf, -np.inf])
        # Mask df with the filter
        pressureDF = pressureDF[~df_filter]
        pressureDF.dropna(inplace=True)


        pressureDF = pressureDF[pressureDF.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)]


        


                        # fill the nulled sparse positions with -1, indicating that position was not apparent on a given play and/or frame
        positions = [x for x in df_presnap.columns.values if x not in one_frame.columns.values]
        df_presnap.loc[:, positions] = df_presnap.loc[:, positions].fillna(-1)  

        pressureDF.loc[:,['pressureValue','officialPosition']]
        # Creating Animated Pressure Gauge for individual plays

    df = pressureDF[['officialPosition','pressureValue','frameId']]
    df = df_presnap.pivot_table(values = 'pressureValue',index=['frameId'], columns = 'officialPosition')
    offense = [
        'QB','RB','WR','TE','FB','T','G','C',
        'QB1','QB2','QB3','QB4','QB5','QB6','QB7','QB8',
        'RB1','RB2','RB3','RB4','RB5','RB6','RB7','RB8',
        'WR','WR1','WR2','WR3','WR4','WR5','WR6','WR7','WR8',
        'TE','TE1','TE2','TE3','TE4','TE5','TE6','TE7','TE8',
        'FB1','FB2','FB3','FB4',
        'T','T1','T2','T3','T4','T5','T6','T7','T8',
        'G','G1','G2','G3','G4','G5','G6','G7','G8',
        'C','C1','C2','C3','C4','C5','C6','C7','C8',
        ]

    df.drop(list(df.filter(regex = '1')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '2')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '3')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '4')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '5')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '6')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '7')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '8')), axis = 1, inplace = True)
    df = df.loc[:, df.columns != 'C']
    df = df.loc[:, df.columns != 'G']
    df = df.loc[:, df.columns != 'T']
    df = df.loc[:, df.columns != 'RB']
    df = df.loc[:, df.columns != 'WR']
    df = df.loc[:, df.columns != 'TE']
    df.iloc[:,0:-1] = df.iloc[:,0:-1]
    top_pressure = set()

    playDescription = pff_joined_df.playDescription.loc[1]

    gameDescription = pff_joined_df.gameId.loc[0]

    for index, row in df.iterrows():
        top_pressure |= set(row[row > -1].sort_values(ascending=False).head(6).index)

    df = df[top_pressure]

    return bcr.bar_chart_race(df = df,n_bars=6,sort='desc',title=f'{playDescription}',filename=f'{gameDescription}.html')

returnHtml(2021090900,137)


