import streamlit as st
import requests
import pandas as pd

# streamlit run front_end/app.py

url_search = "http://127.0.0.1:8000/search"
url_recommend = "http://127.0.0.1:8000/recommend"

st.title("Dataflix : Rechercher un nom de films")

# Champ de texte pour entrer un titre de film
recherche = st.text_input("Entrez votre film")

if recherche:
    st.write("Vous recherchez :", recherche)
    response = requests.get(f"{url_search}?name={recherche}")
    suggestions = response.json()

    choix = st.selectbox(
        "Suggestions :",
        suggestions
        )

    if choix:
        st.write("Vous avez choisi :", choix)
        st.write("Vous pourriez aimer :")
        response_2 = requests.get(f"{url_recommend}?choix={choix}")
        recommandations = response_2.json()
        df_recommandations = pd.DataFrame(recommandations)
        st.dataframe(df_recommandations)
