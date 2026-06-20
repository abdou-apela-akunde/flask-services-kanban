# Flask Services Kanban

## Description

Ce projet a été réalisé dans le cadre du TP #2 : **Développement de Services Web Flask avec Kanban & GitHub Projects**.

L'objectif du projet est de développer plusieurs microservices web indépendants en Python Flask, tout en appliquant une méthode de gestion de projet avec :

- GitHub ;
- GitHub Projects ;
- un tableau Kanban ;
- des issues ;
- des branches Git ;
- des commits conventionnels ;
- des Pull Requests ;
- des tests avec Postman, Python et HTML/JavaScript.

Le dépôt commun s'appelle :

```text
flask-services-kanban
```

---

## Objectifs du TP

Ce TP permet de travailler plusieurs compétences :

* organiser le travail d'équipe avec un tableau Kanban ;
* créer un dépôt GitHub commun ;
* créer et gérer des issues GitHub ;
* travailler avec des branches Git ;
* ouvrir des Pull Requests ;
* faire des revues de code ;
* développer des API REST avec Flask ;
* utiliser des données JSON ;
* connecter Flask à une base de données MySQL ;
* charger un fichier CSV dans MySQL ;
* tester les services avec Postman, Python et HTML/JavaScript.

---

## Architecture générale du projet

Le projet est composé de 4 services principaux.

| Service   | Description                             | Port |
| --------- | ---------------------------------------- | ---- |
| Service 1 | Calculs mathématiques sur matrices      | 5001 |
| Service 2 | Fonctions statistiques sur données JSON | 5002 |
| Service 3 | Fonctions statistiques depuis MySQL     | 5003 |
| Service 4 | Chargement CSV vers MySQL               | 5004 |

Les services 3 et 4 partagent la même base de données MySQL.

---

## Structure du dépôt

```text
flask-services-kanban/
├── service1_matrices/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── service2_statistiques/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── service3_stats_mysql/
│   ├── app.py
│   ├── db.py
│   ├── test_service3.py
│   ├── client_test_service3.html
│   ├── requirements.txt
│   └── README.md
│
├── service4_csv_mysql/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── data/
│   └── donnees_exemple.csv
│
├── sql/
│   └── init_db.sql
│
├── .gitignore
└── README.md
```

---

## Service 1 – Calculs matriciels

Le Service 1 permet d'effectuer des calculs mathématiques sur des matrices.

Il utilise principalement :

* Flask ;
* NumPy.

### Port utilisé

```text
5001
```

### Routes principales

```http
POST /matrices/add
POST /matrices/multiply
POST /matrices/transpose
POST /matrices/determinant
POST /matrices/inverse
```

### Exemple de requête

```bash
curl -X POST http://localhost:5001/matrices/add \
     -H "Content-Type: application/json" \
     -d "{\"A\": [[1,2],[3,4]], \"B\": [[5,6],[7,8]]}"
```

### Réponse attendue

```json
{
  "operation": "addition",
  "resultat": [[6.0, 8.0], [10.0, 12.0]]
}
```

---

## Service 2 – Statistiques JSON

Le Service 2 permet d'effectuer des calculs statistiques à partir de données envoyées au format JSON.

Il utilise principalement :

* Flask ;
* NumPy ;
* SciPy.

### Port utilisé

```text
5002
```

### Routes principales

```http
POST /stats/describe
POST /stats/correlation
POST /stats/test_normalite
POST /stats/test_student
```

### Exemple de requête

```bash
curl -X POST http://localhost:5002/stats/describe \
     -H "Content-Type: application/json" \
     -d "{\"data\": [12.5, 15.3, 8.7, 21.0, 13.2]}"
```

---

## Service 3 – Statistiques depuis MySQL

Le Service 3 permet de récupérer des données depuis une base MySQL et de calculer des statistiques.

Il utilise principalement :

* Flask ;
* NumPy ;
* SciPy ;
* MySQL ;
* mysql-connector-python ;
* python-dotenv.

### Port utilisé

```text
5003
```

### Routes principales

```http
GET /
GET /db/stats/describe?serie=serie_A
GET /db/stats/correlation?serie_x=serie_A&serie_y=serie_B
```

### Route d'accueil

```http
GET /
```

Exemple :

```text
http://127.0.0.1:5003/
```

Réponse :

```json
{
  "message": "Service 3 Stats MySQL fonctionne",
  "routes": [
    "/db/stats/describe?serie=serie_A",
    "/db/stats/correlation?serie_x=serie_A&serie_y=serie_B"
  ]
}
```

### Description statistique

```http
GET /db/stats/describe?serie=serie_A
```

Exemple :

