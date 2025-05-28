import streamlit as st
import requests
import pandas as pd

# streamlit run front_end/app.py

st.markdown("""
<style>
.stApp {
    background-color: black;
    color: white;
}
.stApp * {
    color: white !important;
}

/* Titre */
.stApp h1 {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    font-weight: 900 !important;
    font-size: 5rem !important;
    text-align: center !important;
    background: linear-gradient(90deg, #ff3333, #cc0000);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 3px 10px rgba(204, 0, 0, 0.9);
    margin-bottom: 1rem !important;
}

/* Boutons */
.stButton>button {
    background-color: #e50914 !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 0.5em 1.2em;
    cursor: pointer;
}
.stButton>button:hover {
    background-color: #b20710 !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #1a1a1a;
    color: white;
    border-radius: 5px;
    border: 1px solid #e50914;
}
div[data-baseweb="select"] div[role="option"] {
    background-color: black;
    color: white;
}

/* Text input */
div[data-baseweb="input"] {
    background-color: #1a1a1a;
    border: 1px solid #e50914;
    border-radius: 6px;
    padding: 0.25em 0.5em;
}

input {
    background-color: #000000 !important;
    color: white !important;
    border: none !important;
    padding: 0.5em 0.25em;
}

input:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px #e50914;
}
</style>
""", unsafe_allow_html=True)

url_search = "http://127.0.0.1:8000/search"
url_recommend = "http://127.0.0.1:8000/recommend"

st.title("Dataflix")
st.header("Recommandation de films")
st.subheader("Recherche de films")

# Champ de texte pour entrer un titre de film
recherche = st.text_input("Entrez votre film")

if recherche:
    st.write("Vous recherchez :", recherche)
    response = requests.get(f"{url_search}?name={recherche}")
    suggestions = response.json()
    df_films_possibles = pd.DataFrame(suggestions)
    liste_films_possibles = df_films_possibles["originalTitle"]
    st.dataframe(df_films_possibles)

    choix = st.selectbox(
        "Suggestions :",
        liste_films_possibles
        )

    if choix:
        st.write("Vous avez choisi :", choix)
        st.write("Vous pourriez aimer :")
        response_2 = requests.get(f"{url_recommend}?choix={choix}")
        recommandations = response_2.json()
        df_recommandations = pd.DataFrame(recommandations)
        st.dataframe(df_recommandations)
