import streamlit as st
import requests
import pandas as pd

# streamlit run front_end/app.py
# Pour le déploiement sur Render : streamlit run front_end/app.py --server.port $PORT --server.address 0.0.0.0

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Background - NE PAS OUBLIER DE METTRE L'IMAGE DU BACKGROUND DANS LE MEME DOSSIER
import base64
with open("Background.jpg", "rb") as img_file:    # J'ai appelé l'image Background sur mon pc (Transparence de 3 sur Canva)
    encoded = base64.b64encode(img_file.read()).decode()
background_img = "data:image/jpeg;base64,{}".format(encoded)

st.markdown("""
<style>
.stApp {
    background-image: url('""" + background_img + """');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
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

# url_search = "http://127.0.0.1:8000/search"
# url_recommend = "http://127.0.0.1:8000/recommend"

st.sidebar.title("Dataflix")
# st.title("Dataflix")
st.subheader("Recommandation de films")

# Champ pour entrer un titre de film
recherche = st.text_input(" ", placeholder="Recherchez votre film")

if recherche:
    # Requete API pour récupérer le résultat des films possibles
    response = requests.get(f"https://dataflix.onrender.com/search?name={recherche}")
    # On récupère la réponse dans un json puis transformation en DF
    suggestions = response.json()
    df_films_possibles = pd.DataFrame(suggestions)
    liste_films_possibles_avec_annee = df_films_possibles["originalTitle_year"]
    # st.dataframe(df_films_possibles)

    # On laisse l'utilisateur choisir le film dans la liste des films possibles
    choix_film_avec_annee = st.selectbox(
        "Selectionnez votre film :",
        liste_films_possibles_avec_annee,
        index = None
        )

    

    if choix_film_avec_annee:
        # On récupère le nom du film (on avait choisit le film avec l'année)
        choix = df_films_possibles[df_films_possibles["originalTitle_year"] == choix_film_avec_annee]["originalTitle"].values[0]

        # Affichage des infos du film choisi
        with st.sidebar:
            url = f"https://image.tmdb.org/t/p/w500/{df_films_possibles[df_films_possibles['originalTitle'] == choix]['poster_path'].values[0]}"
            st.subheader(f"Vous avez choisi : {choix}")
            st.image(url, width=200)
            genre = df_films_possibles[df_films_possibles['originalTitle'].str.contains(recherche, case=False, na=False)]['genres'].values[0].replace(",", ", ")
            st.write(f"**Genre(s)** : {genre}")
            director = df_films_possibles[df_films_possibles["originalTitle_year"] == choix_film_avec_annee]["director"].values[0]
            st.write(f"**Réalisateur** : {director}")
            acteurs = df_films_possibles[df_films_possibles["originalTitle_year"] == choix_film_avec_annee]["actor/actress"].values[0]
            st.write(f"**Acteurs/Actrices** : {acteurs}")
            synopsis = df_films_possibles[df_films_possibles["originalTitle_year"] == choix_film_avec_annee]["overview"].values[0]
            st.write(f"**Synopsis** : {synopsis}")

        # On envoie dans l'API le tconst (les caractères spéciaux posaient problème)
        choix_tconst = df_films_possibles[df_films_possibles["originalTitle_year"] == choix_film_avec_annee]["tconst"].values[0]

        # Requete API pour récupérer le résultat des recommandations de films
        st.write("**Vous pourriez aimer :**")
        response_2 = requests.get(f"https://dataflix.onrender.com/recommend?tconst={choix_tconst}")
        # On récupère la réponse dans un json puis transformation en DF
        recommandations = response_2.json()
        df_recommandations = pd.DataFrame(recommandations).reset_index(drop=True)
        

        # Création de n colonnes 
        nb_colonne = 5
        cols = st.columns(nb_colonne)
        for film in range(nb_colonne):
            with cols[film]:
                url = f'https://image.tmdb.org/t/p/w500/{df_recommandations.loc[film,"poster_path"]}'
                st.image(url)
                st.write(df_recommandations.loc[film, "originalTitle_year"])
                st.write(f"⭐ {df_recommandations.loc[film, 'averageRating']} / 10")
                st.write(f"**Genre(s)** : {df_recommandations.loc[film, 'genres'].replace(',', ', ')}")
                st.write(f"**Réalisateur** : {df_recommandations.loc[film, 'director']}")
                st.write(f"**Acteurs/Actrices** : {df_recommandations.loc[film, 'actor/actress']}")

        # st.dataframe(df_recommandations)

        # Feedback
        st.write('___')
        st.markdown("Notre recommandation vous a-t-elle été utile ?")
        st.feedback("stars")
        st.write('___')

        # Liens utiles
        st.link_button('FAQ', url="https://www.wildcodeschool.com/contact")
        st.link_button("Conditions d'utilisation", url="https://www.cnil.fr/fr/reglement-europeen-protection-donnees")
        st.link_button('Mentions légales', url="https://www.police-nationale.interieur.gouv.fr/")
        st.link_button('Nous contacter', url="https://www.linkedin.com/in/julie-oriol-3741ab171/")
        st.link_button('Recrutement', url="https://www.linkedin.com/in/vivien-schneider-007a7462/")
