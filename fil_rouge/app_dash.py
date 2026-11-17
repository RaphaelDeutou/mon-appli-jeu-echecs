"""Exo 4 : la même appli en Dash, avec un drill-down."""

import dash_ag_grid as dag  # noqa: F401
import plotly.express as px  # noqa: F401
from dash import Dash, Input, Output, callback, dcc, html  # noqa: F401

from data import load_data

df = load_data()

app = Dash(__name__, title="Carburants Loiret")
server = app.server

app.layout = html.Div(
    [
        html.H2("Prix par commune : cliquez une barre"),
        # 2. un dcc.Dropdown des carburants (id="carburant") et un dcc.Graph (id="communes")
        # 3. un titre (id="titre-detail") et un dag.AgGrid (id="stations")
    ]
)

# 2. un callback : carburant → les 15 communes les moins chères
# 3. un callback : clic sur une barre (clickData) → les stations de la commune

if __name__ == "__main__":
    app.run(debug=True)
