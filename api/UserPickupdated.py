# Import dependencies 
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly
import plotly.animation as animation
import plotly.graph_objects as go
import plotly.io
from raceplotly.plots import barplot
from IPython.display import HTML
import io
from base64 import b64encode

pd.options.mode.chained_assignment = None 
pd.set_option('display.max_columns', None)

import warnings 
warnings.filterwarnings("ignore")

# Import Data
games = pd.read_csv("https://storage.googleapis.com/big-data-bowl/games.csv")
plays = pd.read_csv("https://storage.googleapis.com/big-data-bowl/plays.csv")
players = pd.read_csv("https://storage.googleapis.com/big-data-bowl/players.csv")
week1 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week1.csv", low_memory=False)
week2 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week2.csv", low_memory=False)
week3 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week3.csv", low_memory=False)
week4 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week4.csv", low_memory=False)
week5 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week5.csv", low_memory=False)
week6 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week6.csv", low_memory=False)
week7 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week7.csv", low_memory=False)
week8 = pd.read_csv("https://storage.googleapis.com/big-data-bowl/week8.csv", low_memory=False)

pffScoutingData = pd.read_csv("https://storage.googleapis.com/big-data-bowl/pffScoutingData.csv")

tracking = week1.append([
    week2,
    week3,
    week4,
    week5,
    week6,
    week7,
    week8,])

joined_all = pd.merge(games,plays,how="inner",on = "gameId")
joined_all = pd.merge(joined_all,tracking,how="inner",on=["gameId","playId"])
# left join on players to keep football records
joined_all = pd.merge(joined_all,players,how="left",on = "nflId")
joined_all = pd.merge(joined_all,pffScoutingData,how="left",on=["gameId","playId",'nflId'])



# This function is designed for the user to pick specific plays to analyze
def pickingAnimatedPlay(df):
    # do work
    return userInputs(df)

