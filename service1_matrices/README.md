# Service 1 - Calculs Matriciels

## Description

API REST Flask pour effectuer des calculs sur des matrices avec NumPy.

Le service fonctionne sur le port `5001`.

## Installation

```bash
cd service1_matrices
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Sous Linux/Mac, l'activation du venv se fait avec :

```bash
source venv/bin/activate
```

## Routes disponibles

### POST /matrices/add

Additionne deux matrices de memes dimensions.

Corps de la requete JSON :

```json
{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}
```

Exemple curl :

```bash
curl -X POST http://localhost:5001/matrices/add \
  -H 'Content-Type: application/json' \
  -d '{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}'
```

Reponse attendue :

```json
{"operation": "addition", "resultat": [[6.0, 8.0], [10.0, 12.0]]}
```

Erreurs possibles : `400` si les dimensions sont incompatibles.

### POST /matrices/multiply

Multiplie deux matrices si le nombre de colonnes de `A` est egal au nombre de lignes de `B`.

Corps de la requete JSON :

```json
{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}
```

Exemple curl :

```bash
curl -X POST http://localhost:5001/matrices/multiply \
  -H 'Content-Type: application/json' \
  -d '{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}'
```

Reponse attendue :

```json
{"operation": "multiplication", "resultat": [[19.0, 22.0], [43.0, 50.0]]}
```

Exemple curl avec deux matrices 3x3 :

```bash
curl -X POST http://localhost:5001/matrices/multiply \
  -H 'Content-Type: application/json' \
  -d '{"A": [[1,2,3],[4,5,6],[7,8,9]], "B": [[9,8,7],[6,5,4],[3,2,1]]}'
```

Erreurs possibles : `400` si les dimensions sont incompatibles.

### POST /matrices/transpose

Retourne la transposee d'une matrice.

Corps de la requete JSON :

```json
{"A": [[1,2,3],[4,5,6]]}
```

Exemple curl :

```bash
curl -X POST http://localhost:5001/matrices/transpose \
  -H 'Content-Type: application/json' \
  -d '{"A": [[1,2,3],[4,5,6]]}'
```

Reponse attendue :

```json
{"operation": "transposee", "resultat": [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]}
```

### POST /matrices/determinant

Calcule le determinant d'une matrice carree.

Corps de la requete JSON :

```json
{"A": [[1,2],[3,4]]}
```

Exemple curl :

```bash
curl -X POST http://localhost:5001/matrices/determinant \
  -H 'Content-Type: application/json' \
  -d '{"A": [[1,2],[3,4]]}'
```

Reponse attendue :

```json
{"operation": "determinant", "resultat": -2.0}
```

Erreurs possibles : `400` si la matrice n'est pas carree.

### POST /matrices/inverse

Calcule l'inverse d'une matrice carree non singuliere.

Corps de la requete JSON :

```json
{"A": [[1,2],[3,4]]}
```

Exemple curl :

```bash
curl -X POST http://localhost:5001/matrices/inverse \
  -H 'Content-Type: application/json' \
  -d '{"A": [[1,2],[3,4]]}'
```

Reponse attendue :

```json
{"operation": "inverse", "resultat": [[-2.0, 1.0], [1.5, -0.5]]}
```

Avec NumPy, les nombres decimaux peuvent parfois apparaitre sous une forme tres proche, par exemple `-1.9999999999999996` au lieu de `-2.0`.

Erreurs possibles :

- `400` si la matrice n'est pas carree.
- `400` si la matrice est singuliere et donc non inversible.

## Tests demandes dans le sujet

Le sujet demande de faire des tests avec Postman, puis d'ecrire du code de test unitaire en HTML/JSON et en Python pour la partie client.

### 1. Tests avec Postman

Demarrer le serveur :

```bash
python app.py
```

Dans Postman :

- methode : `POST`
- URL : `http://localhost:5001/matrices/add`
- onglet Body : `raw` puis `JSON`
- JSON :

```json
{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}
```

Refaire le meme principe pour :

- `POST /matrices/multiply`
- `POST /matrices/transpose`
- `POST /matrices/determinant`
- `POST /matrices/inverse`

### 2. Test unitaire Python du service

Ce test utilise le client de test Flask. Il verifie toutes les routes sans ouvrir le navigateur.

```bash
python -m unittest test_service1.py
```

Resultat attendu :

```text
Ran 6 tests
OK
```

### 3. Test Python de la partie client

Ce test envoie de vraies requetes HTTP JSON vers le serveur Flask, comme un client externe.

Dans un premier terminal :

```bash
python app.py
```

Dans un deuxieme terminal ou depuis le bouton Run de l'editeur :

```bash
python client_python_test.py
```

Resultat attendu :

```text
Resultat final client Python : 6/6 tests reussis
```

### 4. Test HTML/JSON de la partie client

Demarrer le serveur :

```bash
python app.py
```

Puis ouvrir dans le navigateur :

```text
http://localhost:5001/
```

La page affiche un formulaire JSON et des boutons pour tester :

- addition
- multiplication
- transposee
- determinant
- inverse

## Reponses aux questions de verification - Service 1

Q1. La bibliotheque Python utilisee pour les calculs matriciels est NumPy. Installation : `pip install numpy`.

Q2. Si on essaie d'inverser une matrice singuliere, elle n'a pas d'inverse. Le service teste le determinant : si `abs(det) < 1e-10`, il renvoie une erreur HTTP `400`.

Q3. Le developpement se fait sur une branche `feature/s1-...`. Les commits suivent la convention : `feat(s1): ajoute la route addition`.

Q4. Apres les routes 1 et 2, les cartes `#2` et `#3` doivent etre en `Termine`, donc 2 cartes terminees.

Q5. Exemple de requete curl pour tester la multiplication de deux matrices 3x3 :

```bash
curl -X POST http://localhost:5001/matrices/multiply \
  -H 'Content-Type: application/json' \
  -d '{"A": [[1,2,3],[4,5,6],[7,8,9]], "B": [[9,8,7],[6,5,4],[3,2,1]]}'
```
