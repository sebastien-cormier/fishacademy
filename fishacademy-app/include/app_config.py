import os

APP_VERSION = "0.0.2"
APP_VERSION_DATE = "Lundi 2 septembre 2024"

# Elasticsearch
ELASTIC_HOST = os.environ['ELASTIC_HOST']
ELASTIC_USER = 'elastic'
ELASTIC_PASSWORD = os.environ['ELASTIC_PASSWORD']
ELASTIC_CERTIFICAT = os.environ['ELASTIC_CERTIFICAT']
ELASTIC_INDEX = 'fishacademy'

INIT_DATAS_DOC_ID = os.environ['INIT_DATAS_DOC_ID']
INIT_DATAS_DOC_URL = f"https://docs.google.com/spreadsheets/d/{INIT_DATAS_DOC_ID}/export?format=csv"

PICKLE_NEXT_SESSION = '/datas/next_session.obj'

# CSV
CSV_NEXT_SESSION = '/datas/next_game_registration.csv'
CSV_CURRENT_SESSION = '/datas/current_session.csv'
