# Service 3 – Statistiques MySQL

## Description

Le Service 3 est une API REST développée avec Flask.
Il permet de calculer des statistiques à partir de données stockées dans une base de données MySQL.

Les données sont enregistrées dans la table `donnees`.

---

## Technologies utilisées

- Python
- Flask
- NumPy
- SciPy
- MySQL
- mysql-connector-python
- python-dotenv

---

## Structure du service

```text
service3_stats_mysql/
├── app.py
├── db.py
├── test_service3.py
├── client_test_service3.html
├── requirements.txt
├── .env
└── README.md
```

---

## Configuration

Créer un fichier `.env` dans le dossier `service3_stats_mysql` :

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=flask_stats
```

La base de données doit être créée avec le fichier :

```text
sql/init_db.sql
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Lancement du service

```bash
python app.py
```

Le service est disponible sur :

```text
http://127.0.0.1:5003
```

---

## Routes disponibles

### Route d'accueil

```http
GET /
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

---

### Description statistique

```http
GET /db/stats/describe?serie=serie_A
```

Cette route retourne les statistiques descriptives d'une série.

Exemple de réponse :

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

---

### Corrélation entre deux séries

```http
GET /db/stats/correlation?serie_x=serie_A&serie_y=serie_B
```

Cette route calcule la corrélation de Pearson entre deux séries.

Exemple de réponse :

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

## Tests

### Test avec Postman

Tester les routes suivantes :

```text
http://127.0.0.1:5003/db/stats/describe?serie=serie_A
```

```text
http://127.0.0.1:5003/db/stats/correlation?serie_x=serie_A&serie_y=serie_B
```

---

### Tests Python

Lancer :

```bash
python test_service3.py
```

---

### Test HTML / JavaScript

Ouvrir le fichier :

```text
client_test_service3.html
```

Puis cliquer sur les boutons pour afficher les résultats JSON.

---

## Gestion des erreurs

| Code | Signification          |
| ---- | ----------------------- |
| 200  | Requête réussie         |
| 400  | Paramètre manquant      |
| 404  | Série inexistante       |
| 500  | Erreur base de données  |

---

## Auteur

Service réalisé par Abdou APELA AKUNDE.