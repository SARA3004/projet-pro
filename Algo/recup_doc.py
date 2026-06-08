import pandas as pd
import requests
import time
import os
from tqdm import tqdm

# Configuration
API_KEYS = ['3efc75a7']  
BASE_URL = 'http://www.omdbapi.com/'

input_file = 'films_cinema_2020_2025.csv'
output_file = 'resultats_omdb2.csv'


df_ids = pd.read_csv(input_file)
id_list = df_ids['tconst'].tolist()


if os.path.exists(output_file):
    df_saved = pd.read_csv(output_file)
    processed_ids = set(df_saved['ID'])
    print(f" {len(processed_ids)} IDs déjà récupérés, reprise en cours...")
else:
    df_saved = pd.DataFrame()
    processed_ids = set()
    print(" Aucun fichier de sauvegarde trouvé, démarrage d'une nouvelle collecte...")

# Fonction pour interroger l'API avec une clé donnée
def fetch_movie_data(movie_id, api_key):
    params = {'apikey': api_key, 'i': movie_id, 'plot': 'full'}
    response = requests.get(BASE_URL, params=params)
    return response.json()

current_api_index = 0  # Index de la clé API en cours

# Utilisation de tqdm pour la barre de progression
for movie_id in tqdm(id_list, desc="Collecte des films", unit="film"):
    if movie_id in processed_ids:
        continue  

    while current_api_index < len(API_KEYS):
        current_api_key = API_KEYS[current_api_index]
        try:
            data = fetch_movie_data(movie_id, current_api_key)

            # Gestion des erreurs de quota
            if 'Error' in data and 'limit' in data['Error'].lower():
                print(f"\n Quota atteint pour la clé {current_api_key}. Passage à la clé suivante...")
                current_api_index += 1 
                if current_api_index >= len(API_KEYS):
                    print(" Toutes les clés ont atteint leur limite. Arrêt du script.")
                    break
                continue  

            # Film non trouvé
            if data.get('Response') == 'False':
                print(f"\n Film non trouvé : {movie_id}")
                break  

            # Filtrer les films selon l'année (garder 2020 et plus)
            year_str = data.get('Year', '')
            # Certaines années peuvent être au format '2020–' ou '2020-2022' => prendre les 4 premiers chiffres
            year = None
            if year_str:
                year = int(year_str[:4]) if year_str[:4].isdigit() else None

            if year is None or year < 2020:
                print(f"\nℹ Film {data.get('Title')} ({year_str}) ignoré (avant 2020).")
                break  
            
            # Préparation des données
            film_data = {
                'ID': data.get('imdbID'),
                'Titre': data.get('Title'),
                'Année': data.get('Year'),
                'Durée': data.get('Runtime'),
                'Genre': data.get('Genre'),
                'Réalisateur': data.get('Director'),
                'Scénariste': data.get('Writer'),
                'Acteurs': data.get('Actors'),
                'Synopsis': data.get('Plot'),
                'Langue': data.get('Language'),
                'Pays': data.get('Country'),
                'Récompenses': data.get('Awards'),
                'Affiche': data.get('Poster'),
                'Score IMDb': data.get('imdbRating'),
                'Votes IMDb': data.get('imdbVotes'),
                'Type': data.get('Type'),
                'DVD': data.get('DVD'),
                'BoxOffice': data.get('BoxOffice'),
                'Production': data.get('Production')
            }

            # Sauvegarde
            df_saved = pd.concat([df_saved, pd.DataFrame([film_data])], ignore_index=True)
            df_saved.to_csv(output_file, index=False)

            print(f"\nFilm récupéré : {data.get('Title')}")
            time.sleep(0.2)
            break 

        except Exception as e:
            print(f"\n Erreur : {e}")
            break  

    else:
        
        print("\n Fin du script : toutes les clés API sont épuisées.")
        break

print("\n Sauvegarde terminée. Vous pouvez relancer le script demain pour continuer.")