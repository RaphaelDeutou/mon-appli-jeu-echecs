"""Exo 6 : votre propre serveur MCP. Fin à 17h00.

Question : un LLM doit pouvoir interroger mes parties.
À produire : un serveur FastMCP de deux ou trois outils au-dessus de votre API (api.py doit
tourner). Le LLM choisit un outil d'après son nom, sa docstring et ses arguments : soignez-les.
Lancer : uv run python fil_rouge/mcp_server.py   (stdio : c'est le client LLM qui le lance,
voir contexte/README.md pour le brancher)
"""

import os

import requests  # noqa: F401
from mcp.server.fastmcp import FastMCP

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")
mcp = FastMCP("echecs")

# TODO 1. Une fonction qui appelle l'API et lève une erreur si la réponse n'est pas un succès
# TODO 2. @mcp.tool() : mes pires ouvertures pour une cadence (GET /ouvertures)
# TODO 3. @mcp.tool() : mes chances de victoire dans une situation donnée (POST /predict)

if __name__ == "__main__":
    mcp.run()
