import pandas as pd
import pytest

import data

PARTIES = ["partie_id", "date_jeu", "resultat", "cadence", "couleur", "elo_joueur", "elo_adverse"]


def test_csv_des_parties_se_lisent():
    df = pd.read_csv(data.DATA / "parties.csv")
    assert len(df) > 1000
    assert set(PARTIES) <= set(df.columns)
    assert df["partie_id"].is_unique


def test_csv_des_coups_juges_se_lisent():
    coups = pd.read_csv(data.DATA / "coups_juges.csv")
    assert {"partie_id", "coup", "jugement", "phase"} <= set(coups.columns)


def test_csv_des_phases_se_lit():
    phases = data.load_phases()
    assert {"partie_id", "phase", "gaffes_joueur"} <= set(phases.columns)
    assert not phases.empty


def test_load_data_une_ligne_par_partie():
    df = data.load_data()
    assert df["partie_id"].is_unique
    assert df["score"].isin([0, 0.5, 1]).all()
    assert set(df["resultat"].unique()) <= {"victoire", "nulle", "défaite"}
    assert pd.api.types.is_datetime64_any_dtype(df["date_jeu"])
    assert {"annee", "heure", "ecart_elo"} <= set(df.columns)
    assert "aucune" in set(df["cadence"])


def test_familles_pire_en_premier():
    f = data.familles(data.load_data(), 30)
    assert f["score"].is_monotonic_increasing
    assert (f["n"] >= 30).all()


def test_valider_refuse_un_resultat_inconnu():
    df = pd.DataFrame(
        {
            "partie_id": ["P0001"],
            "date_jeu": ["2026-01-01"],
            "resultat": ["inconnu"],
            "cadence": ["blitz"],
            "couleur": ["white"],
            "elo_joueur": [1500],
            "elo_adverse": [1500],
            "ouverture_famille": ["Sicilienne"],
            "gaffes_joueur": [0],
        }
    )
    with pytest.raises(ValueError, match="resultat"):
        data.valider(df)
