# Import dependencies
import pandas as pd
from scipy.stats import norm
import pickle, mpld3
import matplotlib.pyplot as plt

team_abbr = {
    'TB': 'Tampa Bay Buccaneers',
    'ATL': 'Atlanta Falcons',
    'BUF': 'Buffalo Bills',
    'CAR': 'Carolina Panthers',
    'CIN': 'Cincinnati Bengals',
    'DET': 'Detroit Lions',
    'HOU': 'Houston Texans',
    'IND': 'Indianapolis Colts',
    'TEN': 'Tennessee Titans',
    'WAS': 'Washington Redskins',
    'KC': 'Kansas City Chiefs',
    'NE': 'New England Patriots',
    'NO': 'New Orleans Saints',
    'NYG': 'New York Giants',
    'LA': 'Los Angeles Rams',
    'LV': 'Oakland Raiders',
    'CHI': 'Chicago Bears',
    'CLE': 'Cleveland Browns',
    'JAX': 'Jacksonville Jaguars',
    'MIA': 'Miami Dolphins',
    'NYJ': 'New York Jets',
    'PHI': 'Philadelphia Eagles',
    'PIT': 'Pittsburgh Steelers',
    'ARI': 'Arizona Cardinals',
    'LAC': 'Los Angeles Chargers',
    'SEA': 'Seattle Seahawks',
    'BAL': 'Baltimore Ravens',
    'GB': 'Green Bay Packers',
    'DEN': 'Denver Broncos',
    'MIN': 'Minnesota Vikings',
    'SF': 'San Francisco 49ers',
    'DAL': 'Dallas Cowboys'
}
team_colors_primary = {
    'Arizona Cardinals': '#97233f',
    'Atlanta Falcons': '#a71930',
    'Baltimore Ravens': '#241773',
    'Buffalo Bills': '#00338d',
    'Carolina Panthers': '#0085ca',
    'Chicago Bears': '#0b162a',
    'Cincinnati Bengals': '#000000',
    'Cleveland Browns': '#311d00',
    'Dallas Cowboys': '#002244',
    'Denver Broncos': '#fb4f14',
    'Detroit Lions': '#0076b6',
    'Green Bay Packers': '#203731',
    'Houston Texans': '#03202f',
    'Indianapolis Colts': '#002c5f',
    'Jacksonville Jaguars': '#006778',
    'Kansas City Chiefs': '#e31837',
    'Los Angeles Chargers': '#002244',
    'Los Angeles Rams': '#002244',
    'Miami Dolphins': '#008e97',
    'Minnesota Vikings': '#4f2683',
    'New England Patriots': '#002244',
    'New Orleans Saints': '#d3bc8d',
    'New York Giants': '#0b2265',
    'New York Jets': '#003f2d',
    'Oakland Raiders': '#a5acaf',
    'Las Vegas Raiders': '#a5acaf',
    'Philadelphia Eagles': '#004c54',
    'Pittsburgh Steelers': '#000000',
    'San Francisco 49ers': '#aa0000',
    'Seattle Seahawks': '#002244',
    'Tampa Bay Buccaneers': '#d50a0a',
    'Tennessee Titans': '#002244',
    'Washington Redskins': '#773141',
    'Washington Commanders': '#773141'
}
team_colors_secondary = {
    'Arizona Cardinals': '#000000',
    'Atlanta Falcons': '#000000',
    'Baltimore Ravens': '#9e7c0c',
    'Buffalo Bills': '#c60c30',
    'Carolina Panthers': '#000000',
    'Chicago Bears': '#c83803',
    'Cincinnati Bengals': '#fb4f14',
    'Cleveland Browns': '#ff3c00',
    'Dallas Cowboys': '#869397',
    'Denver Broncos': '#002244',
    'Detroit Lions': '#b0b7bc',
    'Green Bay Packers': '#ffb612',
    'Houston Texans': '#a71930',
    'Indianapolis Colts': '#a5acaf',
    'Jacksonville Jaguars': '#000000',
    'Kansas City Chiefs': '#ffb612',
    'Los Angeles Chargers': '#0073cf',
    'Los Angeles Rams': '#b3995d',
    'Miami Dolphins': '#f26a24',
    'Minnesota Vikings': '#ffc62f',
    'New England Patriots': '#c60c30',
    'New Orleans Saints': '#d3bc8d',
    'New York Giants': '#a71930',
    'New York Jets': '#000000',
    'Oakland Raiders': '#000000',
    'Las Vegas Raiders': '#000000',
    'Philadelphia Eagles': '#a5acaf',
    'Pittsburgh Steelers': '#a5acaf',
    'San Francisco 49ers': '#b3995d',
    'Seattle Seahawks': '#69be28',
    'Tampa Bay Buccaneers': '#34302b',
    'Tennessee Titans': '#4b92db',
    'Washington Redskins': '#ffb612',
    'Washington Commanders': '#ffb612'
}

# Read offensive and defensive stats historical through 2011
season_stats_offense = pd.read_csv('https://storage.googleapis.com/big-data-bowl/season-stats-offense.csv', encoding='latin')
season_stats_defense = pd.read_csv('https://storage.googleapis.com/big-data-bowl/season-stats-defense.csv', encoding='latin')

