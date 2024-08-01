import pandas as pd

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



def get_next_session() :
	return pd.read_csv(CSV_NEXT_SESSION, 
					usecols = ["player", "iscoming"],
					dtype = {
						'player': 'string',
						'iscoming': 'int'
						})

