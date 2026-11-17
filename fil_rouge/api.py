"""Exo 5 : le service FastAPI. Fin à 16h15.

Question : mes parties et mon modèle, derrière une API que n'importe quel client peut appeler.
À produire : GET /parties, GET /ouvertures et POST /predict (corps validé par Pydantic).
Le modèle est chargé une fois, au démarrage. Lancez train.py d'abord.
Lancer : uv run uvicorn api:app --app-dir fil_rouge --host 127.0.0.1 --port 8000 --reload
Documentation interactive : http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

from data import familles, load_data  # noqa: F401

app = FastAPI(title="Mes parties d'échecs", version="1.0")

# TODO 1. Charger le modèle : joblib.load(Path(__file__).parent / "model.joblib")
# TODO 2. GET /parties : filtres facultatifs cadence et couleur, limit
# TODO 3. GET /ouvertures : les familles, la pire d'abord (familles de data.py)
# TODO 4. Une classe Partie(BaseModel) : couleur, cadence, ecart_elo, heure (0 à 23)
# TODO 5. POST /predict : renvoie {"proba_victoire": ...}
