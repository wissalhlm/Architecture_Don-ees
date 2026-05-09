FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout ton projet
COPY . .

# Création des dossiers pour l'architecture Médaillon 
RUN mkdir -p data/bronze data/silver data/gold

# Commande par défaut pour lancer le pipeline complet (scraping, cleaning, analyse)
CMD python scraping.py && python cleaning.py && python analyse.py