import streamlit as st

import pandas as pd
import numpy as np

from include.app_config import *
from include.next_session import save_registration, get_next_session, FLAG_ABSENT, FLAG_NO_ANSWER, FLAG_PRESENT

df = get_next_session()

list_player = df.player.unique()

next_game_host = df.iloc[0].player
number_of_players = df.loc[df.iscoming==FLAG_PRESENT].shape[0]

st.markdown("# Prochaine session : 27 août")
st.sidebar.markdown("# Prochaine partie")

with st.sidebar.expander("Inscription", expanded=True):
	with st.form("registration"):

		registered_player = st.selectbox("Qui ?",list_player)
		options = [":man-shrugging: Sais pas encore...", ":white_check_mark: je viens !", ":x: Je ne viens pas."]
		is_coming_radio = st.radio(
		    "Présence", options, label_visibility='collapsed', 
		    index=None,
		)
		submit = st.form_submit_button('Valider')

		if submit:
			save_registration(df, registered_player, options.index(is_coming_radio))
			st.rerun()

st.markdown(f"La prochaine partie aura lieu le mardi 27 août chez {next_game_host} (ou chez JC).")
st.markdown(f"Nombre de joueurs confirmés : __{number_of_players} joueurs__.")

st.header(":white_check_mark: Présents")

st.markdown(f"- {next_game_host} (hôte)")
for index, row in df.iloc[1:].loc[df.iscoming==FLAG_PRESENT].iterrows() :
	st.markdown(f"- {row.player}")

st.header(":x: Absents")
for index, row in df.iloc[1:].loc[df.iscoming==FLAG_ABSENT].iterrows() :
	st.markdown(f"- {row.player}")

st.header(":man-shrugging: En attente de réponse")
for index, row in df.iloc[1:].loc[df.iscoming==FLAG_NO_ANSWER].iterrows() :
	st.markdown(f"- {row.player}")

st.markdown(f":information_source: _Pour lister un nouveau joueur, contacter Sébastien._")
