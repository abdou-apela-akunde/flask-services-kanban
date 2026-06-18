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
