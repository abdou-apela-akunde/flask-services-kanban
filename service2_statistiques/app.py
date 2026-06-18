from flask import Flask, request, jsonify
import numpy as np
from scipy import stats  # ajout pour utiliser la corrélation et le test de normalité

app = Flask(__name__)


@app.route("/stats/describe", methods=["POST"])
def describe():
    try:
        data = request.get_json()
        valeurs = data["data"]

        resultat = {
            "n": len(valeurs),
            "moyenne": round(float(np.mean(valeurs)), 4),
            "mediane": round(float(np.median(valeurs)), 4),
            "ecart_type": round(float(np.std(valeurs, ddof=1)), 4),
            "variance": round(float(np.var(valeurs, ddof=1)), 4),
            "minimum": round(float(np.min(valeurs)), 4),
            "maximum": round(float(np.max(valeurs)), 4)
        }

        return jsonify({
            "operation": "description",
            "resultat": resultat
        })

    except Exception as e:
        return jsonify({"erreur": str(e)}), 400


#route POST
@app.route("/stats/correlation", methods=["POST"])
def correlation():
    try:
        data = request.get_json()

        x = data["x"]
        y = data["y"]

        if len(x) != len(y):
            return jsonify({"erreur": "x et y doivent avoir la même longueur"}), 400

        r, p_value = stats.pearsonr(x, y)

        resultat = {
            "r": round(float(r), 4),
            "p_value": round(float(p_value), 6)
        }

        return jsonify({
            "operation": "correlation_pearson",
            "resultat": resultat
        })

    except Exception as e:
        return jsonify({"erreur": str(e)}), 400


#route POST
@app.route("/stats/test_normalite", methods=["POST"])
def test_normalite():
    try:
        data = request.get_json()

        valeurs = data["data"]

        statistique, p_value = stats.shapiro(valeurs)

        resultat = {
            "statistique": round(float(statistique), 6),
            "p_value": round(float(p_value), 6),
            "est_normale": bool(p_value > 0.05)
        }

        return jsonify({
            "operation": "test_normalite_shapiro_wilk",
            "resultat": resultat
        })

    except Exception as e:
        return jsonify({"erreur": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5002)