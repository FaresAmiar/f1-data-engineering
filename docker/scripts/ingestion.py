import requests
import json
import os

# Années de récupération des données
START_YEAR = 2000
END_YEAR = 2025  # Ajuste selon ton besoin

# Dossier pour sauvegarder les fichiers
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_race_results(year):
    """Récupère les résultats des courses F1 pour une année donnée"""
    url = f"http://ergast.com/api/f1/{year}/results.json?limit=1000"  # API Ergast
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data["MRData"]["RaceTable"]["Races"]
    else:
        print(f"Erreur {response.status_code} pour l'année {year}")
        return []

def save_to_json(data, year):
    """Sauvegarde les résultats en JSON"""
    if data:
        with open(f"{OUTPUT_DIR}/f1_results_{year}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Données {year} sauvegardées ✅")
    else:
        print(f"Aucune donnée pour {year} ❌")

# Boucle sur les années
for year in range(START_YEAR, END_YEAR + 1):
    race_results = fetch_race_results(year)
    save_to_json(race_results, year)

print("Extraction terminée 🚀")
