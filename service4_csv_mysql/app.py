from __future__ import annotations

import io
import os
from datetime import date
from typing import Any

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)

COLONNES_REQUISES = {"nom_serie", "valeur"}
COLONNES_VALIDES = ["nom_serie", "valeur", "categorie", "date_mesure"]
TAILLE_MAX_OCTETS = 5 * 1024 * 1024


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def _none_if_empty(value: Any) -> Any:
    if pd.isna(value) or value == "":
        return None
    return value


def lire_et_valider_csv(content: bytes) -> tuple[pd.DataFrame, dict[str, int]]:
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise ValueError(f"Lecture CSV impossible : {exc}") from exc

    colonnes_manquantes = sorted(COLONNES_REQUISES - set(df.columns))
    if colonnes_manquantes:
        raise ValueError(
            "Colonnes obligatoires manquantes : " + ", ".join(colonnes_manquantes)
        )

    df = df[[col for col in COLONNES_VALIDES if col in df.columns]].copy()
    nb_initial = len(df)

    df["nom_serie"] = df["nom_serie"].astype("string").str.strip()
    df["nom_serie"] = df["nom_serie"].replace("", pd.NA)
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")

    lignes_sans_serie = int(df["nom_serie"].isna().sum())
    lignes_valeur_invalide = int(df["valeur"].isna().sum())
    df = df.dropna(subset=["nom_serie", "valeur"])

    lignes_date_invalide = 0
    if "date_mesure" in df.columns:
        dates = pd.to_datetime(df["date_mesure"], format="%Y-%m-%d", errors="coerce")
        lignes_date_invalide = int(dates.isna().sum())
        df = df.loc[dates.notna()].copy()
        df["date_mesure"] = dates.loc[dates.notna()].dt.date

    colonnes_doublon = [col for col in COLONNES_VALIDES if col in df.columns]
    lignes_doublons = int(df.duplicated(subset=colonnes_doublon).sum())
    df = df.drop_duplicates(subset=colonnes_doublon)

    if df.empty:
        raise ValueError("Aucune ligne valide dans le CSV")

    compteurs = {
        "lignes_lues": nb_initial,
        "lignes_sans_serie": lignes_sans_serie,
        "lignes_valeur_invalide": lignes_valeur_invalide,
        "lignes_date_invalide": lignes_date_invalide,
        "lignes_doublons_ignorees": lignes_doublons,
        "lignes_invalides_ignorees": (
            lignes_sans_serie + lignes_valeur_invalide + lignes_date_invalide
        ),
    }
    return df, compteurs


def inserer_donnees(df: pd.DataFrame) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    insertions = 0

    try:
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO donnees (nom_serie, valeur, categorie, date_mesure) "
                "VALUES (%s, %s, %s, %s)",
                (
                    str(row["nom_serie"]),
                    float(row["valeur"]),
                    _none_if_empty(row.get("categorie")),
                    _none_if_empty(row.get("date_mesure")),
                ),
            )
            insertions += 1

        conn.commit()
        return insertions
    finally:
        cursor.close()
        conn.close()


@app.route("/upload/csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"erreur": 'Aucun fichier envoye (cle "file" manquante)'}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"erreur": "Nom de fichier vide"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"erreur": "Seuls les fichiers .csv sont acceptes"}), 400

    content = file.read()
    if len(content) > TAILLE_MAX_OCTETS:
        return jsonify({"erreur": "Fichier trop volumineux (max 5 Mo)"}), 413

    try:
        df, compteurs = lire_et_valider_csv(content)
    except ValueError as exc:
        return jsonify({"erreur": str(exc)}), 400

    try:
        insertions = inserer_donnees(df)
    except Exception as exc:
        return jsonify({"erreur": "Erreur base de donnees", "detail": str(exc)}), 500

    return (
        jsonify(
            {
                "statut": "success",
                "lignes_inserees": insertions,
                "message": f"{insertions} ligne(s) chargee(s) dans la table donnees",
                **compteurs,
            }
        ),
        201,
    )


@app.route("/upload/series", methods=["GET"])
def list_series():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nom_serie, COUNT(*) AS n, MIN(date_mesure), MAX(date_mesure) "
            "FROM donnees GROUP BY nom_serie ORDER BY nom_serie"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as exc:
        return jsonify({"erreur": "Erreur base de donnees", "detail": str(exc)}), 500

    series = [
        {
            "serie": row[0],
            "n_points": row[1],
            "debut": row[2].isoformat() if isinstance(row[2], date) else str(row[2]),
            "fin": row[3].isoformat() if isinstance(row[3], date) else str(row[3]),
        }
        for row in rows
    ]
    return jsonify({"series": series, "total": len(series)})


if __name__ == "__main__":
    app.run(debug=True, port=5004)
