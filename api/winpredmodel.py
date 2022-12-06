# Import dependencies
import pandas as pd
from scipy.stats import norm
import pickle

import warnings
warnings.filterwarnings('ignore')

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


def winpred(home, visitor):
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
    
    if prediction_confidence < 0.5:
        return ('Too close to call!', 0.5)

    if predicted_score_difference > 0:
        return (prediction_data_cleaned['Team'].iloc[1], prediction_confidence)
    else:
        return (prediction_data_cleaned['Team'].iloc[0], prediction_confidence)

    return predicted

if __name__ == "__main__":
    print('Testing...')
    print(winpred('Green Bay Packers', 'Philadelphia Eagles'))