import json
import urllib.error
import urllib.request


BASE_URL = 'http://localhost:5001'


def post_json(route, payload):
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        BASE_URL + route,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read().decode('utf-8'))


def resultats_equivalents(obtenu, attendu):
    if isinstance(attendu, list):
        if not isinstance(obtenu, list) or len(obtenu) != len(attendu):
            return False
        return all(resultats_equivalents(o, a) for o, a in zip(obtenu, attendu))

    if isinstance(attendu, float):
        return abs(obtenu - attendu) < 0.000001

    return obtenu == attendu


def verifier(nom, route, payload, resultat_attendu=None, code_attendu=200):
    code, response = post_json(route, payload)

    if code != code_attendu:
        print(f'[ECHEC] {nom} : code HTTP {code}, attendu {code_attendu}')
        print(response)
        return False

    if resultat_attendu is not None and not resultats_equivalents(response.get('resultat'), resultat_attendu):
        print(f'[ECHEC] {nom} : resultat incorrect')
        print('Attendu :', resultat_attendu)
        print('Obtenu  :', response.get('resultat'))
        return False

    print(f'[OK] {nom}')
    print(response)
    return True


def lancer_tests_client():
    scenarios = [
        (
            'Addition',
            '/matrices/add',
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]},
            [[6.0, 8.0], [10.0, 12.0]],
            200
        ),
        (
            'Multiplication',
            '/matrices/multiply',
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]},
            [[19.0, 22.0], [43.0, 50.0]],
            200
        ),
        (
            'Transposee',
            '/matrices/transpose',
            {'A': [[1, 2, 3], [4, 5, 6]]},
            [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]],
            200
        ),
        (
            'Determinant',
            '/matrices/determinant',
            {'A': [[1, 2], [3, 4]]},
            -2.0,
            200
        ),
        (
            'Inverse',
            '/matrices/inverse',
            {'A': [[1, 2], [3, 4]]},
            [[-2.0, 1.0], [1.5, -0.5]],
            200
        ),
        (
            'Erreur inverse matrice singuliere',
            '/matrices/inverse',
            {'A': [[1, 2], [2, 4]]},
            None,
            400
        ),
    ]

    total_ok = 0
    for nom, route, payload, attendu, code in scenarios:
        if verifier(nom, route, payload, attendu, code):
            total_ok += 1
        print('-' * 50)

    print(f'Resultat final client Python : {total_ok}/{len(scenarios)} tests reussis')


if __name__ == '__main__':
    print('Demarrer le service avec python app.py avant de lancer ce fichier.')
    lancer_tests_client()
