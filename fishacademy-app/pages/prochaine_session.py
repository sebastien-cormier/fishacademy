import streamlit as st

import pandas as pd
import numpy as np

from include.app_config import *
from include.next_session import save_registration, get_next_session, init_next_session_file, FLAG_ABSENT, FLAG_HOST, FLAG_NO_ANSWER, FLAG_PRESENT
from include.es_queries import get_players
from include.es_client import get_es_client

next_session = get_next_session()
default_host = 'JC'
es_client = get_es_client()
list_all_players = get_players(es_client)

if next_session is None :
	
	with st.form("create_next_session"):
		 
		host_ = st.selectbox("Hote de la session ?", list_all_players, index=list_all_players.index(default_host))
		session_date_ = st.date_input("Date de la prochaine session ?")
		submit = st.form_submit_button('Valider')
		if submit:
			init_next_session_file(host_, session_date_)
			st.rerun()

else :

	number_of_players = len(next_session['coming']) + 1
	list_not_answer =  list_all_players.copy()
	list_not_answer.remove(next_session['host'])
	list_all_players_without_host = list_all_players.copy()
	list_all_players_without_host.remove(next_session['host'])

	st.markdown(f"# Prochaine session : {next_session['date']}")
	st.sidebar.markdown("# Prochaine partie")

	with st.sidebar.expander("Inscription", expanded=True):
		with st.form("registration"):

			registered_player = st.selectbox("Qui ?",list_all_players_without_host)
			options = [":man-shrugging: Sais pas encore...", ":white_check_mark: je viens !", ":x: Je ne viens pas."]
			is_coming_radio = st.radio(
				"Présence", options, label_visibility='collapsed', 
				index=None,
			)
			submit = st.form_submit_button('Valider')

			if submit:
				save_registration(next_session, registered_player, options.index(is_coming_radio))
				st.rerun()

	st.markdown(f"La prochaine partie aura lieu le {next_session['date']} chez {next_session['host']}.")
	st.markdown(f"Nombre de joueurs confirmés : __{number_of_players} joueurs__.")

	st.header(":white_check_mark: Présents")

	st.markdown(f"- {next_session['host']} (hôte)")
	for player_ in next_session['coming'] :
		st.markdown(f"- {player_}")
		list_not_answer.remove(player_)

	st.header(":x: Absents")
	for player_ in next_session['not_coming'] :
		st.markdown(f"- {player_}")
		list_not_answer.remove(player_)

	st.header(":man-shrugging: En attente de réponse")
	
	for player_ in  list_not_answer :
		st.markdown(f"- {player_}")
	
	st.markdown(f":information_source: _Pour lister un nouveau joueur, contacter Sébastien._")
