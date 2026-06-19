import numpy as np


def parse_matrix(data, key):  # Recupere une matrice dans un JSON
    """Convertit une liste de listes en tableau NumPy."""
    try:  # Essaie de convertir la matrice
        return np.array(data[key], dtype=float)  # Transforme la liste en matrice NumPy
    except (KeyError, ValueError, TypeError) as e:  # Gere les erreurs possibles
        raise ValueError(f"Matrice '{key}' invalide : {e}")  # Renvoie une erreur claire


def add(A, B):  # Additionne deux matrices
    if A.shape != B.shape:  # Verifie les dimensions
        raise ValueError("Dimensions incompatibles")  # Signale l'erreur
    return (A + B).tolist()  # Renvoie le resultat en liste


def multiply(A, B):  # Multiplie deux matrices
    if A.shape[1] != B.shape[0]:  # Verifie colonnes A = lignes B
        raise ValueError("Colonnes(A) doit egalerLignes(B)")  # Signale l'erreur
    return np.dot(A, B).tolist()  # Renvoie le produit


def transpose(A):  # Transpose une matrice
    return A.T.tolist()  # Renvoie la transposee


def determinant(A):  # Calcule le determinant
    if A.shape[0] != A.shape[1]:  # Verifie que la matrice est carree
        raise ValueError("La matrice doit etre carree")  # Signale l'erreur
    return round(np.linalg.det(A), 6)  # Renvoie le determinant arrondi


def inverse(A):  # Calcule l'inverse
    if A.shape[0] != A.shape[1]:  # Verifie que la matrice est carree
        raise ValueError("La matrice doit etre carree")  # Signale l'erreur

    det = np.linalg.det(A)  # Calcule le determinant
    if abs(det) < 1e-10:  # Verifie si la matrice est singuliere
        raise ValueError("Matrice singuliere, non inversible")  # Signale l'erreur

    return np.linalg.inv(A).tolist()  # Renvoie l'inverse
