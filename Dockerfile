FROM python:3.9-slim

WORKDIR /app

# Copier le fichier des dépendances en premier (optimise le cache Docker)
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout ton projet
COPY . .

# Création des dossiers pour l'architecture Médaillon [cite: 7, 12, 13]
RUN mkdir -p data/bronze data/silver data/gold

# Commande par défaut pour lancer le pipeline complet [cite: 14, 15]
CMD python scraping.py && python cleaning.py && python analyse.py