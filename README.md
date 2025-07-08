# Projet Pro

## Tableau de Bord Cinéma
Un tableau de bord interactif pour analyser et visualiser des données de films avec des graphiques dynamiques et des statistiques détaillées.  

### 📋 Fonctionnalités
#### Statistiques Générales

+ Total des films analysés
+ Note moyenne des films
+ Budget total des productions
+ Recettes totales du box-office

#### Visualisations Graphiques

- Distribution par genre - Graphique en barres des genres les plus populaires  
- ROI moyen par genre - Rentabilité des investissements par genre  
- Répartition par pays - Graphique en secteurs des pays de production  
- Évolution par année - Tendance temporelle du nombre de films  
- Budget vs Recettes - Graphique de corrélation pour les top 10 films  


#### Analyses par genre :
- Top 10 des genres par recettes
- Top 10 des genres les plus rentables
- Top 10 des genres avec le moins de recettes


#### Analyses des réalisateurs :

- Top 10 par nombre de films
- Top 10 par recettes totales


#### Analyses des acteurs :

- Top 10 par nombre de films
- Top 10 par recettes totales


### 🚀 Utilisation
#### Prérequis

Un navigateur web moderne (Chrome, Firefox, Safari, Edge)  
Un fichier CSV contenant les données de films

#### Format des données CSV
Le fichier CSV doit contenir les colonnes suivantes :

- ID = Identifiant unique du film
- Titre = Titre du film
- Genre = Genre(s) du film (séparés par des espaces)
- Date_sortie = Année de sortie
- Realisateurs = Nom(s) du/des réalisateur(s) (séparés par des virgules)
- Acteurs_principaux = Nom(s) des acteurs principaux (séparés par des virgules)
- Pays_origine = Pays de production (séparés par des virgules)
- Budget = Budget de production (en dollars)
- Recettes = Recettes du box=office (en dollars)
- Note_moyenne = Note moyenne du film (sur 10)
- Nombre_votes = Nombre de votes reçus

#### Lancement

Ouvrez le fichier Dashboard.html dans votre navigateur  
Cliquez sur "Choisir un fichier" pour sélectionner votre fichier CSV  
Puis cliquez sur "Charger les données"  
Le tableau de bord se génère automatiquement avec vos données

### 🛠️ Technologies Utilisées

HTML5 - Structure de la page  
CSS3 - Styles et mise en page responsive  
JavaScript ES6 - Logique applicative  
Chart.js - Bibliothèque de graphiques interactifs  
Papa Parse - Parsing des fichiers CSV

### 📊 Traitement des Données
#### Gestion des Valeurs Manquantes

Les valeurs nulles, vides ou égales à 0 sont automatiquement filtrées
Les calculs moyens excluent les valeurs invalides
Traitement spécial pour les genres composés (ex: "Science-Fiction")

#### Calculs Statistiques

ROI (Return on Investment) = (Recettes - Budget) / Budget × 100  
Moyennes pondérées pour les analyses par genre, réalisateur et acteur

### 🎨 Interface
#### Design Responsive

Grilles adaptatives pour tous les écrans  
Cartes de statistiques avec indicateurs visuels  
Graphiques redimensionnables automatiquement  

### 📁 Structure du Projet
```
|- Algo                     # Dossier contenant les scripts
    |- film_cinema.py       # Filtre pour ne garder que les films sortis au cinéma
    |- genres.py            # Normalisation des genres
    |- merge.py             # Merge des différents fichier csv en un seul
    |- recup_doc.py         # Recuppérer des données via API
    |- scrapping.py         # Première version du scrapping
    |- scrapping2.py        # Deuxième version du scrapping
|- Analyse_Films.ipynb      # Création des graphiques
|- Dashboard.html           # Visualisation des données
|- films_final.csv          # Fichier CSV
|- README.md                # Explication du projet
```