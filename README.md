# E4FI_Projet_Quizz_Sport

## Présentation

Ce projet est une application web de quiz sportif. Elle permet à tout visiteur de répondre à une série de questions sur le sport, d’obtenir un score, et de se comparer aux autres participants. 

## Fonctionnalités principales

### Front
- Accès libre au quiz sans authentification
- Saisie du nom du participant
- Parcours des questions à choix multiples
- Affichage du score final et du classement général

### Back
- Accès réservé aux administrateurs (authentification par mot de passe)
- Ajout, modification et suppression de questions
- Visualisation des participants et de leurs scores

## Stack technique

- **Back-end** : Python 3, Flask, SQLite, JWT pour l’authentification
- **Front-end** : Vue.js 3, Vite, Axios, CSS personnalisé
- **API REST** : Communication entre le front et le back via des endpoints JSON

## Installation et lancement

### Prérequis
- Python >= 3.12.10
- Node.js & npm

### Installation du back-end
1. Placez-vous dans le dossier `quizz_app/quizz_api`
2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez le serveur Flask :
   ```bash
   python app.py
   ```

### Installation du front-end
1. Placez-vous dans le dossier `quizz_app/quizz_ui`
2. Installez les dépendances :
   ```bash
   npm install
   ```
3. Lancez le serveur de développement :
   ```bash
   npm run dev
   ```
   
## Authentification administrateur pour génération des questions
- Mot de passe par défaut : `iloveflask`
1. Connectez-vous à l'interface d'admin
2. Ajoutez, modifiez ou supprimez des questions
3. Les questions sont stockées dans la base de données SQLite

## Schéma de la base de données

La base de données SQLite comporte trois tables principales :

![schema_bdd](schema_bdd.png)

- **questions** :
  - `id` (INTEGER, PK, auto-incrémenté)
  - `position` (INTEGER, ordre d’affichage)
  - `content` (TEXT, énoncé de la question)
  - `title` (TEXT, titre ou catégorie)
  - `image` (TEXT, URL ou chemin de l’image)

- **reponses** :
  - `id` (INTEGER, PK, auto-incrémenté)
  - `correct` (INTEGER, 1 = bonne réponse, 0 = mauvaise)
  - `content` (TEXT, texte de la réponse)
  - `id_question` (INTEGER, FK vers `questions.id`)

- **joueur** :
  - `id` (INTEGER, PK, auto-incrémenté)
  - `nom` (TEXT, nom du participant)
  - `score` (INTEGER, score obtenu)

**Relations** :
- Une question possède plusieurs réponses
- Un joueur a un score associé à son nom