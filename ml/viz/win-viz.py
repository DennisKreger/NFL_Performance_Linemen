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
    'New York Jets Colors': '#003f2d',
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
    'New York Jets': '#ffffff',
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


def make_plot(home, visitor, home_win, confidence):
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
    ax.set_aspect(1)
    ax.set_ylim(-0.5,2.5)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    make_plot('Washington Commanders', 'SEA', 0, 0.5)