# User input on selecting a play 
# Select Team, Formation, Pass Result
def userInputs(df):

    # Colors for each NFL team and Color for Football
    colors = {
    'ARI':"#97233F", 
    'ATL':"#A71930", 
    'BAL':'#241773', 
    'BUF':"#00338D", 
    'CAR':"#0085CA", 
    'CHI':"#C83803", 
    'CIN':"#FB4F14", 
    'CLE':"#311D00", 
    'DAL':'#003594',
    'DEN':"#FB4F14", 
    'DET':"#0076B6", 
    'GB':"#203731", 
    'HOU':"#03202F", 
    'IND':"#002C5F", 
    'JAX':"#9F792C", 
    'KC':"#E31837", 
    'LA':"#003594", 
    'LAC':"#0080C6", 
    'LV':"#000000",
    'MIA':"#008E97", 
    'MIN':"#4F2683", 
    'NE':"#002244", 
    'NO':"#D3BC8D", 
    'NYG':"#0B2265", 
    'NYJ':"#125740", 
    'PHI':"#004C54", 
    'PIT':"#FFB612", 
    'SEA':"#69BE28", 
    'SF':"#AA0000",
    'TB':'#D50A0A', 
    'TEN':"#4B92DB", 
    'WAS':"#5A1414", 
    'football':'#CBB67C'}
  
    # load data here
    df = joined_all
    # An empty Pandas DataFrame is created to hold and return all user inputs
    gameList = pd.DataFrame()

    # Create a while loop to return incorrect user inputs
    # Choosing an offensive team
    while True:       
        try:
            offTeam = df['possessionTeam'].unique()
            teams = offTeam
            teamOff_Input = input(f'Pick an Offensive Team: {teams}')
            off_team = teamOff_Input.upper()

        except ValueError:
            print(f'Choose a team from the list: {teams}')
            continue

        if off_team not in offTeam:
            print(f'{off_team} does not exist. Input Valid Team Abbreviation')
            continue
        
        elif off_team in offTeam:
            team = df.loc[df['possessionTeam']==teamOff_Input.upper()] 
            next
            
        # Choosing a defensive team
        while True:
            try:
                teamPlayed = team['defensiveTeam'].unique()
                teamsDE = teamPlayed    
                teamDEF_Input = input(f'Chose a Defensive Team: {teamsDE}')
                def_team = teamDEF_Input.upper()

            except ValueError:
                print(f'Choose a team from the list: {def_team}')
                continue

            if teamDEF_Input.upper() not in teamPlayed:
                print(f"{def_team} did not play {off_team} " + "\n" + "choose another Defensive Team")
                continue

            elif teamDEF_Input.upper() in teamPlayed:
                team_defense = team.loc[team['defensiveTeam']==teamDEF_Input.upper()]
                next

        # Choosing specific game if multiple games against the defense exist
            while True:
                try:
                    gamePlayed = team_defense['gameDate'].unique()
                    uniqueGame = gamePlayed
                    game_input = input(f'Choose which game to analyze: {uniqueGame}')

                except ValueError:
                    print(f'Choose a date from the list: {uniqueGame}')
                    continue

                if game_input not in gamePlayed:
                    print(f'Choose a date from the list: {uniqueGame}')
                    continue

                elif game_input in gamePlayed:
                    unique_Game = team_defense.loc[team_defense['gameDate'] == game_input]
                    next

        # Choosing a pass play result
                while True:
                    try:
                        passPlayResult = unique_Game['passResult'].unique()
                        playResult = passPlayResult
                        passPlay_Input = input(f'Choose a pass play result: {playResult}')
                        passInput = passPlay_Input.upper()
                        playResult = unique_Game['passResult'].tolist()
                    
                    except ValueError:
                        print(f'{off_team} did not have any {passInput} against {def_team}')
                        continue

                    if passInput not in playResult:
                        print(f"There were no {passInput} plays found" + "\n" + "choose another play result")
                        continue

                    elif passInput.upper() in playResult:
                        pass_play_result = unique_Game.loc[unique_Game['passResult']==passInput.upper()]   
                        next

        # Choosing where play happened on field
                    while True:
                        try:
                            yardLine = pass_play_result['absoluteYardlineNumber'].unique()
                            ydLine = yardLine
                            ydLine_Input = int(input(f'Which part of the field do you want to analyzie? {ydLine}'))
                            side_of_field = ydLine_Input
                        
                        except ValueError:
                            print(f'{off_team} did not play at that {ydLine_Input}')
                            continue

                        if ydLine_Input not in yardLine:
                            print(f'{off_team} did not play on {ydLine_Input}. Choose another {yardLine}')
                            continue

                        elif ydLine_Input in yardLine:
                            field_of_play = pass_play_result.loc[pass_play_result['absoluteYardlineNumber']==side_of_field]
                
        # Chosing an offensive formation
                        while True:
                            try:
                                OFF_formation = field_of_play['offenseFormation'].unique()
                                team_formation = OFF_formation
                                offFormation_Input = input(f'Choose an Offensive Formation: {team_formation}')
                                formation = offFormation_Input.upper()
                                offFormation = field_of_play['offenseFormation'].tolist()

                            except ValueError:
                                print(f'{off_team} did not play any {formation} this game')
                                continue

                            if offFormation_Input.upper() not in offFormation:
                                print(f"No {formation} plays against {def_team} found" + "\n" + "choose another formation")
                                continue

                            elif offFormation_Input.upper() in offFormation:
                                off_formation = field_of_play.loc[field_of_play['offenseFormation']==offFormation_Input.upper()]       
                                gameList = gameList.append(off_formation)

        # Creating Animation from selected play
                            
                                selected_play_df = gameList
                                selected_tracking_df = gameList

                                sorted_frame_list = selected_tracking_df.frameId.unique()
                                sorted_frame_list.sort()

                                # get play General information 
                                line_of_scrimmage = selected_play_df.absoluteYardlineNumber.values[0]
                                first_down_marker = line_of_scrimmage + selected_play_df.yardsToGo.values[0]
                                down = selected_play_df.down.values[0]
                                quarter = selected_play_df.quarter.values[0]
                                gameClock = selected_play_df.gameClock.values[0]
                                playDescription = selected_play_df.playDescription.values[0]

                                # Handle case where we have a really long Play Description and want to split it into two lines
                                if len(playDescription.split(" "))>15 and len(playDescription)>115:
                                    playDescription = " ".join(playDescription.split(" ")[0:16]) + "<br>" + " ".join(playDescription.split(" ")[16:])

                                # initialize plotly start and stop buttons for animation
                                updatemenus_dict = [
                                    {
                                        "buttons": [
                                            {
                                                "args": [None, {"frame": {"duration": 100, "redraw": False},
                                                            "fromcurrent": True, "transition": {"duration": 0}}],
                                                "label": "Play",
                                                "method": "animate"
                                            },
                                            {
                                                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                                                "mode": "immediate",
                                                                "transition": {"duration": 0}}],
                                                "label": "Pause",
                                                "method": "animate"
                                            }
                                        ],
                                        "direction": "left",
                                        "pad": {"r": 10, "t": 87},
                                        "showactive": False,
                                        "type": "buttons",
                                        "x": 0.1,
                                        "xanchor": "right",
                                        "y": 0,
                                        "yanchor": "top"
                                    }
                                ]
                                # initialize plotly slider to show frame position in animation
                                sliders_dict = {
                                    "active": 0,
                                    "yanchor": "top",
                                    "xanchor": "left",
                                    "currentvalue": {
                                        "font": {"size": 20},
                                        "prefix": "Frame:",
                                        "visible": True,
                                        "xanchor": "right"
                                    },
                                    "transition": {"duration": 300, "easing": "cubic-in-out"},
                                    "pad": {"b": 10, "t": 50},
                                    "len": 0.9,
                                    "x": 0.1,
                                    "y": 0,
                                    "steps": []
                                }

                                frames = []
                                for frameId in sorted_frame_list:
                                    data = []
                                    # Add Numbers to Field 
                                    data.append(
                                        go.Scatter(
                                            x=np.arange(20,110,10), 
                                            y=[5]*len(np.arange(20,110,10)),
                                            mode='text',
                                            text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
                                            textfont_size = 30,
                                            textfont_family = "Courier New, monospace",
                                            textfont_color = "#ffffff",
                                            showlegend=False,
                                            hoverinfo='none'
                                        )
                                    )
                                    data.append(
                                        go.Scatter(
                                            x=np.arange(20,110,10), 
                                            y=[53.5-5]*len(np.arange(20,110,10)),
                                            mode='text',
                                            text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
                                            textfont_size = 30,
                                            textfont_family = "Courier New, monospace",
                                            textfont_color = "#ffffff",
                                            showlegend=False,
                                            hoverinfo='none'
                                        )
                                    )
                                    # Add line of scrimage 
                                    data.append(
                                        go.Scatter(
                                            x=[line_of_scrimmage,line_of_scrimmage], 
                                            y=[0,53.5],
                                            line_dash='dash',
                                            line_color='blue',
                                            showlegend=False,
                                            hoverinfo='none'
                                        )
                                    )
                                    # Add First down line 
                                    data.append(
                                        go.Scatter(
                                            x=[first_down_marker,first_down_marker], 
                                            y=[0,53.5],
                                            line_dash='dash',
                                            line_color='yellow',
                                            showlegend=False,
                                            hoverinfo='none'
                                        )
                                    )
                                    # Plot Players
                                    for team in selected_tracking_df.team.unique():
                                        plot_df = selected_tracking_df[(selected_tracking_df.team==team)&(selected_tracking_df.frameId==frameId)].copy()
                                        if team != "football":
                                            hover_text_array=[]
                                            for nflId in plot_df.nflId:
                                                selected_player_df = plot_df[plot_df.nflId==nflId]
                                                hover_text_array.append("nflId:{}<br>displayName:{}<br>Position:{}<br>Role:{}".format(selected_player_df["nflId"].values[0],
                                                                                                                selected_player_df["displayName"].values[0],
                                                                                                                selected_player_df["pff_positionLinedUp"].values[0],
                                                                                   selected_player_df["pff_role"].values[0]))
                                            data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"],mode = 'markers',marker_color=colors[team],name=team,hovertext=hover_text_array,hoverinfo="text"))
                                        else:
                                            data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"],mode = 'markers',marker_color=colors[team],name=team,hoverinfo='none'))
                                    # add frame to slider
                                    slider_step = {"args": [
                                        [frameId],
                                        {"frame": {"duration": 100, "redraw": False},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}
                                    ],
                                        "label": str(frameId),
                                        "method": "animate"}
                                    sliders_dict["steps"].append(slider_step)
                                    frames.append(go.Frame(data=data, name=str(frameId)))
                                    
                                scale=10
                                layout = go.Layout(
                                    autosize=False,
                                    width=120*scale,
                                    height=60*scale,
                                    xaxis=dict(range=[0, 120], autorange=False, tickmode='array',tickvals=np.arange(10, 111, 5).tolist(),showticklabels=False),
                                    yaxis=dict(range=[0, 53.3], autorange=False,showgrid=False,showticklabels=False),

                                    plot_bgcolor='#00B140',
                                    # Create title and add play description at the bottom of the chart for better visual appeal
                                    title=f"{playDescription}"+"<br>"*19+ f"<br>"f"Game Clock: {gameClock}"+"<br>"f"{quarter}Quarter",
                                    updatemenus=updatemenus_dict,
                                    sliders = [sliders_dict]
                                )

                                fig = go.Figure(
                                    data=frames[0]["data"],
                                    layout= layout,
                                    frames=frames[1:]
                                )
                                # Create First Down Markers 
                                for y_val in [0,53]:
                                    fig.add_annotation(
                                            x=first_down_marker,
                                            y=y_val,
                                            text=str(down),
                                            showarrow=False,
                                            font=dict(
                                                family="Courier New, monospace",
                                                size=16,
                                                color="black"
                                                ),
                                            align="center",
                                            bordercolor="black",
                                            borderwidth=2,
                                            borderpad=4,
                                            bgcolor="#ff7f0e",
                                            opacity=1
                                            )

                                return fig
                                        


def returnHTML(gameId,playId):
    print("generating html")
    print(gameId)
    print(playId)

    print(joined_all.count())
    print(joined_all.head())
    # load data here
    print("df loaded")
    df = joined_all.loc[joined_all['gameId']==int(gameId)]
    print(df.count())
    df = df.loc[df['playId']==int(playId)]
    print(df.count())
    print(df.head())

    print("joined data")
    field_animation = pickingAnimatedPlay(df)

    buffer = io.StringIO()
    field_animation.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    return html_bytes
