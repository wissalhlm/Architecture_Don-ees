import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import io
from minio import Minio

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

print(f"✅ {len(jobs)} offres récupérées et sauvegardées localement !")

# Envoi vers MinIO (Data Lake) pour conserver l'historique
try:
    minio_host = os.getenv("MINIO_HOST", "localhost:9000")
    client = Minio(
        minio_host,
        access_key="admin",
        secret_key="password",
        secure=False
    )
    
    bucket_name = "datalake"
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Création du nom de fichier avec horodatage
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bronze/jobs_{timestamp}.json"
    
    # Convertir les données en bytes pour l'upload direct
    json_bytes = json.dumps(jobs, ensure_ascii=False, indent=4).encode('utf-8')
    data_stream = io.BytesIO(json_bytes)
    
    client.put_object(
        bucket_name,
        filename,
        data_stream,
        length=len(json_bytes),
        content_type="application/json"
    )
    print(f"✅ Historique sauvegardé dans MinIO : {filename}")
except Exception as e:
    print(f"⚠️ Erreur de connexion à MinIO : {e}")