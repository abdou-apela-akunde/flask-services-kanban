from __future__ import annotations

import io
import os
from datetime import date
from typing import Any

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, request #lire ce qu on recoit

# Charge les variables du fichier .env : DB_HOST, DB_PORT, DB_USER, etc.
load_dotenv()

# Creation de l'application Flask.
app = Flask(__name__)

# Colonnes oblg CSV.
COLONNES_REQUISES = {"nom_serie", "valeur"}

# Colonnes ttl.
COLONNES_VALIDES = ["nom_serie", "valeur", "categorie", "date_mesure"]

# Taille maximum autorisee pour un fichier envoye : 5 Mo.
TAILLE_MAX_OCTETS = 5 * 1024 * 1024


def get_connection():
    """Ouvre une connexion a la base MySQL avec les informations du .env."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def _none_if_empty(value: Any) -> Any:
    """Transforme les champs vides en NULL pour MySQL."""
    if pd.isna(value) or value == "":
        return None
    return value


def lire_et_valider_csv(content: bytes) -> tuple[pd.DataFrame, dict[str, int]]:
    """Lit le fichier CSV, nettoie les donnees et retourne les lignes valides."""
    try:
        # pandas lit le contenu du fichier recu sous forme de bytes.
        df = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise ValueError(f"Lecture CSV impossible : {exc}") from exc

    # On verifie que le CSV contient au moins nom_serie et valeur.
    colonnes_manquantes = sorted(COLONNES_REQUISES - set(df.columns))
    if colonnes_manquantes:
        raise ValueError(
            "Colonnes obligatoires manquantes : " + ", ".join(colonnes_manquantes)
        )

    # On garde seulement les colonnes utiles au service.
    df = df[[col for col in COLONNES_VALIDES if col in df.columns]].copy()
    nb_initial = len(df)

    # Nettoyage du nom de serie : suppression des espaces et refus des noms vides.
    df["nom_serie"] = df["nom_serie"].astype("string").str.strip()
    df["nom_serie"] = df["nom_serie"].replace("", pd.NA)

    # Conversion de la colonne valeur en nombre. Les valeurs impossibles deviennent NaN.
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")

    # Comptage puis suppression des lignes invalides.
    lignes_sans_serie = int(df["nom_serie"].isna().sum())
    lignes_valeur_invalide = int(df["valeur"].isna().sum())
    df = df.dropna(subset=["nom_serie", "valeur"])

    # Si une date est fournie, elle doit respecter le format YYYY-MM-DD.
    lignes_date_invalide = 0
    if "date_mesure" in df.columns:
        dates = pd.to_datetime(df["date_mesure"], format="%Y-%m-%d", errors="coerce")
        lignes_date_invalide = int(dates.isna().sum())
        df = df.loc[dates.notna()].copy()
        df["date_mesure"] = dates.loc[dates.notna()].dt.date

    # Suppression des doublons presents dans le meme fichier CSV.
    colonnes_doublon = [col for col in COLONNES_VALIDES if col in df.columns]
    lignes_doublons = int(df.duplicated(subset=colonnes_doublon).sum())
    df = df.drop_duplicates(subset=colonnes_doublon)

    # Si toutes les lignes ont ete rejetees, on renvoie une erreur.
    if df.empty:
        raise ValueError("Aucune ligne valide dans le CSV")

    # Ces compteurs permettent d'expliquer ce qui a ete insere ou ignore.
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
    """Insere les lignes valides du DataFrame dans la table MySQL donnees."""
    conn = get_connection()
    cursor = conn.cursor()
    insertions = 0

    try:
        for _, row in df.iterrows():
            # Requete parametree : les %s evitent de concatener les valeurs dans le SQL.
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

        # On valide definitivement les insertions dans MySQL.
        conn.commit()
        return insertions
    finally:
        # Fermeture propre de la connexion, meme en cas d'erreur.
        cursor.close()
        conn.close()


# =========================
# ROUTE 1 : POST /upload/csv
# =========================
# Cette route recoit un fichier CSV depuis le client.
# Exemple de test :
# curl.exe -X POST http://127.0.0.1:5004/upload/csv -F "file=@data/donnees_exemple.csv"
@app.route("/upload/csv", methods=["POST"])
def upload_csv():
    """Route principale : receptionne un CSV, le valide puis l'insere en base."""
    # Le fichier doit etre envoye avec la cle multipart "file".
    if "file" not in request.files:
        return jsonify({"erreur": 'Aucun fichier envoye (cle "file" manquante)'}), 400

    file = request.files["file"]

    # Verification du nom et de l'extension du fichier.
    if file.filename == "":
        return jsonify({"erreur": "Nom de fichier vide"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"erreur": "Seuls les fichiers .csv sont acceptes"}), 400

    # Lecture du contenu et controle de la taille maximale.
    content = file.read()
    if len(content) > TAILLE_MAX_OCTETS:
        return jsonify({"erreur": "Fichier trop volumineux (max 5 Mo)"}), 413

    # Validation metier du CSV : colonnes, valeurs numeriques, dates, doublons.
    try:
        df, compteurs = lire_et_valider_csv(content)
    except ValueError as exc:
        return jsonify({"erreur": str(exc)}), 400

    # Insertion MySQL des donnees nettoyees.
    try:
        insertions = inserer_donnees(df)
    except Exception as exc:
        return jsonify({"erreur": "Erreur base de donnees", "detail": str(exc)}), 500

    # Reponse JSON en cas de succes.
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


# ============================
# ROUTE 2 : GET /upload/series
# ============================
# Cette route permet de verifier les series deja inserees dans MySQL.
# Elle peut etre testee directement dans le navigateur :
# http://127.0.0.1:5004/upload/series
@app.route("/upload/series", methods=["GET"])
def list_series():
    """Route bonus : liste les series deja presentes dans la table donnees."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Regroupe les donnees par serie et calcule le nombre de points.
        cursor.execute(
            "SELECT nom_serie, COUNT(*) AS n, MIN(date_mesure), MAX(date_mesure) "
            "FROM donnees GROUP BY nom_serie ORDER BY nom_serie"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as exc:
        return jsonify({"erreur": "Erreur base de donnees", "detail": str(exc)}), 500

    # Mise en forme des resultats SQL en JSON lisible.
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
    # Lancement du service 4 sur le port demande dans le sujet.
    app.run(debug=True, port=5004)
