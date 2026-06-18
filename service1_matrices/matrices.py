import numpy as np


def parse_matrix(data, key):
    """Convertit une matrice JSON en tableau NumPy."""
    try:
        matrix = np.array(data[key], dtype=float)
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError(f"Matrice '{key}' invalide : {exc}")

    if matrix.ndim != 2:
        raise ValueError(f"Matrice '{key}' invalide : elle doit etre en 2 dimensions")

    return matrix


def add(A, B):
    if A.shape != B.shape:
        raise ValueError("Dimensions incompatibles")
    return (A + B).tolist()


def multiply(A, B):
    if A.shape[1] != B.shape[0]:
        raise ValueError("Le nombre de colonnes de A doit etre egal au nombre de lignes de B")
    return np.dot(A, B).tolist()


def transpose(A):
    return A.T.tolist()
