"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# our database config
USERNAME = 'postgres'
DB_PASSWORD = environ.get('DB_PASSWORD')
PUBLIC_IP = '34.72.136.99'
DBNAME = 'big-data-bowl'