```text
http://127.0.0.1:5003/db/stats/describe?serie=serie_A
```

Réponse possible :

```json
{
  "source": "mysql",
  "resultat": {
    "serie": "serie_A",
    "n": 5,
    "moyenne": 14.14,
    "mediane": 13.2,
    "ecart_type": 4.6341,
    "minimum": 8.7,
    "maximum": 21.0
  }
}
```

### Corrélation entre deux séries

```http
GET /db/stats/correlation?serie_x=serie_A&serie_y=serie_B
```

Exemple :

```text
http://127.0.0.1:5003/db/stats/correlation?serie_x=serie_A&serie_y=serie_B
```

Réponse possible :

```json
{
  "source": "mysql",
  "series": {
    "x": "serie_A",
    "y": "serie_B",
    "n_points": 4
  },
  "resultat": {
    "r": 0.1234,
    "p_value": 0.456789,
    "significatif": false
  }
}
```

---

## Service 4 – Chargement CSV vers MySQL

Le Service 4 permet d'envoyer un fichier CSV et de charger ses données dans la table MySQL `donnees`.

Il utilise principalement :

* Flask ;
* pandas ;
* MySQL ;
* mysql-connector-python ;
* python-dotenv.

### Port utilisé

```text
5004
```

### Routes principales

```http
POST /upload/csv
GET /upload/series
```

### Upload d'un fichier CSV

```http
POST /upload/csv
```

Exemple avec curl :

```bash
curl -X POST http://localhost:5004/upload/csv \
     -F "file=@data/donnees_exemple.csv"
```

Réponse possible :

```json
{
  "statut": "success",
  "lignes_inserees": 22,
  "lignes_invalides_ignorees": 0,
  "message": "22 ligne(s) chargée(s) dans la table donnees"
}
```

### Lister les séries disponibles

```http
GET /upload/series
```

Exemple :

```text
http://127.0.0.1:5004/upload/series
```

---

## Base de données MySQL

Les Services 3 et 4 utilisent la même base de données MySQL.

Le script SQL se trouve dans :

```text
sql/init_db.sql
```

Ce fichier permet de créer :

* la base de données `flask_stats` ;
* la table `donnees` ;
* des données de test.

### Structure de la table `donnees`

```text
donnees
├── id
├── nom_serie
├── valeur
├── categorie
├── date_mesure
└── created_at
```

### Exemple de création de table

```sql
CREATE TABLE IF NOT EXISTS donnees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_serie VARCHAR(100) NOT NULL,
    valeur DECIMAL(12,4) NOT NULL,
    categorie VARCHAR(50) DEFAULT NULL,
    date_mesure DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Fichier CSV de démonstration

Le fichier CSV de démonstration se trouve dans :

```text
data/donnees_exemple.csv
```

Il contient des données organisées sous cette forme :

```csv
nom_serie,valeur,categorie,date_mesure
serie_A,12.50,temperature,2024-01-15
serie_A,15.30,temperature,2024-01-16
serie_B,45.10,pression,2024-01-15
serie_C,220.50,debit,2024-01-15
```

### Colonnes attendues

| Colonne     | Obligatoire | Description            |
| ----------- | ----------- | ----------------------- |
| nom_serie   | Oui         | Nom de la série        |
| valeur      | Oui         | Valeur numérique       |
| categorie   | Non         | Catégorie de la mesure |
| date_mesure | Non         | Date de la mesure      |

---

## Configuration des variables d'environnement

Les services utilisant MySQL doivent posséder un fichier `.env`.

Exemple pour les services 3 et 4 :

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=flask_stats
```

Attention : le fichier `.env` ne doit pas être envoyé sur GitHub.

Il doit être ajouté dans `.gitignore`.

---

## Exemple de fichier `.gitignore`

```gitignore
# Environnements virtuels Python
venv/
env/
.venv/

# Fichiers de configuration sensibles
.env
*.env

# Fichiers Python compilés
__pycache__/
*.pyc
*.pyo

# Fichiers d'éditeur
.vscode/
.idea/
*.swp

# Fichiers système
.DS_Store
Thumbs.db
```

---

## Installation générale

### 1. Cloner le dépôt

```bash
git clone https://github.com/UTILISATEUR/flask-services-kanban.git
cd flask-services-kanban
```

### 2. Installer les dépendances d'un service

Exemple avec le Service 3 :

```bash
cd service3_stats_mysql
pip install -r requirements.txt
```

### 3. Lancer le service

```bash
python app.py
```

---

## Lancement des services

Chaque service se lance séparément dans son propre dossier.

### Service 1

```bash
cd service1_matrices
python app.py
```

URL :

