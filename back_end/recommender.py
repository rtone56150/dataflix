import pandas as pd
import unidecode
import re
from sklearn.neighbors import NearestNeighbors
# Import outil standardisation de la donnée
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Import le dataframe en CSV
df_nlp = pd.read_csv("df_nlp.csv")


# Fonction de normalisation
def normalize(text):
    text = unidecode.unidecode(text)        # Supprime les accents
    text = text.lower()                     # Met en minuscules
    text = re.sub(r'\s+', ' ', text)        # Supprime les espaces multiples
    text = re.sub(r'[^\w\s]', ' ', text)    # Remplace ponctuation par espace
    text = text.strip()
    return text


# Fonction listes des films possibles


def liste_films_possibles(film_recherche: str):
    film_recherche_normalise = normalize(film_recherche)
    df_nlp["originalTitle_normalise"] = df_nlp["originalTitle"].apply(normalize)
    df_film_possible = df_nlp[df_nlp["originalTitle_normalise"].apply(lambda x: set(film_recherche_normalise).issubset(set(x)))]
    return df_film_possible["originalTitle"].to_list()


def liste_films_possibles_knarf(film_recherche: str):
    film_recherche_normalise = normalize(film_recherche)
    df_nlp["originalTitle_normalise"] = df_nlp["originalTitle"].apply(normalize)
    df_film_possible = df_nlp[df_nlp['originalTitle_normalise'].str.contains(film_recherche_normalise, case=False, na=False)]
    df_film_possible = df_film_possible.fillna(value="Inconnu")
    return df_film_possible[[
        "originalTitle",
        "originalTitle_year",
        "startYear",
        "genres",
        "averageRating",
        "numVotes",
        "popularity",
        "overview",
        "poster_path"
        ]].sort_values("numVotes", ascending=False).to_dict()


# Définition des features
#X = df_nlp(columns=["Unnamed: 0", "index", "tconst", "originalTitle", "genres", "numVotes", "nconst", "director", "actor/actress", "poster_path", "overview", "originalTitle_year", "tagline", "texte_nlp_cleaned"])

# Standardisation des features
#scaler_knn = StandardScaler()
#X_scaled = scaler_knn.fit_transform(X)

# Entrainement du modèle
#k = 6  # Le nombre de films à recommander (le film choisi étant inclus)
# Donc 5 films recommandés
#nn_model = NearestNeighbors(n_neighbors=k, algorithm='auto', metric='euclidean')
# .fit() indexe les données X_knn_scaled
#nn_model.fit(X_scaled)  # Entraîner sur les données standardisées X_class

# Fonction recommandation


def find_neighbors_by_title(movie_title: str):

    # Récupérer l'ID du film à partir du titre
    movie_id = df_nlp[df_nlp["originalTitle"] == movie_title].index.to_list()[0]

    # Récupérer les features du film cible
    movie_features = X.loc[[movie_id]]  # Garder le format DataFrame

    # Standardiser les features du film cible avec le même scaler
    movie_features_scaled = scaler_knn.transform(movie_features)

    # Trouver les k voisins (incluant potentiellement lui-même en premier)
    distances, indices = nn_model.kneighbors(movie_features_scaled, n_neighbors=6)

    # Passage en dimension 1
    indices = indices[0][1:]

    # Récupérer les index originaux des voisins trouvés dans le DF original
    neighbor_original_indices = X.iloc[indices].index

    # Utiliser .loc avec la liste des index originaux des voisins
    neighbor_info = df_nlp.loc[neighbor_original_indices]

    # display(neighbor_info[["originalTitle", "genres_x", "startYear", "averageRating", "numVotes", "runtime", "popularity"]])
    # print("\nDistances euclidiennes correspondantes:")
    # Afficher seulement les distances pour les voisins valides trouvés
    # print(distances[0][:len(indices)])
    return neighbor_info[[
        "originalTitle",
        "genres_x",
        "startYear",
        "averageRating",
        "numVotes",
        "popularity"
    ]].to_dict()


X_nlp = df_nlp["texte_nlp_cleaned"]

model_vectorizer = TfidfVectorizer()

X_nlp_CV = model_vectorizer.fit_transform(X_nlp)


def find_neighbors_nlp(movie_title:str):
    # Récupérer l'ID du film à partir du titre
    movie_id = df_nlp[df_nlp["originalTitle"] == movie_title].index.to_list()[0]

    # Récupérer les features du film cible
    movie_features = X_nlp_CV[movie_id]  # Garder le format DataFrame

    # Trouver les k voisins (incluant potentiellement lui-même en premier)
    cosine_sim_scores = cosine_similarity(movie_features, X_nlp_CV)

    # On classe pour récupérer les indices triés par similarité décroissante
    neighbor_original_indices = np.argsort(cosine_sim_scores[0])[::-1][1:20]

    # Utiliser .loc avec la liste des index originaux des voisins
    neighbor_info = df_nlp.loc[neighbor_original_indices]

    neighbor_info = neighbor_info.fillna(value="Inconnu")

    return neighbor_info[[
        "originalTitle",
        "genres",
        "startYear",
        'director',
        "actor/actress",
        "averageRating",
        "numVotes",
        "popularity"
    ]].to_dict()
