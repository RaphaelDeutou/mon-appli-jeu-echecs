"""Entraîne un petit modèle de prix et l'enregistre."""

from pathlib import Path

import joblib
from sklearn.compose import make_column_transformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

from data import load_data

df = load_data()
X, y = df[["carburant", "axe", "lat", "lon"]], df["prix"]

model = make_pipeline(
    make_column_transformer(
        (OneHotEncoder(handle_unknown="ignore"), ["carburant", "axe"]),
        remainder="passthrough",
    ),
    GradientBoostingRegressor(random_state=0),
)
cv = KFold(5, shuffle=True, random_state=0)
mae = -cross_val_score(model, X, y, cv=cv, scoring="neg_mean_absolute_error").mean()

# La référence à battre : le prix médian de chaque carburant, appris sur les mêmes plis
erreurs = []
for train, test in cv.split(X):
    mediane = df.iloc[train].groupby("carburant")["prix"].median()
    erreurs.append((df.iloc[test]["carburant"].map(mediane) - y.iloc[test]).abs().mean())
base = sum(erreurs) / len(erreurs)

print(f"Erreur moyenne du modèle : {mae:.3f} €/L")
print(f"Erreur moyenne de la médiane par carburant : {base:.3f} €/L")
joblib.dump(model.fit(X, y), Path(__file__).parent / "model.joblib")
