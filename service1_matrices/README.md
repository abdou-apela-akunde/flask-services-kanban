# Service 1 - Calculs Matriciels

API REST Flask permettant de faire des calculs sur des matrices avec NumPy.

## Installation

```bash
cd service1_matrices
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Le service demarre sur le port `5001`.

## Routes disponibles

### POST /matrices/add

Additionne deux matrices de memes dimensions.

```bash
curl -X POST http://localhost:5001/matrices/add ^
  -H "Content-Type: application/json" ^
  -d "{\"A\": [[1,2],[3,4]], \"B\": [[5,6],[7,8]]}"
```

Reponse attendue :

```json
{"operation":"addition","resultat":[[6.0,8.0],[10.0,12.0]]}
```

### POST /matrices/multiply

Multiplie deux matrices quand le nombre de colonnes de A est egal au nombre de lignes de B.

```bash
curl -X POST http://localhost:5001/matrices/multiply ^
  -H "Content-Type: application/json" ^
  -d "{\"A\": [[1,2],[3,4]], \"B\": [[5,6],[7,8]]}"
```

Reponse attendue :

```json
{"operation":"multiplication","resultat":[[19.0,22.0],[43.0,50.0]]}
```

Exemple avec deux matrices 3x3 :

```bash
curl -X POST http://localhost:5001/matrices/multiply ^
  -H "Content-Type: application/json" ^
  -d "{\"A\": [[1,2,3],[4,5,6],[7,8,9]], \"B\": [[9,8,7],[6,5,4],[3,2,1]]}"
```

### POST /matrices/transpose

Retourne la transposee d'une matrice.

```bash
curl -X POST http://localhost:5001/matrices/transpose ^
  -H "Content-Type: application/json" ^
  -d "{\"A\": [[1,2,3],[4,5,6]]}"
```

### POST /matrices/determinant

Calcule le determinant d'une matrice carree.

```bash
curl -X POST http://localhost:5001/matrices/determinant ^
  -H "Content-Type: application/json" ^
  -d "{\"A\": [[1,2],[3,4]]}"
```

### POST /matrices/inverse

Calcule l'inverse d'une matrice carree non singuliere.

```bash
curl -X POST http://localhost:5001/matrices/inverse ^
  -H "Content-Type: application/json" ^
  -d "{\"A\": [[1,2],[3,4]]}"
```

Si la matrice est singuliere, le service renvoie une erreur `400 Bad Request`.

## Tests

Tests unitaires Python :

```bash
python -m unittest test_service1.py
```

Tests executables directement depuis le code :

```bash
python run_tests_code.py
```

Test client HTML/JS :

1. Lancer le service avec `python app.py`.
2. Ouvrir `client_test.html` dans le navigateur.
3. Cliquer sur les boutons pour envoyer des requetes au service.

## Reponses aux questions de verification

Q1. La bibliotheque utilisee est NumPy. Installation : `pip install numpy`.

Q2. Si on inverse une matrice singuliere, elle n'a pas d'inverse. Le service teste le determinant : s'il est proche de 0, il renvoie une erreur HTTP 400.

Q3. Je developpe sur une branche `feature/s1-...`. Les commits suivent le format : `feat(s1): ajoute la route addition`.

Q4. Apres les routes 1 et 2, les cartes #2 et #3 doivent etre en `Termine`, donc 2 cartes terminees.

Q5. Exemple curl 3x3 :

```bash
curl -X POST http://localhost:5001/matrices/multiply ^
  -H "Content-Type: application/json" ^
  -d "{\"A\": [[1,2,3],[4,5,6],[7,8,9]], \"B\": [[9,8,7],[6,5,4],[3,2,1]]}"
```
