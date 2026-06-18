from app import app


def verifier_resultat(nom_test, response, resultat_attendu=None, code_attendu=200):
    data = response.get_json()

    if response.status_code != code_attendu:
        print(f"[ECHEC] {nom_test} : code HTTP {response.status_code}, attendu {code_attendu}")
        print(data)
        return False

    if resultat_attendu is not None and data.get('resultat') != resultat_attendu:
        print(f"[ECHEC] {nom_test} : resultat incorrect")
        print("Attendu :", resultat_attendu)
        print("Obtenu  :", data.get('resultat'))
        return False

    print(f"[OK] {nom_test}")
    print(data)
    return True


def lancer_tests():
    client = app.test_client()
    tests_ok = 0
    total_tests = 0

    scenarios = [
        {
            'nom': 'Addition',
            'route': '/matrices/add',
            'json': {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]},
            'attendu': [[6.0, 8.0], [10.0, 12.0]],
            'code': 200
        },
        {
            'nom': 'Multiplication',
            'route': '/matrices/multiply',
            'json': {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]},
            'attendu': [[19.0, 22.0], [43.0, 50.0]],
            'code': 200
        },
        {
            'nom': 'Transposee',
            'route': '/matrices/transpose',
            'json': {'A': [[1, 2, 3], [4, 5, 6]]},
            'attendu': [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]],
            'code': 200
        },
        {
            'nom': 'Determinant',
            'route': '/matrices/determinant',
            'json': {'A': [[1, 2], [3, 4]]},
            'attendu': -2.0,
            'code': 200
        },
        {
            'nom': 'Inverse',
            'route': '/matrices/inverse',
            'json': {'A': [[1, 2], [3, 4]]},
            'attendu': [[-2.0, 1.0], [1.5, -0.5]],
            'code': 200
        },
        {
            'nom': 'Erreur inverse matrice singuliere',
            'route': '/matrices/inverse',
            'json': {'A': [[1, 2], [2, 4]]},
            'attendu': None,
            'code': 400
        },
    ]

    for scenario in scenarios:
        total_tests += 1
        response = client.post(scenario['route'], json=scenario['json'])
        ok = verifier_resultat(
            scenario['nom'],
            response,
            resultat_attendu=scenario['attendu'],
            code_attendu=scenario['code']
        )
        if ok:
            tests_ok += 1
        print("-" * 50)

    print(f"Resultat final : {tests_ok}/{total_tests} tests reussis")

    if tests_ok == total_tests:
        print("Tout fonctionne bien pour le Service 1.")
    else:
        print("Certains tests ont echoue, il faut corriger le service.")


if __name__ == '__main__':
    lancer_tests()
