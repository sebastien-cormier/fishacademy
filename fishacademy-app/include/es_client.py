from elasticsearch import Elasticsearch

from include.app_config import *

def get_es_client() :
    return Elasticsearch(ELASTIC_HOST, ca_certs=ELASTIC_CERTIFICAT, basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD))

