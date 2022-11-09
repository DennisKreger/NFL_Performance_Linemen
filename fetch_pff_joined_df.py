# from fetch_pff_joined_df import fetch_pff_joined_df
# df = fetch_pff_joined_df('liam', 'T,gnCs\g)|2[*$}^')

import pandas as pd
import psycopg2


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

def fetch_pff_joined_df(user, password):
    param_dic = {
            'database': 'big-data-bowl',
            'user': user,
            'password': password,
            'host': '34.72.136.99',
            'port': 5432,
    }

    # Connect to the database
    conn = connect(param_dic)
    column_names = ["gameId", "playId", "nflId", "week", "homeTeamAbbr", "visitorTeamAbbr",
                    "height", "weight", "birthDate", "collegeName", "officialPosition", "displayName",
                    "quarter", "down", "yardsToGo", "possessionTeam", "defensiveTeam", "yardlineNumber",
                    "gameClock", "preSnapHomeScore", "preSnapVisitorScore", "playResult", "offensiveFormation",
                    "personnelO", "defendersInTheBox", "personnelD", "dropbackType", "pff_playAction", "pff_passCoverage", "pff_passCoverageType",
                    "pff_role", "pff_positionLinedUp", "pff_hit", "pff_hurry", "pff_sack", "pff_beatenByDefender",
                    "pff_hitAllowed", "pff_hurryAllowed", "pff_sackAllowed", "pff_nflIdBlockedPlayer", "pff_blockType", "pff_backFieldBlock",
                    ]
    query = "SELECT pff.\"gameId\", pff.\"playId\",pff.\"nflId\",       \
        gm.week, gm.\"homeTeamAbbr\", gm.\"visitorTeamAbbr\",        \
        plr.height, plr.weight, plr.\"birthDate\",                     \
        plr.\"collegeName\", plr.\"officialPosition\",                 \
        plr.\"displayName\",                                           \
        pl.quarter, pl.down, pl.\"yardsToGo\", pl.\"possessionTeam\",  \
        pl.\"defensiveTeam\", pl.\"yardlineNumber\", pl.\"gameClock\", \
        pl.\"preSnapHomeScore\", pl.\"preSnapVisitorScore\",           \
        pl.\"playResult\", pl.\"offenseFormation\",                    \
        pl.\"personnelO\", pl.\"defendersInBox\", pl.\"personnelD\",   \
        pl.\"dropbackType\",  pl.\"pff_playAction\",                   \
        pl.\"pff_passCoverage\", pl.\"pff_passCoverageType\",          \
        pff.pff_role, pff.\"pff_positionLinedUp\", pff.pff_hit,        \
        pff.pff_hurry, pff.pff_sack, pff.\"pff_beatenByDefender\",     \
        pff.\"pff_hitAllowed\", pff.\"pff_hurryAllowed\",              \
        pff.\"pff_sackAllowed\", pff.\"pff_nflIdBlockedPlayer\",       \
        pff.\"pff_blockType\", pff.\"pff_backFieldBlock\"              \
    FROM pffscoutingdata as pff                                         \
    LEFT JOIN plays as pl                                               \
    ON pff.\"gameId\" = pl.\"gameId\"                                   \
    AND pff.\"playId\" = pl.\"playId\"                                  \
    LEFT JOIN games as gm                                               \
    ON pff.\"gameId\" = gm.\"gameId\"                                   \
    LEFT JOIN players as plr                                            \
    ON pff.\"nflId\" = plr.\"nflID\"                                    \
    WHERE plr.\"officialPosition\" IN ('C', 'G', 'T', 'TE') "

    # Execute the "SELECT" query
    pff_joined_df = postgresql_to_dataframe(conn, query, column_names)
    return pff_joined_df