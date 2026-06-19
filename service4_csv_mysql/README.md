# Service 4 - Chargement CSV vers MySQL

Service Flask de l'etudiant D. Il charge un fichier CSV dans la table MySQL
`donnees`, partagee avec le Service 3.

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Creer un fichier `.env` local, sans le versionner :

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=flask_stats
```

Initialiser la base :

```bash
mysql -u root -p < sql/init_db.sql
```

## Lancer le service

```bash
python app.py
```

Le service ecoute sur `http://localhost:5004`.

## Routes

### POST /upload/csv

Charge un fichier CSV envoye avec la cle multipart `file`.

```bash
curl -X POST http://localhost:5004/upload/csv ^
  -F "file=@data/donnees_exemple.csv"
```

Reponse attendue :

```json
{
  "statut": "success",
  "lignes_inserees": 30,
  "lignes_invalides_ignorees": 0,
  "lignes_doublons_ignorees": 0,
  "message": "30 ligne(s) chargee(s) dans la table donnees"
}
```

### GET /upload/series

Liste les series chargees et leur nombre de points.

```bash
curl http://localhost:5004/upload/series
```

## Validations effectuees

- Presence du fichier dans la cle `file`.
- Nom de fichier non vide.
- Extension `.csv`.
- Taille maximale de 5 Mo.
- Colonnes obligatoires `nom_serie` et `valeur`.
- Conversion de `valeur` en nombre.
- Rejet des lignes sans serie, valeur numerique ou date ISO `YYYY-MM-DD`.
- Suppression des doublons presents dans le fichier avant insertion.

## Tests

Tests unitaires Flask sans dependance a un vrai serveur MySQL :

```bash
python -m unittest discover -s tests
```

Clients de test demandes dans le TP :

```bash
python clients/client_test_service4.py
```

Ouvrir aussi `clients/test_upload.html` dans un navigateur pendant que
`python app.py` est lance.

## Reponses aux questions Service 4

Q1. Les controles sont : fichier present, extension CSV, taille maximale,
colonnes obligatoires, serie non vide, valeur numerique, date ISO valide,
doublons retires, puis insertion MySQL.

Q2. Les valeurs non numeriques dans `valeur` sont converties en valeurs
invalides, ignorees, et comptees dans `lignes_valeur_invalide`.

Q3. Le schema est coordonne avec l'etudiant C via `sql/init_db.sql` : meme
base `flask_stats`, meme table `donnees`, memes colonnes.

Q4. Sans colonne `valeur`, la route retourne HTTP 400 avec un message
`Colonnes obligatoires manquantes : valeur`.

Q5. Apres chargement du CSV, le Service 3 doit retourner pour `serie_C` :
N = 10, moyenne = 223.33, min = 198.20, max = 245.10, categorie = `debit`.
Pour l'ecart-type, le resultat depend de la convention du Service 3 :
14.82 avec `ddof=0` (population) ou 15.63 avec `ddof=1` (echantillon).
