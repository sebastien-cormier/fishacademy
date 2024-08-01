import streamlit as st

from datetime import datetime
from elasticsearch import Elasticsearch

import pandas as pd

from include.es_client import get_es_client
from include.es_queries import get_wallet


df_wallet = get_wallet(get_es_client())

st.markdown("# Compta")
st.sidebar.markdown("# Compta")

st.dataframe(df_wallet.set_index(df_wallet.columns[0]))
