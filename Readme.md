Table des matières:

1. Installation
2. Composition
3. Utilisation
4. Credits

------------------------------------------------------------

1. INSTALLATION

Tout simplement télécharger (ou faire un gitclone) depuis GitHub.
Toutes les bibliothèques utilisées sont dans requirements.txt à la racine du projet.

-------------------------------------------------------------

2. COMPOSITION

### Structure du projet

| Emplacement            | Fichier                      | Description                                             |
|------------------------|------------------------------|---------------------------------------------------------|
|    Back                | `__init__.py`                | Permet la relation inter-dossier                        |
|                        | `recommender.py`             | Contient les fonctions de recommandation                |
|    Front               | `app.py`                     | Interface utilisateur avec Streamlit                    |
|    Racine du projet    | `requirements.txt`           | Liste des bibliothèques utilisées                       |
|                        | `readme.txt`                 | C’est ici ! 😄                                          |
|                        | `df_nlp.csv`                 | Table de données utilisée pour les recommandations      |
|                        | `Background.jpg`             | Image de fond du site                                   |
|                        | `main.py`                    | Contient l’API                                          |

---

###  Détail `df_nlp.csv`

- **Taille** : 49380 lignes × 41 colonnes


###  Colonnes principales

| Colonne             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `index`             | Numéro de ligne                                                             |
| `tconst`            | Identifiant IMDB                                                            |
| `originalTitle`     | Titre original du film                                                      |
| `startYear`         | Année de sortie                                                             |
| `genres`            | Genres du film (max 3)                                                      |
| `averageRating`     | Note moyenne IMDB                                                           |
| `numVotes`          | Nombre de votes IMDB                                                        |
| `nconst`            | Identifiants IMDB des acteurs et du réalisateur                             |
| `actor/actress`     | Nom et prénom des acteurs & actrice                                         |
| `director`          | Nom et prénom du réalisateur                                                |
| `overview`          | Résumé du film (en anglais)                                                 |
| `popularity`        | Popularité du film                                                          |
| `poster_path`       | Lien (partiel) vers le poster (depuis AlloCiné)                             |
| `tagline`           | Phrase d'accroche du film                                                   |
| `spoken_languages`  | Langues parlées dans le film                                                |
| `keywords`          | Mots-clés associés (depuis TMDB)                                            |
| `texte_nlp_cleaned` | Concaténation de genres, overview, acteurs, keywords, Bonfilm, année        |


###  Métrique NLP : `Popularité`

| Colonne                | Critères de classification               |
|------------------------|------------------------------------------|
| `trèspopulaire`        | si `popularity > 9.85`                   |
| `populaire`            | si `popularity > 4.79`                   |
| `paspopulaire`         | si `popularity > 2.51`                   |
| `pasdutoutpopulaire`   | si `popularity < 2.51`                   |
 
   
###  Métrique NLP : `Note Moyenne`

| Colonne                | Critères de classification               |
|------------------------|------------------------------------------|
| `trèsbon`              | si `averageRating > 7`                   |
| `bon`                  | si `averageRating > 6.3`                 |
| `mauvais`              | si `averageRating > 5.5`                 |
| `trèsmauvais`          | si `averageRating < 5.5`                 |
  
   
📌 Périmètre de la base de données :  

- Pas de films pour adultes
- Pas de films avec moins de 368 votes

-------------------------------------------------------------

3. UTILISATION.

1/ Charger l'ensemble du projet.  

2/ Ouvrir le fichier recommender.py avec VScode ou un autre IDE.  

3/ Dans l'invite de commande, taper (sous BASH): uvicorn main:app --reload   

Ca va lancer l'API (Attention! il faut bien être dans le dossier Dataset sur BASH!).  

4/ Ouvrir une nouvelle invite de commande et se déplacer dans le dossier Front  

5/ Taper streamlit run app.py  


---Dans le navigateur---

1/ Taper un nom de film ou fragment de nom de film  

2/ Cliquer et choisir dans la liste déroulante le film désiré  

Voilà!

-------------------------------------------------------------

4. CREDITS

Merci à tous, la promo Wild 2025, Viven, Abdel.
