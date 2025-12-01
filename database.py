import sqlite3

DB_NAME = "consultations.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            texte TEXT NOT NULL,
            FOREIGN KEY(consultation_id) REFERENCES consultations(id)
        )
    """)

    conn.commit()
    conn.close()


def enregistrer_consultation(nom, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO consultations (nom, description) VALUES (?, ?)",
        (nom, description)
    )
    conn.commit()
    conn.close()


def enregistrer_contribution(consultation_id, texte):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contributions (consultation_id, texte) VALUES (?, ?)",
        (consultation_id, texte)
    )
    conn.commit()
    conn.close()


def get_consultations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM consultations")
    data = cursor.fetchall()
    conn.close()
    return data


def get_consultation_details(consultation_id):
    """Récupère les détails d'une consultation (nom et description)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nom, description FROM consultations WHERE id = ?",
        (consultation_id,)
    )
    data = cursor.fetchone()
    conn.close()
    return data


def get_contributions(consultation_id):
    """Récupère toutes les contributions d'une consultation."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, texte FROM contributions WHERE consultation_id = ?",
        (consultation_id,)
    )
    data = cursor.fetchall()
    conn.close()
    return data


def count_contributions(consultation_id):
    """Compte le nombre de contributions pour une consultation."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM contributions WHERE consultation_id = ?",
        (consultation_id,)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count
