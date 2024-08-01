import pandas as pd

from pathlib import Path
from include.es_client import get_es_client
from include.es_queries import get_players

from include.app_config import *

FLAG_NO_ANSWER = 0
FLAG_PRESENT = 1
FLAG_ABSENT = 2

def save_registration(_df, _player, _is_coming) :
	# Suppression de la ligne existante
	df_ = _df.loc[_df.player!=_player]

	# Ajout de la nouvelle inscription
	new_row = pd.DataFrame({'player':_player, 'iscoming':_is_coming}, index=[0])
	df_ = pd.concat([df_.loc[:],new_row]).reset_index(drop=True)

	# Enregistrement du fichier
	df_.to_csv('/datas/next_game_registration.csv', encoding='utf-8')


def init_next_session_file() :
	df_=pd.DataFrame()
	for p_ in get_players(get_es_client()) :
		new_row = pd.DataFrame({'player':p_, 'iscoming':0}, index=[0])
		df_ = pd.concat([df_.loc[:],new_row]).reset_index(drop=True)
	df_.to_csv(CSV_NEXT_SESSION, sep=',', encoding='utf-8')

def get_next_session() :
	if not Path(CSV_NEXT_SESSION).is_file() :
		init_next_session_file()
	
	return pd.read_csv(CSV_NEXT_SESSION,
					usecols = ["player", "iscoming"],
					dtype = {
						'player': 'string',
						'iscoming': 'int'})

