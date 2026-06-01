
# Préparation des Données et Agrégation par Utilisateur (MongoDB)

## Contexte du Projet

Ce dépôt contient le **pipeline de préparation, nettoyage et agrégation des données** développé dans le cadre du projet IF29 :

> **« Comparaison de deux méthodes de classification pour la détection de profils atypiques sur X (Twitter) »**

L’objectif de ce travail est de transformer un **jeu de données brut de tweets** (niveau tweet) en un **jeu de données agrégé au niveau utilisateur**, exploitable directement par des **modèles de Machine Learning** (supervisés et non supervisés).

Cette étape constitue la **fondation du projet**, garantissant la qualité, la cohérence et la robustesse des variables utilisées pour l’analyse comportementale.

---

## Description du Jeu de Données

### Données d’Entrée

* **Source** : Dataset *Tweet_Worldcup*
* **Format** : Documents JSON
* **Base de données** : MongoDB
* **Collection** : `tweets`
* **Granularité** : un document par tweet

Chaque document suit la structure JSON native de l’API Twitter/X et contient notamment :

* les métadonnées du tweet,
* les informations sur l’auteur (`user`),
* éventuellement le contenu d’un tweet retweeté (`retweeted_status`).

### Hypothèse Fondamentale

L’analyse porte **uniquement sur l’auteur du tweet observé** (`user`)
👉 Les informations de `retweeted_status.user` ne sont **pas utilisées**, afin de ne pas biaiser le profil comportemental.

---

## Objectif du Pipeline

Le pipeline a pour but de :

* nettoyer les données brutes,
* enrichir chaque tweet avec des variables calculées,
* agréger les tweets par **identifiant utilisateur**,
* produire un **jeu de données utilisateur robuste et homogène**.

Chaque ligne du dataset final correspond à **un profil Twitter unique**.

---

## Vue d’Ensemble du Pipeline

Le pipeline est implémenté sous forme d’une **agrégation MongoDB**, exécutable via `mongosh`.

### Étapes Principales

1. Enrichissement des tweets (features calculées)
2. Conversion et validation des dates
3. Agrégation des tweets par utilisateur
4. Calcul des métriques comportementales
5. Calcul des métriques temporelles
6. Nettoyage et normalisation des variables
7. Écriture du résultat dans une nouvelle collection

---

## Enrichissement au Niveau Tweet

Pour chaque tweet, les variables suivantes sont calculées :

### Indicateurs d’Activité

* `is_retweet_flag` : indicateur binaire de retweet (1 = retweet)
* `tweet_length` : longueur du texte du tweet

### Indicateurs de Contenu

* `hashtags_count` : nombre de hashtags
* `urls_count` : nombre d’URLs
* `mentions_count` : nombre de mentions utilisateur

### Indicateur Temporel

* `tweet_date` : date du tweet convertie au format `ISODate`

Ces transformations garantissent des **types cohérents** et évitent les erreurs lors de l’agrégation.

---

## Agrégation au Niveau Utilisateur

Les tweets sont groupés par `user.id`.
Pour chaque utilisateur, les catégories de variables suivantes sont produites :

---

## Métriques Sociales (Profil)

* `followers_count` : nombre d’abonnés
* `friends_count` : nombre d’abonnements
* `followers_friends_ratio` : ratio abonnés / abonnements
* `verified` : compte certifié ou non
* `default_profile_image` : image de profil par défaut
* `profile_lang` : langue déclarée du profil

Ces variables permettent de détecter des **profils anormaux ou artificiels**.

---

## Métriques d’Activité

* `nb_tweets` : nombre total de tweets observés
* `nb_retweets` : nombre de retweets
* `retweet_ratio` : proportion de retweets

Ces indicateurs caractérisent le **niveau d’activité** et la **nature du comportement**.

---

## Métriques de Contenu

* `avg_tweet_length` : longueur moyenne des tweets
* `avg_hashtags` : hashtags moyens par tweet
* `avg_urls` : URLs moyennes par tweet
* `avg_mentions` : mentions moyennes par tweet

Ils décrivent la **richesse et la structure du contenu publié**.

---

## Métriques d’Engagement

* `avg_favorites` : moyenne des likes reçus
* `avg_retweet_count` : moyenne des retweets reçus

⚠️ Ces variables peuvent être nulles ou nulles sur certains datasets (ex. collecte partielle), comme notre cas , mais sont conservées pour assurer la **compatibilité avec des modèles génériques**.

---

## Métriques Temporelles (Essentielles)

Les dates sont **indispensables** pour caractériser le comportement d’un profil.

À partir de `tweet_date`, le pipeline calcule :

* `first_tweet_date` : première activité observée
* `last_tweet_date` : dernière activité observée
* `active_days` : nombre de jours distincts d’activité
* `tweet_frequency` : moyenne de tweets par jour

### Importance

Sans métriques temporelles :

* il est impossible de distinguer un humain d’un bot,
* la détection d’activité anormale devient irréalisable,
* toute analyse comportementale est biaisée.

---

## Collection de Sortie

Le pipeline écrit le résultat dans la collection :

```text
users_aggregated
```

Chaque document représente **un utilisateur Twitter enrichi**.

---

## Export des Données

Les données finales sont exportées sous deux formats :

### JSON

* Fichier : `users_aggregated.json`
* Conservation complète des types
* Recommandé pour archivage et réutilisation

### CSV

* Fichier : `users_aggregated.csv`
* Format tabulaire
* Directement exploitable pour :

  * pandas
  * scikit-learn ...


---

## Utilisation Prévue

Le dataset final est conçu pour :

* la détection de profils atypiques,
* l’apprentissage non supervisé (clustering),
* l’apprentissage supervisé (classification bot / humain),
* l’analyse exploratoire des comportements.

Toutes les variables sont **numériques ou booléennes**, facilitant la normalisation et l’entraînement des modèles.

---

## Reproductibilité

Le pipeline est **déterministe** :

* une exécution sur les mêmes données produit exactement le même résultat.

Dépendances :

* MongoDB
* mongosh
* mongoexport

---

## Auteur et Rôle

**Housseni – Data Engineer / Data Cleaner**

Responsable de :

* l’extraction des données,
* le nettoyage,
* la structuration,
* l’agrégation finale des profils utilisateurs.

Ce travail fournit le **jeu de données d’entrée unique** pour l’ensemble des modèles de Machine Learning du projet.

https://www.dropbox.com/t/UWZb0yeAMm9BN59p(les fichiers CSV, Json aggrégés)

