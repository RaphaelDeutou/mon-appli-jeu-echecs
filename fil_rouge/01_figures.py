"""Exo 1 : trois figures. Environ 25 min.

Question : où ce joueur perd-il des points ?
À produire : trois figures Plotly dont le titre dit ce qu'elles montrent.
Lancer : uv run python fil_rouge/01_figures.py
"""

import plotly.express as px

from data import familles, load_coups, load_data


def main() -> None:
    df, coups = load_data(), load_coups()
    print(f"{df.shape[0]} parties, {coups.shape[0]} coups juges")

    par_famille = familles(df)
    if par_famille.empty:
        raise ValueError("Aucune famille d'ouvertures n'atteint le nombre minimal de parties.")

    figure_familles = px.bar(
        par_famille,
        x="score",
        y="famille",
        orientation="h",
        title="Les familles d'ouvertures où mon score est le plus faible",
        labels={"score": "Score moyen", "famille": "Famille", "n": "Parties", "gaffes": "Gaffes par partie"},
        hover_data=["n", "gaffes"],
    )
    figure_familles.update_yaxes(autorange="reversed")
    figure_familles.update_xaxes(range=[0, 1])
    figure_familles.show(renderer="browser")

    phases = ["opening", "middlegame", "endgame"]
    noms_phases = {
        "opening": "Ouverture",
        "middlegame": "Milieu de partie",
        "endgame": "Finale",
    }
    gaffes = coups.loc[coups["jugement"].eq("blunder")]
    par_phase = (
        gaffes["phase"]
        .value_counts()
        .reindex(phases, fill_value=0)
        .rename_axis("phase")
        .reset_index(name="gaffes")
    )
    par_phase["phase"] = par_phase["phase"].map(noms_phases)
    figure_phases = px.bar(
        par_phase,
        x="phase",
        y="gaffes",
        title="Dans quelle phase surviennent mes gaffes ?",
        labels={"phase": "Phase de la partie", "gaffes": "Nombre de gaffes"},
        category_orders={"phase": list(noms_phases.values())},
    )
    figure_phases.show(renderer="browser")

    par_heure = (
        df.groupby("heure", as_index=False)
        .agg(n=("partie_id", "size"), score=("score", "mean"))
        .loc[lambda donnees: donnees["n"] >= 30]
    )
    figure_heures = px.line(
        par_heure,
        x="heure",
        y="score",
        markers=True,
        title="Mon score selon l'heure de début des parties (UTC)",
        labels={"heure": "Heure UTC", "score": "Score moyen", "n": "Parties"},
        hover_data=["n"],
    )
    figure_heures.update_xaxes(dtick=1, range=[-0.5, 23.5])
    figure_heures.update_yaxes(range=[0, 1])
    figure_heures.show(renderer="browser")


if __name__ == "__main__":
    main()
