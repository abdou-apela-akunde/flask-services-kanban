import unittest

from app import app


class Service1MatricesTestCase(unittest.TestCase):
    def setUp(self): 
        self.client = app.test_client() 

    def post_json(self, route, payload):  # Envoie une requete POST JSON
        return self.client.post(route, json=payload)  # Retourne la reponse Flask

    def assertMatrixAlmostEqual(self, result, expected):  # Compare deux matrices avec tolerance
        self.assertEqual(len(result), len(expected))  # Compare le nombre de lignes
        for result_row, expected_row in zip(result, expected):  # Parcourt les lignes
            self.assertEqual(len(result_row), len(expected_row))  # Compare le nombre de colonnes
            for result_value, expected_value in zip(result_row, expected_row):  # Parcourt les valeurs
                self.assertAlmostEqual(result_value, expected_value, places=6)  # Compare presque egal

    def test_add(self):  # Teste l'addition
        response = self.post_json(  # Envoie une requete de test
            '/matrices/add',  # Route testee
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]}  # Donnees envoyees
        )  # Fin de la requete
        self.assertEqual(response.status_code, 200)  # Verifie le code HTTP
        self.assertEqual(response.get_json()['resultat'], [[6.0, 8.0], [10.0, 12.0]])  # Verifie le resultat

    def test_multiply(self): 
        response = self.post_json( 
            '/matrices/multiply', 
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]} 
        )  # Fin de la requete
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.get_json()['resultat'], [[19.0, 22.0], [43.0, 50.0]])  

    def test_transpose(self):  
        response = self.post_json('/matrices/transpose', {'A': [[1, 2, 3], [4, 5, 6]]})
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.get_json()['resultat'], [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]) 

    def test_determinant(self): 
        response = self.post_json('/matrices/determinant', {'A': [[1, 2], [3, 4]]})  
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.get_json()['resultat'], -2.0) 

    def test_inverse(self):
        response = self.post_json('/matrices/inverse', {'A': [[1, 2], [3, 4]]}) 
        self.assertEqual(response.status_code, 200)  
        self.assertMatrixAlmostEqual(response.get_json()['resultat'], [[-2.0, 1.0], [1.5, -0.5]]) 

    def test_inverse_singular_matrix(self):
        response = self.post_json('/matrices/inverse', {'A': [[1, 2], [2, 4]]}) 
        self.assertEqual(response.status_code, 400)
        self.assertIn('singuliere', response.get_json()['erreur']) 


if __name__ == '__main__': 
    unittest.main()  
