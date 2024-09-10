import pandas as pd

from datetime import datetime
import dateutil.parser

from include.app_config import ELASTIC_INDEX
from include.utils import serie_to_euro_format, convert_series_to_date, serie_reformat_isodate

# Commons queries
QUERY_MATCH_ALL = { "match_all": {}}
QUERY_FILTER_SELL_OR_BUY_CHIPS = { "bool": { "filter": [ { "terms": { "tx_type": ["BUY_CHIPS","SELL_CHIPS"] } } ] } }

def get_query_filter_by_type(_tx_type) :
	return { "bool": { "filter": [ { "term": { "tx_type": _tx_type } } ] } }

def get_players(_client) :
	"""
	Get all players from the index
	"""
	aggs_ = { "player_agg": { "terms": { "field": "player" } } }
	resp = _client.search(index=ELASTIC_INDEX, size=0, query=QUERY_MATCH_ALL, aggs=aggs_)
	list_players = []
	for bucket in resp['aggregations']['player_agg']['buckets']:
		list_players.append(bucket["key"])
	return list_players



def get_sessions(_client) :
	"""
	Get all games session from the index
	"""
	aggs_ = { "session_agg": { "terms": { "field": "session" } } }
	resp = _client.search(index=ELASTIC_INDEX, size=0, query=QUERY_MATCH_ALL, aggs=aggs_)
	list_sessions = []
	for bucket in resp['aggregations']['session_agg']['buckets']:
		list_sessions.append(bucket["key"])
	return list_sessions


def get_last_transactions(_client, _size=10) :
	"""
	Get last transactions from the index
	"""
	query_ = {
		"bool": {
			"filter": [
				{ "term": { "tx_type": "TRANSFERT" } },
				{ "range": { "amount": { "gte": 0 } } }
			]
		}
	}
	resp = _client.search(index=ELASTIC_INDEX, size=_size, query=query_, sort='@timestamp:desc')
	list_transfert = []
	for hit in resp['hits']['hits']:
		list_transfert.append( {
				"Date": hit["_source"]["@timestamp"],
				"Emetteur": hit["_source"]["player"],
				"Beneficiaire": hit["_source"]["beneficiary"],
				"Montant": round(float(hit["_source"]["amount"]),2),
				"Moyen": hit["_source"]["method"]
			})
	df_ = pd.DataFrame(list_transfert)
	df_['Montant'] = serie_to_euro_format(df_['Montant'])
	df_['Date'] = serie_reformat_isodate(df_['Date'])
	return df_


def index_game_session(_client, _df_session) :
	"""
	Save the whole game session in the index once it's validate
	"""
	_df_session = _df_session.sort_values('@timestamp', ascending=True)
	_df_session['@timestamp_ts'] = convert_series_to_date(_df_session['@timestamp'])

	for index, row in _df_session.iterrows() :
		doc = {
			"@timestamp": row['@timestamp_ts'],
			"session": str(row['session']),
			"player": str(row['player']),
			"tx_type": str(row['tx_type']),
			"amount": str(row['amount']),
			"beneficiary": str(row['beneficiary'])
		}
		resp = _client.index(index=ELASTIC_INDEX, document=doc)

def get_leaderboard(_client) :
	"""
	Get the historical winning amount for all players
	"""
	aggs_ = {
	    "player_agg": {
	      "terms": {
	        "field": "player"
	      },
	      "aggs": {
	        "winninf_aggs": {
	          "sum": {
	            "field": "amount"
	          }
	        },
	        "winning_bucket_sort": {
	          "bucket_sort": {
	            "sort": [
	              { "winninf_aggs": { "order": "desc" } } 
	            ],
	            "size": 100                                
	          }
	        }
	      }
	    }
	  }
	resp = _client.search(index=ELASTIC_INDEX, size=0, query=QUERY_FILTER_SELL_OR_BUY_CHIPS, aggs=aggs_)

	result = []
	for bucket in resp['aggregations']['player_agg']['buckets']:
		result.append({"Joueur":bucket["key"], "winning":round(float(bucket["winninf_aggs"]["value"]),2)})
	df_ = pd.DataFrame(result)
	df_['Gains Totaux'] = serie_to_euro_format(df_['winning'])

	return df_[['Joueur','Gains Totaux']]



def get_games(_client) :
	"""
	Get last sessions with the winner and associated amount
	"""
	aggs_ = {
	    "session_agg": {
	      "terms": {
	        "field": "session"
	      },
	      "aggs": {
	        "player_aggs": {
	          "terms": {
	            "field": "player"
	          },
	          "aggs": {
	            "winning_aggs": {
	              "sum": {
	                "field": "amount"
	              }
	            },
	            "winning_bucket_sort": {
	              "bucket_sort": {
	                "sort": [
	                  {
	                    "winning_aggs": {
	                      "order": "desc"
	                    }
	                  }
	                ],
	                "size": 1
	              }
	            }
	          }
	        }
	      }
	    }
	  }

	resp = _client.search(index=ELASTIC_INDEX, size=0, query=QUERY_FILTER_SELL_OR_BUY_CHIPS, aggs=aggs_)

	result = []
	for bucket in resp['aggregations']['session_agg']['buckets']:
		result.append(
			{
				"Parties":bucket["key"], 
				"Vainqueur":bucket["player_aggs"]['buckets'][0]['key'], 
				"winning":round(float(bucket["player_aggs"]['buckets'][0]['winning_aggs']['value']),2)
			}
		)

	df_ = pd.DataFrame(result)
	df_['Gains'] = serie_to_euro_format(df_['winning'])
	
	return df_[['Parties','Vainqueur','Gains']].sort_values("Parties", ascending=False)



