import json
import urllib.error 
import urllib.request  


BASE_URL = 'http://localhost:5001'  


def post_json(route, payload):  # Envoie une requete POST avec du JSON
    data = json.dumps(payload).encode('utf-8')  # Convertit le dictionnaire en JSON
    request = urllib.request.Request(  # Prepare la requete HTTP
        BASE_URL + route,  # Construit l'URL complete
        data=data,  # Ajoute le corps JSON
        headers={'Content-Type': 'application/json'},  # Indique que c'est du JSON
        method='POST'  # Utilise la methode POST
    )  # Fin de la creation de requete

    try:  # Essaie d'envoyer la requete
        with urllib.request.urlopen(request) as response:  # Envoie la requete
            return response.status, json.loads(response.read().decode('utf-8'))  # Retourne code et JSON
    except urllib.error.HTTPError as error:  # Recupere aussi les erreurs HTTP
        return error.code, json.loads(error.read().decode('utf-8'))  # Retourne code et JSON d'erreur


def resultats_equivalents(obtenu, attendu):  # Compare deux resultats
    if isinstance(attendu, list):  # Si le resultat attendu est une liste
        if not isinstance(obtenu, list) or len(obtenu) != len(attendu):  # Verifie le type et la taille
            return False  # Les resultats sont differents
        return all(resultats_equivalents(o, a) for o, a in zip(obtenu, attendu))  # Compare chaque valeur

    if isinstance(attendu, float):  # Si le resultat attendu est un decimal
        return abs(obtenu - attendu) < 0.000001  # Compare avec une petite tolerance

    return obtenu == attendu  # Compare normalement


def verifier(nom, route, payload, resultat_attendu=None, code_attendu=200):  # Verifie un scenario
    code, response = post_json(route, payload)  # Envoie la requete

    if code != code_attendu:  # Verifie le code HTTP
        print(f'[ECHEC] {nom} : code HTTP {code}, attendu {code_attendu}')  
        print(response)  # Affiche la reponse
        return False  # Le test echoue

    if resultat_attendu is not None and not resultats_equivalents(response.get('resultat'), resultat_attendu):  # Verifie
        print(f'[ECHEC] {nom} : resultat incorrect')  
        print('Attendu :', resultat_attendu)  
        print('Obtenu  :', response.get('resultat'))  # Affiche l'obtenu
        return False  # Le test echoue

    print(f'[OK] {nom}')  # Affiche que le test est reussi
    print(response)  # Affiche la reponse JSON
    return True  # Le test reussit


def lancer_tests_client():  # Lance tous les tests client
    scenarios = [  # Liste des tests a faire
        (  # Scenario addition
            'Addition',  
            '/matrices/add',  
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]},  
            [[6.0, 8.0], [10.0, 12.0]], 
            200 
        ),  
        (  # Scenario multiplication
            'Multiplication', 
            '/matrices/multiply',  
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]},  
            [[19.0, 22.0], [43.0, 50.0]], 
            200 
        ),  
        (  # Scenario transposee
            'Transposee',  
            '/matrices/transpose',  
            {'A': [[1, 2, 3], [4, 5, 6]]},  
            [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]], 
            200 
        ),  
        (  # Scenario determinant
            'Determinant',  
            '/matrices/determinant',  
            {'A': [[1, 2], [3, 4]]},  
            -2.0, 
            200 
        ),  
        (  # Scenario inverse
            'Inverse',  
            '/matrices/inverse',  
            {'A': [[1, 2], [3, 4]]},  
            [[-2.0, 1.0], [1.5, -0.5]], 
            200 
        ),  
        (  # Scenario erreur inverse
            'Erreur inverse matrice singuliere',  
            '/matrices/inverse',  
            {'A': [[1, 2], [2, 4]]},  
            None,  # Pas de resultat attendu
            400 
        ),  
    ]  # Fin de la liste

    total_ok = 0  # Compteur de tests reussis
    for nom, route, payload, attendu, code in scenarios:  # Parcourt les scenarios
        if verifier(nom, route, payload, attendu, code):  # Lance un test
            total_ok += 1  # Ajoute 1 si le test reussit
        print('-' * 50)  # Affiche une separation

    print(f'Resultat final client Python : {total_ok}/{len(scenarios)} tests reussis') 


if __name__ == '__main__': 
    print('Demarrer le service avec python app.py avant de lancer ce fichier.') 
    lancer_tests_client() 
