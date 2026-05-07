import json
import os

# créer dossier silver
os.makedirs("data/silver", exist_ok=True)

# lire Bronze
with open("data/bronze/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

cleaned_jobs = []
seen = set()

for job in jobs:
    # Gérer les cas où une valeur pourrait être nulle (None)
    titre = job.get("titre", "")
    entreprise = job.get("entreprise", "")
    ville = job.get("ville", "")

    titre = titre.strip().lower() if titre else "non spécifié"
    entreprise = entreprise.strip().lower() if entreprise else "non spécifié"
    ville = ville.strip().lower() if ville else "non spécifié"

    # supprimer doublons
    key = (titre, entreprise, ville)
    if key in seen:
        continue
    seen.add(key)

    cleaned_jobs.append({
        "titre": titre,
        "entreprise": entreprise,
        "ville": ville
    })

# sauvegarde Silver
with open("data/silver/jobs_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_jobs, f, ensure_ascii=False, indent=4)

print(f"✅ {len(cleaned_jobs)} données propres !")