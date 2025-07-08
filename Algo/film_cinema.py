import pandas as pd

# Charger le fichier
df = pd.read_csv('resultats_omdb2_clean.csv', dtype=str)

# Conversion des colonnes en numériques
df['Score IMDb'] = pd.to_numeric(df['Score IMDb'], errors='coerce').fillna(0)
df['Votes IMDb'] = pd.to_numeric(df['Votes IMDb'], errors='coerce').fillna(0)
df['BoxOffice'] = pd.to_numeric(df['BoxOffice'], errors='coerce').fillna(0)

# Identifier les films à supprimer
films_to_remove = df[
    (df['Score IMDb'] < 1) &
    (df['Votes IMDb'] < 10) &
    (df['BoxOffice'] < 50000)
]

print(f"🚫 Films supprimés : {len(films_to_remove)}")

# Garder uniquement les films avec au moins une information
df_clean = df.drop(films_to_remove.index)

print(f"✅ Nombre de films restants : {len(df_clean)}")

# Sauvegarder le fichier nettoyé
df_clean.to_csv('films_fusionnes_clean1.csv', index=False, encoding='utf-8')

print("💾 Fichier nettoyé sauvegardé sous 'films_fusionnes_clean1.csv'")
