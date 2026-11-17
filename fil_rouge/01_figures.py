"""Exo 1 : trois figures sur les prix des carburants."""

import plotly.express as px  # noqa: F401

from data import load_data

df = load_data()
print(df.shape)

# 1. Le prix médian par carburant, route contre autoroute (px.bar, barmode="group")

# 2. La carte des stations pour le gazole (px.scatter_map, n'oubliez pas center=)

# 3. La répartition des prix d'un carburant de votre choix (px.histogram)
