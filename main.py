from fastapi import FastAPI
from back_end.recommender import liste_films_possibles, find_neighbors_by_title

# Pour lancer : fastapi dev main.py

app = FastAPI()


@app.get("/search/")
def suggest(name: str):
    return liste_films_possibles(name)
