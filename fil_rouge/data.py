"""Exo 1 : lire mes parties d'échecs. Environ 25 min.

Question : je joue depuis 2023, je stagne, qu'est-ce que je devrais travailler ?
À produire : un DataFrame propre, prêt pour les figures de l'exo 1 et pour l'appli de l'exo 2.
Les colonnes et leurs pièges sont dans data/echecs/LISEZMOI.md : lisez-le d'abord.
Lancer : uv run python fil_rouge/data.py
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "echecs"


def valider(df: pd.DataFrame) -> pd.DataFrame:
    """Plan B : s'arrêter avec un message clair si le fichier n'a pas la forme attendue.

    Colonnes absentes, colonnes entièrement vides, nombres lus comme du texte,
    identifiant de partie en double, résultat inconnu.
    """
    colonnes_requises = {
        "partie_id",
        "date_jeu",
        "resultat",
        "cadence",
        "couleur",
        "elo_joueur",
        "elo_adverse",
        "ouverture_famille",
        "gaffes_joueur",
    }
    manquantes = colonnes_requises - set(df.columns)
    if manquantes:
        raise ValueError(f"Colonnes manquantes dans parties.csv : {', '.join(sorted(manquantes))}")

    vides = [colonne for colonne in colonnes_requises if df[colonne].isna().all()]
    if vides:
        raise ValueError(f"Colonnes entierement vides dans parties.csv : {', '.join(sorted(vides))}")

    colonnes_numeriques = ("elo_joueur", "elo_adverse", "gaffes_joueur")
    texte = [colonne for colonne in colonnes_numeriques if not pd.api.types.is_numeric_dtype(df[colonne])]
    if texte:
        raise ValueError(f"Colonnes numeriques lues comme du texte : {', '.join(texte)}")

    if df["partie_id"].isna().any() or df["partie_id"].duplicated().any():
        raise ValueError("La colonne partie_id contient une valeur vide ou un doublon.")

    resultats_connus = {"win", "draw", "lose"}
    resultats = set(df["resultat"].dropna().unique())
    inconnus = resultats - resultats_connus
    if df["resultat"].isna().any() or inconnus:
        valeurs = ", ".join(sorted(str(valeur) for valeur in inconnus))
        detail = f" Valeurs inconnues : {valeurs}." if valeurs else ""
        raise ValueError(f"La colonne resultat contient une valeur vide ou inconnue.{detail}")

    return df


def load_data() -> pd.DataFrame:
    """Une ligne par partie (data/echecs/parties.csv), validée.

    Ajoutez : le résultat de mon point de vue en français, un score (1, 0,5 ou 0),
    l'année, l'heure, et l'écart d'Elo avec l'adversaire. Une cadence vide veut dire
    « aucune » : ne la laissez pas disparaître des filtres.
    Les exos suivants lisent ces colonnes, gardez ces noms : date_jeu (en datetime),
    resultat (victoire, nulle, défaite), score, annee, heure (UTC), ecart_elo
    (Elo de l'adversaire moins le mien), cadence.
    """
    df = valider(pd.read_csv(DATA / "parties.csv"))
    df["date_jeu"] = pd.to_datetime(df["date_jeu"], errors="raise")
    df["resultat"] = df["resultat"].map({"win": "victoire", "draw": "nulle", "lose": "défaite"})
    df["score"] = df["resultat"].map({"victoire": 1.0, "nulle": 0.5, "défaite": 0.0})
    df["annee"] = df["date_jeu"].dt.year
    df["heure"] = df["date_jeu"].dt.hour
    df["ecart_elo"] = df["elo_adverse"] - df["elo_joueur"]
    df["cadence"] = df["cadence"].fillna("aucune")
    return df


def load_coups() -> pd.DataFrame:
    """Un de mes coups jugés mauvais par ligne (data/echecs/coups_juges.csv)."""
    return pd.read_csv(DATA / "coups_juges.csv")


def load_phases() -> pd.DataFrame:
    """Les statistiques d'une partie par phase (data/echecs/phases.csv)."""
    return pd.read_csv(DATA / "phases.csv")


def familles(df: pd.DataFrame, min_n: int = 30) -> pd.DataFrame:
    """Score moyen par famille d'ouvertures, la pire d'abord.

    Colonnes : famille, n (parties), score, gaffes (par partie).
    Sous min_n parties le chiffre ne dit rien : écartez la famille.
    """
    colonnes_requises = {"partie_id", "ouverture_famille", "score", "gaffes_joueur"}
    manquantes = colonnes_requises - set(df.columns)
    if manquantes:
        raise ValueError(f"Colonnes manquantes pour les familles : {', '.join(sorted(manquantes))}")
    if min_n < 1:
        raise ValueError("min_n doit etre superieur ou egal a 1.")

    donnees = df.loc[
        df["ouverture_famille"].notna() & df["ouverture_famille"].astype("string").str.strip().ne("")
    ]
    resultat = (
        donnees.groupby("ouverture_famille", as_index=False)
        .agg(
            n=("partie_id", "size"),
            score=("score", "mean"),
            gaffes=("gaffes_joueur", "mean"),
        )
        .rename(columns={"ouverture_famille": "famille"})
    )
    return (
        resultat.loc[resultat["n"] >= min_n]
        .sort_values(["score", "famille"], ascending=[True, True])
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    d = load_data()
    print(d.shape)
