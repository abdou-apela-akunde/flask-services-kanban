import io
import unittest
from datetime import date
from unittest.mock import patch

from app import app


class FakeCursor:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.executed = []
        self.closed = False

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.rows

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, rows=None):
        self.cursor_obj = FakeCursor(rows)
        self.committed = False
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True


class Service4TestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def upload(self, csv_text, filename="donnees.csv"):
        return self.client.post(
            "/upload/csv",
            data={"file": (io.BytesIO(csv_text.encode("utf-8")), filename)},
            content_type="multipart/form-data",
        )

    def test_upload_csv_insere_lignes_valides(self):
        fake_conn = FakeConnection()
        csv_text = (
            "nom_serie,valeur,categorie,date_mesure\n"
            "serie_A,12.5,temperature,2024-01-15\n"
            "serie_A,abc,temperature,2024-01-16\n"
            "serie_A,12.5,temperature,2024-01-15\n"
            "serie_B,52.8,pression,2024-01-16\n"
        )

        with patch("app.get_connection", return_value=fake_conn):
            response = self.upload(csv_text)

        body = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body["lignes_inserees"], 2)
        self.assertEqual(body["lignes_valeur_invalide"], 1)
        self.assertEqual(body["lignes_doublons_ignorees"], 1)
        self.assertTrue(fake_conn.committed)
        self.assertEqual(len(fake_conn.cursor_obj.executed), 2)

    def test_upload_refuse_colonne_valeur_manquante(self):
        response = self.upload("nom_serie,categorie\nserie_A,temperature\n")

        self.assertEqual(response.status_code, 400)
        self.assertIn("valeur", response.get_json()["erreur"])

    def test_upload_refuse_extension_non_csv(self):
        response = self.upload("nom_serie,valeur\nserie_A,1\n", "donnees.txt")

        self.assertEqual(response.status_code, 400)
        self.assertIn(".csv", response.get_json()["erreur"])

    def test_list_series_retourne_resume(self):
        fake_conn = FakeConnection(
            rows=[
                ("serie_A", 10, date(2024, 1, 15), date(2024, 1, 24)),
                ("serie_C", 10, date(2024, 1, 15), date(2024, 1, 24)),
            ]
        )

        with patch("app.get_connection", return_value=fake_conn):
            response = self.client.get("/upload/series")

        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["total"], 2)
        self.assertEqual(body["series"][0]["serie"], "serie_A")
        self.assertEqual(body["series"][0]["debut"], "2024-01-15")


if __name__ == "__main__":
    unittest.main()
