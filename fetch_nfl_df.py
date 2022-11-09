# from fetch_nfl_df import fetch_pff_joined_df
# df = fetch_nfl_df(table_name, user, pass)

import pandas as pd
import psycopg2


TABLE_COLUMNS = {
    'games': [
        'gameId',
        'season',
        'week',
        'gameDate',
        'gameTimeEastern',
        'homeTeamAbbr',
        'visitorTeamAbbr'
    ],
    'pffscoutingdata': [
        'gameId',
        'playId',
        'nflId',
        'pff_role',
        'pff_positionLinedUp',
        'pff_hit',
        'pff_hurry',
        'pff_sack',
        'pff_beatenByDefender',
        'pff_hitAllowed',
        'pff_hurryAllowed',
        'pff_sackAllowed',
        'pff_nflIdBlockedPlayer',
        'pff_blockType',
        'pff_backFieldBlock'
    ],
    'players': [
        'nflID',
        'height',
        'weight',
        'birthDate',
        'collegeName',
        'officialPosition',
        'displayName'
    ],
    'plays': [
        'gameId',
        'playId',
        'playDescription',
        'quarter',
        'down',
        'yardsToGo',
        'possessionTeam',
        'defensiveTeam',
        'yardlineSide',
        'yardlineNumber',
        'gameClock',
        'preSnapHomeScore',
        'preSnapVisitorScore',
        'passResult',
        'penaltyYards',
        'prePenaltyPlayResult',
        'playResult',
        'foulName1',
        'foulNFLId1',
        'foulName2',
        'foulNFLId2',
        'foulName3',
        'foulNFLId3',
        'absoluteYardlineNumber',
        'offenseFormation',
        'personelO',
        'defendersInBox',
        'personnelD',
        'dropbackType',
        'pff_playAction',
        'pff_passCoverage',
        'pff_passCoverageType'
    ],
    'trackingdata': [
        'gameId',
        'playId',
        'nflId',
        'frameId',
        'time',
        'jerseyNumber',
        'team',
        'playDirection',
        'x',
        'y',
        's',
        'a',
        'dis',
        'o',
        'dir',
        'event'
    ]
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
    print("Connection successful")
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

def fetch_nfl_df(table_name, user, password):
    param_dic = {
            'database': 'big-data-bowl',
            'user': user,
            'password': password,
            'host': '34.72.136.99',
            'port': 5432,
    }

    # Connect to the database
    conn = connect(param_dic)
    query = f"SELECT * FROM {table_name}"

    # Execute the "SELECT" query
    pff_joined_df = postgresql_to_dataframe(conn, query, TABLE_COLUMNS[table_name])
    return pff_joined_df