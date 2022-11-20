# Flask

## Running API on local dev environment

### Install required dependencies:
pip install psycopg2-binary
pip install flask-sqlalchemy
pip install Flask-Migrate


### Configure db user and db password in a .env file 
Create a .env file in the api directory with the user and password as follows:
```
DB_USER='user'
DB_PASSWORD='password'
```

### Configure Flask
export FLASK_APP=app.py

### Run Flask
flask run

