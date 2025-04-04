import streamlit as st

from include.app_config import *
from include.es_client import get_es_client
from include.es_queries import *
from include.utils import serie_to_euro_format

es_client = get_es_client()
list_sessions = sorted(get_sessions(es_client), key=str.lower, reverse=True)

st.markdown(f"# Historique des sessions")

with st.form("form_session"):
    selected_session = st.selectbox("Session",list_sessions)
    submit = st.form_submit_button('Choisir')

st.markdown(f"Session : {selected_session}")

df_session_result = get_session_result(es_client, selected_session)
df_session_result['Gains'] = serie_to_euro_format(df_session_result['winning'])
df_session_result = df_session_result.drop('winning', axis=1)

st.dataframe(df_session_result.set_index(df_session_result.columns[0]))