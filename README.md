# 🚀 Analyse du Marché de l'Emploi au Maroc (Data Engineering Pipeline)

Ce projet est une plateforme de **Data Engineering** permettant de scraper, nettoyer, analyser et visualiser les données du marché de l'emploi marocain à partir du site Rekrute.com.

Il implémente une **Architecture Médaillon** complète, de l'ingestion brute des données jusqu'à leur mise à disposition dans un Data Warehouse via Docker.

## 🏗️ Architecture du Projet

L'architecture est divisée en trois couches principales (Architecture Médaillon) :

1.  **Couche Bronze (Raw Data) - `scraping.py` :**
    -   Script de Web Scraping (BeautifulSoup).
    -   Extraction des offres brutes au format JSON (`data/bronze/jobs.json`).
    -   Composant le **Data Lake** brut.

2.  **Couche Silver (Cleaned Data) - `cleaning.py` :**
    -   Nettoyage des données (Standardisation du texte).
    -   Dédoublonnage des offres et gestion des valeurs nulles.
    -   Stockage dans le Data Lake formaté (`data/silver/jobs_cleaned.json`).

3.  **Couche Gold (Aggregated Data) - `analyse.py` :**
    -   Enrichissement des données (détection des mots-clés : Python, Data, Java, Cloud, etc.).
    -   Création d'agrégations (Top Villes, Top Compétences, Top Entreprises).
    -   Génération automatique de visualisations avec Matplotlib & Seaborn (`data/gold/viz/`).
    -   Chargement final dans un **Data Warehouse** relationnel (MySQL).

## 🛠️ Stack Technique

-   **Langage :** Python 3.9
-   **Bibliothèques :** Requests, BeautifulSoup4, Pandas, Matplotlib, Seaborn, MySQL-Connector
-   **Base de données :** MySQL 8
-   **Conteneurisation :** Docker, Docker Compose
-   **Interface SGBD :** PhpMyAdmin

## 🚀 Comment lancer le projet ?

Grâce à Docker, le lancement de toute l'architecture se fait en une seule commande. 

### Prérequis
- Avoir [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et en cours d'exécution sur votre machine.

### Démarrage
1. Ouvrez un terminal dans le dossier du projet.
2. Exécutez la commande suivante :
```bash
docker-compose up --build
```
3. L'orchestrateur va automatiquement :
    - Démarrer le serveur MySQL.
    - Démarrer l'interface PhpMyAdmin.
    - Exécuter le pipeline complet (Scraping -> Nettoyage -> Analyse -> Visualisation -> Export MySQL).

### Résultats
- **Fichiers Locaux :** Les images des graphiques générés seront disponibles dans le dossier `/data/gold/viz/`.
- **Base de données :** Vous pouvez accéder au Data Warehouse via PhpMyAdmin en ouvrant `http://localhost:8080` dans votre navigateur (Serveur : `db`, Utilisateur : `root`, Mot de passe : `root`).
