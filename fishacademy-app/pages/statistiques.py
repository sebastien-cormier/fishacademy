import streamlit as st

import pandas as pd
from include.es_client import get_es_client
from include.es_queries import get_winning_history, get_players, get_sessions, get_rebuy_per_sessions, get_leaderboard
from include.utils import serie_to_euro_format

# -------------- #
# Initiatisation #
# -------------- #

es_client = get_es_client()
list_sessions = get_sessions(es_client)
list_players = get_players(es_client)

def init_df_winning() :
    df_winning_ = pd.DataFrame()
    for p in get_players(es_client) :
        df_winning_ = pd.concat([df_winning_.loc[:],get_winning_history(es_client,p)])
        
    df_winning_["Session CG #0"] = 0.0
    df_winning_.fillna(0.0, inplace=True)
    df_winning_ = df_winning_.reindex(sorted(df_winning_.columns), axis=1)

    # Parcourt des colonnes pour avoir les gains cumulés au lien des gains de la session
    prev_c = None
    for c_ in df_winning_.columns :
        if prev_c is None :
            prev_c = c_
        else :
            df_winning_[c_] = df_winning_[c_] + df_winning_[prev_c]
            prev_c = c_
    
    return df_winning_

def get_sessions_stats() :
    df_leaderboard = get_leaderboard(es_client)
    df_recaves= get_rebuy_per_sessions(es_client)
    df_stats_sessions = pd.merge(df_leaderboard, df_recaves, left_on='Joueur', right_on='Joueur', how='left')
    df_stats_sessions['Gains moyens'] = serie_to_euro_format(round((df_stats_sessions['winning'] / df_stats_sessions['Nb sessions']), 2))
    return df_stats_sessions[['Joueur','Nb sessions', 'Recaves (moy.)','Max.','Gains moyens']]

# --------- #
# Affichage #
# --------- #

st.sidebar.markdown("# Statistiques")

st.markdown("# Statistiques")
st.divider()
st.markdown("## Evolutions des gains")
st.line_chart(init_df_winning().T)

st.divider()
st.markdown("## Recaves")

df_sessions_stats = get_sessions_stats()
st.dataframe(df_sessions_stats.set_index(df_sessions_stats.columns[0]))
st.write(":information_source: _Une recave correspond à 10 euros._")
