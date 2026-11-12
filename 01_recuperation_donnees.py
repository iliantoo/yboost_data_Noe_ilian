import os
import pandas as pd

# 1. Configuration des URLs et du dossier de destination
BASE_URL = "https://raw.githubusercontent.com/martj42/international_results/master/"
DATA_DIR = "data"
FILES = ["results.csv", "shootouts.csv", "former_names.csv", "goalscorers.csv"]

os.makedirs(DATA_DIR, exist_ok=True)


def fetch_international_results():
    datasets = {}

    for filename in FILES:
        url = BASE_URL + filename
        local_path = os.path.join(DATA_DIR, filename)

        print(f"Téléchargement de {filename}...")
        df = pd.read_csv(url)

        # Sauvegarde locale pour éviter de retélécharger à chaque exécution
        df.to_csv(local_path, index=False)
        datasets[filename.replace(".csv", "")] = df
        print(f" -> {len(df):,} lignes sauvegardées dans {local_path}")

    return datasets


# 2. Récupération des fichiers
data = fetch_international_results()
results = data["results"]
former_names = data["former_names"]
shootouts = data["shootouts"]

# 3. Nettoyage de base (dates + normalisation des anciens noms de pays)
results["date"] = pd.to_datetime(results["date"])
former_names["start_date"] = pd.to_datetime(former_names["start_date"])
former_names["end_date"] = pd.to_datetime(former_names["end_date"])

# Dictionnaire de correspondance (ex: West Germany -> Germany)
name_mapping = dict(zip(former_names["former"], former_names["current"]))
results["home_team"] = results["home_team"].replace(name_mapping)
results["away_team"] = results["away_team"].replace(name_mapping)

# Tri chronologique indispensable pour la suite du projet
results = results.sort_values("date").reset_index(drop=True)

# 4. Aperçu rapide
print("\n--- Aperçu des données prêtes à l'emploi ---")
print(
    f"Période couverte : du {results['date'].min().date()} au {results['date'].max().date()}"
)
print(f"Nombre total de matchs : {len(results):,}")
print(results.tail(5))