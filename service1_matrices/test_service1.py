import unittest

from app import app


class Service1MatricesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def post_json(self, route, payload):
        return self.client.post(route, json=payload)

    def assertMatrixAlmostEqual(self, result, expected):
        self.assertEqual(len(result), len(expected))
        for result_row, expected_row in zip(result, expected):
            self.assertEqual(len(result_row), len(expected_row))
            for result_value, expected_value in zip(result_row, expected_row):
                self.assertAlmostEqual(result_value, expected_value, places=6)

    def test_add(self):
        response = self.post_json(
            '/matrices/add',
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['resultat'], [[6.0, 8.0], [10.0, 12.0]])

    def test_multiply(self):
        response = self.post_json(
            '/matrices/multiply',
            {'A': [[1, 2], [3, 4]], 'B': [[5, 6], [7, 8]]}
        )
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
