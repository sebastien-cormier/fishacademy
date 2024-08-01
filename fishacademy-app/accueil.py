import streamlit as st

from datetime import datetime

import pandas as pd
import numpy as np

from include.app_config import *
from include.es_client import get_es_client
from include.es_queries import get_leaderboard, get_games

es_client = get_es_client()

st.markdown("# Accueil")
st.sidebar.markdown("# Accueil")
st.sidebar.image('../resources/fishacademy.png', caption='Fish Academy')

st.markdown("La prochaine partie a lieu chez Sebastien le mardi 30 juillet 2024.")

col1, col2 = st.columns(2)

col1.markdown("## Leaderboard")
df_leaderboard = get_leaderboard(es_client)
col1.dataframe(df_leaderboard.set_index(df_leaderboard.columns[0]))

col2.markdown("## Dernières parties")
df_last_games = get_games(es_client)
col2.dataframe(df_last_games.set_index(df_last_games.columns[0]))
