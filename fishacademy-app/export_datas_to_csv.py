from include.es_client import get_es_client
from include.es_queries import export_all_datas
from include.app_config import ELASTIC_INDEX, CSV_EXPORT_FILE

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
