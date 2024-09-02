import streamlit as st

from datetime import datetime

import pandas as pd
import numpy as np

from include.app_config import *
from include.es_client import get_es_client
from include.es_queries import get_leaderboard, get_games
from include.next_session import get_next_session

es_client = get_es_client()
next_session = get_next_session()

st.markdown("# Accueil")
st.sidebar.markdown("# Accueil")
st.sidebar.image('../resources/fishacademy.png', caption='Fish Academy')

st.markdown(f"La prochaine partie a lieu chez {next_session['host']} le {next_session['date']}.")

col1, col2 = st.columns(2)

col1.markdown("## Leaderboard")
df_leaderboard = get_leaderboard(es_client)
col1.dataframe(df_leaderboard.set_index(df_leaderboard.columns[0]))

col2.markdown("## Dernières parties")
df_last_games = get_games(es_client)
col2.dataframe(df_last_games.set_index(df_last_games.columns[0]))

st.divider()
st.write(f"Version __{APP_VERSION}__")
st.write(f"Déployé le _{APP_VERSION_DATE}_")