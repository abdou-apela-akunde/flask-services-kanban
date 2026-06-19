import unittest
from app import app

class TestService3(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_describe_serie_A(self):
        response = self.client.get("/db/stats/describe?serie=serie_A")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["source"], "mysql")
        self.assertEqual(data["resultat"]["serie"], "serie_A")
        self.assertIn("moyenne", data["resultat"])

    def test_describe_parametre_manquant(self):
        response = self.client.get("/db/stats/describe")
        self.assertEqual(response.status_code, 400)

    def test_correlation_serie_A_B(self):
        response = self.client.get(
            "/db/stats/correlation?serie_x=serie_A&serie_y=serie_B"
        )
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["source"], "mysql")
        self.assertEqual(data["series"]["x"], "serie_A")
        self.assertEqual(data["series"]["y"], "serie_B")
        self.assertIn("r", data["resultat"])

    def test_correlation_parametre_manquant(self):
        response = self.client.get("/db/stats/correlation")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()