import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Table présences
cursor.execute("""
CREATE TABLE IF NOT EXISTS presences(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nom TEXT,
postnom TEXT,
date TEXT
)
""")

# Table dépenses
cursor.execute("""
CREATE TABLE IF NOT EXISTS depenses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
description TEXT,
montant REAL,
categorie TEXT
)
""")

conn.commit()
conn.close()

print("✅ Base de données créée avec succès")