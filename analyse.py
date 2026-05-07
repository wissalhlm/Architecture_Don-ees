import json
import os
from collections import Counter
import mysql.connector
import time
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg') # Pour éviter les erreurs d'interface graphique dans Docker

# --- 1. Partie Analyse (Ton code actuel) ---
os.makedirs("data/gold", exist_ok=True)

with open("data/silver/jobs_cleaned.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

villes = [job["ville"] for job in jobs]
count_villes = Counter(villes)

entreprises = [job["entreprise"] for job in jobs]
count_entreprises = Counter(entreprises)

skills = []
keywords = ["python", "data", "engineer", "developer", "manager", "java", "php", "sql", "cloud", "consultant"]
for job in jobs:
    titre = job.get("titre", "")
    for key in keywords:
        if key in titre:
            skills.append(key)
count_skills = Counter(skills)

gold_data = {
    "offres_par_ville": dict(count_villes),
    "offres_par_entreprise": dict(count_entreprises),
    "top_skills": dict(count_skills)
}

with open("data/gold/jobs_gold.json", "w", encoding="utf-8") as f:
    json.dump(gold_data, f, ensure_ascii=False, indent=4)

print("✅ GOLD layer créé localement !")

# --- 1.5 Partie Visualisation avec Matplotlib & Seaborn ---
print("📊 Génération des visualisations...")
os.makedirs("data/gold/viz", exist_ok=True)
sns.set_theme(style="whitegrid")

# Graphique 1: Offres par ville (Top 10)
villes_sorted = sorted(count_villes.items(), key=lambda x: x[1], reverse=True)[:10]
if villes_sorted:
    v_names, v_counts = zip(*villes_sorted)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(v_names), y=list(v_counts), hue=list(v_names), legend=False, palette="viridis")
    plt.title("Top 10 des villes avec le plus d'offres")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/gold/viz/top_villes.png")
    plt.close()

# Graphique 2: Top Skills demandés
skills_sorted = sorted(count_skills.items(), key=lambda x: x[1], reverse=True)
if skills_sorted:
    s_names, s_counts = zip(*skills_sorted)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(s_counts), y=list(s_names), hue=list(s_names), legend=False, palette="magma")
    plt.title("Compétences les plus demandées")
    plt.xlabel("Nombre d'offres")
    plt.tight_layout()
    plt.savefig("data/gold/viz/top_skills.png")
    plt.close()

# Graphique 3: Top Entreprises (Top 10)
entreprises_sorted = sorted(count_entreprises.items(), key=lambda x: x[1], reverse=True)[:10]
if entreprises_sorted:
    e_names, e_counts = zip(*entreprises_sorted)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(e_counts), y=list(e_names), hue=list(e_names), legend=False, palette="plasma")
    plt.title("Top 10 des entreprises qui recrutent le plus")
    plt.xlabel("Nombre d'annonces")
    plt.tight_layout()
    plt.savefig("data/gold/viz/top_entreprises.png")
    plt.close()

print("✅ Visualisations sauvegardées dans data/gold/viz/ !")

# --- 2. Partie Data Warehouse (MySQL) ---
# Petit temps d'attente pour être sûr que MySQL est bien démarré dans Docker
time.sleep(10) 

try:
    # On utilise os.getenv("DB_HOST", "localhost") pour que ça marche à la fois localement et sur Docker
    db_host = os.getenv("DB_HOST", "localhost")
    db = mysql.connector.connect(
        host=db_host, 
        user="root",
        password="root",
        database="jobs_warehouse"
    )
    cursor = db.cursor()

    # Nettoyage et Insertion pour les Skills
    cursor.execute("CREATE TABLE IF NOT EXISTS top_skills (skill VARCHAR(255), count INT)")
    cursor.execute("TRUNCATE TABLE top_skills") # On vide pour repartir à neuf
    for skill, count in gold_data["top_skills"].items():
        cursor.execute("INSERT INTO top_skills (skill, count) VALUES (%s, %s)", (skill, count))

    # Nettoyage et Insertion pour les Villes
    cursor.execute("CREATE TABLE IF NOT EXISTS jobs_by_city (city VARCHAR(255), count INT)")
    cursor.execute("TRUNCATE TABLE jobs_by_city")
    for city, count in gold_data["offres_par_ville"].items():
        cursor.execute("INSERT INTO jobs_by_city (city, count) VALUES (%s, %s)", (city, count))

    db.commit()
    print("✅ Données Gold envoyées vers le Data Warehouse (MySQL) !")

except Exception as e:
    print(f"⚠️ Erreur de connexion DB : {e}")
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()