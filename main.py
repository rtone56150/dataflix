from fastapi import FastAPI
from back_end.recommender import liste_films_possibles_knarf
from back_end.recommender import find_neighbors_by_title
from back_end.recommender import find_neighbors_nlp


# Pour lancer : fastapi dev main.py
# Pour déploiement sur Render : uvicorn main:app --host 0.0.0.0 --port $PORT

app = FastAPI()

# Fonction pour la recherche du film
@app.get("/search")
def suggest(name: str):
    return liste_films_possibles_knarf(name)


# Fonction pour la recommandation des films
@app.get("/recommend")
def recommend(tconst: str):
    return find_neighbors_nlp(tconst)
