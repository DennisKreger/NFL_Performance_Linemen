# Presentation

## Team Members

Dennis Kreger - [Github](https://github.com/DennisKreger)

Liam Selfors - [Github](https://github.com/liam-selfors)

Greg Winkelman - [Github]()

Robert Loesch - [Github](https://github.com/googlecloudlab)


## Selected topic

The team has selected to participate in a Kaggle competition for the [NFL Big Data Bowl 2023](https://www.kaggle.com/competitions/nfl-big-data-bowl-2023) and is planning to submit an entry into the competition. 

The topic of the 2023 NFL Big Data Bowl competition is Linemen on Pass Plays. Quarterbacks may get the glory, but some of the most important work takes place a few feet in front of them. The offensive line protects the passer, providing precious seconds to find receivers downfield. At the same time, the opposing team’s defensive line attempts to find a disruptive path. If a defender sneaks through, it can mean a sack, a blocked pass, or even a turnover. Some of the game’s most important plays happen on the line and this competition examines the data behind the hardest workers in football.



## Reasons for selecting the topic

The team is enthusiastic about sports and football in particular. Some team members strive to be Sports Data Scientists, and the opportunity to present findings and results, would be life changing on its own. Getting exposure to Kaggle and the potential to win the competition would also showcase skills in data science and would be useful for future job opportunities. In addition, there is a $10,000 prize that the team members could win. Greg also has experience with the performance side of things (insight-wise), as that is what a lot of his schooling/background is in. 


## Description of the source of data

In this competition, the team have access to the NFL’s Next Gen Stats data, including player tracking, play, game, and player information, as well as Pro Football Focus (PFF) scouting data for 2021 passing plays (Weeks 1-8 of the NFL season). The team will create new metrics and stats for America's most popular sports league. 

The competition has provided a set of data by the NFL Next Gen Stats team. There is also scouting data that is provided by Pro Football Focus. The team might decide to bring in supplemental NFL data if needed. Such supplemental data must be free and publicly available.

Here is a high level description of the data that is provided by the competition:

- Game data: The games.csv contains the teams playing in each game. The key variable is gameId.

- Play data: The plays.csv file contains play-level information from each game. The key variables are gameId and playId.

- Player data: The players.csv file contains player-level information from players that participated in any of the tracking data files. The key variable is nflId.

- PFF Scouting data: The pffScoutingData.csv file contains player-level scouting information for each game and play. The key variables are gameId, playId, and nflId.

- Tracking data: Files week[week].csv contain player tracking data from season [week]. The key variables are gameId, playId, and nflId.


## Questions we hope to answer with the data

The team will participate in the Kaggle competition of the Metric track. The team hopes to create a metric to assess performance and/or strategy. This can be focused on offensive or defensive players, and on teams or individuals.

The team has gathered a list of ideas for analyzing the data:

- Detect offensive or defensive formations from an image taken just before the snap, then we could use that data to evaluate which formations perform better against others.

- Analyze if the initial direction of each lineman against starting formations has an impact on successful sacks vs  unsuccessful. Great opportunity to cut down the data a bit through SQL transformations and train a model to predict sack outcomes. The intended strategic insight would be to predict the optimal direction a lineman should move on snap to position them best to successfully make contact with the QB.