# Loading prediction model
model = pickle.load(open('win-prediction-linear.pkl','rb'))

# Pre-define standard deviations
stdev_correct = 3.166981126573886
stdev_incorrect = 2.869264824251112

# Merge offensive and defensive season stats
season_stats = season_stats_offense.merge(
    season_stats_defense,
    on='Team',
    suffixes=('_offensive', '_defensive')
)

# Create "Next Season" column for merging results data
season_stats['Next Season'] = season_stats['Season_offensive'] + 1
season_stats.drop(['Season_defensive', 'Season_offensive'], axis=1, inplace=True)
season_stats = season_stats.groupby(['Next Season', 'Team']).first().reset_index()

# Filter next season for 2021
season_stats = season_stats[season_stats['Next Season'] == 2021]


def make_plot(home, visitor, home_win, confidence):
    plt.clf()
    if home in team_abbr.keys():
        home = team_abbr[home]
    if visitor in team_abbr.keys():
        visitor = team_abbr[visitor]
    plt.plot(
        [5,-0.35,-0.35,5],
        [0,0,2,2],
        color=team_colors_primary[home],
        linewidth=9
    )
    plt.plot(
        [5,-0.2,-0.2,5],
        [0.15,0.15,1.85,1.85],
        color=team_colors_secondary[home],
        linewidth=6
    )
    plt.plot(
        [5,10.35,10.35,5],
        [0,0,2,2],
        color=team_colors_primary[visitor],
        linewidth=9
    )
    plt.plot(
        [5,10.2,10.2,5],
        [0.15,0.15,1.85,1.85],
        color=team_colors_secondary[visitor],
        linewidth=6
    )
    plt.plot(
        [5,5],
        [-0.1,2.1],
        color='white',
        linewidth=9
    )
    plt.plot(
        [5+(0.5-home_win)*20*(confidence-0.5),5+(0.5-home_win)*20*(confidence-0.5)],
        [0.4,1.6],
        color='black',
        linewidth=4,
        solid_capstyle='round'
    )
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_ylim(-0.5,2.5)
    plt.axis('off')
    filename = f'images/winpred_temp.jpg'
    plt.savefig(f'static/{filename}', bbox_inches ='tight')
    return filename

def winpred(home, visitor):

    home = team_abbr[home]
    visitor = team_abbr[visitor]

    # Gather and merge stats
    home_stats = season_stats[season_stats['Team'] == home]
    visitor_stats = season_stats[season_stats['Team'] == visitor]

    home_stats['isHome'] = 1
    visitor_stats['isHome'] = 0

    prediction_data = pd.merge(
        home_stats, visitor_stats,
        on='Next Season',
        suffixes=('_home', '_visitor')
    )

    # Split data into home and visitor DataFrames and concatenate offensive and opposing defensive from each
    home_prediction_data = prediction_data[[
        col for col in prediction_data.columns if \
            ('_offensive_home' in col) or \
            ('_defensive_visitor' in col) or \
            (col in ['Team_home', 'isHome_home'])
    ]]
    home_prediction_data.rename(columns={col: col.replace('_home', '').replace('_visitor', '_opposing') for col in home_prediction_data.columns}, inplace=True)

    visitor_prediction_data = prediction_data[[
        col for col in prediction_data.columns if \
            ('_offensive_visitor' in col) or \
            ('_defensive_home' in col) or \
            (col in ['Team_visitor', 'isHome_visitor'])
    ]]
    visitor_prediction_data.rename(columns={col: col.replace('_visitor', '').replace('_home', '_opposing') for col in visitor_prediction_data.columns}, inplace=True)
    prediction_data_cleaned = pd.concat([visitor_prediction_data, home_prediction_data])

    # Format home column for prediction
    prediction_data_cleaned['isHomeTeam'] = prediction_data_cleaned['isHome']
    prediction_data_cleaned.drop(columns=['isHome'], inplace=True)
    prediction_data_cleaned.fillna(0, inplace=True)

    # Make predictions
    predictions = model.predict(prediction_data_cleaned.drop(columns=['Team']))

    # Process predictions
    predicted_score_difference = predictions[1] - predictions[0]
    prediction_data_cleaned['predictions'] = predictions
    
    # Calculate confidence
    correct_pdf = norm.pdf(predicted_score_difference,0,stdev_correct)
    incorrect_pdf = norm.pdf(predicted_score_difference,0,stdev_incorrect)
    prediction_confidence = correct_pdf / (correct_pdf + incorrect_pdf)
    print(prediction_confidence)
    if prediction_confidence < 0.5:
        return (
            'This matchup is too close to call!',
            make_plot(home, visitor, 0, 0.5)
        )

    if predicted_score_difference > 0:
        return (
            f'The predicted winner is the {home} with a confidence of {format_pct(prediction_confidence)}.',
            make_plot(home, visitor, 1, prediction_confidence)
        )
    else:
        return (
            f'The predicted winner is the {visitor} with a confidence of {format_pct(prediction_confidence)}.',
            make_plot(home, visitor, 1, prediction_confidence)
        )

def format_pct(dec):
    return str(round(dec*100,2)) + '%'

if __name__ == "__main__":
    print('Testing...')
    print(winpred('GB', 'DAL'))