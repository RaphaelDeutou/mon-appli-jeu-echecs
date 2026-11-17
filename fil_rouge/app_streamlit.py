"""Exo 2 : l'appli Streamlit du fil rouge, sans assistant de code."""

import plotly.express as px  # noqa: F401
import streamlit as st

from data import load_data

st.set_page_config(page_title="Carburants Loiret", layout="wide")
print("relance")  # regardez le terminal à chaque clic


def get_data():  # 6. mettez-la en cache : @st.cache_data(ttl=600)
    return load_data()


df = get_data()
st.title("Où faire le plein dans le Loiret ?")

# 3. Barre latérale : un selectbox pour le carburant, un multiselect pour les communes (avec key=)

# 4. Trois st.metric : prix médian, le moins cher, nombre de stations

# 5. La carte et l'histogramme, côte à côte (st.columns)
