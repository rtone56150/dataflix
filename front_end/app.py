import streamlit as st
import requests
import pandas as pd

# streamlit run front_end/app.py

# Background - NE PAS OUBLIER DE METTRE L'IMAGE DU BACKGROUND DANS LE MEME DOSSIER
import base64
with open("Background.jpg", "rb") as img_file:    # J'ai appelé l'image Background sur mon pc (Transparence de 3 sur Canva)
    encoded = base64.b64encode(img_file.read()).decode()
background_img = "data:image/jpeg;base64,{}".format(encoded)

st.markdown("""
<style>
.stApp {
    background-color: black !important;
    background-image: none !important;
    color: white !important;
    min-height: 100vh;
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
input::placeholder {
    color: white !important;  /* changer la couleur du texte placeholder */
    opacity: 1 !important;   /* forcer l’opacité */
}
 section[data-testid="stSidebar"] {
            background-color: #1e1e1e;
}
</style>
""", unsafe_allow_html=True)

url_search = "http://127.0.0.1:8000/search"
url_recommend = "http://127.0.0.1:8000/recommend"

st.title("Dataflix")
st.header("Recommandation de films")
# st.subheader("Recherche de films")

# Champ de texte pour entrer un titre de film
recherche = st.text_input("Recherche de films", placeholder="Entrez votre film")

if recherche:
    # st.write("Vous recherchez :", recherche)
    response = requests.get(f"{url_search}?name={recherche}")
    suggestions = response.json()
    df_films_possibles = pd.DataFrame(suggestions)
    liste_films_possibles_avec_annee = df_films_possibles["originalTitle_year"]
    # st.dataframe(df_films_possibles)

    choix_film_avec_annee = st.selectbox(
        "Suggestions :",
        liste_films_possibles_avec_annee
        )

    choix = df_films_possibles[df_films_possibles["originalTitle_year"] == choix_film_avec_annee]["originalTitle"].values[0]

    if choix:

        with st.sidebar:
            url = f"https://image.tmdb.org/t/p/w500/{df_films_possibles[df_films_possibles['originalTitle'] == choix]["poster_path"].values[0]}"
            st.subheader(f"Vous avez choisi : {choix}")
            st.image(url, width=200)
            genre = df_films_possibles[df_films_possibles['originalTitle'].str.contains(recherche, case=False, na=False)]['genres'].values[0].replace(",", " ")
            st.write(f"Genre(s) : {genre}")
            synopsis = df_films_possibles[df_films_possibles["originalTitle_year"] == choix_film_avec_annee]["overview"].values[0]
            st.write(f"Synopsis : {synopsis}")

        st.write("Vous pourriez aimer :")
        response_2 = requests.get(f"{url_recommend}?choix={choix}")
        recommandations = response_2.json()
        df_recommandations = pd.DataFrame(recommandations)
        st.dataframe(df_recommandations)

        # Feedback
        st.write('___')
        st.markdown("Notre recommandation vous a-t-elle été utile ?")
        st.feedback("stars")
        st.write('___')

        # Liens utiles
        st.button('FAQ')
        st.button("Conditions d'utilisation")
        st.button('Mention légale')
        st.button('Nous contacter')
