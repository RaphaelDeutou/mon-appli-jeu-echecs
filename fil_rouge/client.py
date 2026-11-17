"""Exo 5 : une appli Streamlit qui appelle le service FastAPI (lancer api.py d'abord)."""

import os

import requests  # noqa: F401
import streamlit as st

API = os.environ.get("API_URL", "http://localhost:8000")

st.title("Estimer le prix d'une station")

with st.form("simulation"):
    carburant = st.selectbox("Carburant", ["GAZOLE", "E10", "SP95", "SP98", "E85", "GPLC"])
    axe = st.radio("Axe", ["Route", "Autoroute"], horizontal=True)
    lat = st.number_input("Latitude", 47.5, 48.4, 47.90)
    lon = st.number_input("Longitude", 1.5, 3.1, 1.90)
    envoyer = st.form_submit_button("Estimer")

# À vous : si envoyer, un requests.post vers f"{API}/predict", puis st.metric du prix estimé.
# Affichez l'erreur moyenne du modèle, et un message lisible si l'API répond 422.
