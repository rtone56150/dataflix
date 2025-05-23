import streamlit as st
import requests

# streamlit run front_end/app.py

url_search = "http://127.0.0.1:8000/search/"

st.title("Dataflix : Rechercher un nom de films")

# Champ de texte pour entrer un titre de film
recherche = st.text_input("Entrez votre film")

if recherche:
    st.write("Vous recherchez :", recherche)
    response = requests.get(f"http://127.0.0.1:8000/search?name={recherche}"
            # url_search,
            # json={"nom_film": recherche}
        )
    suggestions = response.json()

    st.selectbox(
        "Suggestions :",
        suggestions
        )
