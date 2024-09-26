import streamlit as st

from datetime import datetime
from elasticsearch import Elasticsearch
from time import sleep

import pandas as pd

from include.es_client import get_es_client
from include.es_queries import get_wallet, get_last_transactions, get_players, index_transaction, get_sessions

def get_last_session_name(session_list_) :
	return sorted(session_list_)[-1]
	
es_client = get_es_client()
df_wallet = get_wallet(es_client)
df_transaction = get_last_transactions(es_client)
list_all_players = get_players(es_client)
last_session_name = get_last_session_name(get_sessions(es_client))

st.markdown("# Compta")
st.sidebar.markdown("## Situations comptables")
st.sidebar.dataframe(df_wallet.set_index(df_wallet.columns[0]))

with st.expander("Ajout transaction", expanded=False):
	with st.form("transaction"):
		player_from = st.selectbox("Emetteur",list_all_players)
		player_to = st.selectbox("Beneficiaire",list_all_players)
		amount_ = st.slider("Montant (€)", 0.0, 300.0, 10.0,  0.05)
		options = ["PAYPAL", "CASH", "BANK"]
		method_ = st.radio(
				"Moyen", options, label_visibility='collapsed', 
				index=0,
			)
		submit = st.form_submit_button('Ajouter')
		if submit:
			index_transaction(es_client, player_from, player_to, amount_, method_, last_session_name)
			sleep(1)
			st.rerun()
			
st.markdown("## Dernières transactions")
st.dataframe(df_transaction.set_index(df_transaction.columns[0]))

