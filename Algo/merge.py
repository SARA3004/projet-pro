import pandas as pd

# Charger les deux fichiers CSV
df_main = pd.read_csv('films_fusionnes_clean.csv')
df_update = pd.read_csv('films_fusionnes_clean1.csv')

# Clé de fusion (à adapter si ce n'est pas le titre)
merge_column = 'Titre'

# Fusion externe pour garder tous les films
df_merged = pd.merge(df_main, df_update, on=merge_column, how='outer', suffixes=('', '_new'))

# Recettes = BoxOffice si Recettes vide ou 0
df_merged['Recettes'] = df_merged.apply(
    lambda row: row['BoxOffice'] if (pd.isna(row['Recettes']) or row['Recettes'] == 0) and not pd.isna(row.get('BoxOffice')) else row['Recettes'], axis=1
)

# Note_moyenne = max(Note_moyenne, Score IMDb)
df_merged['Note_moyenne'] = df_merged.apply(
    lambda row: row['Score IMDb'] if pd.isna(row['Note_moyenne']) and not pd.isna(row.get('Score IMDb')) else (
        max(row['Note_moyenne'], row['Score IMDb']) if not pd.isna(row.get('Score IMDb')) else row['Note_moyenne']
    ), axis=1
)

# Nombre_votes = max(Nombre_votes, Votes IMDb)
df_merged['Nombre_votes'] = df_merged.apply(
    lambda row: row['Votes IMDb'] if pd.isna(row['Nombre_votes']) and not pd.isna(row.get('Votes IMDb')) else (
        max(row['Nombre_votes'], row['Votes IMDb']) if not pd.isna(row.get('Votes IMDb')) else row['Nombre_votes']
    ), axis=1
)

# Realisateurs = Réalisateur si Realisateurs vide
df_merged['Realisateurs'] = df_merged.apply(
    lambda row: row['Réalisateur'] if (pd.isna(row['Realisateurs']) or row['Realisateurs'] == '') and not pd.isna(row.get('Réalisateur')) else row['Realisateurs'], axis=1
)

# Acteurs_principaux = Acteurs si Acteurs_principaux vide
df_merged['Acteurs_principaux'] = df_merged.apply(
    lambda row: row['Acteurs'] if (pd.isna(row['Acteurs_principaux']) or row['Acteurs_principaux'] == '') and not pd.isna(row.get('Acteurs')) else row['Acteurs_principaux'], axis=1
)

# Garder uniquement les colonnes d'origine
colonnes_finales = df_main.columns.tolist()
df_result = df_merged[colonnes_finales]

# Supprimer les films sans date
df_result = df_result.dropna(subset=['Date_sortie'])
print(f"Nombre de films supprimés pour absence de date : {len(df_result)}")

# Convertir les dates en entier
df_result['Date_sortie'] = df_result['Date_sortie'].astype(int)

# Trier par ordre alphabétique des titres
df_result = df_result.sort_values(by='Titre').reset_index(drop=True)

# Recalculer les ID à partir de 1
df_result['ID'] = range(1, len(df_result) + 1)

# Sauvegarder le fichier final
df_result.to_csv('films_fusionnes_final2.csv', index=False)

print("Fusion, nettoyage et réindexation terminées. Résultat sauvegardé dans 'films_fusionnes_final.csv'.")
