from flask import Flask, request, jsonify, send_from_directory
import numpy as np

app = Flask(__name__)


def parse_matrix(data, key):
    """Convertit une liste de listes en tableau NumPy."""
    try:
        return np.array(data[key], dtype=float)
    except (KeyError, ValueError, TypeError) as e:
        raise ValueError(f"Matrice '{key}' invalide : {e}")


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response


@app.route('/', methods=['GET'])
def home():
    return send_from_directory('.', 'client_test.html')


@app.route('/matrices/add', methods=['POST'])
def add_matrices():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        B = parse_matrix(data, 'B')
        if A.shape != B.shape:
            return jsonify({'erreur': 'Dimensions incompatibles'}), 400
        result = (A + B).tolist()
        return jsonify({'operation': 'addition', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


@app.route('/matrices/multiply', methods=['POST'])
def multiply_matrices():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        B = parse_matrix(data, 'B')
        if A.shape[1] != B.shape[0]:
            return jsonify({'erreur': 'Colonnes(A) doit egalerLignes(B)'}), 400
        result = np.dot(A, B).tolist()
        return jsonify({'operation': 'multiplication', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


@app.route('/matrices/transpose', methods=['POST'])
def transpose_matrix():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        result = A.T.tolist()
        return jsonify({'operation': 'transposee', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


@app.route('/matrices/determinant', methods=['POST'])
def determinant_matrix():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        if A.shape[0] != A.shape[1]:
            return jsonify({'erreur': 'La matrice doit etre carree'}), 400
        det = np.linalg.det(A)
        return jsonify({'operation': 'determinant', 'resultat': round(det, 6)})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


@app.route('/matrices/inverse', methods=['POST'])
def inverse_matrix():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        if A.shape[0] != A.shape[1]:
            return jsonify({'erreur': 'La matrice doit etre carree'}), 400
        det = np.linalg.det(A)
        if abs(det) < 1e-10:
            return jsonify({'erreur': 'Matrice singuliere, non inversible'}), 400
        result = np.linalg.inv(A).tolist()
        return jsonify({'operation': 'inverse', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


@app.route('/matrices/health', methods=['GET'])
def health():
    return jsonify({
        'statut': 'ok',
        'service': 'Service 1 - Calculs Matriciels',
        'port': 5001
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
