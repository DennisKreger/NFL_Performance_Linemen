# Importing dependencies
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
from matplotlib.animation import FuncAnimation
from sklearn.preprocessing import LabelEncoder

# Reading data
matchups = pd.read_csv('https://storage.googleapis.com/big-data-bowl/matchups.csv')
qb_pressure_frames = pd.read_csv('https://storage.googleapis.com/big-data-bowl/qb-pressure-frames.csv')
qb_proximities = pd.read_csv('https://storage.googleapis.com/big-data-bowl/QBProximity-all.csv')

plays = pd.read_csv('https://storage.googleapis.com/big-data-bowl/plays.csv')
week1 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week1.csv')
week2 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week2.csv')
week3 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week3.csv')
week4 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week4.csv')
week5 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week5.csv')
week6 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week6.csv')
week7 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week7.csv')
week8 = pd.read_csv('https://storage.googleapis.com/big-data-bowl/week8.csv')

tracking = pd.concat([
    week1,
    week2,
    week3,
    week4,
    week5,
    week6,
    week7,
    week8
])

def playplot(
    gameId,
    playId
):
    
    matchups_filtered = matchups[
        (matchups['gameId'] == gameId) &\
        (matchups['playId'] == playId)
    ]

    qb_proximities_filtered = qb_proximities[
        (qb_proximities['gameId'] == gameId) &\
        (qb_proximities['playId'] == playId) &\
        (qb_proximities['matchupOpposing'] == 1)
    ]

    player_max_pressure = qb_proximities_filtered[['nflId2', 'distance']].groupby(['nflId2']).min().reset_index()

    matchup = matchups_filtered.merge(
        player_max_pressure,
        left_on=['nflId_defender'],
        right_on=['nflId2']
    ).sort_values(by='distance', ascending=True)\
    .sort_values(by='matchup_win', ascending=False).iloc[0]

    # Extract matchup features
    nflId_defender = matchup['nflId_defender']
    nflId_offender = matchup['nflId_offender']
    matchup_win = matchup['matchup_win']

    # Get play description
    play_description = plays[(plays['gameId'] == gameId) & (plays['playId'] == playId)]['playDescription'].iloc[0]

    # Get tracking data for matchup play
    tracking_play = tracking.loc[
        (tracking['gameId'] == gameId) & \
        (tracking['playId'] == playId)
    ].copy()

    # Encode plot colors
    LE = LabelEncoder()
    tracking_play['color_code'] = LE.fit_transform(tracking_play['team'])
    tracking_play.loc[tracking_play['nflId'] == nflId_defender, 'color_code'] = 3
    tracking_play.loc[tracking_play['nflId'] == nflId_offender, 'color_code'] = 4

    # Get team matchup
    teams = tracking_play[tracking_play['team'] != 'football']['team'].unique().tolist()

    info = f'{" vs ".join(teams)} | Defender Win: {matchup_win == 1} | gameId: {gameId} | playId: {playId}'
    play_description = plays[(plays['gameId'] == gameId) & (plays['playId'] == playId)]['playDescription'].iloc[0]

    scrim_x = tracking_play[
        (tracking_play['team'] == 'football') &\
        (tracking_play['frameId'] == 1)
    ]['x'].iloc[0]

    qb_play_pressure = qb_pressure_frames.loc[
        (qb_pressure_frames['gameId'] == gameId) & \
        (qb_pressure_frames['playId'] == playId)
    ]

    # Build base plot
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [19, 1]})
    fig.set_figheight(6.5)
    fig.set_figwidth(12)

    ax[1].get_yaxis().set_visible(False)
    ax[1].get_xaxis().set_visible(False)
    r = Rectangle((0, 0), 1, 1, facecolor = 'indianred')
    ax[1].add_patch(r)
    g = Rectangle((0, 0), 1, 1, facecolor = 'green')
    ax[1].add_patch(g)


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
    ax[0].set_xticks(range(20, 110, 10), range(10, 100, 10), fontsize=24, color='w')
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
        tracking_frame = tracking_play.loc[
            (tracking_play['frameId'] == frameId)
        ]
        scatter.set_offsets(np.c_[tracking_frame['x'], tracking_frame['y']])
        scatter.set_array(tracking_frame['color_code'])
        
        qb_slice = qb_play_pressure.loc[
            (qb_play_pressure['frameId'] == frameId+1)
        ]
        
        pressure = qb_slice['distance'].iloc[0]
        x = qb_slice['x'].iloc[0]
        y = qb_slice['y'].iloc[0]
        
        c.set(radius=pressure)
        c.center=(x, y)
        
        r.set(width=1 - (pressure/10), alpha = 1 - (pressure/10))
        g.set(width=1 - (pressure/10), alpha = (pressure/10))
        
        return scatter, c, r, g

    # Animate plot
    anim = FuncAnimation(fig, update, frames=tracking_play['frameId'].max(), interval=100, repeat=True)

    writergif = animation.PillowWriter(fps=10)
    filename = f'images/playplot_{gameId}_{playId}.gif'
    anim.save(f'static/{filename}', writer=writergif)
    return filename


if __name__ == '__main__':
    gameId = 2021091904
    playId = 2030

    playplot(
        gameId,
        playId,
        matchups,
        qb_pressure_frames,
        qb_proximities,
        plays,
        tracking
    )