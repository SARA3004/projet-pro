#!/usr/bin/env python3
"""
Version simplifiée du scraper Box Office Mojo
Se concentre sur les données principales sans les budgets (plus difficiles à obtenir)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_money_value(value):
    """Convertit une valeur monétaire en nombre"""
    if not value or value == '-':
        return 0
    clean_value = re.sub(r'[,$]', '', value.strip())
    try:
        return int(clean_value)
    except ValueError:
        return 0

def scrape_box_office_year(year):
    """Scrape les données d'une année"""
    url = f"https://www.boxofficemojo.com/year/world/{year}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        
        if not table:
            logger.warning(f"Pas de tableau trouvé pour {year}")
            return []
        
        movies = []
        rows = table.find_all('tr')[1:]  # Skip header
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 6:
                continue
            
            try:
                # Extraction du titre
                title_cell = cells[1]
                title_link = title_cell.find('a')
                title = title_link.get_text().strip() if title_link else title_cell.get_text().strip()
                
                # Extraction des recettes
                worldwide = clean_money_value(cells[2].get_text())
                domestic = clean_money_value(cells[3].get_text())
                foreign = clean_money_value(cells[5].get_text())
                
                movie_data = {
                    'Année': year,
                    'Rang': cells[0].get_text().strip(),
                    'Titre': title,
                    'Recettes_Mondiales': worldwide,
                    'Recettes_Domestiques': domestic,
                    'Recettes_Étrangères': foreign,
                    'Pourcentage_Domestique': cells[4].get_text().strip(),
                    'Pourcentage_Étranger': cells[6].get_text().strip() if len(cells) > 6 else ''
                }
                
                movies.append(movie_data)
                
            except Exception as e:
                logger.warning(f"Erreur ligne {year}: {e}")
                continue
        
        logger.info(f"✅ {year}: {len(movies)} films collectés")
        return movies
        
    except Exception as e:
        logger.error(f"❌ Erreur {year}: {e}")
        return []

def main():
    """Fonction principale"""
    print("🎬 Scraper Box Office Mojo Simple")
    print("=" * 40)
    
    all_movies = []
    years = range(2020, 2026)  # 2020 à 2025
    
    for year in years:
        print(f"Scraping {year}...")
        movies = scrape_box_office_year(year)
        all_movies.extend(movies)
        
        # Pause entre les requêtes
        time.sleep(2)
    
    if all_movies:
        # Création du DataFrame
        df = pd.DataFrame(all_movies)
        
        # Formatage des colonnes monétaires pour l'affichage
        df_display = df.copy()
        for col in ['Recettes_Mondiales', 'Recettes_Domestiques', 'Recettes_Étrangères']:
            df_display[col + '_Formatted'] = df_display[col].apply(
                lambda x: f"${x:,}" if x > 0 else "N/A"
            )
        
        # Sauvegarde CSV avec valeurs numériques
        filename = '2-box_office_2020_2025.csv'
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"\n✅ Données sauvegardées: {filename}")
        print(f"📊 Total films: {len(df)}")
        
        # Top 15 films
        print("\n🏆 Top 15 films (recettes mondiales):")
        print("-" * 60)
        top_movies = df.nlargest(15, 'Recettes_Mondiales')
        for _, movie in top_movies.iterrows():
            print(f"{movie['Titre']} ({movie['Année']}) - ${movie['Recettes_Mondiales']:,}")
        
        # Statistiques par année
        print("\n📈 Statistiques par année:")
        stats = df.groupby('Année')['Recettes_Mondiales'].agg(['count', 'sum', 'mean']).round(0)
        print(stats)
        
    else:
        print("❌ Aucune donnée collectée")

if __name__ == "__main__":
    main()