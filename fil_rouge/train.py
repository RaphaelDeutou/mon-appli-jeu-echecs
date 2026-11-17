"""Exo 5 : la probabilité de gagner une partie. Fin à 16h15.

Question : avec quelle couleur, à quelle cadence, à quelle heure ce joueur gagne-t-il le plus ?
À produire : un modèle de classification scikit-learn, son erreur mesurée par validation croisée,
une référence à battre (toujours prédire la fréquence de victoire), et model.joblib enregistré
à côté de ce fichier (jamais versionné).
Lancer : uv run python fil_rouge/train.py
"""

import joblib  # noqa: F401

from data import load_data

df = load_data()

# TODO 1. Les variables : couleur, cadence, écart d'Elo, heure. La cible : victoire ou non
# TODO 2. Un Pipeline : encodage des catégories, puis le modèle
# TODO 3. La validation croisée, et la même mesure pour la référence
# TODO 4. print : modèle contre référence
# TODO 5. joblib.dump du modèle entraîné
