import os

APP_VERSION = "0.1.0"
APP_VERSION_DATE = "Lundi 13 janvier 2025"

SESSION_PREFIX = 'Session CG #'

DATE_ZONE_INFO = "Europe/Paris"

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
CSV_CURRENT_SESSION = '/datas/current_session.csv'
CSV_EXPORT_FILE = '/datas/fishacademy_transactions.csv'
CSV_SESION_BACKUP_FILE = '/datas/session_backup/session_backup_<DATE>.csv'

# PLAYERS
RESGISTERED_PLAYERS = ["JC","Sebastien","Adrien","Kevin","Arnaud","Eric","Quentin","Baptiste","Willy","Gauthier","Lyes"]
