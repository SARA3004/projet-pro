import pandas as pd

# Dictionnaire de traduction anglais -> français des genres les plus courants
traduction_genres = {
    'Fantasy': 'Fantastique',
    'Animation': 'Animation',
    'Adventure': 'Aventure',
    'Family': 'Familial',
    'Comedy': 'Comédie',
    'Drama': 'Drame',
    'Action': 'Action',
    'Thriller': 'Thriller',
    'Horror': 'Horreur',
    'Romance': 'Romance',
    'Science Fiction': 'Science-fiction',
    'Sci-Fi': 'Science-fiction',
    'Crime': 'Policier',
    'Mystery': 'Mystère',
    'Music': 'Musique',
    'Documentary': 'Documentaire',
    'War': 'Guerre',
    'Western': 'Western',
    'History': 'Historique',
    'Biography': 'Biographie',
    'Sport': 'Sport',
    'Musical': 'Musique',
    'Family': 'Familial',
    'Fantasy': 'Fantastique',
    # Ajoute d'autres si nécessaire
}

def nettoyer_genres(genre_str):
    if pd.isna(genre_str) or genre_str.strip() == '':
        return ''
    # Séparer les genres (on suppose séparés par espace ou virgule ou slash)
    genres = [g.strip() for g in re.split(r'[,\s/;]+', genre_str) if g.strip()]
    # Traduire et dédupliquer
    genres_traduits = []
    for g in genres:
        # Chercher traduction, sinon garder original
        g_fr = traduction_genres.get(g, g)
        if g_fr not in genres_traduits:
            genres_traduits.append(g_fr)
    # Rejoindre par espace
    return ' '.join(genres_traduits)

if __name__ == '__main__':
    import re
    # Charger le fichier fusionné existant
    df = pd.read_csv('films_fusionnes_final2.csv', dtype=str)
    
    # Nettoyer la colonne Genre
    df['Genre'] = df['Genre'].apply(nettoyer_genres)
    
    # Sauvegarder dans nouveau fichier
    df.to_csv('films_fusionnes_final2.csv', index=False, encoding='utf-8')
    
    print("✅ Nettoyage terminé et sauvegardé dans films_fusionnes_clean.csv")
