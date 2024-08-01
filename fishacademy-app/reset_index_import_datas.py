import pandas as pd

from elasticsearch import Elasticsearch

from include.es_client import get_es_client
from include.app_config import ELASTIC_INDEX, CSV_INIT_DATAS
from include.utils import convert_series_to_date

def convert_euros_to_float(_value) :
    return float(_value.replace('€', '').replace(',', '.').replace(' ', ''))

settings_and_mappings = '''
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "session": {
        "type": "keyword"
      },
      "player": {
        "type": "keyword"
      },
      "tx_type": {
        "type": "keyword"
      },
      "amount": {
        "type": "float"
      },
      "beneficiary": {
        "type": "keyword"
      },
      "method": {
        "type": "keyword"
      },
      "notes": {
        
        "type": "text"
      }
    }
  }
}'''

es_client = get_es_client()

if es_client.indices.exists(index=ELASTIC_INDEX) :
  print(f"Deleting index '{ELASTIC_INDEX}' from elasticsearch.")
  es_client.indices.delete(index=ELASTIC_INDEX)

print(f"Creating index '{ELASTIC_INDEX}' with settings and mappungs.")
es_client.indices.create(index=ELASTIC_INDEX, ignore=400, body=settings_and_mappings)

print(f"Import datas from CSV file.")
print(f"Load data from {CSV_INIT_DATAS}...")
df = pd.read_csv('/datas/FishAcademyCompta - transactions.csv')
df['date'] = convert_series_to_date(df['date'])
df['montant'] = df['montant'].apply(lambda x: convert_euros_to_float(x)).astype(float)
df['beneficiaire'] = df['beneficiaire'].fillna("NULL")
df['methode'] = df['methode'].fillna("NULL")
df['notes'] = df['notes'].fillna("NULL")
for index, row in df.iterrows() :
	doc = {
	  "@timestamp": row['date'].isoformat(),
	  "session": row['session'],
	  "player": row['joueur'],
	  "tx_type": row['type'],
	  "amount": str(row['montant']),
	  "beneficiary": row['beneficiaire'],
	  "method": row['methode'],
	  "notes": row['notes']
	}
	resp = es_client.index(index=ELASTIC_INDEX, document=doc)

