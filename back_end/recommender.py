import pandas as pd
import unidecode
import re
# Import modèle de ML NON Supervisé
from sklearn.neighbors import NearestNeighbors
# Import outil standardisation de la donnée
from sklearn.preprocessing import StandardScaler

# Import le dataframe en CSV
df_ml = pd.read_csv("df_ml.csv")


# Fonction de normalisation
def normalize_and_split(text):
    text = unidecode.unidecode(text)        # Supprime les accents
    text = text.lower()                     # Met en minuscules
    text = re.sub(r'\s+', ' ', text)        # Supprime les espaces multiples
    text = re.sub(r'[^\w\s]', ' ', text)    # Remplace la ponctuation par un espace
    text = text.strip()
    return text.split(" ")


# Fonction listes des films possibles


def liste_films_possibles(film_recherche: str):
    film_recherche_normalise = normalize_and_split(film_recherche)
    df_ml["originalTitle_normalise"] = df_ml["originalTitle"].apply(normalize_and_split)
    df_film_possible = df_ml[df_ml["originalTitle_normalise"].apply(lambda x: set(film_recherche_normalise).issubset(set(x)))]
    return df_film_possible["originalTitle"].to_list()


# Définition des features
X = df_ml.drop(columns=["Unnamed: 0", "index", "tconst", "originalTitle", "genres_x", "numVotes", "poster_path"])

# Standardisation des features
scaler_knn = StandardScaler()
X_scaled = scaler_knn.fit_transform(X)

# Entrainement du modèle
k = 6  # Le nombre de films à recommander (le film choisi étant inclus)
# Donc 5 films recommandés
nn_model = NearestNeighbors(n_neighbors=k, algorithm='auto', metric='euclidean')
# .fit() indexe les données X_knn_scaled
nn_model.fit(X_scaled)  # Entraîner sur les données standardisées X_class

# Fonction recommandation


def find_neighbors_by_title(movie_title: str):

    # Récupérer l'ID du film à partir du titre
    movie_id = df_ml[df_ml["originalTitle"] == movie_title].index.to_list()[0]

    # Récupérer les features du vin cible
    movie_features = X.loc[[movie_id]]  # Garder le format DataFrame

    # Standardiser les features du vin cible avec le même scaler
    movie_features_scaled = scaler_knn.transform(movie_features)

    # Trouver les k voisins (incluant potentiellement lui-même en premier)
    distances, indices = nn_model.kneighbors(movie_features_scaled, n_neighbors=6)

    # Passage en dimension 1
    indices = indices[0]

    # Récupérer les index originaux des voisins trouvés dans le DF original
    neighbor_original_indices = X.iloc[indices].index

    # print(f"\n--- Plus proches voisins pour le film avec ID {movie_id} ---")
    # print("film Cible:")

    # Utiliser .loc pour être sûr avec l'index original
    # display(df_ml.loc[[movie_id], ["originalTitle", "genres_x", "startYear", "averageRating", "numVotes", "runtime", "popularity"]])

    # print(f"\n{len(neighbor_original_indices)} plus proches voisins trouvés
    # (basé sur les features de X_scaled):")

    # Utiliser .loc avec la liste des index originaux des voisins
    neighbor_info = df_ml.loc[neighbor_original_indices]

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
        "runtime",
        "popularity"
    ]]
