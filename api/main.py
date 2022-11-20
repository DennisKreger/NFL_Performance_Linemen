from flask import Flask,request,render_template,url_for,jsonify,redirect,flash
from flask_sqlalchemy import SQLAlchemy
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