```text
http://127.0.0.1:5001
```

### Service 2

```bash
cd service2_statistiques
python app.py
```

URL :

```text
http://127.0.0.1:5002
```

### Service 3

```bash
cd service3_stats_mysql
python app.py
```

URL :

```text
http://127.0.0.1:5003
```

### Service 4

```bash
cd service4_csv_mysql
python app.py
```

URL :

```text
http://127.0.0.1:5004
```

---

## Tests

Les services sont testés de plusieurs façons :

* avec Postman ;
* avec des scripts Python ;
* avec des pages HTML/JavaScript ;
* avec des tests unitaires Python.

---

## Tests avec Postman

### Service 3

Description statistique :

```http
GET http://127.0.0.1:5003/db/stats/describe?serie=serie_A
```

Corrélation :

```http
GET http://127.0.0.1:5003/db/stats/correlation?serie_x=serie_A&serie_y=serie_B
```

### Service 4

Upload CSV :

```http
POST http://127.0.0.1:5004/upload/csv
```

Dans Postman :

* choisir la méthode `POST` ;
* aller dans `Body` ;
* choisir `form-data` ;
* ajouter une clé `file` ;
* choisir le fichier `data/donnees_exemple.csv`.

---

## Tests Python

Exemple pour le Service 3 :

```bash
cd service3_stats_mysql
python test_service3.py
```

Les tests vérifient notamment :

* la présence des paramètres ;
* le code HTTP retourné ;
* le contenu JSON de la réponse ;
* le fonctionnement des routes principales.

---

## Tests HTML / JavaScript

Certains services possèdent des clients de test HTML/JS.

Exemple pour le Service 3 :

```text
service3_stats_mysql/client_test_service3.html
```

Pour l'utiliser :

1. lancer le service Flask ;
2. ouvrir le fichier HTML dans un navigateur ;
3. cliquer sur les boutons de test ;
4. vérifier que la réponse JSON s'affiche.

---

## Gestion des erreurs HTTP

Les services utilisent des codes HTTP cohérents.

| Code | Signification         | Exemple d'utilisation                |
| ---- | ---------------------- | -------------------------------------- |
| 200  | OK                     | Requête réussie                       |
| 201  | Created                | Données insérées avec succès          |
| 400  | Bad Request            | Paramètre manquant ou mauvais format  |
| 404  | Not Found              | Série inexistante                     |
| 413  | Payload Too Large      | Fichier trop volumineux               |
| 500  | Internal Server Error  | Erreur serveur ou base de données     |

---

## Organisation Git

Le projet utilise plusieurs branches.

### Branches principales

```text
main
develop
```

### Branches de fonctionnalités

```text
feature/s1-matrices
feature/s2-statistiques
feature/s3-stats-mysql
feature/s4-csv-mysql
feature/client-html-js
feature/client-python
```

### Branches de correction

```text
fix/s1-nom-bug
fix/s2-nom-bug
fix/s3-nom-bug
fix/s4-nom-bug
```

---

## Rôle des branches

| Branche     | Rôle                                |
| ----------- | ------------------------------------ |
| main        | Branche stable, code validé          |
| develop     | Branche d'intégration                |
| feature/... | Développement d'une fonctionnalité   |
| fix/...     | Correction d'un bug                  |

---

## Convention de commits

Les commits suivent le format :

```text
type(service): description courte
```

### Exemples

```text
feat(s1): ajoute la route matrices multiply
feat(s2): ajoute le calcul de correlation
feat(s3): ajoute la route db stats describe
feat(s4): ajoute upload csv
test(s3): ajoute les tests clients html et python
fix(s4): corrige la validation csv
docs: ajoute le readme global
```

### Types de commits

| Type     | Signification                  |
| -------- | -------------------------------- |
| feat     | Nouvelle fonctionnalité         |
| fix      | Correction d'un bug             |
| test     | Ajout ou modification de tests  |
| docs     | Documentation                   |
| refactor | Amélioration du code            |
| chore    | Tâche technique                 |

---

## Pull Requests

Chaque fonctionnalité doit être proposée avec une Pull Request.

La Pull Request doit contenir :

* un titre clair ;
* une description ;
* le numéro de l'issue liée ;
* un reviewer ;
* la mention `Closes #N` si elle ferme une issue.

### Exemple de description de Pull Request

```markdown
## Description

Ajout de la route GET /db/stats/describe pour le Service 3.

## Modifications

- ajout de la route Flask ;
- récupération des données depuis MySQL ;
- calcul des statistiques avec NumPy ;
- gestion des erreurs ;
- ajout des tests.

## Issue liée

Closes #12
```

---

## Organisation Kanban

