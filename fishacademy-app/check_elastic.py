from include.es_client import get_es_client
from include.es_queries import get_players
from include.app_config import ELASTIC_INDEX

list_players = get_players(get_es_client())

if len(list_players)>0 :
    print('Elasticsearch and data import is OK')
