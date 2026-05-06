# 1. Description propre du dataset CSV 

## Dataset utilisateurs – Projet IF29

### Source

* Base MongoDB : `database_local`
* Collection : `users_aggregated`
* Extraction issue de **1 161 999 tweets Twitter (tweet WorldCup dataset)**



## Structure générale

* **1 ligne = 1 utilisateur Twitter**
* Données obtenues par **agrégation de comportements observés au niveau tweet**
* Aucun label (ni supervision, ni classe cible)

---

#  Description détaillée des variables

## 🔹 1. Identité et statut du compte

### `followers_count`

Nombre d’abonnés du compte Twitter
➡️ Indicateur de popularité / influence



### `friends_count`

Nombre de comptes suivis par l’utilisateur
➡️ Indicateur d’activité sociale (following)



### `verified`

Statut du compte (0/1 ou false/true)
➡️ Indique si le compte est certifié Twitter



### `statuses_count`

Nombre total de tweets publiés par le compte
➡️ Mesure de l’activité globale historique



### `favourites_count`

Nombre total de likes donnés par l’utilisateur
➡️ Indicateur d’engagement passif



## 🔹 2. Activité observée dans le dataset

### `nb_tweets_observed`

Nombre de tweets présents dans le dataset pour cet utilisateur
➡️ Activité mesurée sur la période du dataset (et non totale)



### `nb_retweets`

Nombre de tweets classés comme retweets
➡️ Mesure du comportement de diffusion


## 🔹 3. Engagement moyen reçu

### `avg_favorite_count`

Nombre moyen de likes reçus par tweet
➡️ Indicateur d’attractivité des contenus



### `avg_retweet_count`

Nombre moyen de retweets reçus par tweet
➡️ Indicateur de viralité



## 🔹 4. Variables dérivées (feature engineering simple)

### `follower_friend_ratio`

Ratio :

followers_count / friends_count

➡️ Mesure d’influence relative

* élevé → compte suivi massivement
* faible → compte “follow-back” ou suspect



### `retweet_ratio`

Ratio :

nb_retweets / nb_tweets_observed

➡️ Mesure du comportement de diffusion

* proche de 1 → compte principalement amplificateur
* proche de 0 → compte original

---

# 2. Partie IMPORT (MongoDB) – propre et justifiée


##  Script d’import des données brutes (MongoDB)

```bash id="mongo_import_if29"
#!/bin/bash

DB_NAME="database_local"
COLLECTION_NAME="tweets"
DATA_DIR="/home/el-professor/Téléchargements/IF29/raw"
MONGO_URI="mongodb://localhost:27017"

# Vérification de mongoimport
if ! command -v mongoimport &> /dev/null; then
  echo "mongoimport introuvable"
  exit 1
fi

# Vérification du serveur MongoDB
if ! mongosh --quiet --eval "db.runCommand({ ping: 1 })" &> /dev/null; then
  echo "MongoDB local non démarré"
  exit 1
fi

# Récupération des fichiers JSON
shopt -s nullglob
files=("$DATA_DIR"/*.json)

if [ ${#files[@]} -eq 0 ]; then
  echo "Aucun fichier JSON trouvé dans $DATA_DIR"
  exit 0
fi

echo " ${#files[@]} fichiers détectés"

# Import des fichiers dans MongoDB
for file in "${files[@]}"; do
  echo "Import de $(basename "$file")..."
  
  mongoimport \
    --uri="$MONGO_URI" \
    --db="$DB_NAME" \
    --collection="$COLLECTION_NAME" \
    --file="$file" \
    --mode=insert \
    --numInsertionWorkers=4
done

echo " Import local terminé avec succès"
```

---

# 3. Justification (IMPORTANT NOTE)

## 🔹 Phase d’ingestion des données

> Les données Twitter ont été importées dans MongoDB à l’aide de l’outil `mongoimport`, permettant la gestion efficace de fichiers JSON volumineux et semi-structurés.
> Cette étape garantit la conservation du format natif des données sociales et facilite leur traitement ultérieur.

---

#  4. Le TRAVAIL démontre:

Rôle :

##  Data Engineer / Data Cleaner

J'ai fait :

### ✔ Ingestion

* JSON → MongoDB

### ✔ Structuration

* tweets → utilisateurs

### ✔ Agrégation

* 1M+ tweets → 643k utilisateurs

### ✔ Feature engineering léger

* ratios simples

### ✔ Export

* CSV : https://github.com/ElProfesormika/PROJET_IF29_GR03/blob/main/users_aggregated.csv
* JSON : https://www.dropbox.com/t/igamCRcvLkc6uKom

