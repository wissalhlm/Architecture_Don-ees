import requests
from bs4 import BeautifulSoup
import json
import os

os.makedirs("data/bronze", exist_ok=True)

url = "https://www.rekrute.com/offres.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

jobs = []

for page in range(1, 10):  
    target_url = f"{url}?p={page}"
    response = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    offers = soup.find_all("li", class_="post-id")

    for offer in offers:
        titre_elem = offer.find("a", class_="titreJob")
        entreprise_elem = offer.find("img", class_="photo")
        
        titre = titre_elem.text.strip() if titre_elem else None
        entreprise = entreprise_elem.get("alt").strip() if entreprise_elem and entreprise_elem.has_attr("alt") else None
        
        ville = None
        if titre and " | " in titre:
            parts = titre.split(" | ")
            titre = parts[0].strip()
            ville = parts[1].strip()

        job = {
            "titre": titre,
            "entreprise": entreprise,
            "ville": ville
        }

        jobs.append(job)

with open("data/bronze/jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=4)

print(f"✅ {len(jobs)} offres récupérées !")