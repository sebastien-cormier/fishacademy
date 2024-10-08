import os

APP_VERSION = "0.1.0"
APP_VERSION_DATE = "jeudi 26 septembre 2024"

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

PICKLE_NEXT_SESSION = '/datas/fishacademy/next_session.obj'

# CSV
CSV_CURRENT_SESSION = '/datas/fishacademy/current_session.csv'
CSV_EXPORT_FILE = '/datas/fishacademy/fishacademy_transactions.csv'
CSV_SESION_BACKUP_FILE = '/datas/fishacademy/session_backup/session_backup_<DATE>.csv'