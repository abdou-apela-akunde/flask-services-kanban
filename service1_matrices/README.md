# Service 1 - Calculs Matriciels

## Description

API REST Flask pour effectuer des calculs sur des matrices avec NumPy.

Le service utilise le port `5001`.

## Structure

```text
service1_matrices/
|-- app.py                 # Application Flask principale
|-- matrices.py            # Fonctions de calcul matriciel
|-- requirements.txt       # Dependances Python
|-- README.md              # Documentation du service
|-- client_test.html       # Client HTML/JSON
|-- client_python_test.py  # Client Python HTTP
`-- test_service1.py       # Tests unitaires Python
```

## Installation

Sous Windows PowerShell :

```powershell
cd "C:\Users\but-info\OneDrive - UPEC\Documents\BUT-1\S2\Ressources\R210 - GPO\tp2\flask-services-kanban\service1_matrices"
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe app.py
```

Sous Linux/Mac :

```bash
cd service1_matrices
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Routes disponibles

Les exemples ci-dessous utilisent `curl.exe --%`, qui fonctionne bien dans PowerShell avec du JSON.

### POST /matrices/add

Additionne deux matrices de memes dimensions.

Corps de la requete JSON :

```json
{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}
```

Commande curl PowerShell :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/add -H "Content-Type: application/json" -d "{\"A\": [[1,2],[3,4]], \"B\": [[5,6],[7,8]]}"
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

Commande curl PowerShell :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/multiply -H "Content-Type: application/json" -d "{\"A\": [[1,2],[3,4]], \"B\": [[5,6],[7,8]]}"
```

Reponse attendue :

```json
{"operation": "multiplication", "resultat": [[19.0, 22.0], [43.0, 50.0]]}
```

Exemple curl PowerShell avec deux matrices 3x3 :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/multiply -H "Content-Type: application/json" -d "{\"A\": [[1,2,3],[4,5,6],[7,8,9]], \"B\": [[9,8,7],[6,5,4],[3,2,1]]}"
```

Erreurs possibles : `400` si les dimensions sont incompatibles.

### POST /matrices/transpose

Retourne la transposee d'une matrice.

Corps de la requete JSON :

```json
{"A": [[1,2,3],[4,5,6]]}
```

Commande curl PowerShell :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/transpose -H "Content-Type: application/json" -d "{\"A\": [[1,2,3],[4,5,6]]}"
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

Commande curl PowerShell :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/determinant -H "Content-Type: application/json" -d "{\"A\": [[1,2],[3,4]]}"
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

Commande curl PowerShell :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/inverse -H "Content-Type: application/json" -d "{\"A\": [[1,2],[3,4]]}"
```

Reponse attendue :

```json
{"operation": "inverse", "resultat": [[-2.0, 1.0], [1.5, -0.5]]}
```

Avec NumPy, certains decimaux peuvent apparaitre sous une forme tres proche, par exemple `-1.9999999999999996` au lieu de `-2.0`.

Erreur attendue pour une matrice singuliere :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/inverse -H "Content-Type: application/json" -d "{\"A\": [[1,2],[2,4]]}"
```

Reponse attendue :

```json
{"erreur": "Matrice singuliere, non inversible"}
```

## Tests demandes dans le sujet

Le sujet demande de tester avec Postman ou curl, puis d'ecrire du code de test en HTML/JSON et en Python.

### 1. Tests avec curl ou Postman

Demarrer le serveur :

```powershell
venv\Scripts\python.exe app.py
```

Puis tester par exemple l'addition :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/add -H "Content-Type: application/json" -d "{\"A\": [[1,2],[3,4]], \"B\": [[5,6],[7,8]]}"
```

### 2. Tests unitaires Python

Ces tests utilisent le client de test Flask.

```powershell
venv\Scripts\python.exe -m unittest test_service1.py
```

Resultat attendu :

```text
Ran 6 tests
OK
```

### 3. Test Python de la partie client

Ce fichier envoie de vraies requetes HTTP JSON vers le serveur Flask.

Terminal 1 :

```powershell
venv\Scripts\python.exe app.py
```

Terminal 2 :

```powershell
venv\Scripts\python.exe client_python_test.py
```

Resultat attendu :

```text
Resultat final client Python : 6/6 tests reussis
```

### 4. Test HTML/JSON de la partie client

Demarrer le serveur :

```powershell
venv\Scripts\python.exe app.py
```

Puis ouvrir :

```text
http://localhost:5001/
```

La page permet de tester les routes avec du JSON depuis le navigateur.

## Reponses aux questions de verification - Service 1

Q1. La bibliotheque utilisee est NumPy. Installation : `pip install numpy`.

Q2. Si on essaie d'inverser une matrice singuliere, elle n'a pas d'inverse. Le service teste le determinant : si `abs(det) < 1e-10`, il renvoie une erreur HTTP `400`.

Q3. Je developpe sur une branche `feature/s1-...`. Les commits suivent le format : `feat(s1): ajoute la route addition`.

Q4. Apres les routes 1 et 2, les cartes `#2` et `#3` doivent etre en `Termine`, donc 2 cartes terminees.

Q5. Exemple de requete curl pour tester la multiplication de deux matrices 3x3 :

```powershell
curl.exe --% -X POST http://localhost:5001/matrices/multiply -H "Content-Type: application/json" -d "{\"A\": [[1,2,3],[4,5,6],[7,8,9]], \"B\": [[9,8,7],[6,5,4],[3,2,1]]}"
```
