import os

# Elasticsearch
ELASTIC_HOST = os.environ['ELASTIC_HOST']
ELASTIC_USER = 'elastic'
ELASTIC_PASSWORD = os.environ['ELASTIC_PASSWORD']
ELASTIC_CERTIFICAT = os.environ['ELASTIC_CERTIFICAT']
ELASTIC_INDEX = 'fishacademy'

# CSV
CSV_INIT_DATAS = 'FishAcademyCompta - transactions.csv'
CSV_NEXT_SESSION = '/datas/next_game_registration.csv'
CSV_CURRENT_SESSION = '/datas/current_session.csv'