Le projet est suivi avec GitHub Projects.

### Colonnes utilisées

```text
📋 Backlog
📌 À faire
🔧 En cours
👀 En revue
🧪 En test
✅ Terminé
```

### Règle WIP

La limite WIP est fixée à :

```text
1 tâche maximum en cours par étudiant.
```

Cela signifie qu'un étudiant ne doit pas avoir plusieurs cartes dans la colonne `En cours`.

---

## Champs personnalisés du Kanban

Le tableau GitHub Projects contient les champs personnalisés suivants :

### Priorité

```text
🔴 Critique
🟠 Haute
🟡 Moyenne
🟢 Basse
```

### Service

```text
Service 1
Service 2
Service 3
Service 4
Commun
```

### Estimation

```text
Nombre d'heures estimées
```

### Étudiant

```text
Étudiant A
Étudiant B
Étudiant C
Étudiant D
Tous
```

---

## Issues principales

| Issue | Tâche                              | Service   |
| ----- | ------------------------------------ | --------- |
| #1    | Init structure dossier service1     | Service 1 |
| #2    | Route POST /matrices/add            | Service 1 |
| #3    | Route POST /matrices/multiply       | Service 1 |
| #4    | Route POST /matrices/transpose      | Service 1 |
| #5    | Route POST /matrices/determinant    | Service 1 |
| #6    | Route POST /matrices/inverse        | Service 1 |
| #7    | Init structure dossier service2     | Service 2 |
| #8    | Route POST /stats/describe          | Service 2 |
| #9    | Route POST /stats/correlation       | Service 2 |
| #10   | Route POST /stats/test_normalite    | Service 2 |
| #11   | Init BDD MySQL + table donnees      | Service 3 |
| #12   | Route GET /db/stats/describe        | Service 3 |
| #13   | Route GET /db/stats/correlation     | Service 3 |
| #14   | Init structure dossier service4     | Service 4 |
| #15   | Route POST /upload/csv              | Service 4 |
| #16   | Validation & erreurs CSV            | Service 4 |
| #17   | Tests finaux & README global        | Commun    |

---

## Sécurité

Le projet respecte quelques règles de sécurité :

* ne pas envoyer le fichier `.env` sur GitHub ;
* ne pas écrire de mot de passe directement dans `app.py` ;
* utiliser des requêtes SQL paramétrées ;
* vérifier les données envoyées par l'utilisateur ;
* retourner des erreurs JSON claires.

Exemple de requête SQL paramétrée :

```python
cursor.execute(
    "SELECT valeur FROM donnees WHERE nom_serie = %s ORDER BY date_mesure",
    (nom_serie,)
)
```

---

## Bonnes pratiques appliquées

Pendant le projet, les bonnes pratiques suivantes sont utilisées :

* une branche par fonctionnalité ;
* un commit clair par modification importante ;
* une Pull Request avant fusion ;
* une revue de code par un autre étudiant ;
* un tableau Kanban mis à jour ;
* des tests avant de passer une tâche en terminé ;
* une documentation pour chaque service.

---

## Auteurs

Projet réalisé en groupe dans le cadre du TP Flask Services Kanban.

| Étudiant   | Rôle                                   |
| ---------- | ---------------------------------------- |
| Étudiant A | Service 1 – Calculs matriciels          |
| Étudiant B | Service 2 – Statistiques JSON           |
| Étudiant C | Service 3 – Statistiques MySQL          |
| Étudiant D | Service 4 – Chargement CSV vers MySQL   |

---

## État final attendu

À la fin du projet :

* chaque service doit fonctionner ;
* toutes les routes principales doivent être testées ;
* les issues doivent être dans la colonne `Terminé` ;
* les Pull Requests doivent être mergées ;
* les README doivent être présents ;
* le fichier `.env` ne doit pas être présent sur GitHub ;
* les services doivent pouvoir être testés avec Postman ou curl.

---

## Commandes utiles

### Voir les branches

```bash
git branch
```

### Créer une branche

```bash
git checkout -b feature/nom-branche
```

### Ajouter les fichiers

```bash
git add .
```

### Faire un commit

```bash
git commit -m "feat(s3): ajoute la route db stats describe"
```

### Envoyer sur GitHub

```bash
git push -u origin feature/nom-branche
```

### Récupérer les dernières modifications

```bash
git pull
```

---

## Conclusion

Ce projet permet de mettre en pratique le développement de services web avec Flask, la gestion d'un projet en équipe avec GitHub Projects, ainsi que les bonnes pratiques Git.

Chaque service est indépendant, mais l'ensemble forme un projet commun organisé autour d'un tableau Kanban et d'un dépôt GitHub partagé.