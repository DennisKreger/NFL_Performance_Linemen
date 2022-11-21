# Flask

## Running API on local dev environment

### Install required dependencies:
```
pip install psycopg2-binary
pip install flask-sqlalchemy
pip install Flask-Migrate
```

In the api folder, run the following command:
```
pip install -r requirements.txt
```

### Configure db user and db password in a .env file 
Create a .env file in the api directory with the user and password as follows:
```
DB_USER='user'
DB_PASSWORD='password'
```

### Configure Flask
export FLASK_APP=main.py

### Run Flask locally
In the api folder, run the following command:
```
python main.py
```

## Running API on Google Cloud AppEngine

### 

### Setup and configuration

Follow the steps in [this tutorial](https://cloud.google.com/appengine/docs/standard/python3/building-app) for setup and configuration steps

### Deploy
Run the following command from the api directory:
```
gcloud app deploy
gcloud app browse
```