def get_winning_history(_client, _player) :

	query_ = {
		"bool": {
			"filter": [
				{ "terms": { "tx_type": [ "BUY_CHIPS", "SELL_CHIPS" ] } },
				{ "term": { "player": _player } }
			]
		}
	}
	aggs_ = {
	    "session_agg": {
			"terms": { "field": "session" },
			"aggs": {
				"player_aggs": { "terms": { "field": "player" },
				"aggs": {
					"winning_aggs": { "sum": { "field": "amount" } }
					}
				}
			}
	    }
	}
	resp = _client.search(index=ELASTIC_INDEX, size=0, query=query_, aggs=aggs_)

	result = []
	for bucket in resp['aggregations']['session_agg']['buckets']:
		result.append(
			{
				"Player" : _player,
				bucket["key"] : round(float(bucket["player_aggs"]['buckets'][0]['winning_aggs']['value']),2), 
			}
		)
	return pd.DataFrame(result).groupby('Player').sum()



def get_wallet(_client) :
	"""
	Compute all player Wallet
	"""
	aggs_ = {
	    "player_aggs": {
	      "terms": { "field": "player" },
	      "aggs": {
	        "money_aggs": {
	          "sum": {
	            "field": "amount"
	          }
	        },
	        "money_bucket_sort": {
	          "bucket_sort": {
	            "sort": [ { "money_aggs": {  "order": "desc" } } ],
	            "size": 10
	          }
	        }
	      }
	    }
	  }
	resp = _client.search(index=ELASTIC_INDEX, size=0, query=QUERY_MATCH_ALL, aggs=aggs_)

	result = []
	for bucket in resp['aggregations']['player_aggs']['buckets']:
		name = bucket["key"]
		amount_ = round(float(bucket["money_aggs"]["value"]),2)
		if name=="Sebastien" : # Cas particulier -> C'est la banque d'un point de vu comptable
			name="Banque (Seb)"
			amount_ = -amount_

		result.append({"Joueur":name, "money":amount_})
	df_ = pd.DataFrame(result)
	df_['Solde'] = serie_to_euro_format(df_['money'])

	return df_[['Joueur','Solde']]

def index_transaction(es_client, player_from, player_to, amount_, method_, session_) :
	doc = {
	  "@timestamp": datetime.now().isoformat(),
	  "session": session_,
	  "player": player_from,
	  "tx_type": 'TRANSFERT',
	  "amount": amount_,
	  "beneficiary": player_to,
	  "method": method_,
	  "notes": 'created with fishacademy app'
	}
	resp = es_client.index(index=ELASTIC_INDEX, document=doc)
	doc = {
	  "@timestamp": datetime.now().isoformat(),
	  "session": session_,
	  "player": player_to,
	  "tx_type": 'TRANSFERT',
	  "amount": -amount_,
	  "beneficiary": player_from,
	  "method": method_,
	  "notes": 'created with fishacademy app'
	}
	resp = es_client.index(index=ELASTIC_INDEX, document=doc)

def get_rebuy_per_sessions(_client) :
	"""
	Get all rebuy sum for each player for each sessions
	"""
	aggs_ = {
		"player_agg": {
		"terms": {
			"field": "player"
		},
		"aggs": {
			"session_agg": {
			"terms": {
				"field": "session"
			},
			"aggs": {
				"amount": {
				"sum": {
					"field": "amount"
				}
				}
			}
			}
		}
		}
	}
	resp = _client.search(index=ELASTIC_INDEX, size=0, query=get_query_filter_by_type("BUY_CHIPS"), aggs=aggs_)
	
	result = []
	for bucket_player in resp['aggregations']['player_agg']['buckets']:
		player_ = bucket_player["key"]
		max_amount_ = 0.0
		cumul_amount_ = 0.0
		session_count_ = 0
		for bucket_session in bucket_player['session_agg']['buckets']:
			session_count_ = session_count_ + 1
			amount_ = -float(bucket_session["amount"]["value"])
			cumul_amount_ = round( (cumul_amount_ + amount_), 2)
			if max_amount_ < amount_ : 
				max_amount_ = round(amount_,2)

		avg_rebuy_ = round( ((cumul_amount_ / session_count_) / 10.0), 2)
		result.append({"Joueur":player_, "Nb sessions":session_count_, "Recaves (moy.)": avg_rebuy_, "Max.": max_amount_})
	df_ = pd.DataFrame(result)

	return df_[['Joueur','Nb sessions','Recaves (moy.)','Max.']]