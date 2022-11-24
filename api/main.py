from flask import Flask,request,render_template,url_for,jsonify,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_session import flask_scoped_session
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import datetime
from os import environ, path


# Init App
app = Flask(__name__)
basedir = path.abspath(path.dirname(__file__))
app.config.from_pyfile('config.py')

instance_connection_name = app.config["INSTANCE_CONNECTION_NAME"]  
db_user = app.config["DB_USER"]  
db_pass = app.config["DB_PASS"]  
db_name = app.config["DB_NAME"]  
ip = app.config["PUBLIC_IP"]

# initialize Cloud SQL Python Connector object
def getconn():
    with Connector() as connector:
        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=IPTypes.PUBLIC
        )
        return conn

app = Flask(__name__)

# configuration
# app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{app.config['USERNAME']}:{app.config['DB_PASSWORD']}@{app.config['PUBLIC_IP']}:5432/{app.config['DBNAME']}"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db = SQLAlchemy(app)

# Create A Model For Players Table
class Players(db.Model):
    __tablename__ = 'players'
    nflID = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.String(10))
    weight = db.Column(db.Float)
    birthDate = db.Column(db.String(10))
    collegeName = db.Column(db.String(50))
    officialPosition = db.Column(db.String(3))
    displayName = db.Column(db.String(50))
    age = db.Column(db.Float)
    heightCm = db.Column(db.Float)
    conference = db.Column(db.String(50))
    conferenceId = db.Column(db.Float)

    def __init__(self, nflID, height, weight, birthDate, collegeName, officialPosition, displayName, age, heightCm, conference, conferenceId):
        self.nflID = nflID
        self.height = height
        self.weight = weight
        self.birthDate = birthDate
        self.collegeName = collegeName
        self.officialPosition = officialPosition
        self.displayName = displayName
        self.age = age
        self.heightCm = heightCm
        self.conference = conference
        self.conferenceId = conferenceId

    def __repr__(self):
        return f"<Player {self.displayName}>"

# Create A Model For Games Table
class Games(db.Model):
    __tablename__ = 'games'
    gameId = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    week =  db.Column(db.Integer)
    gameDate = db.Column(db.Date)
    gameTimeEastern = db.Column(db.Time)
    homeTeamAbbr = db.Column(db.String(3))
    visitorTeamAbbr = db.Column(db.String(3))

    def __init__(self, gameId, season, week, gameDate, gameTimeEastern, homeTeamAbbr, visitorTeamAbbr):
        self.gameId = gameId
        self.season = season
        self.week = week
        self.gameDate = gameDate
        self.gameTimeEastern = gameTimeEastern
        self.homeTeamAbbr = homeTeamAbbr
        self.visitorTeamAbbr = visitorTeamAbbr

    def __repr__(self):
        return f"<Game {self.gameId}>"


# Create A Model For Plays Table
class Plays(db.Model):
    __tablename__ = 'plays'
    gameId = db.Column(db.Integer, primary_key=True)
    playId = db.Column(db.Integer, primary_key=True)
    playDescription = db.Column(db.String(500))
    quarter = db.Column(db.Integer)
    down = db.Column(db.Integer)
    yardsToGo = db.Column(db.Integer)
    possessionTeam = db.Column(db.String(3))
    defensiveTeam = db.Column(db.String(3))
    yardlineSide = db.Column(db.String(3))
    yardlineNumber = db.Column(db.Integer)
    gameClock = db.Column(db.String(5))
    preSnapHomeScore = db.Column(db.Integer)
    preSnapVisitorScore = db.Column(db.Integer)
    offenseFormation = db.Column(db.String(50))
    personnelO = db.Column(db.String(50))
    personnelD = db.Column(db.String(50))
    dropbackType = db.Column(db.String(50))
    pff_passCoverage = db.Column(db.String(50))
    pff_passCoverageType = db.Column(db.String(50)) 
 
    def __init__(self, gameId, playId, playDescription, quarter, down, yardsToGo,
                       possessionTeam, defensiveTeam, yardlineSide, yardlineNumber,
                       gameClock, preSnapHomeScore, preSnapVisitorScore,
                       offenseFormation, personnelO, personnelD, dropbackType, 
                       pff_passCoverage, pff_passCoverageType):
        self.gameId = gameId
        self.playId = playId
        self.playDescription = playDescription
        self.quarter = quarter
        self.down = down
        self.yardsToGo = yardsToGo
        self.possessionTeam =  possessionTeam
        self.defensiveTeam = defensiveTeam
        self.yardlineSide = yardlineSide
        self.yardlineNumber = yardlineNumber
        self.gameClock = gameClock
        self.preSnapHomeScore = preSnapHomeScore
        self.preSnapVisitorScore = preSnapVisitorScore
        self.offenseFormation = offenseFormation
        self.personnelO = personnelO
        self.personnelD = personnelD
        self.dropbackType = dropbackType
        self.pff_passCoverage = pff_passCoverage
        self.pff_passCoverageType = pff_passCoverageType

    def __repr__(self):
        return f"<Plays {self.playDescription}>"

# Create A Model For Trackingdata Table
class Trackingdata(db.Model):
    __tablename__ = 'trackingdata'
    gameId = db.Column(db.Integer, primary_key=True)
    playId = db.Column(db.Integer, primary_key=True)
    nflId = db.Column(db.Integer, primary_key=True)
    jerseyNumber = db.Column(db.Integer)
    team = db.Column(db.String(5))

    def __init__(self, gameId, playId, nflId, jerseyNumber, team):
        self.gameId = gameId
        self.playId = playId
        self.nflId = nflId
        self.jerseyNumber = jerseyNumber
        self.team = team

    def __repr__(self):
        return f"<trackingdata {self.jerseyNumber}>"

