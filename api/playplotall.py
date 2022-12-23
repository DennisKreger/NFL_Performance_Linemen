# Importing dependencies
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
from matplotlib.animation import FuncAnimation
from sklearn.preprocessing import LabelEncoder
from os import environ, path
from dotenv import load_dotenv
import psycopg2, sys

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
dbPassword = environ.get('DB_PASSWORD')

PARAMS = {
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
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    return conn


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


def playgifs(gameId, playId):
    # Connect and query from database
    conn = connect(PARAMS)
    print('Fetching plays')
    column_names = [
        "gameId",
        "playId",
        "playDescription"
    ]
    query = f'''
        SELECT ALL
            p."gameId",
            p."playId",
            p."playDescription"
        FROM plays AS p
        WHERE p."gameId" = {gameId} AND p."playId" = {playId}
        '''
    plays = postgresql_to_dataframe(conn, query, column_names)

    print('Fetching qbpressure')
    column_names = [
        "gameId",
        "playId",
        "frameId",
        "distance",
        "x",
        "y"
    ]
    query = f'''
        SELECT ALL
            qbp."gameId",
            qbp."playId",
            qbp."frameId",
            qbp."distance",
            qbp."x",
            qbp."y"
        FROM qbpressure AS qbp
        WHERE qbp."gameId" = {gameId} AND qbp."playId" = {playId}
        '''
    qbpressure = postgresql_to_dataframe(conn, query, column_names)

    print('Fetching tracking')
    column_names = [
        "gameId",
        "playId",
        "frameId",
        "nflId",
        "team",
        "x",
        "y"
    ]
    query = f'''
        SELECT ALL
            t."gameId",
            t."playId",
            t."frameId",
            t."nflId",
            t."team",
            t."x",
            t."y"
        FROM trackingdata AS t
        WHERE t."gameId" = {gameId} AND t."playId" = {playId}
        '''
    tracking = postgresql_to_dataframe(conn, query, column_names)

    print('Fetching qbproximity')
    column_names = [
        "gameId", 
        "playId",
        "nflId2",
        "matchupOpposing",
        "distance"
    ]
    query = f'''
        SELECT ALL
            qbp."gameId",
            qbp."playId",
            qbp."nflId2",
            qbp."matchupOpposing",
            qbp."distance"
        FROM qbproximity AS qbp
        WHERE qbp."gameId" = {gameId} AND qbp."playId" = {playId} AND qbp."matchupOpposing" = 1
        '''
    qbproximity = postgresql_to_dataframe(conn, query, column_names)

    print('Fetching matchups')
    column_names = [
        "gameId", 
        "playId",
        "nflId_defender",
        "nflId_offender",
        "matchup_win",
        "displayName_defender",
        "displayName_offender"
    ]
    query = f'''
        SELECT ALL
            mu."gameId",
            mu."playId",
            mu."nflId_defender",
            mu."nflId_offender",
            mu."matchup_win",
            p."displayName",
            p2."displayName"
        FROM matchups AS mu
        LEFT JOIN players AS p
        ON p."nflID" = mu."nflId_defender"
        LEFT JOIN players AS p2
        ON p2."nflID" = mu."nflId_offender"
        WHERE mu."gameId" = {gameId} AND mu."playId" = {playId};
        '''
    matchups = postgresql_to_dataframe(conn, query, column_names)

    # Find and merge max play pressure of each matched player
    player_max_pressure = qbproximity[['nflId2', 'distance']].groupby(['nflId2']).min().reset_index()
    matchups = matchups.merge(
        player_max_pressure,
        left_on=['nflId_defender'],
        right_on=['nflId2']
    ).sort_values(by='distance', ascending=True)\
    .sort_values(by='matchup_win', ascending=False)

    # Create a GIF for no player matchup selected
    no_matchup = playplot(
                gameId,
                playId,
                plays,
                qbpressure,
                tracking,
                {
                    'gameId': gameId,
                    'playId': playId,
                    'nflId_defender': 0,
                    'nflId_offender': 0,
                    'matchup_win': 0,
                    'displayName_defender': 'N/A',
                    'displayName_offender': 'N/A',
                    'distance': 0
                }
            )

    # Loop through matchups to generate GIFs
    matchup_data = []
    for i, matchup in matchups.iterrows():
        if matchup['displayName_defender'] == 0:
            next
        matchup_data.append([
            matchup['displayName_defender'],
            matchup['displayName_offender'],
            f'{matchup["distance"]:.2f}',
            'Defense' if matchup['matchup_win'] == 1 else 'Offense',
            playplot(
                gameId,
                playId,
                plays,
                qbpressure,
                tracking,
                matchup
            )
        ])

    return matchup_data, no_matchup


def playplot(
    gameId,
    playId,
    plays,
    qbpressure,
    tracking,
    matchup
):
    # Extract matchup features
    nflId_defender = matchup['nflId_defender']
    nflId_offender = matchup['nflId_offender']
    matchup_win = matchup['matchup_win']
    print(f'Plotting matchup: {nflId_defender} vs {nflId_offender}')

    # Get play description
    play_description = plays[(plays['gameId'] == gameId) & (plays['playId'] == playId)]['playDescription'].iloc[0]

    # Encode plot colors
    LE = LabelEncoder()
    tracking['color_code'] = LE.fit_transform(tracking['team'])
    tracking.loc[tracking['nflId'] == nflId_defender, 'color_code'] = 3
    tracking.loc[tracking['nflId'] == nflId_offender, 'color_code'] = 4
    

    # Define play features
    teams = tracking[tracking['team'] != 'football']['team'].unique().tolist()
    info = f'{" vs ".join(teams)} | gameId: {gameId} | playId: {playId}'
    play_description = plays[(plays['gameId'] == gameId) & (plays['playId'] == playId)]['playDescription'].iloc[0]
    scrim_x = tracking[
        (tracking['team'] == 'football') &\
        (tracking['frameId'] == 1)
    ]['x'].iloc[0]

    # Build base plot
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [19, 1]})
    fig.set_figheight(6.5)
    fig.set_figwidth(12)

    # ax[1] is the pressure gauge
    ax[1].get_yaxis().set_visible(False)
    ax[1].get_xaxis().set_visible(False)

    r = Rectangle((0, 0), 1, 1, facecolor = 'indianred')
    ax[1].add_patch(r)
    g = Rectangle((0, 0), 1, 1, facecolor = 'green')
    ax[1].add_patch(g)

    # ax[0] is the play plot itself
    ax[0].set_xlim(0, 120)
    ax[0].set_ylim(0, 53.3)
    ax[0].set_xlabel(play_description, fontsize=8)
    ax[0].set_title(info)

    # Add yard lines
    for i in range(10, 120, 10):
        ax[0].axvline(i, color='w')
        
    # Define line of scrimmage
    ax[0].axvline(scrim_x, color='y')

    # Color field
    ax[0].set_facecolor("darkgray")
    ax[0].add_patch(Rectangle((10, 0), 100, 53.3, facecolor = 'gainsboro'))
        
    # Format yardline labels
    ax[0].get_yaxis().set_visible(False)
    ax[0].set_xticks(range(20, 110, 10), [10, 20, 30, 40, 50, 40, 30, 20, 10], fontsize=24, color='w')
    ax[0].tick_params(
        axis="x",
        direction="in",
        pad=-30,
        top=False,
        labeltop=True,
        bottom=False,
        labelbottom=True
    )

    # Initialize scatter plot
    scatter = ax[0].scatter([], [],zorder=10)
    c = Circle((5, 5), radius=1, alpha=0.25, color='gray',zorder=5)
    ax[0].add_patch(c)

    # Function to update plot animation
    def update(frameId):
        # Get data for just this play
        tracking_frame = tracking.loc[
            (tracking['frameId'] == frameId)
        ]

        # Add dummy players to force color scheme
        if len(tracking_frame) > 0:
            tracking_frame = pd.concat([tracking_frame, pd.DataFrame({
                'gameId': [gameId, gameId, gameId, gameId, gameId],
                'playId': [playId, playId, playId, playId, playId],
                'frameId': [frameId, frameId, frameId, frameId, frameId],
                'nflId': [0, 0, 0, 0, 0],
                'team': ['NA', 'NA', 'NA', 'NA', 'NA'],
                'x': [-10, -10, -10, -10, -10],
                'y': [-10, -10, -10, -10, -10],
                'color_code': [0, 1, 2, 3, 4]
            })])

        # Update scatter plot
        scatter.set_offsets(np.c_[tracking_frame['x'], tracking_frame['y']])
        scatter.set_array(tracking_frame['color_code'])
        
        # Animate QB pocket circle
        qb_slice = qbpressure.loc[
            (qbpressure['frameId'] == frameId+1)
        ]
        pressure = qb_slice['distance'].iloc[0]
        x = qb_slice['x'].iloc[0]
        y = qb_slice['y'].iloc[0]
        c.set(radius=pressure)
        c.center=(x, y)
        
        # Animate pressure gauge
        r.set(width=1 - (pressure/10), alpha = 1 - (pressure/10))
        g.set(width=1 - (pressure/10), alpha = (pressure/10))
        
        return scatter, c, r, g

    # Animate plot
    anim = FuncAnimation(fig, update, frames=tracking['frameId'].max(), interval=100, repeat=True)

    # Save plot
    writergif = animation.PillowWriter(fps=10)
    filename = f'images/playplot_{gameId}_{playId}_{int(nflId_defender)}_{int(nflId_offender)}.gif'
    anim.save(f'static/{filename}', writer=writergif)
    return filename


if __name__ == '__main__':
    gameId = 2021091904
    playId = 2030

    print(playgifs(
        gameId,
        playId
    ))