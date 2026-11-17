"""Exo 5 : le service FastAPI. Lancer avec : uv run uvicorn api:app --app-dir fil_rouge --reload"""

from functools import lru_cache

from fastapi import FastAPI

from data import load_data

app = FastAPI(title="Carburants Loiret", version="1.0")


@lru_cache
def data():
    return load_data()


@app.get("/stations")
def stations(carburant: str = "E10", limit: int = 20):
    vue = data()[data()["carburant"] == carburant.upper()].nsmallest(limit, "prix")
    return vue[["ville", "adresse", "prix"]].to_dict("records")


# À vous : POST /predict
# - une classe Station(BaseModel) : carburant, axe (Literal), lat, lon
# - le modèle chargé UNE fois, au démarrage : joblib.load(Path(__file__).parent / "model.joblib")
# - la route renvoie {"prix_estime": ...}
