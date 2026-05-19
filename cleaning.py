import json
import os
import datetime
import io
from minio import Minio

os.makedirs("data/silver", exist_ok=True)

with open("data/bronze/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

cleaned_jobs = []
seen = set()

for job in jobs:
    titre = job.get("titre", "")
    entreprise = job.get("entreprise", "")
    ville = job.get("ville", "")

    titre = titre.strip().lower() if titre else "non spécifié"
    entreprise = entreprise.strip().lower() if entreprise else "non spécifié"
    ville = ville.strip().lower() if ville else "non spécifié"

    key = (titre, entreprise, ville)
    if key in seen:
        continue
    seen.add(key)

    cleaned_jobs.append({
        "titre": titre,
        "entreprise": entreprise,
        "ville": ville
    })

with open("data/silver/jobs_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_jobs, f, ensure_ascii=False, indent=4)

print(f"✅ {len(cleaned_jobs)} données propres sauvegardées localement !")

# Envoi vers MinIO (Data Lake - Couche Silver)
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

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"silver/jobs_cleaned_{timestamp}.json"
    
    json_bytes = json.dumps(cleaned_jobs, ensure_ascii=False, indent=4).encode('utf-8')
    data_stream = io.BytesIO(json_bytes)
    
    client.put_object(
        bucket_name,
        filename,
        data_stream,
        length=len(json_bytes),
        content_type="application/json"
    )
    print(f"✅ Historique Silver sauvegardé dans MinIO : {filename}")
except Exception as e:
    print(f"⚠️ Erreur de connexion à MinIO : {e}")