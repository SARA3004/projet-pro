#!/usr/bin/env python3
"""
Scraper pour Box Office Mojo - Films de 2020 à maintenant
Collecte les données de titre, recettes mondiales, domestiques et étrangères
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BoxOfficeMojoScraper:
    def __init__(self):
        self.base_url = "https://www.boxofficemojo.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.movies_data = []
    
    def clean_money_value(self, value):
        """Nettoie et convertit les valeurs monétaires en nombres"""
        if not value or value == '-':
            return 0
        # Supprime les symboles $ et , puis convertit en float
        clean_value = re.sub(r'[,$]', '', value.strip())
        try:
            return float(clean_value)
        except ValueError:
            return 0
    
    def get_movie_budget(self, movie_url):
        """Tente de récupérer le budget d'un film depuis sa page détaillée"""
        try:
            full_url = urljoin(self.base_url, movie_url)
            response = self.session.get(full_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Recherche du budget dans différents endroits possibles
            budget = None
            
            # Méthode 1: Recherche dans les spans avec money class
            money_spans = soup.find_all('span', class_='money')
            for span in money_spans:
                parent_text = span.parent.get_text() if span.parent else ""
                if 'budget' in parent_text.lower() or 'production' in parent_text.lower():
                    budget = span.get_text()
                    break
            
            # Méthode 2: Recherche dans le texte
            if not budget:
                text = soup.get_text()
                budget_match = re.search(r'Budget[:\s]*\$?([\d,]+(?:\.\d+)?)\s*million', text, re.IGNORECASE)
                if budget_match:
                    budget = f"${budget_match.group(1)} million"
            
            return budget
            
        except Exception as e:
            logger.warning(f"Impossible de récupérer le budget pour {movie_url}: {e}")
            return None
    
    def scrape_year(self, year):
        """Scrape les données d'une année donnée"""
        url = f"{self.base_url}/year/world/{year}/"
        logger.info(f"Scraping année {year}...")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Trouve le tableau principal
            table = soup.find('table')
            if not table:
                logger.warning(f"Aucun tableau trouvé pour l'année {year}")
                return
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 6:
                        continue
                    
                    # Extraction des données de base
                    rank = cells[0].get_text().strip()
                    title_cell = cells[1]
                    title_link = title_cell.find('a')
                    
                    if title_link:
                        movie_title = title_link.get_text().strip()
                        movie_url = title_link.get('href')
                    else:
                        movie_title = title_cell.get_text().strip()
                        movie_url = None
                    
                    worldwide_gross = self.clean_money_value(cells[2].get_text())
                    domestic_gross = self.clean_money_value(cells[3].get_text())
                    domestic_percent = cells[4].get_text().strip()
                    foreign_gross = self.clean_money_value(cells[5].get_text())
                    foreign_percent = cells[6].get_text().strip() if len(cells) > 6 else ""
                    
                    # Tentative de récupération du budget (limité pour éviter trop de requêtes)
                    budget = None
                    if movie_url and len(self.movies_data) % 10 == 0:  # Budget pour 1 film sur 10
                        budget = self.get_movie_budget(movie_url)
                        time.sleep(2)  # Pause pour être respectueux
                    
                    movie_data = {
                        'year': year,
                        'rank': rank,
                        'title': movie_title,
                        'worldwide_gross': worldwide_gross,
                        'domestic_gross': domestic_gross,
                        'domestic_percent': domestic_percent,
                        'foreign_gross': foreign_gross,
                        'foreign_percent': foreign_percent,
                        'budget': budget,
                        'movie_url': movie_url
                    }
                    
                    self.movies_data.append(movie_data)
                    logger.info(f"Ajouté: {movie_title} ({year})")
                    
                except Exception as e:
                    logger.error(f"Erreur lors du traitement d'une ligne: {e}")
                    continue
            
            # Pause entre les années
            time.sleep(3)
            
        except Exception as e:
            logger.error(f"Erreur lors du scraping de l'année {year}: {e}")
    
    def scrape_years(self, start_year=2020, end_year=2025):
        """Scrape plusieurs années"""
        for year in range(start_year, end_year + 1):
            self.scrape_year(year)
            logger.info(f"Terminé année {year}. Total films: {len(self.movies_data)}")
    
    def save_to_csv(self, filename='box_office_data.csv'):
        """Sauvegarde les données dans un fichier CSV"""
        if not self.movies_data:
            logger.warning("Aucune donnée à sauvegarder")
            return
        
        df = pd.DataFrame(self.movies_data)
        
        # Réorganise les colonnes
        columns_order = [
            'year', 'rank', 'title', 'budget', 
            'worldwide_gross', 'domestic_gross', 'domestic_percent',
            'foreign_gross', 'foreign_percent', 'movie_url'
        ]
        
        df = df[columns_order]
        
        # Formate les colonnes monétaires
        for col in ['worldwide_gross', 'domestic_gross', 'foreign_gross']:
            df[col] = df[col].apply(lambda x: f"${x:,.0f}" if x > 0 else "N/A")
        
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Données sauvegardées dans {filename}")
        logger.info(f"Total: {len(df)} films collectés")
        
        # Affiche un aperçu
        print("\nAperçu des données:")
        print(df.head(10).to_string())
        
        return filename
    
    def get_top_movies_summary(self, n=20):
        """Affiche un résumé des top films"""
        if not self.movies_data:
            return
        
        df = pd.DataFrame(self.movies_data)
        top_movies = df.nlargest(n, 'worldwide_gross')
        
        print(f"\nTop {n} films par recettes mondiales:")
        print("-" * 80)
        for _, movie in top_movies.iterrows():
            print(f"{movie['title']} ({movie['year']}) - ${movie['worldwide_gross']:,.0f}")

def main():
    """Fonction principale"""
    print("🎬 Scraper Box Office Mojo - Films 2020-2025")
    print("=" * 50)
    
    scraper = BoxOfficeMojoScraper()
    
    try:
        # Scrape les années 2020 à 2025
        scraper.scrape_years(2020, 2025)
        
        # Sauvegarde en CSV
        filename = scraper.save_to_csv('films_box_office_2020_2025.csv')
        
        # Affiche un résumé
        scraper.get_top_movies_summary(20)
        
        print(f"\n✅ Scraping terminé! Données sauvegardées dans: {filename}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Scraping interrompu par l'utilisateur")
        if scraper.movies_data:
            scraper.save_to_csv('films_box_office_partiel.csv')
    except Exception as e:
        logger.error(f"Erreur générale: {e}")

if __name__ == "__main__":
    main()