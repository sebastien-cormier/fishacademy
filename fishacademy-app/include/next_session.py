import pandas as pd
import pickle

from pathlib import Path
from include.es_client import get_es_client
from include.es_queries import get_players

from include.app_config import *

FLAG_NO_ANSWER = 0
FLAG_HOST = 1
FLAG_PRESENT = 2
FLAG_ABSENT = 3

def save_registration(_next_session, _player, _is_coming) :

	# Suppression de la ligne existante
	if _player in  _next_session['coming']:  _next_session['coming'].remove(_player)
	if _player in  _next_session['not_coming']: _next_session['not_coming'].remove(_player)

	# Ajout de la nouvelle inscription
	if _is_coming == 2 :
		_next_session['not_coming'].append(_player)

	elif _is_coming == 1 :
		_next_session['coming'].append(_player)

	# Enregistrement du fichier
	with open(PICKLE_NEXT_SESSION, 'wb') as handle:
		pickle.dump(_next_session, handle, protocol=pickle.HIGHEST_PROTOCOL)
	return _next_session


def init_next_session_file(_host, _session_date) :
	next_session_ = {
		"host": _host,
		"date": _session_date.strftime("%d/%m/%Y"),
		"coming": [],
		"not_coming": []
	}
	with open(PICKLE_NEXT_SESSION, 'wb') as handle:
		pickle.dump(next_session_, handle, protocol=pickle.HIGHEST_PROTOCOL)
	return next_session_

def get_next_session() :
	if not Path(PICKLE_NEXT_SESSION).is_file() :
		return None
	else :
		filehandler = open(PICKLE_NEXT_SESSION, 'rb') 
		return pickle.load(filehandler)

def get_next_session_name(_previous_sessions) :
	max_ = 0
	for session_ in _previous_sessions :
		session_num_ = int(session_.replace(SESSION_PREFIX,''))
		if max_ < session_num_ :
			max_ = session_num_

	return f'Session CG #{max_+1}'