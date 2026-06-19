from flask import Flask, request, jsonify  #Flask pour créer l'API, request pour récupérer le JSON, jsonify pour renvoyer du JSON
import numpy as np  #NumPy pour faire les calculs statistiques
from scipy import stats  #SciPy pour Pearson et Shapiro-Wilk
from flask_cors import CORS  #CORS pour autoriser le client HTML

app = Flask(__name__)  #Création de l'application Flask

CORS(app)  #Permet au fichier HTML de communiquer avec Flask


#Vérifie les données envoyées

def validate_data(data, key='data'):
    #Vérifie si la clé existe dans JSON
    if key not in data:
        raise ValueError(f"Clé '{key}' manquante dans la requête")

    values = data[key]

    #Vérifie que les données sont une liste et vérifie aussi qu'il y a au moins 2 valeurs
    
    if not isinstance(values, list) or len(values) < 2:
        raise ValueError(f"'{key}' doit être une liste d'au moins 2 valeurs")

    return np.array(values, dtype=float)  #Transforme la liste en tableau NumPy


#Route POST /stats/describe

@app.route('/stats/describe', methods=['POST'])
def describe():
    data = request.get_json()  #Récupère le JSON envoyé par le client

    try:
        values = validate_data(data)

        result = {
            'n': int(len(values)),  #Nombre de valeurs
            'moyenne': round(float(np.mean(values)), 4),  #Moyenne
            'mediane': round(float(np.median(values)), 4),  #Médiane
            'ecart_type': round(float(np.std(values, ddof=1)), 4),  #Écart-type
            'variance': round(float(np.var(values, ddof=1)), 4),  #Variance
            'minimum': round(float(np.min(values)), 4),  #Minimum
            'maximum': round(float(np.max(values)), 4),  #Maximum
            'q1': round(float(np.percentile(values, 25)), 4),  #Premier quartile
            'q3': round(float(np.percentile(values, 75)), 4),  #Troisième quartile
            'etendue': round(float(np.ptp(values)), 4)  #Étendue
        }

        return jsonify({'operation': 'description', 'resultat': result})  #Renvoie le résultat en JSON

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400  #Renvoie une erreur si les données sont mauvaises


#Route POST /stats/correlation

@app.route('/stats/correlation', methods=['POST'])
def correlation():
    data = request.get_json()  #Récupère le JSON envoyé

    try:
        x = validate_data(data, 'x')  #Récupère la liste x
        y = validate_data(data, 'y')  #Récupère la liste y

        #Vérifie que les deux listes ont la même longueur
        if len(x) != len(y):
            return jsonify({'erreur': 'x et y doivent avoir la même longueur'}), 400

        r, p_value = stats.pearsonr(x, y)  #Corrélation de Pearson

        interpretation = (
            'forte' if abs(r) > 0.7
            else 'modérée' if abs(r) > 0.4
            else 'faible'
        )  #Interprétation de la corrélation

        return jsonify({
            'operation': 'correlation_pearson',
            'resultat': {
                'r': round(r, 4),  #Coefficient de corrélation
                'p_value': round(p_value, 6),  #p-value
                'interpretation': interpretation,  #Faible, modérée ou forte
                'significatif': bool(p_value < 0.05)  #Résultat significatif ou non
            }
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400  #Renvoie une erreur si les données sont mauvaises


#Route POST /stats/test_normalite
@app.route('/stats/test_normalite', methods=['POST'])
def test_normalite():
    data = request.get_json()  #Récupère le JSON envoyé

    try:
        values = validate_data(data)

        #Vérifie que le test Shapiro-Wilk ne dépasse pas 5000 valeurs
        if len(values) > 5000:
            return jsonify({'erreur': 'Shapiro-Wilk limité à 5000 valeurs'}), 400

        stat, p_value = stats.shapiro(values)  #Test de normalité Shapiro-Wilk

        return jsonify({
            'operation': 'test_normalite_shapiro_wilk',
            'resultat': {
                'statistique': round(float(stat), 6),  #Statistique du test
                'p_value': round(float(p_value), 6),  #p-value du test
                'est_normale': bool(p_value > 0.05),  #True si la distribution est normale
                'interpretation': (
                    'Distribution normale (p > 0.05)'
                    if p_value > 0.05
                    else 'Distribution non normale (p <= 0.05)'
                )  #Interprétation du test
            }
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400  #Renvoie une erreur si les données sont mauvaises


if __name__ == '__main__':
    app.run(debug=True, port=5002)  #Lance le serveur sur le port 5002