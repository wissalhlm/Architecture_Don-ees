# 🚀 Analyse du Marché de l'Emploi au Maroc (Data Engineering Pipeline)

Ce projet est une plateforme de **Data Engineering** permettant de scraper, nettoyer, analyser et visualiser les données du marché de l'emploi marocain à partir du site Rekrute.com.

Il implémente une **Architecture Médaillon** complète, de l'ingestion brute des données jusqu'à leur mise à disposition dans un Data Warehouse, le tout orchestré par Apache Airflow et stocké dans un Data Lake MinIO via Docker.

## 🏗️ Architecture du Projet

L'architecture est divisée en trois couches principales (Architecture Médaillon) et s'appuie sur un Data Lake objet (MinIO) ainsi qu'un Data Warehouse (MySQL) :

1.  **Couche Bronze (Raw Data) - `scraping.py` :**
    -   Script de Web Scraping (BeautifulSoup).
    -   Extraction des offres brutes au format JSON.
    -   Stockage historique dans le **Data Lake MinIO** (`datalake/bronze/`) et localement.

2.  **Couche Silver (Cleaned Data) - `cleaning.py` :**
    -   Nettoyage des données (Standardisation du texte, minuscules).
    -   Dédoublonnage des offres et gestion des valeurs nulles.
    -   Stockage de l'historique dans le **Data Lake MinIO** (`datalake/silver/`) et localement.

3.  **Couche Gold (Aggregated Data) - `analyse.py` :**
    -   Enrichissement des données (détection des mots-clés : Python, Data, Java, Cloud, etc.).
    -   Création d'agrégations (Top Villes, Top Compétences, Top Entreprises).
    -   Stockage de l'historique dans le **Data Lake MinIO** (`datalake/gold/`) et localement.
    -   Génération automatique de visualisations avec Matplotlib & Seaborn (`data/gold/viz/`).
    -   Chargement final dans un **Data Warehouse** relationnel (MySQL) pour interrogation.

## 🛠️ Stack Technique

-   **Langage :** Python 3.9
-   **Bibliothèques Python :** Requests, BeautifulSoup4, Pandas, Matplotlib, Seaborn, MySQL-Connector, Minio
-   **Orchestration :** Apache Airflow (DAGs)
-   **Data Lake :** MinIO (Stockage Objet / S3-compatible)
-   **Data Warehouse :** MySQL 8
-   **Conteneurisation :** Docker, Docker Compose
-   **Interface SGBD :** PhpMyAdmin

## 🚀 Comment lancer le projet ?

Grâce à Docker Compose, le lancement de toute l'architecture (Base de données, Data Lake et Orchestrateur) se fait en une seule commande. 

### Prérequis
- Avoir [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et en cours d'exécution sur votre machine.

### Démarrage
1. Ouvrez un terminal dans le dossier du projet.
2. Exécutez la commande suivante en arrière-plan :
```bash
docker-compose up -d --build
```
3. L'infrastructure démarre et lance les services suivants : MySQL, PhpMyAdmin, MinIO et Apache Airflow. *Note: Le premier démarrage d'Airflow peut prendre 1 à 2 minutes pour initialiser sa base de données interne.*

### Accès aux Interfaces et Exécution du Pipeline

Une fois les conteneurs démarrés, vous pouvez accéder aux différentes interfaces :

- 🌪️ **Apache Airflow (Orchestration)** : 
  - **URL :** [http://localhost:8081](http://localhost:8081)
  - **Identifiants :** Utilisateur: `admin` | Mot de passe : *généré dans les logs Docker ou `standalone_admin_password.txt` (ex: `eEHtbcax8n7S8Y3G`)*.
  - **Action :** Activez (unpause) le DAG `job_pipeline_dag` et déclenchez-le manuellement en cliquant sur le bouton "Play" (Trigger DAG). Cela exécutera le Scraping -> Nettoyage -> Analyse.

- 🪣 **MinIO (Data Lake)** : 
  - **URL :** [http://localhost:9001](http://localhost:9001)
  - **Identifiants :** `admin` / `password`
  - **Action :** Vous y retrouverez votre bucket `datalake` contenant tout l'historique des exécutions, trié dans les dossiers `bronze`, `silver`, et `gold`.

- 📊 **PhpMyAdmin (Data Warehouse)** : 
  - **URL :** [http://localhost:8080](http://localhost:8080)
  - **Identifiants :** Serveur : `db` | Utilisateur : `root` | Mot de passe : `root`
  - **Action :** Vous y retrouverez votre base `jobs_warehouse` avec les tables Gold prêtes pour le requêtage SQL.

### Résultats Locaux
- **Fichiers Locaux :** Les images des graphiques générés sont disponibles dans votre dossier `/data/gold/viz/`.