@app.route('/')
def root():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route('/players',methods=['GET'])
def players():
    players = Players.query.all()
    results = [
        {
            "nflID": player.nflID,
            "height": player.height,
            "weight": player.weight,
            "birthDate": player.birthDate,
            "collegeName": player.collegeName,
            "officialPosition": player.officialPosition,
            "displayName": player.displayName,
            "age": player.age,
            "heightCm": player.heightCm,
            "conference": player.conference,
            "conferenceId": player.conferenceId
        } for player in players]    
    return {"count": len(results), "players": results}


@app.route('/players/<teamAbbr>',methods=['GET'])
def team_players(teamAbbr):
    players = Trackingdata.query.distinct(
                    Trackingdata.nflId
                ).filter(
                    Trackingdata.team==teamAbbr
                ).join(
                    Players, Trackingdata.nflId==Players.nflID
                ).add_columns(
                    Trackingdata.nflId,
                    Trackingdata.jerseyNumber,
                    Trackingdata.team,
                    Players.displayName,
                    Players.officialPosition
                )
    results = [
        {
            "nflId": player.nflId,
            "jerseyNumber": player.jerseyNumber,
            "displayName": player.displayName,
            "officialPosition": player.officialPosition,
            "team": player.team
            
        } for player in players]    
    return {"count": len(results), "players": results}


@app.route('/players/<teamAbbr>/<positions>',methods=['GET'])
def position_team_players(teamAbbr, positions):
    position_list = positions.split(",")
    players = Trackingdata.query.distinct(
                    Trackingdata.jerseyNumber
                ).filter(
                    Trackingdata.team==teamAbbr
                ).join(
                    Players, Trackingdata.nflId==Players.nflID
                ).add_columns(
                    Trackingdata.nflId,
                    Trackingdata.jerseyNumber,
                    Trackingdata.team,
                    Players.displayName,
                    Players.officialPosition
                ).filter(
                    Players.officialPosition.in_(position_list)
                ).order_by(
                    Trackingdata.jerseyNumber
                )
    results = [
        {
            "nflId": player.nflId,
            "jerseyNumber": player.jerseyNumber,
            "displayName": player.displayName,
            "officialPosition": player.officialPosition,
            "team": player.team
            
        } for player in players]    
    return {"count": len(results), "players": results}



@app.route('/plays')
def get_plays():
    plays = Plays.query.all()
    results = [
        {
            "gameId": play.gameId,
            "playId": play.playId,
            "playDescription": play.playDescription,
            "quarter": play.quarter,
            "down": play.down, 
            "yardsToGo": play.yardsToGo,
            "possessionTeam": play.possessionTeam,
            "defensiveTeam": play.defensiveTeam, 
            "yardlineSide": play.yardlineSide, 
            "yardlineNumber": play.yardlineNumber,
            "gameClock": play.gameClock, 
            "preSnapHomeScore": play.preSnapHomeScore, 
            "preSnapVisitorScore": play.preSnapVisitorScore,
            "offenseFormation": play.offenseFormation,
            "personnelO": play.personnelO,
            "personnelD": play.personnelD,
            "dropbackType": play.dropbackType,
            "pff_passCoverage": play.pff_passCoverage,            
            "pff_passCoverageType": play.pff_passCoverageType
        } for play in plays]    
    return {"count": len(results), "plays": results}

@app.route('/offenseFormations')
def offenseFormations():
    results = []
    for play in Plays.query.distinct(Plays.offenseFormation).order_by(Plays.offenseFormation):
        results.append(play.offenseFormation)
    return {"count": len(results), "offenseFormations": results}

@app.route('/personnelO')
def personnelO():
    results = []
    for play in Plays.query.distinct(Plays.personnelO).order_by(Plays.personnelO):
        results.append(play.personnelO)
    return {"count": len(results), "personnelO": results}

@app.route('/personnelD')
def personnelD():
    results = []
    for play in Plays.query.distinct(Plays.personnelD).order_by(Plays.personnelD):
        results.append(play.personnelD)
    return {"count": len(results), "personnelD": results}

@app.route('/dropBackTypes')
def dropBackTypes():
    results = []
    for play in Plays.query.distinct(Plays.dropbackType).order_by(Plays.dropbackType):
        results.append(play.dropbackType)
    return {"count": len(results), "dropBackTypes": results}

@app.route('/passCoverageTypes')
def passCoverageTypes():
    results = []
    for play in Plays.query.distinct(Plays.pff_passCoverageType).order_by(Plays.pff_passCoverageType):
        results.append(play.pff_passCoverageType)
    return {"count": len(results), "pff_passCoverageTypes": results}

@app.route('/passCoverage')
def passCoverage():
    results = []
    for play in Plays.query.distinct(Plays.pff_passCoverage).order_by(Plays.pff_passCoverage):
        results.append(play.pff_passCoverage)
    return {"count": len(results), "pff_passCoverage": results}

@app.route('/games',methods=['GET'])
def games():
    games = Games.query.all()
    results = [
        {
        "gameId": game.gameId,
        "season": game.season,
        "week": game.week,
        "gameDate": game.gameDate,
        "gameTimeEastern": game.gameTimeEastern,
        "homeTeamAbbr": game.homeTeamAbbr,
        "visitorTeamAbbr": game.visitorTeamAbbr
        } for game in games]
    return {"count": len(results), "games": results}

@app.route('/teams',methods=['GET'])
def teams():
    results = []
    for team in Games.query.distinct(Games.homeTeamAbbr).order_by(Games.homeTeamAbbr):
        results.append(team.homeTeamAbbr)
    return {"count": len(results), "teams": results}




if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    with app.app_context():
        db.create_all() # <--- create db object.
    app.run(host='127.0.0.1', port=8080, debug=True)