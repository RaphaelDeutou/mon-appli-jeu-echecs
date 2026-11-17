"""Exo 4 : la même appli en Dash, avec un drill-down. Fin à 15h00.

Question : quelles ouvertures coûtent des points, et dans quelles parties ?
À produire : un clic sur une barre d'ouverture liste les parties, un clic sur une partie liste
les coups jugés mauvais, dans deux AG Grid.
Lancer : uv run python fil_rouge/app_dash.py   (http://127.0.0.1:8050)
"""

import dash_ag_grid as dag  # noqa: F401
import plotly.express as px  # noqa: F401
from dash import Dash, Input, Output, callback, dcc, html  # noqa: F401

from data import load_coups, load_data  # noqa: F401

app = Dash(__name__, title="Mes parties d'échecs")
server = app.server  # Dash tourne sur Flask

app.layout = html.Div(
    [
        html.H2("Quelles ouvertures me coûtent des points ? Cliquez une barre"),
        # TODO 1. un dcc.Graph (id="familles")
        # TODO 2. un dag.AgGrid (id="parties"), une ligne sélectionnable à la fois
        # TODO 3. un dag.AgGrid (id="coups")
    ]
)

# TODO 4. callback : clickData de "familles" -> les parties de cette famille
# TODO 5. callback : selectedRows de "parties" -> les coups jugés de cette partie

if __name__ == "__main__":
    app.run(debug=False, port=8050)
