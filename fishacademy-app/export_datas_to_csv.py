import pandas as pd
import csv

from elasticsearch import Elasticsearch

from include.es_client import get_es_client
from include.es_queries import export_all_datas
from include.app_config import ELASTIC_INDEX, CSV_EXPORT_FILE
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

if not es_client.indices.exists(index=ELASTIC_INDEX) :
  print(f"Index '{ELASTIC_INDEX}' not found in elasticsearch.")

df_export_ = export_all_datas(es_client)
df_export_.to_csv(CSV_EXPORT_FILE, 
                  sep = '\t', 
                  encoding = 'utf-8', 
                  index = False, 
                  na_rep = '', 
                  #quotechar = '"',
                  #quoting = csv.QUOTE_NONNUMERIC
                  )
