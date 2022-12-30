# Importing dependencies
import pandas as pd
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

def get_matchups(gameId, playId):
    # Connect and query from database
    conn = connect(PARAMS)

    # Find matchups
    print('Fetching matchups')
    column_names = [
        "gameId", 
        "playId",
        "nflId_defender",
        "displayName_defender",
        "nflId_offender",
        "displayName_offender",
        "matchup_duration",
        "matchup_broken",
        "trouble_generated",
        "pressure_gain",
        "pressure_gain_pct",
    ]
    query = f'''
        SELECT ALL
            mu."gameId",
            mu."playId",
            mu."nflId_defender",
            p."displayName",
            mu."nflId_offender",
            p2."displayName",
            mu."matchup_duration",
            mu."matchup_broken",
            mu."trouble_generated",
            mu."pressure_gain",
            mu."pressure_gain_pct"
        FROM matchupsall AS mu
        LEFT JOIN players AS p
        ON p."nflID" = mu."nflId_defender"
        LEFT JOIN players AS p2
        ON p2."nflID" = mu."nflId_offender"
        WHERE mu."gameId" = {gameId} AND mu."playId" = {playId};
        '''
    matchups = postgresql_to_dataframe(conn, query, column_names)

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

    player_max_pressure = qbproximity[['nflId2', 'distance']].groupby(['nflId2']).min().reset_index()
    matchups = matchups.merge(
        player_max_pressure,
        left_on=['nflId_defender'],
        right_on=['nflId2']
    ).sort_values(by='distance', ascending=True)\
    .sort_values(by='trouble_generated', ascending=False)

    matchup_data = []
    for i, matchup in matchups.iterrows():
        if matchup['displayName_defender'] == 0:
            next
        matchup_data.append([
            matchup['displayName_defender'],
            matchup['displayName_offender'],
            f'{matchup["distance"]:.2f}',
            f'{matchup["matchup_duration"]/10:.2f}sec',
            f'{matchup["matchup_broken"]==1}',
            f'{matchup["trouble_generated"]==1}',
            f'{matchup["pressure_gain"]==1}',
            f'{matchup["pressure_gain_pct"]:.2%}',
        ])

    return matchup_data


if __name__ == '__main__':
    print(get_matchups(2021090900, 97))